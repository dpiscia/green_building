# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
C:\Users\dpiscia\.spyder2\.temp.py
"""

import xlrd
import sqlite3 as sql
import data_functions.py

#'''list variables declaration'''
#first_column = []  #0
#year = [] #1
#day = [] #2
#hour = []#3
#t_rad_ext = []#4
#rad_ext = []#5
#t_rad_int = []#6
#rad_int_sup_solar = []#7
#rad_int_inf_solar = []#8
#rad_int_inf_term = []#9
#rad_int_sup_term = []#10
#temp_1 = []#11
#RH_1 = []#12
#temp_2 = []#13
#RH_2 = []#14
#battery = []#15
#prog = []#16
#thermo1 = []#17
#thermo2 = []#18
#SHF = []#19
#rs_1 = []#20
#rs_2 = []#21
#rs_3 = []#22
#t_soil = []#23
#t_ext = []#24
#RH_ext = []#25
#time_balanca = []#26
#peso_balanca = []#27
#dati = [first_column,year,day,hour,t_rad_ext,rad_ext,t_rad_int,
#        rad_int_sup_solar, rad_int_inf_solar, rad_int_inf_term, 
#        rad_int_sup_term, temp_1,RH_1,temp_2,RH_2,battery,
#       prog,thermo1,thermo2,SHF,rs_1,rs_2,rs_3,t_soil,t_ext,RH_ext,time_balanca,
#       peso_balanca]
       
excel_file= '22062010.xls'
book = xlrd.open_workbook(excel_file)
sheet = book.sheet_by_index(0)
#for col in range(len(dati)): #number of columns
#    for row in range(sheet.nrows):    #numbers of rows
#            dati[col].append(sheet.cell_value(row,col))
con = sql.connect('greenhouse.db')
cur = con.cursor()
for row in range(1,sheet.nrows):
    cur.execute("INSERT INTO data values(?,?)", (data_functions.set_date_time(sheet.cell_value(row,1),sheet.cell_value(row,2),sheet.cell_value(row,3)), sheet.cell_value(row,4)))
con.close() 

            


def create_table():
    ''' function to create a sqlite table from zero, to be used only once'''
    ''' use .tables and .schema for getting table and schema info from sqlite shell'''
    
    con = sql.connect('greenhouse.db')
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS data")
    cur.execute("CREATE TABLE data(Id INT,date DATETIME, t_rad_ext FLOAT, rad_ext FLOAT,t_rad_int FLOAT,rad_int_sup_solar FLOAT,rad_int_inf_solar FLOAT,rad_int_inf_term FLOAT,rad_int_sup_term FLOAT, temp_1 FLOAT,RH_1 FLOAT,temp_2 FLOAT,RH_2 FLOAT, thermo1 FLOAT,thermo2 FLOAT,SHF FLOAT,t_soil FLOAT,t_ext FLOAT,RH_ext FLOAT,time_balanca FLOAT,peso_balanca FLOAT)")
    con.close() 