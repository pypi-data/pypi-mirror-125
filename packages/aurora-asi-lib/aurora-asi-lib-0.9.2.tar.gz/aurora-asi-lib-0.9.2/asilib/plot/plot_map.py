"""
This module contains functions to project the ASI images to a map.
"""
from typing import List, Union
from datetime import datetime
import importlib

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np

try:
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
except ImportError:
    pass  # make sure that asilb.__init__ fully loads and crashes if the user calls asilib.plot_map().

from asilib.io import load
from asilib.io import utils

def plot_map(
    asi_array_code: str,
    location_code: str,
    time: utils._time_type,
    map_alt: float,
    time_thresh_s: float = 3,
    ax: plt.Axes = None,
    map_style = 'green',
    color_map: str = 'auto',
    min_elevation: float = 10,
    norm=True,
    asi_label=True,
    color_bounds: Union[List[float], None] = None,
    color_norm: str = 'log',
    pcolormesh_kwargs={},
):
    """
    Projects the ASI images to a map at an altitude defined in the skymap calibration file.

    Parameters
    ----------
    asi_array_code: str
        The imager array name, i.e. ``THEMIS`` or ``REGO``.
    location_code: str
        The ASI station code, i.e. ``ATHA``
    time: datetime.datetime or str
        The date and time to download of the data. If str, ``time`` must be in the
        ISO 8601 standard.
    map_alt: float
        The altitude in kilometers to project to. Must be an altitude value
        in the skymap calibration.
    time_thresh_s: float
        The maximum allowable time difference between ``time`` and an ASI time stamp.
        This is relevant only when ``time`` is specified.
    ax: plt.Axes
        The subplot to plot the image on. If None, this function will
        create one.
    map_style: str
        If ax is None, this kwarg toggles between two predefined map styles:
        'green' map has blue oceans and green land, while the `white` map
        has white oceans and land with black coastlines.
    color_map: str
        The matplotlib colormap to use. If 'auto', will default to a
        black-red colormap for REGO and black-white colormap for THEMIS.
        For more information See https://matplotlib.org/3.3.3/tutorials/colors/colormaps.html
    min_elevation: float
        Masks the pixels below min_elevation degrees.
    norm: bool
        If True, normalizes the image array to 0-1. This is useful when
        mapping images from multiple imagers.
    asi_label: bool
        Annotates the map with the ASI code in the center of the image.
    color_bounds: List[float] or None
        The lower and upper values of the color scale. If None, will
        automatically set it to low=1st_quartile and
        high=min(3rd_quartile, 10*1st_quartile)
    color_norm: str
        Sets the 'lin' linear or 'log' logarithmic color normalization.
    pcolormesh_kwargs: dict
        A dictionary of keyword arguments (kwargs) to pass directly into
        plt.pcolormesh. One use of this parameter is to change the colormap. For example,
        pcolormesh_kwargs = {'cmap':'tu}

    Returns
    -------
    image_time: datetime.datetime
        The time of the current image.
    image: np.array
        The 2d ASI image corresponding to image_time.
    skyamp: dict
        The skymap calibration for that ASI.
    ax: plt.Axes
        The subplot object to modify the axis, labels, etc.
    p: plt.AxesImage
        The plt.pcolormesh image object. Common use for p is to add a colorbar.
    """
    # Halt here if cartopy is not installed.
    if importlib.util.find_spec("cartopy") is None:
        raise ImportError(
            "cartopy can't be imported. This is a required dependency for asilib.plot_map()"
            " that must be installed separately. See https://scitools.org.uk/cartopy/docs/latest/installing.html"
            " and https://aurora-asi-lib.readthedocs.io/en/latest/installation.html."
        )

    image_time, image = load.load_image(
        asi_array_code, location_code, time=time, time_thresh_s=time_thresh_s
    )
    skymap = load.load_skymap(asi_array_code, location_code, time)

    # Check that the map_alt is in the skymap calibration data.
    assert (
        map_alt in skymap['FULL_MAP_ALTITUDE'] / 1000
    ), f'{map_alt} km is not in skymap calibration altitudes: {skymap["FULL_MAP_ALTITUDE"]/1000} km'
    alt_index = np.where(skymap['FULL_MAP_ALTITUDE'] / 1000 == map_alt)[0][0]

    image, lon_map, lat_map = _mask_low_horizon(
        image,
        skymap['FULL_MAP_LONGITUDE'][alt_index, :, :],
        skymap['FULL_MAP_LATITUDE'][alt_index, :, :],
        skymap['FULL_ELEVATION'],
        min_elevation,
    )

    if norm:
        image /= np.nanmax(image)

    # Set up the plot parameters
    if ax is None:
        ax = _make_map(map_style)

    if color_bounds is None:
        lower, upper = np.nanquantile(image, (0.25, 0.98))
        color_bounds = [lower, np.min([upper, lower * 10])]

    if (color_map == 'auto') and (asi_array_code.lower() == 'themis'):
        color_map = 'Greys_r'
    elif (color_map == 'auto') and (asi_array_code.lower() == 'rego'):
        color_map = colors.LinearSegmentedColormap.from_list('black_to_red', ['k', 'r'])
    else:
        raise NotImplementedError('color_map == "auto" but the asi_array_code is unsupported')

    if color_norm == 'log':
        norm = colors.LogNorm(vmin=color_bounds[0], vmax=color_bounds[1])
    elif color_norm == 'lin':
        norm = colors.Normalize(vmin=color_bounds[0], vmax=color_bounds[1])
    else:
        raise ValueError('color_norm must be either "log" or "lin".')

    p = _pcolormesh_nan(lon_map, lat_map, image, ax, cmap=color_map, norm=norm)

    if asi_label:
        ax.text(
            skymap['SITE_MAP_LONGITUDE'],
            skymap['SITE_MAP_LATITUDE'],
            location_code.upper(),
            color='r',
            transform=ccrs.PlateCarree(),
            va='center',
            ha='center',
        )
    return image_time, image, skymap, ax, p

