# -*- coding: utf-8 -*-
"""
Created on Fri Nov 02 13:24:49 2012

@author: dpiscia
"""
import math
import numpy as np

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

def convective_coeff(kc,l,Gr,Re,Pr,regime_type):
    ''' return leaf convective coefficient as function of:
        thermal conductivity
        charactheristic lenght
        Grashoff number
        Reynols
        Prandtl
        regime type:1 -free convection McAdmams(1954)
                    2 -forced convection Grober and Erk (1961)
                    3 -mixed convection Stanghellini(1987)
    '''
    __h__ = 0
    if (regime_type ==1):
        __h__ = 0.4*(kc/l)*pow(Gr*Pr,0.25)
    elif (regime_type ==2):
        __h__ = 0.66*(kc/l)*pow(Re,0.5)*pow(Pr,0.33333)
    elif (regime_type ==3):
        __h__ = 0.37*(kc/l)*pow((Gr+6.92*pow(Re,2)),0.25)     
    return __h__
    
def density_regression(T):
    ''' density function of T (K), is the result of the formula:
    10^3/(2.8329*T) (kg/m^3)        
    '''
    rho = 0
    rho = pow(10,3)/(2.8329*T)
    return rho

def DPV(T,RH):
    ''' return the vapour pressure deficit
    DPV = vap_pressure_Sat - vap_pressure
    '''
    if ((0.0 < RH) & (RH > 1.0)).all():
        print "error RH has to be between 0 and 1"
        
    
    __DPV__ = 0
    __DPV__=saturated_pressure(T) - saturated_pressure(T)*RH
    return __DPV__
def external_resistance(rho,cp,LAI,h):
    ''' return the external aerodynamic resistance as function of:
        - rho
        -specific heat capacity
        -LAI
        -convective coeff
    '''
    __ra__ = 0
    __ra__ = rho*cp/(2*LAI*h)
    print "__ra__", __ra__
    print "h" , h
    return __ra__
    
def find_irrigation_point(delta_peso,tempo):
    ''' find irrigation point and drenage point by analazing delta weight'''
    irr_dre_points = np.array([],dtype='datetime64')
    lista = []
    lista_in = []
    for i in range(len(delta_peso)):
        if (delta_peso[i] >= 0 ):
            print "irrigation point", tempo[i], "delta is ", delta_peso[i]
            #print "irrigation duration is"
            irr_dre_points = np.append(irr_dre_points,tempo[i])
            lista.append(i)
        elif (delta_peso[i] <= -0.2):
            print "drenage point", tempo[i] , "delta is ", delta_peso[i]
            irr_dre_points = np.append(irr_dre_points,tempo[i])
            lista.append(i)
        else :
            lista_in.append(i)
    return irr_dre_points  , lista     , lista_in 

def gradient_saturation(T):
    ''' derivative of saturation pressure curve at point T (K)'''
    return central_difference(saturated_pressure,T,0.1)

def Gr(l,vi,T0,Ta):
    ''' return the Grashof number
    formula is g*Beta*l^3*t0-Ta()/u^2
    '''
    g = 9.8
    Beta = 1.0/T0
    __Gr__ = 0
    __Gr__ = g*Beta*pow(l,3)*abs(T0-Ta)/pow(vi,2)
  
    return __Gr__


        

def heat_conductivity(T):
    ''' return heat conductivity of plant (W m^-1 K^-1)
    '''
    __k__ = 0
    __k__ = 7.8*pow(10,-5)*T+2.69*pow(10,-3)
    return __k__
    
def internal_resistance(T,DPV,LAI,I_sol):
    ''' internal resistance:
    based on ri0 of ficus benjamina formula
    rint = r(T)*r(DPV)*ri/LAI stanghellini(1987,pag33)
    '''
    __rint__ = 0
    #Iq = 1400 #(microE m^-2  s^-1)
    ri0 = 46 + 54500/(55+I_sol/0.463)
    r_T = (5*np.exp(-0.15*(T-270)))+(1.7/(314-T))+(0.85)
    r_DPV = 0.05*np.exp(1.1*DPV/1000)+1

    print "__rint__ with formulas", r_T*r_DPV*ri0/LAI
    print "__rint__ no formulas", ri0/LAI
    __rint__ = ri0/LAI
    return __rint__

