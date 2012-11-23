# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 09:01:34 2012

@author: dpiscia
"""

import numpy as np

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
    
    
   
