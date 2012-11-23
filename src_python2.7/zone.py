# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/home/dpiscia/.spyder2/.temp.py
"""
import functions_green as fg
import optical_functions as of
import geo_functions as gf
import numpy as np

class zone:
    """ the zone class can represent the greeenhouse """
    def __init__(self, folder):
         """ folder represents the folder where DB data files are located"""
         print "folder passed is ", folder
         self.folder = folder
         self.geometry = gf.geometry(self.folder)
         self.elements = gf.dictionary_set()
         self.area = np.zeros(shape = (8))
         self.Vol = (self.geometry.properties['span_number']*(self.geometry.properties['span_width']*
                     self.geometry.properties['span_height'] + self.geometry.properties['cover_height']
                     *self.geometry.properties['span_width']/2))
         self.F = np.zeros(shape = (8, 8))
         of.view_factor(self.geometry, self.F, self.area, self.Vol)
         tran = [self.geometry.properties['tra_cover_out'],0.0,0.0,
                 self.geometry.properties['tra_sidewall_out'],
                 self.geometry.properties['tra_cover_in'],
                 self.geometry.properties['tra_sidewall_in'],0.0,0.0]
         emi = [self.geometry.properties['emi_cover_out'],1.0,1.0,
                 self.geometry.properties['emi_sidewall_out'],
                 self.geometry.properties['emi_cover_in'],
                 self.geometry.properties['emi_sidewall_in'],1.0,1.0]                 
         self.tr, self.em, self.re = of.optictal_prop(tran,emi)
         if ((self.tr + self.em).any() > 1.0):
             print "error in optical properties"
         self.T = np.zeros(shape = (2,10))
         self.RH = np.zeros(shape = (2,10))
         # 8 inside,9 outside 
         self.qcond = np.zeros(shape = (2,8))
         self.qconv = np.zeros(shape = (2,8))
         self.qrad = np.zeros(shape = (2,8))
         self.j = np.zeros(shape = (2,8))
         self.g = np.zeros(shape = (2,8))
         self.alpha = np.zeros(shape = (2,8))
         deltaT = 300
         fg.set_initial_conditions(self.geometry.properties['t_air_inside'],
                                   278,
                                   self.geometry.properties['RH_in'],self.T,self.RH , self.geometry.properties['t_air'],self.g,
                                   self.geometry.properties['sky_temp'])
         self.T, self.j, self.g, self.alpha, self.qrad, self.qconv = fg.solver_T(self.T,self.qrad,self.qconv,self.alpha,self.j,self.g,self.em,self.tr,
                     self.geometry.properties['wind_speed']
                     ,self.F,self.geometry.properties['heat_flux'],1,1.0,self.area,
                    self.geometry.properties['rho'],self.geometry.properties['cp'],self.Vol,deltaT)

if (__name__=="__main__"):
    prova = zone('.')
