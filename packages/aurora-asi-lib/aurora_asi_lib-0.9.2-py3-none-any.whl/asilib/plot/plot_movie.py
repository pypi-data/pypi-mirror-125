import pathlib
from typing import List, Union, Sequence, Generator, Tuple
from datetime import datetime
import collections

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
import ffmpeg

import asilib
from asilib.io import utils
from asilib.io.load import load_image, load_skymap
from asilib.analysis.start_generator import start_generator


def plot_movie(
    asi_array_code: str, 
    location_code: str, 
    time_range: utils._time_range_type, 
    **kwargs
) -> None:
    """
    Make a movie of THEMIS or REGO fisheye images.

    This function basically runs plot_movie_generator() in a for loop. The two function's
    arguments and keyword arguments are identical, so see plot_movie_generator() docs for 
    the full argument list.

    Note: To make movies, you'll need to install ffmpeg in your operating system.

    Parameters
    ----------
    asi_array_code: str
        The imager array name, i.e. ``THEMIS`` or ``REGO``.
    location_code: str
        The ASI station code, i.e. ``ATHA``
    time_range: list of datetime.datetimes or stings
        Defined the duration of data to download. Must be of length 2.
    force_download: bool
        If True, download the file even if it already exists. Useful if a prior 
        data download was incomplete. 
    label: bool
        Flag to add the "asi_array_code/location_code/image_time" text to the plot.
    color_map: str
        The matplotlib colormap to use. If 'auto', will default to a
        black-red colormap for REGO and black-white colormap for THEMIS.
        For more information See
        https://matplotlib.org/3.3.3/tutorials/colors/colormaps.html
    color_bounds: List[float] or None
        The lower and upper values of the color scale. If None, will
        automatically set it to low=1st_quartile and
        high=min(3rd_quartile, 10*1st_quartile)
    ax: plt.Axes
        The optional subplot that will be drawn on.
    azel_contours: bool
        Switch azimuth and elevation contours on or off.
    movie_container: str
        The movie container: mp4 has better compression but avi was determined
        to be the official container for preserving digital video by the
        National Archives and Records Administration.
    ffmpeg_output_params: dict
        The additional/overwitten ffmpeg output prameters. The default parameters are:
        framerate=10, crf=25, vcodec=libx264, pix_fmt=yuv420p, preset=slower.
    overwrite: bool
        If true, the output will be overwritten automatically. If false it will
        prompt the user to answer y/n.
    color_norm: str
        Sets the 'lin' linear or 'log' logarithmic color normalization.

    Returns
    -------
    None

    Raises
    ------
    NotImplementedError
        If the colormap is unspecified ('auto' by default) and the
        auto colormap is undefined for an ASI array.
    ValueError
        If the color_norm kwarg is not "log" or "lin".

    Example
    -------
    | from datetime import datetime
    |
    | import asilib
    |
    | time_range = (datetime(2015, 3, 26, 6, 7), datetime(2015, 3, 26, 6, 12))
    | asilib.plot_movie('THEMIS', 'FSMI', time_range)
    | print(f'Movie saved in {asilib.config["ASI_DATA_DIR"] / "movies"}')
    """

    # Create a subplot object if one is not passed.
    ax = kwargs.get('ax', None)
    if ax is None:
        _, ax = plt.subplots(figsize=(6, 6))
        kwargs['ax'] = ax
        plt.tight_layout()

    movie_generator = plot_movie_generator(asi_array_code, location_code, time_range, **kwargs)

    for image_time, image, im, ax in movie_generator:
        pass
    return


Images = collections.namedtuple('Images', ['time', 'images'])


