import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math
import csv
import sys

LEFT = 0.12
BOTTOM = 0.1
RIGHT = 0.9
TOP = 0.9
WSPACE = 0.2
HSPACE = 0.2

FIGSZ_W = 8
FIGSZ_H = 6


class StaticPlot:
    DPI = 80

    def __init__(self, title, rows=1, cols=1, draw_axes=False):
        self.fig = plt.figure(figsize=(FIGSZ_W,FIGSZ_H), dpi=self.DPI)
        self.fig.suptitle(title)
        self.rows = rows
        self.cols = cols
        self.draw_axes = draw_axes
        self.lines = []
        self.legend = []
        self.axis_config = []
        self.fig.subplots_adjust(left=LEFT, bottom=BOTTOM, right=RIGHT,
                                 top=TOP, wspace=WSPACE, hspace=HSPACE)

    def add_plot(self, xlabel, ylabel, logx=False, logy=False):
        plot_num = len(self.axis_config)+1
        self.fig.add_subplot(self.rows,self.cols,plot_num)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        self.axis_config.append([logx,logy])

    def add_line(self, plot_num, xs, ys, legend=None,
                 marker_sz=None, mark_with_line=False):
        self._add_data(plot_num, xs, ys, legend, marker_sz,
                       False, mark_with_line)

    def add_scat(self, plot_num, xs, ys, logx=False, logy=False,
                 legend=None, marker_sz=None):
        if logx:
          plt.gca().set_xscale('log')
        if logy:
          plt.gca().set_yscale('log')
        self._add_data(plot_num, xs, ys, legend, marker_sz, True, False)

    def _add_data(self, plot_num, xs, ys, legend, marker_sz,
                  scatter, mark_with_line):
        xs, ys, use_ticks = self._convert_values(xs, ys, plot_num, scatter)
        if scatter:
            l = self._add_scat_type(plot_num, xs, ys, marker_sz)
        else:
            l = self._add_line_type(plot_num, xs, ys, marker_sz, mark_with_line, use_ticks)
        self.lines.append(l)
        if legend is not None:
            self.legend.append(legend)

    def _create_array(self, vals):
        return np.ndarray((len(vals),), buffer=np.array([float(val) for val in vals]))

    def _convert_values(self, xs, ys, plot_num, scatter):
        use_ticks = False
        if type(xs) is list:
            if not scatter and not self.axis_config[plot_num-1][0]:
                try:
                    xs = self._create_array(xs)
                except ValueError:
                    # Just use as strings labelling the x-axis.
                    use_ticks = True
                    pass
            else:
                xs = self._create_array(xs)
        if type(ys) is list:
            ys = self._create_array(ys)
        return xs, ys, use_ticks

    def _add_scat_type(self, plot_num, xs, ys, marker_sz):
        # Need to manually do the cycling for the scatter.
        axes = plt.gca()
        color_cycle = axes._get_lines.prop_cycler
        col = next(color_cycle)['color']
        return plt.scatter(xs, ys, color=col, s=20, edgecolor='none')

    def _add_line_type(self, plot_num, xs, ys, marker_sz, mark_with_line, use_ticks):
        kwargs = {'basex':10}
        if marker_sz:
            kwargs = {'basex':10, 'linestyle':'None' if not mark_with_line else 'solid', 'marker':'o', 'markerfacecolor':'black', 'markersize':marker_sz}
        if self.axis_config[plot_num-1][0] and self.axis_config[plot_num-1][1]:
            l, = plt.loglog(xs, ys, **kwargs)
        elif self.axis_config[plot_num-1][0]:
            l, = plt.semilogx(xs, ys, **kwargs)
        elif self.axis_config[plot_num-1][1]:
            kwargs.pop('basex')
            if not use_ticks:
              l, = plt.semilogy(xs, ys, **kwargs)
            else:
              l, = plt.semilogy(ys, **kwargs)
        else:
            kwargs.pop('basex')
            if not use_ticks:
              l, = plt.plot(xs, ys, **kwargs)
            else:
              l, = plt.plot(ys, **kwargs)
        if use_ticks:
            if rotate_tick_lbls:
                plt.xticks(range(len(xs)), xs, rotation='vertical')
            else:
                plt.xticks(range(len(xs)), xs)
        if dash_cycle is not None:
            l.set_dashes(dash_cycle[dash_index])
        return l

    def reveal(self, display, vlines=[]):
        if self.draw_axes:
            plt.axhline(0, color='black')
            plt.axvline(0, color='black')

        if len(self.legend) > 0:
            if legend_axis_reduction is None: 
                plt.legend(self.lines, self.legend, labelspacing=legend_spacing, prop={'size':legend_font_size})
            else:
                plt.legend(self.lines, self.legend, labelspacing=legend_spacing, prop={'size':legend_font_size}, bbox_to_anchor=(1.04,1), loc="upper left")
        else:
            if legend_axis_reduction is None: 
                plt.legend(labelspacing=legend_spacing, prop={'size':legend_font_size})
            else:
                plt.legend(labelspacing=legend_spacing, prop={'size':legend_font_size}, bbox_to_anchor=(1.04,1), loc="upper left")
        if legend_axis_reduction is not None: 
            plt.subplots_adjust(right=1.0-legend_axis_reduction/100.)

        if line_width is not None:
            for line in self.lines:
                line.set_linewidth(line_width)
        axes = plt.gca()
        if xlim is not None:
            axes.set_xlim(xlim)
        if ylim is not None:
            axes.set_ylim(ylim)
        for v_line in vlines:
            plt.axvline(x=v_line, linewidth=vline_width, color=vline_colour)
        plt.draw()
        if display:
            plt.show()

    def save(self, path):
        self.fig.savefig(path, dpi=self.DPI)

