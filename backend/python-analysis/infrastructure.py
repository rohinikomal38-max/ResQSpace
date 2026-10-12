
def assess_exposure(asset_geometry, flood_geometry):
    """
    Assess potential exposure by checking whether an asset
    intersects the supplied flood geometry.

    Returns:
        exposed: True if the geometries intersect, otherwise False.
    """
    if asset_geometry is None or flood_geometry is None:
        return None

    if asset_geometry.is_empty or flood_geometry.is_empty:
        return None

    return asset_geometry.intersects(flood_geometry)
