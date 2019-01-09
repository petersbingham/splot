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
  
    def __init__(self, title, rows=1, cols=1, drawAxes=False):
        self.fig = plt.figure(figsize=(FIGSZ_W,FIGSZ_H), dpi=self.DPI)
        self.fig.suptitle(title)
        self.rows = rows
        self.cols = cols
        self.drawAxes = drawAxes
        self.lines = []
        self.legends = []
        self.axisConfig = []
        self.fig.subplots_adjust(left=LEFT, bottom=BOTTOM, right=RIGHT, top=TOP, wspace=WSPACE, hspace=HSPACE)
  
    def add_plot(self, xlabel, ylabel, logx=False, logy=False):
        plotNum = len(self.axisConfig)+1
        self.fig.add_subplot(self.rows,self.cols,plotNum)
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        #plt.gca().set_color_cycle(['red', 'blue', 'red', 'purple'])
        self.axisConfig.append([logx,logy])
    
    def add_line(self, plotNum, xs, ys, legend=None, markerSz=None, markWithLine=False):
        self._add_data(plotNum, xs, ys, legend, markerSz, False, markWithLine)
    
    def add_scat(self, plotNum, xs, ys, logx=False, logy=False, legend=None, markerSz=None):
        if logx:
          plt.gca().set_xscale('log')
        if logy:
          plt.gca().set_yscale('log')
        self._add_data(plotNum, xs, ys, legend, markerSz, True, False)
  
    def _add_data(self, plotNum, xs, ys, legend, markerSz, scatter, markWithLine):
        xs, ys = self._convert_values(xs, ys)
        if scatter:
            l = self._add_scat_type(plotNum, xs, ys, markerSz) 
        else:
            l = self._add_line_type(plotNum, xs, ys, markerSz, markWithLine)  
        self.lines.append(l)
        if legend is not None:
            self.legends.append(legend)
  
    def _convert_values(self, xs, ys):
        if type(xs) is list:
            xs = np.ndarray((len(xs),), buffer=np.array(xs)) #Contents of array need to be floats or can get: "TypeError: buffer is too small for requested array"
        if type(ys) is list:
            ys = np.ndarray((len(ys),), buffer=np.array(ys))
        return (xs,ys)
  
    def _add_scat_type(self, plotNum, xs, ys, markerSz):
        plt.scatter(xs,ys,color=['black', 'red', 'blue', 'purple'][plotNum],s=20,edgecolor='none')
  
    def _add_line_type(self, plotNum, xs, ys, markerSz, markWithLine):
        kwargs = {'basex':10}
        if markerSz:
            kwargs = {'basex':10, 'linestyle':'None' if not markWithLine else 'solid', 'marker':'o', 'markerfacecolor':'black', 'markersize':markerSz}
        if self.axisConfig[plotNum-1][0] and self.axisConfig[plotNum-1][1]:
            l, = plt.loglog(xs, ys, **kwargs)
        elif self.axisConfig[plotNum-1][0]:
            l, = plt.semilogx(xs, ys, **kwargs)
        elif self.axisConfig[plotNum-1][1]:
            kwargs.pop('basex')
            l, = plt.semilogy(xs, ys, **kwargs)
        else:
            kwargs.pop('basex')
            #print str(len(xs)) + " " + str(len(ys))
            l, = plt.plot(xs, ys, **kwargs)
        #for a,b in zip(xs, ys): 
        #    plt.text(a+0.002, b+0.02, '{0:.5f}'.format(b))
        return l
  
    def reveal(self):  
        if self.drawAxes:
            plt.axhline(0, color='black')
            plt.axvline(0, color='black')
        if len(self.legends) > 0:
            plt.legend(self.lines, self.legends, prop={'size':9})
        axes = plt.gca()
        if xlim is not None:
            axes.set_xlim(xlim)
        if ylim is not None:
            axes.set_ylim(ylim)
        plt.draw()
        plt.show()
    
    def save(self, path):
        self.fig.savefig(path, dpi=self.DPI)
  
def set_sub_plot_parameters(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None):
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
    
def turn_off_colour_cycle():
    matplotlib.rcParams['axes.color_cycle'] = ['black']

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
            
def plot_line_from_csv(csvpath,title="",xlabel="",ylabel="",legends=None,logx=False,logy=False,markerSz=None,path=None,markWithLine=False,drawAxes=False):
    xs,yss = _get_data_from_csv(csvpath)
    plot_line(title,xs,yss,xlabel,ylabel,legends,logx,logy,markerSz,markWithLine,path,drawAxes)
    
def plot_lines(xs,yss,title="",xlabel="",ylabel="",legends=None,logx=False,logy=False,markerSz=None,path=None,markWithLine=False,drawAxes=False):
    _plot(title,xs,yss,xlabel,ylabel,legends,logx,logy,markerSz,markWithLine,path,drawAxes)
  
def plot_lines_unsynced(xss,yss,title="",xlabel="",ylabel="",legends=None,logx=False,logy=False,markerSz=None,path=None,markWithLine=False,drawAxes=False):
    _plot2(title,xss,yss,xlabel,ylabel,legends,logx,logy,markerSz,markWithLine,path,drawAxes)

def _plot(title,xs,yss,xlabel,ylabel,legends,logx,logy,markerSz,markWithLine,path,drawAxes):
    p = StaticPlot(title,drawAxes=drawAxes)
    p.add_plot(xlabel, ylabel, logx, logy)
    for i in range(len(yss)):
        if legends is not None:
            p.add_line(1,xs,yss[i],legends[i],markerSz,markWithLine)
        else:
            p.add_line(1,xs,yss[i],None,markerSz,markWithLine)
    p.reveal()
    if path is not None:
        p.save(path)

def _plot2(title,xss,yss,xlabel,ylabel,legends,logx,logy,markerSz,markWithLine,path,drawAxes):
    p = StaticPlot(title,drawAxes=drawAxes)
    p.add_plot(xlabel, ylabel, logx, logy)
    for i in range(len(xss)):
        if type(markerSz) is list:
          ms = markerSz[i]
        else:
          ms = markerSz
    
        if legends is not None:
            p.add_line(1,xss[i],yss[i],legends[i],ms,False)
        else:
            p.add_line(1,xss[i],yss[i],None,ms,False)
    p.reveal()
    if path is not None:
        p.save(path)
  
def plot_scat(xs,ys,title="",xlabel="",ylabel="",logx=False,logy=False,legend=None,markerSz=None,path=None,drawAxes=False):
    p = StaticPlot(title,drawAxes=drawAxes)
    p.add_plot(xlabel, ylabel, logx, logy)
    p.add_scat(1,xs,ys, logx, logy,legend,markerSz)
    p.reveal()
    if path is not None:
        p.save(path) 
  
def plot_scats(xss,yss,title="",xlabel="",ylabel="",logx=False,logy=False,legend=None,markerSz=None,path=None,drawAxes=False):
    p = StaticPlot(title,drawAxes=drawAxes)
    p.add_plot(xlabel, ylabel, logx, logy)
    for i in range(len(xss)):
      p.add_scat(i,xss[i],yss[i],logx,logy,legend,markerSz)
    p.reveal()
    if path is not None:
        p.save(path)  
