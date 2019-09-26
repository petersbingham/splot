import os
import sys
basedir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,basedir+'/../..')

import numpy as np
import splot

x = np.array([1,2,3,4])

y1 = np.array([5,6,7,8])
y2 = np.array([6,7])

splot.line(x, [y1,y2])
