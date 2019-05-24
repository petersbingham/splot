# splot
Simple plot line and scatter plot functions. Built around matplotlib.

## Installation

Clone the repository and install with the following commands:

    git clone https://github.com/petersbingham/splot.git
    cd splot
    python setup.py install

## Dependencies

Third party packages:
 - Matplotlib

## Usage

Provides the following functions:

    def line(xss, yss, title="", xlabel="", ylabel="", legends=None, logx=False, logy=False,
             marker_sz=None, mark_with_line=False, draw_axes=False, path=None, display=True)

    def scatter(xss, yss, title="", xlabel="", ylabel="", logx=False, logy=False,
                legend=None, marker_sz=None, draw_axes=False, path=None, display=True)

    def line_from_csv(csvpath, title="", xlabel="", ylabel="", legends=None, logx=False, logy=False,
                      marker_sz=None, path=None, mark_with_line=False, draw_axes=False)

Note the `display` parameter can be used to suppress the chart display. It only makes sense to use this with the `path` parameter, which will save a copy of the chart (default `png`) at `path`. You may be wanting to do this because you don't have X or you don't have a python backend installed. If the second of these then you may also have to turn the default matplotlib backend off with a command like:

    export MPLBACKEND="agg"

In addition there are the folowing plot configuration functions to override the defaults:

    def set_sub_plot_parameters(left=None, bottom=None, right=None,
                                top=None, wspace=None, hspace=None)
    def set_img_size(width, height)
    def set_extents(xlim_, ylim_)
    def set_colour_cycle(cycle)
    def turn_off_colour_cycle()
    def set_line_width(width)
