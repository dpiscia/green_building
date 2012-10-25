# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 15:16:57 2012

@author: dpiscia
"""
from datetime import datetime

def set_date_time(year,day,minute):
    days_month = [31,28,31,30,31,30,31,31]
    month = 1
    real_day = day
    for i in days_month:
        if (real_day <= i):
             break
        else: 
             real_day = real_day - i
             month = month +1
    hour = 0
    while (minute>60):
        minute = minute-100
        hour = hour+1
    date = datetime(year,month,real_day,hour,minute)
    return date
set_date_time(2010,173,5)