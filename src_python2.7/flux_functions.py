# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 10:50:14 2012

@author: dpiscia
"""
import math
import numpy as np

def conv_flux(T,alphas,qconv,time):
    
    qconv[time][1]=0
    qconv[time][7]=0

    qconv[time][0]= alphas[time][0]*(T[time][0]-T[time][9])
    qconv[time][2]= alphas[time][2]*(T[time][2]-T[time][9])
    qconv[time][3]= alphas[time][3]*(T[time][3]-T[time][9])
    qconv[time][5]= alphas[time][5]*(T[time][5]-T[time][8])
    qconv[time][4]= alphas[time][4]*(T[time][4]-T[time][8])
    qconv[time][6]= alphas[time][6]*(T[time][6]-T[time][8])


def convective_coeff(T,u,alphas,time):
    alphas[time][0] = alphas[time][2] = alphas[time][3] =   0.95 + 6.76*math.pow(u,0.49)   
   
    alphas[time][4] = 2.21*math.pow(math.fabs(T[time][4]-T[time][8]),0.33)
#    print "T4", T[time][4] , "t8 ", T[time][8]    
    alphas[time][6] = 1.86*math.pow(math.fabs(T[time][6]-T[time][8]),0.33)
    alphas[time][5] = 1.246*math.pow(math.fabs(T[time][5]-T[time][8]),0.33)
#    print "alphas", alphas[1]
    

def radiation_flux(T,qrad,Factor,j,g,e,tr,time):
    kbol = 5.67*math.pow(10,-8)

    j[time][0] = e[0]*kbol*math.pow(T[time][0],4) + (1-e[0]-tr[0])*(g[time][0]) + tr[0]*g[time][4] 
    j[time][1] = e[1]*kbol*math.pow(T[time][1],4) + (1-e[1])*(g[time][1])
    j[time][2] = e[2]*kbol*math.pow(T[time][2],4) + (1-e[2])*(g[time][2]) 
    j[time][3] = e[3]*kbol*math.pow(T[time][3],4) + (1-e[3]- tr[3])*(g[time][3]) + tr[3]*g[time][5] 
    j[time][4] = e[4]*kbol*math.pow(T[time][4],4) + (1-e[4]-tr[4])*(g[time][4])  + tr[4]*g[time][0] 
    j[time][5] = e[5]*kbol*math.pow(T[time][5],4) + (1-e[5]-tr[5])*(g[time][5])  + tr[5]*g[time][3] 
    j[time][6] = e[6]*kbol*math.pow(T[time][6],4) + (1-e[6])*(g[time][6])
    j[time][7] = e[7]*kbol*math.pow(T[time][7],4) + (1-e[7])*(g[time][7])

    g[time][0] = Factor[0][1]*j[time][1] + Factor[0][2]*j[time][2] + Factor[0][0]*j[time][0] + Factor[0][3]*j[time][3] + Factor[0][7]*j[time][7]
    g[time][1] = Factor[1][1]*j[time][1] + Factor[1][2]*j[time][2] + Factor[1][0]*j[time][0] + Factor[1][3]*j[time][3] + Factor[1][7]*j[time][7]
    g[time][2] = Factor[2][1]*j[time][1] + Factor[2][2]*j[time][2] + Factor[2][0]*j[time][0] + Factor[2][3]*j[time][3] + Factor[2][7]*j[time][7]
    g[time][3] = Factor[3][1]*j[time][1] + Factor[3][2]*j[time][2] + Factor[3][0]*j[time][0] + Factor[3][3]*j[time][3] + Factor[3][7]*j[time][7]
    g[time][7] = Factor[7][1]*j[time][1] + Factor[7][2]*j[time][2] + Factor[7][0]*j[time][0] + Factor[7][3]*j[time][3] + Factor[7][7]*j[time][7]
          
    g[time][4] = Factor[4][4]*j[time][4] + Factor[4][5]*j[time][5] +  Factor[4][6]*j[time][6] 
    g[time][5] = Factor[5][4]*j[time][4] + Factor[5][5]*j[time][5] +  Factor[5][6]*j[time][6] 
    g[time][6] = Factor[6][4]*j[time][4] + Factor[6][5]*j[time][5] +  Factor[6][6]*j[time][6] 
    
    qrad[time][0]=j[time][0]-g[time][0]
    qrad[time][1]=j[time][1]-g[time][1]
    qrad[time][2]=j[time][2]-g[time][2]
    qrad[time][3]=j[time][3]-g[time][3]
    qrad[time][7]=j[time][7]-g[time][7]
    
    qrad[time][4]=j[time][4]-g[time][4]
    qrad[time][5]=j[time][5]-g[time][5]
    qrad[time][6]=j[time][6]-g[time][6]
    print "rad", qrad[time]
    print "j emitted", j[time]
    print "g recibed", g[time]
    #raw_input("radiaiotn")
def qrad_flux(qrad,A,time):
    
    return np.sum(qrad[time][[4,5,6]]*A[[4,5,6]])
    
def qconv_flux(qconv,A,alphas,time):
    
    print "qconv 4", qconv[time][4] ,"Area ", A[4] , "alpha ", alphas[time][4]
    print "qconv 5", qconv[time][5] ,"Area ", A[5] , "alpha ", alphas[time][5]
    print "qconv 6", qconv[time][6] ,"Area ", A[6] , "alpha ", alphas[time][6]
    print "sum",  qconv[time][4]*A[4]+qconv[time][5]*A[5]+qconv[time][6]*A[6]
    return np.sum(qconv[time][[4,5,6]]*A[[4,5,6]]) 
def thermal_gain_air(cp,rho,Vol,T,deltaT,time):
    return cp*rho*Vol*(T[time][8]-T[time-1][8])/deltaT

#def convective_coef_forced(double X,double v):
#    Pr =0.7
#    rho = 1.2
#    viscosity = 1.8*pow(10,-5)
#    Re =(X*rho*v)/viscosity
#    Nu = 0.037*pow(Re,0.8)*pow(Pr,0.3333)
#    k=0.024
#    coef = k*Nu/X
#    return coef