def set_sub_plot_parameters(left=None, bottom=None, right=None,
                            top=None, wspace=None, hspace=None):
    global LEFT
    global BOTTOM
    global RIGHT
    global TOP
    global WSPACE
    global HSPACE
    if left: LEFT = left
    if bottom: BOTTOM = bottom
    if right: RIGHT = right
    if top: TOP = top
    if wspace: WSPACE = wspace
    if hspace: HSPACE = hspace

def set_img_size(width, height):
    global FIGSZ_W
    global FIGSZ_H
    FIGSZ_W = width
    FIGSZ_H = height

legend_axis_reduction = None
def place_legend_outside(axis_reduction_percent):
    global legend_axis_reduction
    legend_axis_reduction = axis_reduction_percent

legend_spacing = 0.5
def set_legend_spacing(spacing):
    global legend_spacing
    legend_spacing = spacing

legend_font_size = 14
def set_font_size(label_size, legend_size):
    global legend_font_size
    matplotlib.rc('font', size=label_size)
    legend_font_size = legend_size

xlim = None
ylim = None
def set_extents(xlim_, ylim_):
    global xlim
    global ylim
    xlim = xlim_
    ylim = ylim_

# tab20 appears to have the most distinguishable colours.
# call plt.get_cmap('') to get a list of available maps.
def create_colour_cycle(num_colours, alpha=1., map='tab20'):
    cm = [plt.get_cmap(map)(1.*i/num_colours) for i in range(num_colours)]
    return [(t[0],t[1],t[2],alpha) for t in cm]

def set_colour_cycle(cycle):
    from cycler import cycler
    plt.rc('axes', prop_cycle=(cycler('color', cycle)))

def config_colour_cycle(num_colours, alpha=1., map='tab20'):
    set_colour_cycle(create_colour_cycle(num_colours, alpha, map))

def turn_off_colour_cycle():
    from cycler import cycler
    plt.rc('axes', prop_cycle=(cycler('color', ['black'])))

rotate_tick_lbls = False
def rotate_tick_labels():
    global rotate_tick_lbls
    rotate_tick_lbls = not rotate_tick_lbls

dash_cycle = None
dash_index = 0
def set_dash_cycle(cycle):
    global dash_cycle
    dash_cycle = cycle

line_width = None
def set_line_width(width):
    global line_width
    line_width = width

vline_width = None
vline_colour = None
def set_vline_config(width=None, colour=None):
    global vline_width
    global vline_colour
    if width: vline_width = width
    if colour: vline_colour = colour

orig_backend = matplotlib.get_backend()
def backend_off():
    # If not displaying then turn off backend. This will prevent any errors if not available.
    plt.switch_backend('Agg')

def backend_on():
    plt.switch_backend(orig_backend)

def _get_data_from_file(csvpaths, delimiter=',', x_index=0, y_indices=1):
    if isinstance(y_indices, int):
        if x_index == y_indices:
            raise Exception("x and y indices can not be the same")
        y_indices = [y_indices]

    xss = []
    yss = []
    if isinstance(csvpaths, str):
        csvpaths = [csvpaths]
    for csvpath in csvpaths:
        with open(csvpath, 'rb') as csvfile:
            csvReader = csv.reader(csvfile, delimiter=delimiter)
            xs = []
            ys = None
            for row in csvReader:
                if delimiter==' ':
                    row = [el for el in row if el!='']
                xs.append(float(row[x_index].strip()))
                if ys is None:
                    num_yss = len(y_indices)
                    ys = [[] for i in range(0, num_yss)]
                j = 0
                for i in range(0,len(row)):
                    if i in y_indices:
                        ys[j].append(float(row[i]))
                        j += 1
            yss.extend(ys)
            xss.extend([xs]*num_yss)
    return xss, yss

def _finialise(p, path, display, vlines=[]):
    p.reveal(display, vlines)
    if path is not None:
        p.save(path)

