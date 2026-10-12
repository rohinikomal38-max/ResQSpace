
import os
import tempfile
from pathlib import Path

import geopandas as gpd


def write_geojson_atomically(dataframe, output_path):
    """Write GeoJSON to a temporary file, then replace the destination."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            dir=path.parent,
            prefix=f".{path.stem}.",
            suffix=".geojson",
            delete=False,
        ) as temp_file:
            temp_path = Path(temp_file.name)

        dataframe.to_file(temp_path, driver="GeoJSON")
        os.replace(temp_path, path)
        temp_path = None
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def assess_exposure(asset_geometry, flood_geometry):
    """Return True, False, or None if overlap cannot be assessed."""
    if asset_geometry is None or flood_geometry is None:
        return None

    if asset_geometry.is_empty or flood_geometry.is_empty:
        return None

    return asset_geometry.intersects(flood_geometry)


def process_asset_file(assets_path, flood_path, output_path):
    """
    Assess infrastructure overlap with potential-change areas.

    Inputs must have readable geometries and defined CRS information.
    Output is GeoJSON in EPSG:4326.
    """
    assets = gpd.read_file(assets_path)
    flood = gpd.read_file(flood_path)

    if assets.crs is None or flood.crs is None:
        raise ValueError("Both input files must have a defined CRS.")

    if assets.empty or flood.empty:
        raise ValueError(
            "Asset and potential-change files must not be empty."
        )

    assets = assets.to_crs("EPSG:4326")
    flood = flood.to_crs("EPSG:4326")

    flood_geometry = flood.geometry.union_all()

    def classify_asset(geometry):
        if geometry is None or geometry.is_empty:
            return "not_assessed"

        if not geometry.is_valid:
            return "not_assessed"

        if assess_exposure(geometry, flood_geometry):
            return "potentially_affected"

        return "not_flagged"

    assets["exposure_status"] = assets.geometry.apply(classify_asset)
    assets["exposure_fraction"] = None

    valid_assets = (
        assets.geometry.notna()
        & ~assets.geometry.is_empty
        & assets.geometry.is_valid
    )

    if valid_assets.any():
        projected_crs = assets.estimate_utm_crs()

        if projected_crs is not None:
            projected_assets = assets.loc[valid_assets].to_crs(
                projected_crs
            )
            projected_flood = flood.to_crs(projected_crs)
            projected_flood_geometry = (
                projected_flood.geometry.union_all()
            )

            fractions = []

            for geometry in projected_assets.geometry:
                area = geometry.area

                if area <= 0:
                    fractions.append(None)
                else:
                    fraction = (
                        geometry.intersection(
                            projected_flood_geometry
                        ).area / area
                    )
                    fractions.append(
                        min(1.0, max(0.0, fraction))
                    )

            assets.loc[valid_assets, "exposure_fraction"] = fractions

    write_geojson_atomically(assets, output_path)

    counts = assets["exposure_status"].value_counts().to_dict()

    return {
        "total_assets": len(assets),
        "exposure_counts": counts,
        "output_file": str(output_path),
        "crs": "EPSG:4326",
        "classification_note": (
            "Potential geometric overlap with potential-change areas; "
            "not confirmation of flooding or infrastructure damage."
        ),
    }
