# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
C:\Users\dpiscia\.spyder2\.temp.py
"""

import xlrd
from datetime import datetime

'''list variables declaration'''
first_column = []
year = []
day = []
hour = []
t_rad_ext = []
rad_ext = []
t_rad_int = []
rad_int_sup_solar = []
rad_int_inf_solar = []
rad_int_int_inf_term = []
rad_int_sup_term = []
temp_1 = []
RH_1 = []
temp_2 = []
RH_2 = []
battery = []
prog = []
thermo1 = []
thermo2 = []
SHF = []
rs_1 = []
rs_2 = []
rs_3 = []
t_soil = []
t_ext = []
RH_ext = []
time_balanca = []
peso_balanca = []
dati = [first_column,year,day,hour,t_rad_ext,rad_ext,t_rad_int,
        rad_int_sup_solar, rad_int_inf_solar, rad_int_int_inf_term, 
        rad_int_sup_term, temp_1,RH_1,temp_2,RH_2,battery,
       prog,thermo1,thermo2,SHF,rs_1,rs_2,rs_3,t_soil,t_ext,RH_ext,time_balanca,
       peso_balanca]
       
excel_file= '22062010.xls'
book = xlrd.open_workbook(excel_file)
sheet = book.sheet_by_index(0)
for col in range(len(dati)): #number of columns
    for row in range(sheet.nrows):    #numbers of rows
            dati[col].append(sheet.cell_value(row,col))
            
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

