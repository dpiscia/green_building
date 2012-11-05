# -*- coding: utf-8 -*-
"""
Created on Fri Nov 02 13:24:49 2012

@author: dpiscia
"""
import math

def central_difference(function,point,delta):
    ''' central difference scheme
    input: 
        -function
        -variable value
        -delta float
        '''
    delta= float(delta)    
    derivative = (function(point+delta/2)-function(point-delta/2))/(delta)
    return derivative

def gradient_saturation(T):
    ''' derivative of saturation pressure curve at point T'''
    return central_difference(saturated_pressure,T,0.1)

def net_solar_ration(Is,Rs,K,LAI):
    ''' return the net solar radiation as function of these inputs:
        -
        -
        -
        '''
    Rn = 0
    Rn = (Is-Rs)*(1-math.exp(-K*LAI))
        
    return Rn
    
def saturated_pressure(T):
    ''' return the water vapour saturation pressure [Pa]
    input:
        T fluid temperature (K)'''
    if (273.15 < T < (200 + 273.15)):    
        C8 = -5.8002206*pow(10,3);
        C9 = 1.3914993;
        C10 = -4.8640239*pow(10,-2);
        C11 = 4.1764768*pow(10,-5);
        C12 = -1.4452093*pow(10,-8);
        C13 = 6.5459673;
        pws = C8/T + C9 + C10*T + C11*pow(T,2)+C12*pow(T,3) +C13*math.log(T)
        pws = math.exp(pws)
    
    else:
        print "Error, formula is valid for temperature between 0 and 200 oC"
        pws = 0
    return pws



def transpiration_P_M():
    ''' apply the transpiration model of Pennman-Monteith (put reference
    to input data
    input data are:
        Rn net solar radiation corresponding to function net_solar_radiatio(..)
        delta gradient of the water saturation vapour pressure curve (kPa K−1) corresponding to gradient_saturation(T) 
        rho density of air (kg m−3)
        cp  specific heat of air (J kg−1 K−1)
        ra  canopy external, or aerodynamic resistance (s m−1)
        ea_sat  saturated air vapour pressure (kPa)
        ea air vapour pressure (kPa)
        lambda     latent heat of vaporisation (J kg−1)
        rc internal resistance of the leaf canopy to the transfer of water vapour (s m−1)
        -
        '''
    transpiration = 0
    return transpiration
    
def transpiration_from_balance():
    ''' based on weight lost, the function gives the approxmiate transpiration
    rate of the plant.
    inputs are:
        -
        -
        '''
    transpiration = 1
    return transpiration