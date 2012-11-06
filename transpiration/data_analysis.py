# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
C:\Users\dpiscia\.spyder2\.temp.py
"""




       


# 1-think a smart way of retrieving data from sqlite - done
# 2- analysis 
# create function penman-monteih
# create function transpiration_from_weight
# check results


from datetime import datetime
import data_functions as df
import model_functions as mf
data_in = datetime(2010,6,17,6,0,0)
data_fin = datetime(2010,6,18,5,55,0)
dati = df.query_db('greenhouse.db','data',data_in,data_fin)
Rn = mf.net_solar_ration(dati['rad_int_sup_solar'],dati['rad_int_inf_solar'],0.64,2.96)
Rn_b = mf.net_solar_ration(dati['rad_int_sup_solar'],0,0.64,2.96)

tra = mf.transpiration_P_M(dati['rad_int_sup_solar'],dati['rad_int_inf_solar'],0.64,2.96,((dati['temp_1']+dati['temp_2'])/2)+273.15,(dati['RH_1']+dati['RH_2'])/200)
#check order - create uni test against one record file from excel

#import data_functions as df
#df.load_data_list('file_list.txt')
