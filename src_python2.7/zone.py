# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/home/dpiscia/.spyder2/.temp.py
"""
import functions_green as fg

import numpy as np

class zone:
    """ the zone class can represent the greeenhouse """
    def __init__(self, folder):
         """ folder represents the folder where DB data files are located"""
         print "folder passed is ", folder
         self.folder = folder
         self.geometry = fg.geometry(self.folder)
         self.elements = fg.dictionary_set()
         self.area = np.zeros(shape = (8))
         self.Vol = 0
         self.Vol = (self.geometry.properties['span_number']*(self.geometry.properties['span_width']*
                     self.geometry.properties['span_height'] + self.geometry.properties['cover_height']
                     *self.geometry.properties['span_width']/2))
         self.F = np.zeros(shape = (8, 8))
         fg.view_factor(self.geometry, self.F, self.area, self.Vol)
         tran = [self.geometry.properties['tra_cover_out'],0.0,0.0,
                 self.geometry.properties['tra_sidewall_out'],
                 self.geometry.properties['tra_cover_in'],
                 self.geometry.properties['tra_sidewall_in'],0.0,0.0]
         emi = [self.geometry.properties['emi_cover_out'],1.0,1.0,
                 self.geometry.properties['emi_sidewall_out'],
                 self.geometry.properties['emi_cover_in'],
                 self.geometry.properties['emi_sidewall_in'],1.0,1.0]                 
         self.tr, self.em, self.re = fg.optictal_prop(tran,emi)
         if ((self.tr + self.em).any() > 1.0):
             print "error in optical properties"
         self.T = np.zeros(shape = (2,10))
         self.T[1][[3,5,6]]= 283
         self.T[0][1] = self.T[1][7] =  self.geometry.properties['sky_temp']
         self.T[1][2] = 283
         self.RH = np.zeros(shape = (2,10))
         # 8 inside,9 outside 
         self.qcond = np.zeros(shape = (2,8))
         self.qconv = np.zeros(shape = (2,8))
         self.qrad = np.zeros(shape = (2,8))
         self.j = np.zeros(shape = (2,8))
         
         self.g = np.zeros(shape = (2,8))
         self.g[1]=350
         self.alpha = np.zeros(shape = (2,8))
         RH_in = 0.5
         
         fg.set_initial_conditions(self.geometry.properties['t_air_inside'],
                                   278,
                                   RH_in,self.T,self.RH , self.geometry.properties['t_air'])
         fg.solver_T(self.T,self.qrad,self.qconv,self.alpha,self.j,self.g,self.em,self.tr,
                     self.geometry.properties['wind_speed']
                     ,self.F,self.geometry.properties['heat_flux'],1,1.0,self.area,
                    self.geometry.properties['rho'],self.geometry.properties['cp'],self.Vol)
         #,T,qrad,qconv,alphas,j,g,e,tr,u,factor,timestep,nr_timestep
         #solver_T(T,qrad,qconv,alphas,j,g,e,tr,u,view_factor,qcond,timestep,nr_timestep,A,rho,cp,Vol)
         # geometry instead of being populated by aschii file can be created
         #by chosing from db
if (__name__=="__main__"):
    prova = zone('.')