def _plot(title, xs, yss, xlabel, ylabel, legend, logx, logy,
          marker_sz, mark_with_line, draw_axes, path, plot):
    p = plot
    if p is None:
        p = StaticPlot(title,draw_axes=draw_axes)
        p.add_plot(xlabel, ylabel, logx, logy)
    global dash_index
    dash_index = 0
    for i in range(len(yss)):
        if legend is not None:
            p.add_line(1,xs[:len(yss[i])],yss[i],legend[i],marker_sz,mark_with_line)
        else:
            p.add_line(1,xs[:len(yss[i])],yss[i],None,marker_sz,mark_with_line)
        dash_index += 1
    return p

def _plot2(title, xss, yss, xlabel, ylabel, legend, logx,
           logy, marker_sz, mark_with_line, draw_axes, path, plot):
    p = plot
    if p is None:
        p = StaticPlot(title,draw_axes=draw_axes)
        p.add_plot(xlabel, ylabel, logx, logy)
    global dash_index
    dash_index = 0
    for i in range(len(xss)):
        if type(marker_sz) is list:
          ms = marker_sz[i]
        else:
          ms = marker_sz

        if legend is not None:
            p.add_line(1,xss[i][:len(yss[i])],yss[i],legend[i],ms,mark_with_line)
        else:
            p.add_line(1,xss[i][:len(yss[i])],yss[i],None,ms,mark_with_line)
        dash_index += 1
    return p

def _is_container(item):
    return isinstance(item, list) or isinstance(item, np.ndarray)

def _check_input(plot, title, xlabel, ylabel, logx, logy):
    if plot and (title != "" or xlabel != "" or ylabel != "" or logx is not None or logy is not None):
        raise Exception("Cannot configure title, label or log when supplying parent plot. Specify when creating parent.")

def line(xss, yss, title="", xlabel="", ylabel="", legend=None, logx=None, logy=None,
         marker_sz=None, mark_with_line=False, vlines=[], draw_axes=False,
         path=None, display=True, plot=None):
    _check_input(plot, title, xlabel, ylabel, logx, logy)
    logx = False if logx is None else True
    logy = False if logy is None else True

    if not _is_container(yss[0]):
        yss = [yss]
    if not _is_container(xss[0]):
        p = _plot(title, xss, yss, xlabel, ylabel, legend, logx, logy, 
                  marker_sz, mark_with_line, draw_axes, path, plot)
    else:
        if len(yss) != len(xss):
            raise ValueError('There must be the same number of points sets in both xss and yss')
        p = _plot2(title, xss, yss, xlabel, ylabel, legend, logx, logy,
                   marker_sz, mark_with_line, draw_axes, path, plot)
    _finialise(p, path, display, vlines)
    return p

def line_from_file(csvpath, title="", xlabel="", ylabel="", delimiter=" ", x_index=0, y_indices=1,
                   legend=None, logx=None, logy=None, marker_sz=None, mark_with_line=False,
                   vlines=[], draw_axes=False, path=None, display=True):
    xss,yss = _get_data_from_file(csvpath, delimiter, x_index, y_indices)
    line(xss, yss, title, xlabel, ylabel, legend, logx, logy, marker_sz,
         mark_with_line, vlines, draw_axes, path, display)

def line_from_csv(csvpath, title="", xlabel="", ylabel="", x_index=0, y_indices=1,
                  legend=None, logx=None, logy=None, marker_sz=None, mark_with_line=False,
                  draw_axes=False, path=None):
    line_from_file(csvpath, title, xlabel, ylabel, ",", x_index, y_indices, legend, logx, logy,
                   marker_sz, mark_with_line, draw_axes=draw_axes, path=path)

def scatter(xss, yss, title="", xlabel="", ylabel="", logx=None, logy=None,
            legend=None, marker_sz=None, draw_axes=False,
            path=None, display=True, plot=None):
    _check_input(plot, title, xlabel, ylabel, logx, logy)
    logx = False if logx is None else True
    logy = False if logy is None else True

    p = plot
    if p is None:
        p = StaticPlot(title, draw_axes=draw_axes)
        p.add_plot(xlabel, ylabel, logx, logy)
    ls = len(p.lines)
    if not _is_container(xss[0]):
        if _is_container(yss[0]):
            xss = [xss] * len(yss)
        else:
            xss = [xss]
    if not _is_container(yss[0]):
        yss = [yss]
    if len(yss) != len(xss):
        raise ValueError('There must be the same number of points sets in both xss and yss')
    for i in range(len(xss)):
        if legend is None:
            p.add_scat(ls+i, xss[i], yss[i], logx, logy, None, marker_sz)
        else:
            p.add_scat(ls+i, xss[i], yss[i], logx, logy, legend[i], marker_sz)
    _finialise(p, path, display)
    return p