def internal_resistance_2(Sg,Ta,LAI):
    ''' internal resistance based on work of Pollet(1999)
    cited by Boulard and Wang(2002)
    inputs:
        Greenhouse solar radiation (W m-2)
        Ta iar temperature (C)
    '''
    __rint__ = 0
    __rint__=200*(31+Sg)*(1+0.016*pow((Ta-273.15)-16.4,2))/(6.7+Sg)
    return __rint__/LAI

def internal_resistance_3(Is,LAI,DPV):
    ''' internal resistance according to Fucs'''
    __rint__ = 0
    g_max= 0.011
    P = 216
    f = 0.0
    r_DPV = 1
    #r_DPV = 0.05*np.exp(1.1*DPV/1000)+1
    print r_DPV
    raw_input("S")

    g = (1-f)*g_max/(1+(1-f)*P/(2.02*Is))
    __rint__ = (1/g)*r_DPV
    return __rint__/LAI

def internal_resistance_4(Is,LAI,DPV):
    ''' internal resistance according to Jolliet bailey'''
    __rint__ = 0

    
    #r_DPV = 0.05*np.exp(1.1*DPV/1000)+1
    
    raw_input("S")

    g = 0.41*(1-0.66*(200/(Is+200))-0.22*(DPV/1000))
    print g
    __rint__ = (1/g)*10
    print __rint__
    raw_input("S ins")    
    return __rint__
    
def internal_resistance_5(Is,LAI,gmin,gmax):
    ''' internal resistance according to Montero Bailey
    Is has to be converted into micromol m-2 -s / 2
    gmin is the mimimun stomatal conductance
    gmax is the maximun stomatal conductance'''
    __rint__ = 0
    Ilum = Is * 2
    __rint__ = 1/(gmin+(gmax-gmin)*(2.27*Ilum)/(Ilum+1888))
    return __rint__/LAI
    
    #r_DPV = 0.05*np.exp(1.1*DPV/1000)+1
    
    raw_input("S")

    g = 0.41*(1-0.66*(200/(Is+200))-0.22*(DPV/1000))
    print g
    __rint__ = (1/g)*10
    print __rint__
    raw_input("S ins")    
    return __rint__
    
def lambda_constant(T):
    ''' return psychometric constant as functionof T (K) 
    '''
    __lambda__ = 0
    __lambda__ = 0.646 + 0.00064*T
    return __lambda__

def lista_mod(max_value,lista_in):
    ''' return list with valid point'''
    lista_final = []
    for i in range(0,max_value):
        if not(i in lista_in):
            lista_final.append(i)
    
    return lista_final
   
def K_LAI(month):
    K_LAI = (0.0,0.0)
    if (month == 6):
        K_LAI = (0.64,2.96)
    else :
        K_LAI = (0.64,3.98)
    return K_LAI
    
def net_solar_radiation(Is,Rs,K,LAI):
    ''' return the net solar radiation as function of these inputs:
        -
        -
        -
        '''
    Rn = 0
    Rn = (Is-Rs)*(1-math.exp(-K*LAI))
        
    return Rn
    
def remove_no_solar_point(Is,value):
    __lista__ = []
    for i in range(len(Is)):
        if Is[i] <= value:
            __lista__.append(i)
    return __lista__
        
def Re(u,l,vi):
    ''' 
    return Reynolds number, 
    inpus:
    -velocity
    -charactheristc lenght
    -kinematic viscosity
    '''
     #m^2 s^-1 293 K
    __Re__ = 0
    __Re__ = u*l/vi
    return __Re__
def saturated_pressure(T):
    ''' return the water vapour saturation pressure [Pa]
    input:
        T fluid temperature (K)'''
    if ((273.15 < T) & (T < (200 + 273.15))).all():    
        C8 = -5.8002206*pow(10,3);
        C9 = 1.3914993;
        C10 = -4.8640239*pow(10,-2);
        C11 = 4.1764768*pow(10,-5);
        C12 = -1.4452093*pow(10,-8);
        C13 = 6.5459673;
        pws = C8/T + C9 + C10*T + C11*pow(T,2)+C12*pow(T,3) +C13*np.log(T)
        pws = np.exp(pws)
    
    else:
        print "Error, formula is valid for temperature between 0 and 200 oC", T
        pws = 0
    return pws

