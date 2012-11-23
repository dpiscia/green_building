# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 09:12:24 2012

@author: dpiscia
"""
import math

def ventilation(wind, degree):
     ''' input wind speed between 1 and 4 m s-1
        degree between 0 and 90
        return kg s-1 m-1 (depth)'''
     ventilation = 0.0   
     if (wind > 4):
         print "wind speed can not exceed 4, speed will be reset to 4"
     if (degree == 0.0):   
        print "venitlation zero becasue degree is zero"    
     else:    
         sin_angle = math.sin(degree*3.14/180)
         BF1 = max(0.0, sin_angle -0.258690844053802)
         BF2 = max(0.0, 0.258690844053802 - sin_angle)
         BF3 = BF1 * max(0.0, wind -2)
         BF4 = max(0.0, wind -2)
         BF5 = max(0.0, 2 - wind)
         BF6 = BF4 * max(0.0, sin_angle -0.499770102643102)
         BF7 = BF4 * max(0.0, 0.499770102643102 - sin_angle)
         BF8 = max(0.0, 0.865759839492344 - sin_angle)
         BF9 = BF8 * max(0.0, 2 - wind)
         ventilation = (19.3941877273305 + 15.0399995903575*BF1 -22.5664934534249*BF2
                       -4.50069762381828*BF3 +9.85686151491185*BF4 -14.6458277948187*BF5 +19.1931416709916*BF6 -19.418993497707*BF7    
                       -15.074984018779*BF8 +16.4915503604416*BF9)
     return ventilation/12