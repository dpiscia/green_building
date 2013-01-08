# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 12:06:43 2012

@author: dpiscia
"""

import numpy as np
import flux_functions as ff
import math
import ventilation as ve

def set_initial_conditions(T_ins,T_cover,RH_in,T,RH,T_outside,g,sky_temp):
    # 0 inside,1 cover, 2 sidewall, 3 soil
    T[0][8] = T_ins
    T[0][0] = T[0][4] = T_cover
    T[0][9] = T_outside
    RH[0][8] = RH_in
    g[1]=350
    T[0][2] = 283
    T[0][[3,5,6]]= 283
    T[0][1] = T[1][7] =  sky_temp
    
def BC_cond(element,fluid_element,qcond,alphas,e,T,g,time):
    ''' Boundary condition, cond = conv + rad qrad term is split into j and g contribution'''
    kbol = 5.67*math.pow(10,-8)

    T[time][element] = ((qcond + alphas[time][element] *T[time][fluid_element] + e[element]*g[time][element])
    /(e[element]*kbol * math.pow(T[time][element],3)+alphas[time][element]))

def BC_cond_2(element,fluid_element,qcond,qrad,alphas,T,time):
    ''' Boundary condition, cond = conv + rad'''
    
    T[time][element] = ((qcond + alphas[time][element] *T[time][fluid_element] - qrad[time][element])
    /(alphas[time][element]))
    return T[time][element]
    
def BC_cond_3(qcond,qrad,alphas,T_fluid):
    from sympy import Eq, Symbol, solve
    Ti = Symbol('Ti')
    eqn = Eq(qcond-qrad-alphas*(Ti-T_fluid),Ti)
    Ti = solve(eqn)
    return Ti
    
    
def BC_conv_conv(el_inner,el_outer,fluid_el_outer,fluid_el_inner,alphas,e,tr,T,g,j,time):
    ''' Boundary condition, conv + rad = conv + rad, qrad term is split into j and g contribution'''

    kbol = 5.67*math.pow(10,-8)
    T[time][el_inner] = ((e[el_outer]*g[time][el_outer]+alphas[time][el_outer]*T[time][fluid_el_outer]+
    e[el_inner]*g[time][el_inner] + alphas[time][el_inner]*T[time][fluid_el_inner] 
#    - tr[el_outer]*j[time][el_inner]+tr[el_outer]*j[time][el_outer] -
#    - tr[el_inner]*j[time][el_outer] + tr[el_inner]*j[time][el_inner]
    ) /
    (e[el_outer]*kbol*math.pow(T[time][el_inner],3) + alphas[time][el_inner] + alphas[time][el_outer]
     +e[el_inner]*kbol*math.pow(T[time][el_inner],3)))


def BC_conv_conv_2(el_inner,el_outer,fluid_el_outer,fluid_el_inner,alphas,qrad,T,time):
    ''' Boundary condition, conv + rad = conv + rad'''

    T[time][el_inner] = ((qrad[time][el_inner]+qrad[time][el_outer]
                        -alphas[time][el_inner]*T[time][fluid_el_inner]-alphas[time][el_outer]*T[time][fluid_el_outer])/
                         (-alphas[time][el_inner]-alphas[time][el_outer]))


    

def fluid_T_solver(T,alphas,A,Vol,rho,cp,time,deltaT):
   ''' compute air temperature based on energy loads and sinks, qconv term is split '''
   T[time][8]= (((alphas[time][4]*T[time][4]*A[4] + alphas[time][5]*T[time][5]*A[5]+alphas[time][6]*T[time][6]*A[6])   
   + (rho *cp * Vol * T[time-1][8]/ deltaT) ) / 
   ((alphas[time][4]*A[4] + alphas[time][5]*A[5]+alphas[time][6]*A[6])+(rho *cp * Vol / deltaT) ) )

def fluid_T_solver2(T,qconv,A,Vol,rho,cp,time,deltaT):
    ''' compute air temperature based on energy loads and sinks'''
    T[time][8]= (((qconv[time][4]*A[4] + qconv[time][5]*A[5]+qconv[time][6]*A[6])   
    + (rho *cp * Vol * T[time-1][8]/ deltaT) ) / 
    ((rho *cp * Vol / deltaT) ) ) 

def fluid_T_solver3(T,qconv,A,Vol,rho,cp,ventilation,time,deltaT):
    ''' compute air temperature based on energy loads and sinks'''
    T[time][8]= (((qconv[time][4]*A[4] + qconv[time][5]*A[5]+qconv[time][6]*A[6])   
    + (rho *cp * Vol * T[time-1][8]/ deltaT) + rho*cp*ventilation*T[time][9] ) / 
    ((rho *cp * Vol / deltaT) + rho*cp*ventilation) ) 

def fluid_hum_solver(T,RH,qconv,A,Vol,rho,cp,ventilation,time,deltaT):
    ''' compute air humdity based on humidity loads and sinks'''
    T[time][8]= (((qconv[time][4]*A[4] + qconv[time][5]*A[5]+qconv[time][6]*A[6])   
    + (rho *cp * Vol * T[time-1][8]/ deltaT) + rho*cp*ventilation*T[time][9] ) / 
    ((rho *cp * Vol / deltaT) + rho*cp*ventilation) ) 
              
def relax(T,T0,relax_f,time):
    ''' under relax temperature'''
    
    T[time][0] = T[time][4]
    T[time][3] = T[time][5]
    T[time][[0,4,3,5,6,8]] = T0[0][[0,4,3,5,6,8]] + relax_f*(T[time][[0,4,3,5,6,8]]-T0[0][[0,4,3,5,6,8]])
    

def check_convergence(T,T0,criteria,time):
    err_sum = np.sum(np.abs(T0[0][[4,5,6,8]]-T[time][[4,5,6,8]]))
    T0[0] = T[time]
    converged = False
    if (err_sum < criteria):
        converged = True
    return err_sum,converged

def increment_row(T,j,g,alphas,qrad,qconv):
    return  (np.vstack((T,T[-1])) , np.vstack((j,j[-1])), np.vstack((g,g[-1])),
            np.vstack((alphas,alphas[-1])), np.vstack((qrad,qrad[-1])), np.vstack((qconv,qconv[-1])))

    
def solver_T(T,qrad,qconv,alphas,j,g,e,tr,u,view_factor,qcond,timestep,nr_timestep,A,rho,cp,Vol,degree_win,deltaT):
    ''' solver'''
    time_range = range(1,10)
    max_iter = 200
    T0 = np.zeros( shape=(1,10))
    T0[0] = 280
    vent_rate = ve.ventilation(u,degree_win)
    for time in time_range:
        print "time is", time
        T[time] = T[time-1]
        
        for i in range(1,max_iter):
            ff.radiation_flux(T,qrad,view_factor,j,g,e,tr,time)        
            ff.convective_coeff(T,u,alphas,time)
            ff.conv_flux(T,alphas,qconv,time)
            BC_cond_2(6,8,qcond,qrad,alphas,T,time)
            BC_conv_conv_2(4,0,9,8,alphas,qrad,T,time)
            BC_conv_conv_2(5,3,9,8,alphas,qrad,T,time)
            fluid_T_solver3(T,qconv,A,Vol,rho,cp,vent_rate,time,deltaT)
            
            relax(T,T0,0.25,time)
            sum_error,converged = check_convergence(T,T0,math.pow(10,-15),time)
            #print sum_error
            if converged:
                if (time <> max(time_range)):
                    T, j, g, alphas, qrad, qconv = increment_row(T, j, g, alphas, qrad, qconv)
                break
                
    return T, j, g, alphas, qrad, qconv

def solver_T_hum(T,RH,qrad,qconv,alphas,j,g,e,tr,u,view_factor,qcond,timestep,nr_timestep,A,rho,cp,Vol,degree_win,deltaT):
    ''' solver'''
    time_range = range(1,10)
    max_iter = 200
    T0 = np.zeros( shape=(1,10))
    T0[0] = 280
    vent_rate = ve.ventilation(u,degree_win)
    for time in time_range:
        print "time is", time
        T[time] = T[time-1]
        
        for i in range(1,max_iter):
            ff.radiation_flux(T,qrad,view_factor,j,g,e,tr,time)        
            ff.convective_coeff(T,u,alphas,time)
            ff.conv_flux(T,alphas,qconv,time)
            BC_cond_2(6,8,qcond,qrad,alphas,T,time)
            BC_conv_conv_2(4,0,9,8,alphas,qrad,T,time)
            BC_conv_conv_2(5,3,9,8,alphas,qrad,T,time)
            fluid_T_solver3(T,qconv,A,Vol,rho,cp,vent_rate,time,deltaT)
            
            relax(T,T0,0.25,time)
            sum_error,converged = check_convergence(T,T0,math.pow(10,-15),time)
            #print sum_error
            if converged:
                if (time <> max(time_range)):
                    T, j, g, alphas, qrad, qconv = increment_row(T, j, g, alphas, qrad, qconv)
                break
                
    return T, j, g, alphas, qrad, qconv