@start_generator
def plot_movie_generator(
    asi_array_code: str,
    location_code: str,
    time_range: utils._time_range_type,
    force_download: bool = False,
    label: bool = True,
    color_map: str = 'auto',
    color_bounds: Union[List[float], None] = None,
    color_norm: str = 'log',
    azel_contours: bool = False,
    ax: plt.Axes = None,
    movie_container: str = 'mp4',
    ffmpeg_output_params={},
    overwrite: bool = False,
) -> Generator[Tuple[datetime, np.ndarray, plt.Axes, matplotlib.image.AxesImage], None, None]:
    """
    A generator function that loads the ASI data and then yields individual ASI images,
    image by image. This allows the user to add content to each image, such as the
    spacecraft position, and that will convert it to a movie. If you just want to make
    an ASI movie, use the wrapper for this function, plot_movie().

    Once this generator is initiated with the name `gen`, but **before** the for loop,
    you can get the ASI images and times by calling `gen.send('data')`. This will yield a
    collections.namedtuple with `time` and `images` attributes.

    Parameters
    ----------
    asi_array_code: str
        The imager array name, i.e. ``THEMIS`` or ``REGO``.
    location_code: str
        The ASI station code, i.e. ``ATHA``
    time_range: list of datetime.datetimes or stings
        Defined the duration of data to download. Must be of length 2.
    force_download: bool
        If True, download the file even if it already exists. Useful if a prior 
        data download was incomplete.
    label: bool
        Flag to add the "asi_array_code/location_code/image_time" text to the plot.
    color_map: str
        The matplotlib colormap to use. If 'auto', will default to a
        black-red colormap for REGO and black-white colormap for THEMIS.
        For more information See
        https://matplotlib.org/3.3.3/tutorials/colors/colormaps.html
    color_bounds: List[float] or None
        The lower and upper values of the color scale. If None, will
        automatically set it to low=1st_quartile and
        high=min(3rd_quartile, 10*1st_quartile)
    ax: plt.Axes
        The optional subplot that will be drawn on.
    movie_container: str
        The movie container: mp4 has better compression but avi was determined
        to be the official container for preserving digital video by the
        National Archives and Records Administration.
    ffmpeg_output_params: dict
        The additional/overwitten ffmpeg output parameters. The default parameters are:
        framerate=10, crf=25, vcodec=libx264, pix_fmt=yuv420p, preset=slower.
    color_norm: str
        Sets the 'lin' linear or 'log' logarithmic color normalization.
    azel_contours: bool
        Switch azimuth and elevation contours on or off.
    overwrite: bool
        If true, the output will be overwritten automatically. If false it will
        prompt the user to answer y/n.

    Yields
    ------
    image_time: datetime.datetime
        The time of the current image.
    image: np.ndarray
        A 2d image array of the image corresponding to image_time
    ax: plt.Axes
        The subplot object to modify the axis, labels, etc.
    im: plt.AxesImage
        The plt.imshow image object. Common use for im is to add a colorbar.
        The image is oriented in the map orientation (north is up, south is down,
        east is right, and west is left), contrary to the camera orientation where
        the east/west directions are flipped. Set azel_contours=True to confirm.

    Raises
    ------
    NotImplementedError
        If the colormap is unspecified ('auto' by default) and the
        auto colormap is undefined for an ASI array.
    ValueError
        If the color_norm kwarg is not "log" or "lin".

    Example
    -------
    | from datetime import datetime
    |
    | import asilib
    |
    | time_range = (datetime(2015, 3, 26, 6, 7), datetime(2015, 3, 26, 6, 12))
    | movie_generator = asilib.plot_movie_generator('THEMIS', 'FSMI', time_range)
    |
    | for image_time, image, im, ax in movie_generator:
    |       # The code that modifies each image here.
    |       pass
    |
    | print(f'Movie saved in {asilib.config["ASI_DATA_DIR"] / "movies"}')
    """
    try:
        image_times, images = load_image(
            asi_array_code, location_code, time_range=time_range, force_download=force_download
        )
    except AssertionError as err:
        if '0 number of time stamps were found in time_range' in str(err):
            print(
                f'The file exists for {asi_array_code}/{location_code}, but no data '
                f'between {time_range}.'
            )
            raise
        else:
            raise
    if ax is None:
        _, ax = plt.subplots()

    # Create the movie directory inside asilib.config['ASI_DATA_DIR'] if it does
    # not exist.
    image_save_dir = pathlib.Path(
        asilib.config['ASI_DATA_DIR'],
        'movies',
        'images',
        f'{image_times[0].strftime("%Y%m%d_%H%M%S")}_{asi_array_code.lower()}_'
        f'{location_code.lower()}',
    )
    if not image_save_dir.is_dir():
        image_save_dir.mkdir(parents=True)
        print(f'Created a {image_save_dir} directory')

    if (color_map == 'auto') and (asi_array_code.lower() == 'themis'):
        color_map = 'Greys_r'
    elif (color_map == 'auto') and (asi_array_code.lower() == 'rego'):
        color_map = colors.LinearSegmentedColormap.from_list('black_to_red', ['k', 'r'])
    else:
        raise NotImplementedError('color_map == "auto" but the asi_array_code is unsupported')

    # With the @start_generator decorator, when this generator first gets called, it
    # will halt here. This way the errors due to missing data will be raised up front.
    user_input = yield
    # user_input can be used to get the image_times and images out of the generator.
    if isinstance(user_input, str) and 'data' in user_input.lower():
        yield Images(image_times, images)

    for image_time, image in zip(image_times, images):
        # If the image is all 0s we have a bad image and we need to skip it.
        if np.all(image == 0):
            continue
        ax.clear()
        ax.axis('off')
        # if-else statement is to recalculate color_bounds for every image 
        # and set it to _color_bounds. If _color_bounds did not exist, 
        # color_bounds will be overwritten after the first iteration which will 
        # disable the dynamic color bounds for each image. 
        if color_bounds is None:
            lower, upper = np.quantile(image, (0.25, 0.98))
            _color_bounds = [lower, np.min([upper, lower * 10])]
        else:
            _color_bounds = color_bounds

        if color_norm == 'log':
            norm = colors.LogNorm(vmin=_color_bounds[0], vmax=_color_bounds[1])
        elif color_norm == 'lin':
            norm = colors.Normalize(vmin=_color_bounds[0], vmax=_color_bounds[1])
        else:
            raise ValueError('color_norm must be either "log" or "lin".')

        im = ax.imshow(image, cmap=color_map, norm=norm, origin='lower')
        if label:
            ax.text(
                0,
                0,
                f"{asi_array_code.upper()}/{location_code.upper()}\n{image_time.strftime('%Y-%m-%d %H:%M:%S')}",
                va='bottom',
                transform=ax.transAxes,
                color='white',
            )

        if azel_contours:
            _add_azel_contours(asi_array_code, location_code, image_time, ax, force_download)

        # Give the user the control of the subplot, image object, and return the image time
        # so that the user can manipulate the image to add, for example, the satellite track.
        yield image_time, image, ax, im

        # Save the plot before the next iteration.
        save_name = (
            f'{image_time.strftime("%Y%m%d_%H%M%S")}_{asi_array_code.lower()}_'
            f'{location_code.lower()}.png'
        )
        plt.savefig(image_save_dir / save_name)

    # Make the movie
    movie_file_name = (
        f'{image_times[0].strftime("%Y%m%d_%H%M%S")}_'
        f'{image_times[-1].strftime("%H%M%S")}_'
        f'{asi_array_code.lower()}_{location_code.lower()}.{movie_container}'
    )
    _write_movie(image_save_dir, ffmpeg_output_params, movie_file_name, overwrite)
    return


