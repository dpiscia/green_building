# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 10:50:38 2012

@author: dpiscia
"""

import numpy as np


x = 1
y = 10

T =  np.zeros(shape = (x,y))
T0 = np.zeros(shape = T.shape) 
T3 = np.zeros(shape = (x,y,2))
T3[:,:,0] = 21

def solver_unsteady(T,flux0,flux1,time):

    rho = 1.225
    density = 1000
    alpha = 5
    T_out = 5
    deltaT = 60
    k = 1
    dy = 1
    T[0,0,time] = (flux0 +  (k/dy)*T[0,0+1,time] + alpha*T_out + rho*density*dy*T[0,0,time-1]/deltaT   )/(1 + alpha + rho*density*dy/deltaT) 
#    T[0,1] =   (T[0,0] + T[0,2])/2
#    T[0,2] = (T[0,1] + T[0,3])/2
    T[0,1:-1,time] = ( (k/dy)*(T[0,2:,time]+T[0,:-2,time]) + rho*density*dy*T[0,1:-1,time-1]/deltaT)/ (2 + rho*density*dy/deltaT)
    T[0,-1,time] = 20
    return T[0]


def solver(T,flux0,flux1):

    rho = 1.225
    density = 1000
    
    k = 1
    dy = 1
    T[0,0] = (flux0 +  (k/dy)*T[0,0+1] + 5*10   )/(1+5) 
#    T[0,1] =   (T[0,0] + T[0,2])/2
#    T[0,2] = (T[0,1] + T[0,3])/2
    T[0,1:-1] = (T[0,2:]+T[0,:-2])/2
    T[0,-1] = 20
    return T[0]
        
    
    
    #raw_input("ff")
    
import math

for i in range(0,800):
    T[0] = solver(T,25,0)

    
    if (math.fabs(np.sum(T0-T)) < 0.0000000000000000001):
        print "converged, iteration i", i
        break
    T0[0] = T[0]


