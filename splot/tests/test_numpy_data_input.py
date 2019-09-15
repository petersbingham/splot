import os
import sys
basedir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,basedir+'/../..')

import splot

x1 = [1,2]
x2 = [3,4]

y1 = [5,6]
y2 = [6,7]

splot.line(x1, y1)
splot.line(x1, [y1,y2])
splot.line([x1,x2], [y1,y2])
print "**** TESTING ERROR CASES ****"
try:
  splot.line([x1,x2], y1)
  print "FAIL"
except:
  print "PASS"
  
splot.scatter(x1, y1)
splot.scatter(x1, [y1,y2])
splot.scatter([x1,x2], [y1,y2])
print "**** TESTING ERROR CASES ****"
try:
  splot.scatter([x1,x2], y1)
  print "FAIL"
except:
  print "PASS"
