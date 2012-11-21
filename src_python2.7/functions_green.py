# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 12:06:43 2012

@author: dpiscia
"""
import re
import numpy as np
import flux_functions as ff
import math
class geometry:
    """ read a text file and return geometry fields"""
    def __init__(self,folder):
        """ try to open the green_in file located in given folder
        
            the file is called green_in 
                   
        """
        try:
            f = open(folder+'/green_in','r')
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)    
        else:            
            self.properties = {}
            for line in f:
                line_new=line.split('=')
         
                try:
                    self.properties[re.sub(" ","",line_new[0])]=float(line_new[1])
                except :
                    print "error with line ", line
     
            f.close()

def dictionary_set():
    ''' return the dictionary where element names are associated to number
    i.e. elements['cover_out'] = 4'''
    elements = {'cover_out':0}
    elements['sky'] = 1
    elements['ext_soil'] = 2
    elements['sidewall_out'] = 3
    elements['cover_in'] = 4
    elements['sidewall_in'] = 5
    elements['soil'] = 6
    elements['SA*PO'] = 7
    return elements

def set_initial_conditions(T_ins,T_cover,RH_in,T,RH,T_outside):
    # 0 inside,1 cover, 2 sidewall, 3 soil
    T[0][8] = T_ins
    T[0][0] = T[0][4] = T_cover
    T[0][9] = T_outside
    RH[0][8] = RH_in

def BC_cond(element,fluid_element,qcond,alphas,e,T,g,time):
    ''' Boundary condition, cond = conv + rad'''
    kbol = 5.67*math.pow(10,-8)
    T[time][element] = (qcond + alphas[time][element] *T[time][fluid_element] + e[element]*g[time][element])/(e[element]*kbol * math.pow(T[time][element],3)+alphas[time][element])

def BC_cond_2(element,fluid_element,qcond,qrad,alphas,T,time):
    ''' Boundary condition, cond = conv + rad'''
    
    T[time][element] = ((qcond + alphas[time][element] *T[time][fluid_element] - qrad[time][element])
    /(alphas[time][element]))


def BC_conv_conv(el_inner,el_outer,fluid_el_outer,fluid_el_inner,alphas,e,tr,T,g,j,time):
    ''' Boundary condition, conv + rad = conv + rad'''
    #T[4]= (e[0]*g[0]+alpha[0]*geo.T_air+e[4]*g[4]+alpha[4]*T_air_inside -t[0]*j[4]+t[0]*j[0]
    #- t[4]*j[0] +t[4]*j[4])/(e[0]*kbol*pow(T[4],3)+alpha[0]+alpha[4]+e[4]*kbol*pow(T[4],3))
    kbol = 5.67*math.pow(10,-8)
    T[time][el_inner] = ((e[el_outer]+alphas[time][el_outer]*T[time][fluid_el_outer]+
    e[el_outer]*g[time][el_outer] + alphas[time][el_inner]*T[time][fluid_el_inner] -
    tr[el_outer]*j[time][el_inner]+tr[el_outer]*j[time][el_outer] -
    - tr[el_inner]*j[time][el_outer] + tr[el_inner]*j[time][el_inner]) /
    (e[el_outer]*kbol*math.pow(T[time][el_inner],3) + alphas[time][el_inner] + alphas[time][el_outer]
     +e[el_inner]*kbol*math.pow(T[time][el_inner],3)))

def BC_conv_conv_2(el_inner,el_outer,fluid_el_outer,fluid_el_inner,alphas,qrad,T,time):
    ''' Boundary condition, conv + rad = conv + rad'''
    #T[4]= (e[0]*g[0]+alpha[0]*geo.T_air+e[4]*g[4]+alpha[4]*T_air_inside -t[0]*j[4]+t[0]*j[0]
    #- t[4]*j[0] +t[4]*j[4])/(e[0]*kbol*pow(T[4],3)+alpha[0]+alpha[4]+e[4]*kbol*pow(T[4],3))
    kbol = 5.67*math.pow(10,-8)
    T[time][el_inner] = ((qrad[time][el_outer]+alphas[time][el_outer]*T[time][fluid_el_outer]+
    e[el_outer]*g[time][el_outer] + alphas[time][el_inner]*T[time][fluid_el_inner] -
    tr[el_outer]*j[time][el_inner]+tr[el_outer]*j[time][el_outer] -
    - tr[el_inner]*j[time][el_outer] + tr[el_inner]*j[time][el_inner]) /
    (e[el_outer]*kbol*math.pow(T[time][el_inner],3) + alphas[time][el_inner] + alphas[time][el_outer]
     +e[el_inner]*kbol*math.pow(T[time][el_inner],3)))
 
def fluid_T_solver(T,alphas,A,Vol,rho,cp,time,deltaT):
#    T_air_inside = (alpha[5]*T[5]*A[5]+alpha[4]*T[4]*A[4]+alpha[6]*T[6]*A[6]+(geo.rho*geo.cp*Vol*T_inside0
#               /deltaT)+(geo.T_air*geo.cp*Ventilation))/(alpha[5]*A[5]+alpha[4]*A[4]+alpha[6]*A[6]+ 
#               (geo.rho*geo.cp*Vol/deltaT)+(geo.cp*Ventilation));
  
   T[time][8]= (((alphas[time][4]*T[time][4]*A[4] + alphas[time][5]*T[time][5]*A[5]+alphas[time][6]*T[time][6]*A[6])   
   + (rho *cp * Vol * T[time-1][8]/ deltaT) ) / 
   ((alphas[time][4]*A[4] + alphas[time][5]*A[5]+alphas[time][6]*A[6])+(rho *cp * Vol / deltaT) ) )
              
def relax(T,T0,time):
    T[time][0] = T[time][4]
    T[time][3] = T[time][5]
    T[time] = T[time] + 0.25*np.abs(T[time]-T0)
    T0 = T[time]
def solver_T(T,qrad,qconv,alphas,j,g,e,tr,u,view_factor,qcond,timestep,nr_timestep,A,rho,cp,Vol):
    time = 1
    deltaT = 60
    T[time][8] = T[time-1][8]
    T[time][9] = T[time-1][9]
    T0 = np.zeros( shape=(1,10))
    T0[0] = 281
    for i in range(1,400):
        ff.radiation_flux(T,qrad,view_factor,j,g,e,tr,time)        
        ff.convective_coeff(T,u,alphas,time)
        ff.conv_flux(T,alphas,qconv,time)
        BC_cond(6,8,qcond,alphas,e,T,g,time)
        print "t soil", T[time][6]
        #BC_cond_2(6,8,qcond,qrad,alphas,T,time)
    
        BC_conv_conv(4,0,9,8,alphas,e,tr,T,g,j,time)
        print "t cover", T[time][4]
        BC_conv_conv(5,3,9,8,alphas,e,tr,T,g,j,time)
        print "t side", T[time][5]
        fluid_T_solver(T,alphas,A,Vol,rho,cp,time,deltaT)
        print "inside air", T[time][8]
        raw_input("")
        relax(T,T0,time)
#        T[time][6] = T0[6] + relax*(T[6]-T0[6]);
#        T[time][4] = T0[4] + relax*(T[4]-T0[4]);
#        T[time][3] = T0[3] + relax*(T[3]-T0[3]);
     


def optictal_prop(tran_list,emissivity_list):
    ''' return optical properties'''
    tr = np.array(tran_list)
    em = np.array(emissivity_list)
    ref = 1-tr-em
    return tr,em,ref
    
def view_factor(geometry,F,area,Vol):
    """ calculate the view factor for given geometry
    calculate the areas of element                  """

    Dd = geometry.properties['cover_height']
    AB = geometry.properties['ext_land']
    QR = (AB*2)+ (geometry.properties['span_number']*geometry.properties['span_width'])
    BC = geometry.properties['span_height']
    RS = (geometry.properties['domain_height'] - BC - Dd)
    Bb = geometry.properties['span_width'] 
    CD = pow(Dd,2)+ pow(Bb/2,2)
    CD = pow(CD,0.5)
    #internal calculation
    BN = geometry.properties['span_number']*geometry.properties['span_width']

    CN = pow(BN,2)+pow(BC,2)
    CN = pow(CN,0.5)
    F_soil_sidewall= 1-((CN*2) -(BC*2))/(2*BN)
    F_soil_cover= 1 - F_soil_sidewall
    area[6] = BN
    area[5] = BC*2
    area[4] = CD*2*geometry.properties['span_number']
    F_sidewall_soil = F_soil_sidewall*area[6]/area[5]
    F_sidewall_cover = F_sidewall_soil
    F_side_side = 1 - (F_sidewall_soil*2)
    F_cover_soil = F_soil_cover * area[6]/area[4]
    F_cover_sidewall = F_sidewall_cover * area[5]/area[4]
    F_cover_cover = 1 - F_cover_sidewall -F_cover_soil
    F[4][4] = F_cover_cover
    F[4][5] = F_cover_sidewall
    F[4][6] = F_cover_soil
    F[5][4] = F_sidewall_cover
    F[5][5] = F_side_side
    F[5][6] = F_sidewall_soil
    F[6][4] = F_soil_cover
    F[6][5] = F_soil_sidewall
    F[6][6] = 0
    
    #external 
    area[2] = AB*2
    area[3] = BC*2
    AS = BC+Dd
    area[7] = AS*2
    area[1] = QR +(geometry.properties['domain_height']*2 -area[7])
    area[0]=area[4]
    AC = pow(AB,2) +pow(BC,2)
    AC = pow(AC,0.5)
    F[2][3] = ((AB+BC)-AC)/(2*AB)
    F[3][2] = F[2][3]*area[2]/area[3]
    BS = pow(AB,2)+pow(AS,2)
    BS = pow(BS,0.5)
    CS = pow(AB,2) + pow(Dd,2)
    CS = pow(CS,0.5)
    F[3][7]= ((BS+AC-CS-AB)/(2*BC))
    F[3][1] = 1 -F[3][2] -F[3][7]
    F[3][0]=F[3][3]=0
    F[2][2] = 0
    BD = pow(Bb/2,2)+pow(BC+Dd,2)
    BD = pow(BD,0.5)
    AD = pow(AB+Bb/2,2)+pow(BC+Dd,2)
    AD = pow(AD,0.5)
    F[2][0]= (AC+BD-AD-BC)/(AB*2)
    if (F[2][0] <= 0) :
        F[2][0] = 0  
    F[2][7] = (AS+AB-BS)/(2*AB)
    F[2][1] = 1 -F[2][3] -F[2][7]
    F[7][2] = F[2][7]*area[2]/area[7]
    F[7][3] = F[3][7]*area[3]/area[7]
    DS = AB+ Bb/2;
    F[7][0] = (AD+CS-DS-AC)/(2*AS)
    if (F[7][0]<=0 ):
        F[7][0] = 0
    F[7][1]= 1 - F[7][0] - F[7][2] - F[7][3]
    F[0][7] = F[7][0] * area[7]/area[0]
    F[0][3] = 0
    F[0][2] = F[2][0] * area[2]/area[0]
    F_SP_sky = 1
    F[1][1] = 1- (F_SP_sky * QR / (2*RS + QR))
    F[1][2] = F[2][1] * area[2]/area[1]
    F[1][3] = F[3][1] * area[3]/area[1]
    F[1][7] = F[7][1] * area[7]/area[1]
    F[1][0] = 1 - F[1][1] - F[1][2] - F[1][3] - F[1][7]
    F[0][1] = F[1][0] * area[1]/area[0]
    F[0][0] = 1 - F[0][1] - F[0][2] - F[0][3] - F[0][7]
    
    Vol = (geometry.properties['span_number']*(geometry.properties['span_width']*geometry.properties['span_height']
    + geometry.properties['cover_height']*geometry.properties['span_width']/2))
   

#}