def _write_movie(image_save_dir, ffmpeg_output_params, movie_file_name, overwrite):
    """
    Helper function to write a movie using ffmpeg.

    Parameters
    ----------
    image_save_dir: pathlib.Path
        The directory where the individual images are saved to.
    ffmpeg_output_params: dict
        The additional/overwitten ffmpeg output parameters. The default parameters are:
        framerate=10, crf=25, vcodec=libx264, pix_fmt=yuv420p, preset=slower.
    movie_file_name: str
        The movie file name.
    overwrite: bool
        Overwrite the movie.

    """
    ffmpeg_params = {
        'framerate': 10,
        'crf': 25,
        'vcodec': 'libx264',
        'pix_fmt': 'yuv420p',
        'preset': 'slower',
    }
    # Add or change the ffmpeg_params's key:values with ffmpeg_output_params
    ffmpeg_params.update(ffmpeg_output_params)

    movie_save_path = image_save_dir.parents[1] / movie_file_name
    movie_obj = ffmpeg.input(
        str(image_save_dir) + f'/*.png',
        pattern_type='glob',
        # Use pop so it won't be passed into movie_obj.output().
        framerate=ffmpeg_params.pop('framerate'),
    )
    movie_obj.output(str(movie_save_path), **ffmpeg_params).run(overwrite_output=overwrite)
    return


def _add_azel_contours(
    asi_array_code: str,
    location_code: str,
    time: utils._time_type,
    ax: plt.Axes,
    force_download: bool,
    color: str = 'yellow',
) -> None:
    """
    Adds contours of azimuth and elevation to the movie image.

    Parameters
    ----------
    asi_array_code: str
        The asi_array_code, can be either THEMIS or REGO.
    location_code: str
        The imager location code to download the data from.
    time: datetime, or str
        Time is used to find the relevant skymap file: file created nearest to, and before, the time.
    ax: plt.Axes
        The subplot that will be drawn on.
    force_download: bool
        If True, download the file even if it already exists.
    color: str (optional)
        The contour color.
    """
    skymap_dict = load_skymap(asi_array_code, location_code, time, force_download=force_download)

    az_contours = ax.contour(
        skymap_dict['FULL_AZIMUTH'],
        colors=color,
        linestyles='dotted',
        levels=np.arange(0, 361, 90),
        alpha=1,
    )
    el_contours = ax.contour(
        skymap_dict['FULL_ELEVATION'],
        colors=color,
        linestyles='dotted',
        levels=np.arange(0, 91, 30),
        alpha=1,
    )
    plt.clabel(az_contours, inline=True, fontsize=12, colors=color)
    plt.clabel(el_contours, inline=True, fontsize=12, colors=color, rightside_up=True)
    return
