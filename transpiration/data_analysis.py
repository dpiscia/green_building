# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
C:\Users\dpiscia\.spyder2\.temp.py
"""



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
       

import data_functions as df
import sqlite3 as sql
from datetime import datetime
from pandas import DataFrame

#list_file = []
#list_file = df.convert_file_into_list('file_list.txt')
#print list_file
#          
#for i in list_file:
#    df.load_data_into_sqlite(i)

# 1-think a smart way of retrieving data from sqlite
# 2- analysis 

def query_db(DB_name,TB_name,begin_date,end_date):
    try:
        connection = sql.connect(DB_name)
    except:
        print "DB connection problem", DB_name
    cursor = connection.cursor()
    cursor.execute ("SELECT * from data where date >=:fecha_in and date<=:fecha_fin" ,{"fecha_in":begin_date,"fecha_fin":end_date})
    connection.commit()
    dataframe = __processCursor(cursor, dataframe=False)
#    row = cursor.fetchall()
#    for i in row:
#        print i


import numpy as np
import pandas
import decimal
        
def __processCursor(cur, dataframe=False, index=None):
    '''
    Processes a database cursor with data on it into either
    a structured numpy array or a pandas dataframe.

    input:
    cur - a pyodbc cursor that has just received data
    dataframe - bool. if false, a numpy record array is returned
                if true, return a pandas dataframe
    index - list of column(s) to use as index in a pandas dataframe
    '''
    datatypes = []
    colinfo = cur.description
    for col in colinfo:
        print "col 2," ,col[1]
        if col[1] == unicode:
            datatypes.append((col[0], 'U%d' % col[3]))
        elif col[1] == str:
            datatypes.append((col[0], 'S%d' % col[3]))
        elif col[1] in [float, decimal.Decimal]:
            datatypes.append((col[0], 'f4'))
        elif col[1] == datetime:
            datatypes.append((col[0], 'O4'))
        elif col[1] == int:
            datatypes.append((col[0], 'i4'))

    data = []
    for row in cur:
        
        data.append(tuple(row))
        #print data
        print datatypes
    array = np.array(data, dtype=datatypes)
    if dataframe:
        output = pandas.DataFrame.from_records(array)

        if index is not None:
            output = output.set_index(index)

    else:
        output = array

    return output    
data = datetime(2010,6,30,5,25,0)
data_fin = datetime(2010,6,30,5,25,0)
query_db('greenhouse.db',data,data,data_fin)

#problem when cosntructing the dataframe from description,whihc is none:
    #possible solution use sqlalchemy or use pyodbc with sqlite