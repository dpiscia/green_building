# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 15:16:57 2012

@author: dpiscia
"""
from datetime import datetime
import sqlite3 as sql
import xlrd

def set_date_time(year,day,minute):
    days_month = [31,28,31,30,31,30,31,31]
    month = 1
    real_day = day
    hour = 0
    while (minute>60):
        minute = minute-100
        hour = hour+1
        
    if (hour==24):
        hour = 0
        real_day = real_day + 1
    
    for i in days_month:
        if (real_day <= i):
             break
        else: 
             real_day = real_day - i
             month = month +1
    

        
    date = datetime(year,month,real_day,hour,minute)
    return date

def create_table():
    ''' function to create a sqlite table from zero, to be used only once'''
    ''' use .tables and .schema for getting table and schema info from sqlite shell'''
    
    con = sql.connect('greenhouse.db')
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS data")
    cur.execute("CREATE TABLE data(date timestamp PRIMARY KEY, t_rad_ext FLOAT, rad_ext FLOAT,t_rad_int FLOAT,rad_int_sup_solar FLOAT,rad_int_inf_solar FLOAT,rad_int_inf_term FLOAT,rad_int_sup_term FLOAT, temp_1 FLOAT,RH_1 FLOAT,temp_2 FLOAT,RH_2 FLOAT, thermo1 FLOAT,thermo2 FLOAT,SHF FLOAT,t_soil FLOAT,t_ext FLOAT,RH_ext FLOAT,time_balanca FLOAT,peso_balanca FLOAT)")
    con.close() 
    
def load_data_into_sqlite(excel_file):
    book = xlrd.open_workbook(excel_file)
    sheet = book.sheet_by_index(0)
    #for col in range(len(dati)): #number of columns
    #    for row in range(sheet.nrows):    #numbers of rows
    #            dati[col].append(sheet.cell_value(row,col))
    con = sql.connect('greenhouse.db')
    cur = con.cursor()
    for row in range(1,sheet.nrows):
        cur.execute("INSERT INTO data values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (set_date_time(int(sheet.cell_value(row,1)),int(sheet.cell_value(row,2)),
         int(sheet.cell_value(row,3))),float(sheet.cell_value(row,4)),float(sheet.cell_value(row,5))
        ,float(sheet.cell_value(row,6)),float(sheet.cell_value(row,8)),float(sheet.cell_value(row,9)),float(sheet.cell_value(row,7)),float(sheet.cell_value(row,10)),
         float(sheet.cell_value(row,11)),float(sheet.cell_value(row,12)),float(sheet.cell_value(row,13)),float(sheet.cell_value(row,14)),
         float(sheet.cell_value(row,17)),float(sheet.cell_value(row,18)),float(sheet.cell_value(row,19)),float(sheet.cell_value(row,23)),
         float(sheet.cell_value(row,24)),float(sheet.cell_value(row,25)),float(sheet.cell_value(row,26)),float(sheet.cell_value(row,27))))
         #print data_functions.set_date_time(int(sheet.cell_value(row,1)),int(sheet.cell_value(row,2)),int(sheet.cell_value(row,3)))
        #print int(sheet.cell_value(row,1)), " --- ",int(sheet.cell_value(row,2)) ,"-----", int(sheet.cell_value(row,3))
    con.commit()
    con.close()     