def specific_heat_capacity_air():
    ''' return the specific heat capacity (J / kg*K) costant value
    '''
    cp = 1005
    return cp

def transpiration_P_M(Is,Rs,K,LAI,T,RH):
    ''' apply the transpiration model of Pennman-Monteith (put reference
    to input data
    input data are:
        Rn net solar radiation corresponding to function net_solar_radiation(Is,Rs,K,LAI)
        delta gradient of the water saturation vapour pressure curve (kPa K−1) corresponding to gradient_saturation(T) 
        rho density of air (kg m−3) corresponding to density_regression(T)
        cp  specific heat of air (J kg−1 K−1) corresponding to constant specific_heat_capacity_air()
        ra  canopy external, or aerodynamic resistance (s m−1) corr. to external_resistance(rho,cp,LAI,h)
        ea_sat  saturated air vapour pressure (kPa) corr. to saturated_pressure(T)
        ea air vapour pressure (kPa) corr. to RH*saturated_pressure
        lambda     latent heat of vaporisation (J kg−1) corr. to lambda_constant(T)
        rc internal resistance of the leaf canopy to the transfer of water vapour (s m−1) corr. to internal_resistance(T,DPV,LAI)
        -
    '''
    u = 0.2
    l = 0.05
    T0 = T-2
    vi = 1.51*pow(10,-5)
    Rn = net_solar_radiation(Is,Rs,K,LAI)
    delta = gradient_saturation(T)
    rho = density_regression(T)
    cp = specific_heat_capacity_air()
    ra = external_resistance(rho,cp,LAI,convective_coeff(heat_conductivity(T),l,Gr(l,vi,T0,T),Re(u,l,vi),0,3))
    ea_sat = saturated_pressure(T)
    ea = saturated_pressure(T)*RH    
    lambda_value = 66.27 #lambda_constant(T)
    #rc = internal_resistance(T,DPV(T,RH),LAI,Is)
#    rc = internal_resistance_4(Is,LAI,DPV(T,RH))
#    rc2 = internal_resistance_3(Is,LAI,DPV(T,RH))
    rc = internal_resistance_5(Is,LAI,1/250.0,1/90.0)
    for i in rc:
         print i
    raw_input("rc int")
        
    
    raw_input("DD")
    #    print "radiation", Rn
#    print "delta", delta
#    print "rc internal", rc
#    print "ra external" , ra
#    print "convective_coeff(heat_conductivity(T),l,Gr(l,u,T0,T)", convective_coeff(heat_conductivity(T),l,Gr(l,vi,T0,T),Re(u,l,vi),0,3)
#    print "heat_conductivity(T)", heat_conductivity(T)
    print "Gr(l,u,T0,T)", Gr(l,vi,T0,T)
    print "Re(u,l,vi)", Re(u,l,vi)
    print "ri", rc
#    print "ea sat", ea_sat
#    print "ea", ea
#    print "lambda_value", lambda_value
    __transpiration__ = 0
    __transpiration__= (Rn*delta+(rho*cp/ra)*(ea_sat-ea))/(delta+lambda_value*(1+rc/ra))  
    return __transpiration__
    
def transpiration_from_balance(weight,time_diff,L):
    ''' based on weight lost, the function gives the approxmiate transpiration
    rate of the plant.
    inputs are:
        -weight (kg)
        -time_diff (s)
        -L evaporization enthalpy (J kg^-1)
        '''
        
    __transpiration__ = 0
    __transpiration__ = np.diff(weight)*L/time_diff
    return __transpiration__
def transpiration_from_balance_irr(weight,time_diff,L,irrigation_list):
    ''' based on weight lost, the function gives the approxmiate transpiration
    rate of the plant.
    inputs are:
        -weight (kg)
        -time_diff (s)
        -L evaporization enthalpy (J kg^-1)
        '''
        
    lista = []
    tran = []
    #__transpiration__ = np.diff(weight)*L/time_diff
    for i in range(len(weight)-1):
        if ( (i in irrigation_list) ):
            print "irrigation point or drenage"
            tran.append(0)
        else:
            tran.append((weight[i]-weight[i+1])*L/time_diff)
            lista.append(i)
    return np.array(tran),lista
    
