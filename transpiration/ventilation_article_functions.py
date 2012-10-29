# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 13:36:37 2012

@author: dpiscia
"""

angle = [0.087111671, 0.17356104, 0.258690844, 0.499770103, 0.865759839, 0.999999683]
u_wind = [1,2,3,4]
def vent(angle,u_wind):
    BF1 = max(0,angle-0.258690844053802)
    BF2 = max(0, (0.258690844053802 - angle))
    BF3 = BF1 * max(0, (u_wind-2))
    BF4 = max(0, (u_wind -2))
    BF5 = max(0, (2 - u_wind) )
    BF6 = BF4 * max(0, (angle -0.499770102643102))
    BF7 = BF4 * max(0, (0.499770102643102 - angle))
    BF8 = max(0, (0.865759839492344 - angle))
    BF9 = BF8 * max((0, 2 - u_wind))
    vent = 19.3941877273305 +15.0399995903575*BF1 -22.5664934534249*BF2 -4.50069762381828*BF3 +9.85686151491185*BF4 -14.6458277948187*BF5 +19.1931416709916*BF6 -19.418993497707*BF7 -15.074984018779*BF8 +16.4915503604416*BF9
    return vent

for j in u_wind:
    for i in angle:
        print "i,j", vent(i,j)/12