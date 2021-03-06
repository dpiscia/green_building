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
RH = []
emi = []
tra = []
temp_inside = []
spamReader = csv.reader(open('../3D_opt.csv', 'rb'), delimiter=',', quotechar='|')
for row in spamReader:
    emi.append(float(row[1]))
    tra.append(float(row[2]))
    RH.append(float(row[0]))
traa = numpy.array(tra)
emia = numpy.array(emi)

#out_tempi = numpy.linspace(276,290, num = 25)
out_hum_ratioi = numpy.linspace(0.001,0.004 , num = 15)
degreei = numpy.linspace(0.0,40 , num = 15)

#out_hum_ratio = 0.004

out_temp = 276
#RHa = numpy.array(RH)
Traa, Emia = numpy.meshgrid(degreei,out_hum_ratioi)
#RHaa = griddata(traa,emia,RHa, trai,emii)
vfunc = numpy.vectorize(green_function_vent)
RH, temp_inside = vfunc(Traa,Emia,out_temp)

fig = plt.figure()
ax = fig.gca(projection='3d')
surf =ax.plot_surface(Traa,Emia,RH, rstride=2, cstride=1, cmap=cm.jet,linewidth=0, antialiased=True)
ax.set_zlim3d(numpy.min(RH), 1)
ax.set_xlabel('Degree')
ax.set_ylabel('Outside hum_ratio')
ax.set_zlabel('RH % / 100')
#ax.set_xticks([0.1,.2,.3,.4,.5])
#ax.set_yticks([0.1,.2,.3,.4])
fig.colorbar(surf, orientation = 'horizontal')

fig1 = plt.figure()
ax1 = fig1.gca(projection='3d')
#ax1 = fig.add_subplot(1, 2, 2, projection='3d')
surf =ax1.plot_surface(Traa,Emia,temp_inside, rstride=2, cstride=1, cmap=cm.jet,linewidth=0, antialiased=True)
ax1.set_zlim3d(numpy.min(temp_inside), numpy.max(temp_inside))
ax1.set_xlabel('Degree')
ax1.set_ylabel('humidity ratio Kg Kg-1')
ax1.set_zlabel('Temperature K')
#ax1.set_xticks([0.1,.2,.3,.4,.5])
#ax1.set_yticks([0.1,.2,.3,.4])
fig1.colorbar(surf, orientation = 'horizontal')

plt.show()


#In [62]: var1 = []

#In [63]: var2 = []

#In [64]: for i in numpy.nditer(RH[9:10]):
 #   var1.append(i)
 #  ....: 

#In [65]: for i in nu
