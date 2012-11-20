# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 15:16:57 2012

@author: dpiscia
"""
from datetime import datetime,timedelta
import sqlite3 as sql
import xlrd
import csv
import re
import numpy as np
import pandas
import math
import matplotlib.pyplot as plt
import dateutil.parser
def __processCursor(cur,dt,dataframe=False, index=None):
    '''
    Processes a database cursor with data on it into either
    a structured numpy array or a pandas dataframe.

    input:
    cur - a sql cursor that has just received data
    dataframe - bool. if false, a numpy record array is returned
                if true, return a pandas dataframe
    index - list of column(s) to use as index in a pandas dataframe
    '''
    

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
    
def avg_(data,step):
    lista = []
    average = 0
    iterator = 0
    for i in range(len(data)):
        average = average + data[i]
        iterator = iterator + 1
        if  (iterator == step):
            lista.append(average/step)
            average = 0
            iterator = 0
        elif (i == len(data)-1):
            lista.append(average/step)
    return np.array(lista)

   
        
def avg2(data,lista,time_avg):
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
    for iterat,value  in enumerate(lista[:-1]):
        iterator = iterator +1
        
        avg = avg + data[value]
        print "avergae", avg
        print "i ,", iterat , "data value ", data[value]
        print "lista[i+1]", lista[iterat+1] ,"iterator ", iterator
        if (lista[iterat+1]-lista[iterat] > 1 or iterator == time_avg ):
            print "end cycle iterator", iterator
            if (iterator == time_avg):
                value_avg.append(avg/iterator)
                time_list.append(value)
                print "value_Avg", avg/iterator 
                print " "
                
            iterator = 0
            avg = 0
            #raw_input("Press Enter to continue...")
    return np.array(value_avg),time_list    
    
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

def create_table_station_data():
    ''' function to create a sqlite table from zero, to be used 
    only once use .tables 
    and .schema for getting table and schema info from sqlite shell
    '''
    
    con = sql.connect('greenhouse.db')
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS station_data")
    cur.execute("CREATE TABLE station_data(date timestamp PRIMARY KEY, RH FLOAT, RH_min FLOAT,RH_max FLOAT,Water_Vapour_partial_pressure FLOAT,temp FLOAT,temp_min FLOAT,temp_max FLOAT, temp_wet_bulb FLOAT,temp_soil_50cm FLOAT,temp_soil_5_m FLOAT,temp_rugiada FLOAT, wind_speed FLOAT,wet_hum FLOAT,dry_hum FLOAT,global_solar_rad FLOAT,net_radiation FLOAT)")
    con.close() 
   
def load_data_list(file_name):
    ''' get file with a list of name a load data'''
    
    list_file = convert_file_into_list(file_name)
    for i in list_file:
        load_data_into_sqlite(i)

def linear_reg(x,y,plot):
    ''' linera regression of matrix against y
    y = mx +c
    y = Ab
    plot = true enables plotting capability 
    '''
    A = np.vstack([x, np.ones(len(x))]).T
    model, resid = np.linalg.lstsq(A, y)[:2]
    if plot:
 
        plt.plot(x, y, 'o', label='Original data', markersize=5)
        plt.plot(x, model[0]*x + model[1], 'r', label='Fitted line')
        plt.legend()
        plt.show()
    return model,(1 - resid / (y.size * y.var()))
        
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
             except Exception, e:
                 print "error mistake in the record insertion  " 
                 print e
        #print data_functions.set_date_time(int(sheet.cell_value(row,1)),int(sheet.cell_value(row,2)),int(sheet.cell_value(row,3)))
        #print int(sheet.cell_value(row,1)), " --- ",int(sheet.cell_value(row,2)) ,"-----", int(sheet.cell_value(row,3))
    con.commit()
    con.close()  

#def plot_one_variable(x_time,y_value):
    
def load_data_into_sqlite_2(excel_file):
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
    deltaday = timedelta(days=1)
    for row in range(1,sheet.nrows):
             if (sheet.cell_value(row,1)=="24:00"):
                 data = (dateutil.parser.parse(sheet.cell_value(row,0)+" "+"0:00", dayfirst = True))+deltaday
                 
                 
             else:
                 data = (dateutil.parser.parse(sheet.cell_value(row,0)+" "+sheet.cell_value(row,1), dayfirst = True))

             try:
                 cur.execute("INSERT INTO station_data values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (data,
                 float(sheet.cell_value(row,2)),float(sheet.cell_value(row,3)),float(sheet.cell_value(row,4)),
                 float(sheet.cell_value(row,5)),float(sheet.cell_value(row,6)),float(sheet.cell_value(row,7)),
                 float(sheet.cell_value(row,8)),float(sheet.cell_value(row,9)),float(sheet.cell_value(row,10)),
                 float(sheet.cell_value(row,11)),float(sheet.cell_value(row,12)),
                 float(sheet.cell_value(row,14)),float(sheet.cell_value(row,15)),float(sheet.cell_value(row,16)),
                 float(sheet.cell_value(row,17)),float(sheet.cell_value(row,18))))
             except Exception, e:
                 print "error mistake in the record insertion  data,", data
                 print "error ", e
                 
    con.commit()
    con.close()
    
def query_db(DB_name,TB_name,begin_date,end_date):
    ''' qeury a DB based on datetime range, can be further abstracted top be used in diff
    scenarios'''
    try:
        connection = sql.connect(DB_name)
    except:
        print "DB connection problem", DB_name
        print "TB name", TB_name
    print "TB name", TB_name
    cursor = connection.cursor()
    cursor.execute ("SELECT * from %s where date >=:fecha_in and date<=:fecha_fin" % TB_name ,{"data":TB_name,"fecha_in":begin_date,"fecha_fin":end_date})
    connection.commit()
    if (TB_name=="data"):
        dt = np.dtype([('data', 'M8'), ('t_rad_ext', 'float32'),("rad_ext", 'float32'),('t_rad_int', 'float32'),('rad_int_sup_solar', 'float32'),('rad_int_inf_solar', 'float32'),('rad_int_inf_term', 'float32'),('rad_int_sup_term', 'float32'),('temp_1', 'float32'),('RH_1', 'float32'),('temp_2', 'float32'),('RH_2', 'float32'),('thermo1', 'float32'),('thermo2', 'float32'),('SHF', 'float32'),('t_soil', 'float32'),('t_ext', 'float32'),('RH_ext', 'float32'),('time_balanca', 'float32'),('peso_balanca', 'float32')])
    elif(TB_name =="station_data"):
        dt = np.dtype([('data', 'M8'), ('RH', 'float32'),("RH_min", 'float32'),('RH_max', 'float32'),('Water_vapour_partial_pressure', 'float32'),('temp', 'float32'),('temp_min', 'float32'),('temp_max', 'float32'),('temp_wet_bulb', 'float32'),('temp_soil_50cm', 'float32'),('temp_soil_5cm', 'float32'),('temp_rugiada', 'float32'),('wind_speed', 'float32'),('wet_hum', 'float32'),('dry_hum', 'float32'),('global_solar_rad', 'float32'),('net_eadiation', 'float32')])
    dataframe = __processCursor(cursor,dt,dataframe=False)
    
    return dataframe

def RMSE(x,y):
    ''' return root mean square error'''
    return math.pow(np.average(np.power(np.array(x)-np.array(y),2)),0.5)
def RRMSE(RMSE,x):
    ''' return relative root mean square error'''
    return RMSE/np.average(np.array(x))
    
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



def smooht_Is(Is):
    ''' remove the first radiation peak
    due to the greenhouse frame reflection
    '''
    lista = []
    pass_card = False
    deltaIs = np.diff(Is)
    for i,value in enumerate(deltaIs):
        print "value ",value," pass_Card ", pass_card
        print "(value <-0.4 and pass_card)", (value <-0.4 and pass_card)
        if (value <-250 and pass_card):
            lista.append(i)
            pass_card =  False
            print "i", i
            #break
            #raw_input("ee")
        if (value>250 or pass_card):
            lista.append(i+1)
            pass_card = True
            print "i", i
            
            #raw_input("firs if")

    return set(lista)
    
def smooth_value(Is,lista):
    ''' smooth point in the list'''
    Is_copy = np.copy(Is)
    delta = (Is_copy[max(lista)+1]-Is_copy[min(lista)-1])/len(lista)
    print "delta", delta
    for i,value in enumerate(lista):
        
        Is_copy[value] = Is_copy[value-1]+delta
    return Is_copy


