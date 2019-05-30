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
        self.legends = []
        self.axis_config = []
        self.fig.subplots_adjust(left=LEFT, bottom=BOTTOM, right=RIGHT,
                                 top=TOP, wspace=WSPACE, hspace=HSPACE)

    def add_plot(self, xlabel, ylabel, logx=False, logy=False):
        plot_num = len(self.axis_config)+1
        self.fig.add_subplot(self.rows,self.cols,plot_num)
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        #plt.gca().set_color_cycle(['red', 'blue', 'red', 'purple'])
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
            self.legends.append(legend)

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
        plt.scatter(xs,ys,color=['black', 'red', 'blue', 'purple'][plot_num],s=20,edgecolor='none')

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
            plt.xticks(range(len(xs)), xs)
        return l

    def reveal(self, display, vlines=[]):  
        if self.draw_axes:
            plt.axhline(0, color='black')
            plt.axvline(0, color='black')
        if len(self.legends) > 0:
            plt.legend(self.lines, self.legends, prop={'size':9})
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

xlim = None
ylim = None
def set_extents(xlim_, ylim_):
    global xlim
    global ylim
    xlim = xlim_
    ylim = ylim_

def set_colour_cycle(cycle):
    matplotlib.rcParams['axes.color_cycle'] = cycle

def turn_off_colour_cycle():
    matplotlib.rcParams['axes.color_cycle'] = ['black']

line_width = None
def set_line_width(width):
    global line_width
    line_width = width

vline_width = None
vline_colour = None
def set_vline_config(width, colour):
    global vline_width
    global vline_colour
    vline_width = width
    vline_colour = colour

def _get_data_from_csv(csvpath):
    xs = []
    yss = None
    with open(csvpath, 'rb') as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',')
        for row in csvReader:
            xs.append(float(row[0]))
            if yss is None:
                yss = [[] for i in range(0,len(row[1:]))]
            for i in range(0,len(row[1:])):
                yss[i].append(float(row[1+i]))
    return xs, yss

def _initialise(display):
    if not display:
        plt.switch_backend('Agg')

def _finialise(p, path, display, vlines=[]):
    p.reveal(display, vlines)
    if path is not None:
        p.save(path)

def _plot(title, xs, yss, xlabel, ylabel, legends, logx, logy,
          marker_sz, mark_with_line, draw_axes, path, display):
    p = StaticPlot(title,draw_axes=draw_axes)
    p.add_plot(xlabel, ylabel, logx, logy)
    for i in range(len(yss)):
        if legends is not None:
            p.add_line(1,xs,yss[i],legends[i],marker_sz,mark_with_line)
        else:
            p.add_line(1,xs,yss[i],None,marker_sz,mark_with_line)
    return p

def _plot2(title, xss, yss, xlabel, ylabel, legends, logx,
           logy, marker_sz, mark_with_line, draw_axes, path, display):
    p = StaticPlot(title,draw_axes=draw_axes)
    p.add_plot(xlabel, ylabel, logx, logy)
    for i in range(len(xss)):
        if type(marker_sz) is list:
          ms = marker_sz[i]
        else:
          ms = marker_sz

        if legends is not None:
            p.add_line(1,xss[i],yss[i],legends[i],ms,False)
        else:
            p.add_line(1,xss[i],yss[i],None,ms,False)
    return p

def line_from_csv(csvpath, title="", xlabel="", ylabel="", legends=None, logx=False, logy=False,
                  marker_sz=None, path=None, mark_with_line=False, draw_axes=False):
    xs,yss = _get_data_from_csv(csvpath)
    plot_line(title, xs, yss, xlabel, ylabel, legends, logx,
              logy, marker_sz, mark_with_line, path, draw_axes)

def line(xss, yss, title="", xlabel="", ylabel="", legends=None, logx=False, logy=False,
         marker_sz=None, mark_with_line=False, vlines=[], draw_axes=False, path=None, display=True):
    _initialise(display)
    if not isinstance(yss[0], list):
        yss = [yss]
    if not isinstance(xss[0], list):
        p = _plot(title, xss, yss, xlabel, ylabel, legends, logx, logy, 
                  marker_sz, mark_with_line, draw_axes, path, display)
    else:
        p = _plot2(title, xss, yss, xlabel, ylabel, legends, logx, 
                   logy, marker_sz, mark_with_line, draw_axes, path, display)
    _finialise(p, path, display, vlines)

def scatter(xss, yss, title="", xlabel="", ylabel="", logx=False, logy=False,
            legend=None, marker_sz=None, draw_axes=False, path=None, display=True):
    _initialise(display)
    p = StaticPlot(title, draw_axes=draw_axes)
    p.add_plot(xlabel, ylabel, logx, logy)
    if not isinstance(xss[0], list):
        if isinstance(yss[0], list):
            xss = [xss] * len(yss)
        else:
            xss = [xss]
    if not isinstance(yss[0], list):
        yss = [yss]
    for i in range(len(xss)):
      p.add_scat(i, xss[i], yss[i], logx, logy, legend, marker_sz)
    _finialise(p, path, display)