def _make_map(map_style):
    """
    Helper function to make a few types of map styles.
    """
    fig = plt.figure(figsize=(8, 5))
    plot_extent = [-160, -52, 40, 82]
    central_lon = np.mean(plot_extent[:2])
    central_lat = np.mean(plot_extent[2:])
    projection = ccrs.Orthographic(central_lon, central_lat)
    ax = fig.add_subplot(1, 1, 1, projection=projection)
    ax.set_extent(plot_extent, crs=ccrs.PlateCarree())

    if map_style == 'white':
        ax.coastlines()
        ax.gridlines(linestyle=':')
    elif map_style == 'green':
        ax.add_feature(cfeature.LAND, color='green')
        ax.add_feature(cfeature.OCEAN)
        ax.add_feature(cfeature.COASTLINE)
        ax.gridlines(linestyle=':')
    else:
        raise ValueError("Only the 'white' and 'green' map_style are implemented.")
    return ax

def _pcolormesh_nan(x: np.ndarray, y: np.ndarray, c: np.ndarray, ax, cmap=None, norm=None):
    """
    Since pcolormesh cant handle nan lat/lon grid values, we will compress them to the
    nearest valid lat/lon grid. There are two main steps:

    1) All nan values to the left of the first valid value are
    reassigned to the first valid value. Likewise, all nan values to the
    right of the last valid value are reassigned to it.

    2) All nan-filled rows above the first valid row are assigned to the
    maximum value in the first row, likewise for the bottom rows.

    Essentially this is a reassignment (or a compression) of all nan values in the periphery
    to the valid grid values in the center.

    Function taken from Michael, scivision @ GitHub.:
    https://github.com/scivision/python-matlab-examples/blob/0dd8129bda8f0ec2c46dae734d8e43628346388c/PlotPcolor/pcolormesh_NaN.py
    """
    # mask is True when lat and lon grid values are not nan.
    mask = np.isfinite(x) & np.isfinite(y)
    top = None
    bottom = None

    for i, m in enumerate(mask):
        # A common use for nonzero is to find the indices of
        # an array, where a condition is True (not nan or inf)
        good = m.nonzero()[0]

        if good.size == 0:  # Skip row is all columns are nans.
            continue
        # First row that has at least 1 valid value.
        elif top is None:
            top = i
        # Bottom row that has at least 1 value value. All indices in between top and bottom
        else:
            bottom = i

        # Reassign all lat/lon columns after good[-1] (all nans) to good[-1].
        x[i, good[-1] :] = x[i, good[-1]]
        y[i, good[-1] :] = y[i, good[-1]]
        # Reassign all lat/lon columns before good[0] (all nans) to good[0].
        x[i, : good[0]] = x[i, good[0]]
        y[i, : good[0]] = y[i, good[0]]

    # Reassign all of the fully invalid lat/lon rows above top to the the max lat/lon value.
    x[:top, :] = np.nanmax(x[top, :])
    y[:top, :] = np.nanmax(y[top, :])
    # Same, but for the rows below bottom.
    x[bottom:, :] = np.nanmax(x[bottom, :])
    y[bottom:, :] = np.nanmax(y[bottom, :])

    # TODO: skymap rotation.
    # old masked c code: np.ma.masked_where(~mask[:-1, :-1], c)[::-1, ::-1]
    p = ax.pcolormesh(
        x, y, c, cmap=cmap, shading='flat', transform=ccrs.PlateCarree(), norm=norm
    )
    return p


def _mask_low_horizon(image, lon_map, lat_map, el_map, min_elevation):
    """
    Mask the image, skymap['FULL_MAP_LONGITUDE'], skymap['FULL_MAP_LONGITUDE'] arrays
    with np.nans where the skymap['FULL_ELEVATION'] is nan or
    skymap['FULL_ELEVATION'] < min_elevation.
    """
    idh = np.where(np.isnan(el_map) | (el_map < min_elevation))
    # Copy variables to not modify original np.arrays.
    image_copy = image.copy()
    lon_map_copy = lon_map.copy()
    lat_map_copy = lat_map.copy()
    # Can't mask image unless it is a float array.
    image_copy = image_copy.astype(float)
    image_copy[idh] = np.nan
    lon_map_copy[idh] = np.nan
    lat_map_copy[idh] = np.nan

    # For some reason the lat/lon_map arrays are one size larger than el_map, so
    # here we mask the boundary indices in el_map by adding 1 to both the rows
    # and columns.
    idh_boundary_bottom = (idh[0] + 1, idh[1])  # idh is a tuple so we have to create a new one.
    idh_boundary_right = (idh[0], idh[1] + 1)
    lon_map_copy[idh_boundary_bottom] = np.nan
    lat_map_copy[idh_boundary_bottom] = np.nan
    lon_map_copy[idh_boundary_right] = np.nan
    lat_map_copy[idh_boundary_right] = np.nan
    return image_copy, lon_map_copy, lat_map_copy