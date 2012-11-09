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
import data_plot
import numpy as np
data_in = datetime(2010,6,22,10,00,0)
data_fin = datetime(2010,6,22,10,05,0)
dati = df.query_db('greenhouse.db','data',data_in,data_fin)
#Rn = mf.net_solar_ration(dati['rad_int_sup_solar'],dati['rad_int_inf_solar'],0.64,2.96)
#Rn_b = mf.net_solar_ration(dati['rad_int_sup_solar'],0,0.64,2.96)

tra_P_M = mf.transpiration_P_M(dati['rad_int_sup_solar'],dati['rad_int_inf_solar'],0.64,2.96,((dati['temp_1']+dati['temp_2'])/2)+273.15,(dati['RH_1']+dati['RH_2'])/200)
tra_weight = mf.transpiration_from_balance(dati['peso_balanca'],300,2260000)
#check order - create uni test against one record file from excel

#data_plot.plot_time_data_2(dati['data'],dati['peso_balanca'],'peso balanza')
#data_plot.plot_time_data_2_y_axis(dati['data'],dati['peso_balanca'],'peso balanza',tra_P_M,'trans Penman')
#data_plot.plot_time_data_2_y_axis(dati['data'][0:len(tra_weight)],-tra_weight,'trans weight',tra_P_M[0:len(tra_weight)],'trans Penman')
#data_plot.plot_time_data_2_y_axis(dati['data'][0:len(tra_weight)],np.diff(dati['peso_balanca']),'delta weight',dati['peso_balanca'],'peso balanza')

delta_peso = np.diff(dati['peso_balanca'])
fr,lista,lista_in = mf.find_irrigation_point(delta_peso,dati['data'])
tran_weight = mf.transpiration_from_balance_irr(dati['peso_balanca'],300,2260000,lista)   
lista_fin = mf.lista_mod(lista,lista_in)
#data_plot.plot_time_data_2_y_axis(dati['data'][lista_fin],tra_P_M[lista_fin],'tra Penman',tran_weight,'trans weight')


    
tra_P_M_avg,time_P_M = df.avg(tra_P_M[lista_fin],lista_fin,12)
tra_weigh_avg,time_weight = df.avg(tran_weight,lista_fin,12)
#data_plot.plot_time_data_2_y_same_axis(dati['data'][time_P_M],tra_P_M_avg,'tra Penman',tra_weigh_avg,'trans weight')