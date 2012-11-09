# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 15:16:57 2012

@author: dpiscia
"""
from datetime import datetime
import sqlite3 as sql
import xlrd
import csv
import re
import numpy as np
import pandas


def __processCursor(cur, dataframe=False, index=None):
    '''
    Processes a database cursor with data on it into either
    a structured numpy array or a pandas dataframe.

    input:
    cur - a sql cursor that has just received data
    dataframe - bool. if false, a numpy record array is returned
                if true, return a pandas dataframe
    index - list of column(s) to use as index in a pandas dataframe
    '''
    dt = np.dtype([('data', 'M8'), ('t_rad_ext', 'float32'),("rad_ext", 'float32'),('t_rad_int', 'float32'),('rad_int_sup_solar', 'float32'),('rad_int_inf_solar', 'float32'),('rad_int_inf_term', 'float32'),('rad_int_sup_term', 'float32'),('temp_1', 'float32'),('RH_1', 'float32'),('temp_2', 'float32'),('RH_2', 'float32'),('thermo1', 'float32'),('thermo2', 'float32'),('SHF', 'float32'),('t_soil', 'float32'),('t_ext', 'float32'),('RH_ext', 'float32'),('time_balanca', 'float32'),('peso_balanca', 'float32')])

    data = []
    for row in cur:
        
        data.append(tuple(row))
        
        
    array = np.array(data, dtype=dt)
    if dataframe:
        output = pandas.DataFrame.from_records(array)

        if index is not None:
            output = output.set_index(index)

    else:
        output = array

    return output    
    

def avg(data,lista_fin,time_avg):
    ''' average half hour,
    inputs:
        -data
        -time items
        -6 average of half-hour
        -12 hour average'''
    iterator = 0
    value_avg = []
    time_list = []
    avg = 0
    for i in range(len(lista_fin)-1):
        iterator = iterator +1
        avg = avg + data[i]
        if (lista_fin[i]-lista_fin[i+1] > 1 or iterator == time_avg):
            print "end cycle"
            value_avg.append(avg/iterator)
            time_list.append(lista_fin[i])
            iterator = 0
            avg = 0
    return value_avg,time_list    
        
    
def check_item_by_date(conn,cursor,data):
    ''' before of inserting new record into DB, 
    this function will check whether the primary key timeline is
    already inserted'''
    cursor.execute ("SELECT date from data where date =:fecha" ,{"fecha":data})
    conn.commit()
    row = cursor.fetchone()
    if (row <> None):
        print "Error this date is already inserted", data
        return True
    else:
        print "OK data record will be inserted", data
        return False
        
def convert_file_into_list(file_name):
    ''' get a file, containg a list of file, as input and return a
    python list object
    '''
    lista = []
    with open(file_name,'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            lista.append(str(re.sub("[]''[]","",str(row))))
            print re.sub("[]''[]","",str(row))
    return lista  
    
def create_table():
    ''' function to create a sqlite table from zero, to be used 
    only once use .tables 
    and .schema for getting table and schema info from sqlite shell
    '''
    
    con = sql.connect('greenhouse.db')
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS data")
    cur.execute("CREATE TABLE data(date timestamp PRIMARY KEY, t_rad_ext FLOAT, rad_ext FLOAT,t_rad_int FLOAT,rad_int_sup_solar FLOAT,rad_int_inf_solar FLOAT,rad_int_inf_term FLOAT,rad_int_sup_term FLOAT, temp_1 FLOAT,RH_1 FLOAT,temp_2 FLOAT,RH_2 FLOAT, thermo1 FLOAT,thermo2 FLOAT,SHF FLOAT,t_soil FLOAT,t_ext FLOAT,RH_ext FLOAT,time_balanca FLOAT,peso_balanca FLOAT)")
    con.close()     
   
def load_data_list(file_name):
    ''' get file with a list of name a load data'''
    
    list_file = convert_file_into_list(file_name)
    for i in list_file:
        load_data_into_sqlite(i)
        
def load_data_into_sqlite(excel_file):
    ''' read an excel sheet and load data directly into a sqlite DB,
     it can be adapted to other format, but chnges has to be consisten with 
     function create table. pay special attention to primary key date, which is an 
     output of function set_date_time
    '''
    print "excel file is ", excel_file
    book = xlrd.open_workbook(excel_file)
    sheet = book.sheet_by_index(0)
    #for col in range(len(dati)): #number of columns
    #    for row in range(sheet.nrows):    #numbers of rows
    #            dati[col].append(sheet.cell_value(row,col))
    con = sql.connect('greenhouse.db')
    cur = con.cursor()
    for row in range(1,sheet.nrows):
        if not check_item_by_date(con,cur,set_date_time(int(sheet.cell_value(row,1)),int(sheet.cell_value(row,2)),int(sheet.cell_value(row,3)))):
             try:
                 cur.execute("INSERT INTO data values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (set_date_time(int(sheet.cell_value(row,1)),int(sheet.cell_value(row,2)),
                 int(sheet.cell_value(row,3))),float(sheet.cell_value(row,4)),float(sheet.cell_value(row,5))
                 ,float(sheet.cell_value(row,6)),float(sheet.cell_value(row,7)),float(sheet.cell_value(row,8)),float(sheet.cell_value(row,9)),float(sheet.cell_value(row,10)),
                 float(sheet.cell_value(row,11)),float(sheet.cell_value(row,12)),float(sheet.cell_value(row,13)),float(sheet.cell_value(row,14)),
                 float(sheet.cell_value(row,17)),float(sheet.cell_value(row,18)),float(sheet.cell_value(row,19)),float(sheet.cell_value(row,23)),
                 float(sheet.cell_value(row,24)),float(sheet.cell_value(row,25)),float(sheet.cell_value(row,26)),float(sheet.cell_value(row,27))))
             except :
                 print "error mistake in the record insertion  " 
        #print data_functions.set_date_time(int(sheet.cell_value(row,1)),int(sheet.cell_value(row,2)),int(sheet.cell_value(row,3)))
        #print int(sheet.cell_value(row,1)), " --- ",int(sheet.cell_value(row,2)) ,"-----", int(sheet.cell_value(row,3))
    con.commit()
    con.close()  

#def plot_one_variable(x_time,y_value):
    

def query_db(DB_name,TB_name,begin_date,end_date):
    ''' qeury a DB based on datetime range, can be further abstracted top be used in diff
    scenarios'''
    try:
        connection = sql.connect(DB_name)
    except:
        print "DB connection problem", DB_name
    cursor = connection.cursor()
    cursor.execute ("SELECT * from data where date >=:fecha_in and date<=:fecha_fin" ,{"fecha_in":begin_date,"fecha_fin":end_date})
    connection.commit()
    dataframe = __processCursor(cursor, dataframe=False)
    return dataframe
   
def set_date_time(year,day,minute):
    ''' receive numbers of days and find mothns and days
    receive minutes with no format and 
    return hours and minutes
    '''
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



   


