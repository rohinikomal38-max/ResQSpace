import geopandas as gpd


def assess_exposure(asset_geometry, flood_geometry):
    """Return True, False, or None if exposure cannot be assessed."""
    if asset_geometry is None or flood_geometry is None:
        return None

    if asset_geometry.is_empty or flood_geometry.is_empty:
        return None

    return asset_geometry.intersects(flood_geometry)


def process_asset_file(assets_path, flood_path, output_path):
    """
    Assess infrastructure exposure against a flood extent.

    Input files must be readable GeoJSON files with valid CRS information.
    Output is written as GeoJSON in EPSG:4326.
    """
    assets = gpd.read_file(assets_path)
    flood = gpd.read_file(flood_path)

    if assets.crs is None or flood.crs is None:
        raise ValueError("Both input files must have a defined CRS.")

    if assets.empty or flood.empty:
        raise ValueError("Asset and flood files must not be empty.")

    assets = assets.to_crs("EPSG:4326")
    flood = flood.to_crs("EPSG:4326")

    flood_geometry = flood.geometry.union_all()

    assets["exposure_status"] = assets.geometry.apply(
        lambda geometry: (
            "not_assessed"
            if geometry is None or geometry.is_empty
            else (
                "exposed"
                if assess_exposure(geometry, flood_geometry)
                else "not_exposed"
            )
        )
    )

    assets["exposure_fraction"] = None

    valid_assets = assets.geometry.notna() & ~assets.geometry.is_empty

    if valid_assets.any():
        projected_crs = assets.estimate_utm_crs()

        if projected_crs is not None:
            projected_assets = assets.loc[valid_assets].to_crs(
                projected_crs
            )
            projected_flood = flood.to_crs(projected_crs)
            projected_flood_geometry = projected_flood.geometry.union_all()

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

    assets.to_file(output_path, driver="GeoJSON")

    counts = assets["exposure_status"].value_counts().to_dict()

    return {
        "total_assets": len(assets),
        "exposure_counts": counts,
        "output_file": output_path,
        "crs": "EPSG:4326",
    }
