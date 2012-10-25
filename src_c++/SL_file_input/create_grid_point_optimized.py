import os
import csv
import glob
import pylab
import sys
from math import *
import csv
from matplotlib.mlab import griddata
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy
from matplotlib.ticker import LinearLocator, FixedLocator, FormatStrFormatter
from green_function import *
T_sky = []
SHF = []
tra = []
temp_inside = []


T_skyi = numpy.linspace(256,276, num = 25)
SHFi = numpy.linspace(25,100 , num = 25)




#RHa = numpy.array(RH)
T_skya, SHFa = numpy.meshgrid(T_skyi,SHFi)
#RHaa = griddata(traa,emia,RHa, trai,emii)
vfunc = numpy.vectorize(green_function_2)
optfunc = numpy.vectorize(green_function_3_opt)
RH, temp_inside = vfunc(T_skya,SHFa)
RH_opt, temp_ins_opt = optfunc(T_skya,SHFa)
temp_delta = temp_ins_opt - temp_inside
fig = plt.figure()
ax = fig.gca(projection='3d')
surf =ax.plot_surface(T_skya,SHFa,temp_delta, rstride=2, cstride=1, cmap=cm.jet,linewidth=0, antialiased=True)
ax.set_zlim3d(numpy.min(temp_delta),numpy.max(temp_delta))
ax.set_xlabel('Sky temperature K')
ax.set_ylabel('SHF W m-2')
ax.set_zlabel('Inside temperature K')
#ax.set_xticks([0.1,.2,.3,.4,.5])
#ax.set_yticks([0.1,.2,.3,.4])
fig.colorbar(surf, orientation = 'horizontal')


plt.show()
