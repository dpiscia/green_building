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

data_in = datetime(2010,6,24,8,00,0)
data_fin = datetime(2010,6,24,18,00,0)
dati = df.query_db('greenhouse.db','data',data_in,data_fin)


tra_P_M = mf.transpiration_P_M(dati['rad_int_sup_solar'],dati['rad_int_inf_solar'],0.64,2.96,((dati['temp_1']+dati['temp_2'])/2)+273.15,(dati['RH_1']+dati['RH_2'])/200)
tra_weight = mf.transpiration_from_balance(dati['peso_balanca'],300,2260000)


delta_peso = np.diff(dati['peso_balanca'])
fr,lista_irr,lista_irr_free = mf.find_irrigation_point(delta_peso,dati['data'])
lista_night = mf.remove_no_solar_point(dati['rad_int_sup_solar'],10)
Is = dati['rad_int_sup_solar']

lista_no = list(set(lista_irr+ lista_night))

tran_weight,lista_yes = mf.transpiration_from_balance_irr(dati['peso_balanca'],300,2260000,lista_no) 
min_avg = 6 
tra_weigh_avg,time_weight = df.avg(tran_weight,lista_yes,min_avg)
tra_P_M_avg,time_P_M = df.avg(tra_P_M,lista_yes,min_avg)

data_plot.plot_time_data_2_y_same_axis(dati['data'][time_P_M],tra_P_M_avg,'tra Penman',tra_weigh_avg,'trans weight')
RMSE = df.RMSE(tra_P_M_avg,tra_weigh_avg)
print "RMSE is", RMSE
print "RRMSE is", df.RRMSE(RMSE,tra_weigh_avg)

data_plot.plot_time_data_2(dati['data'],dati['peso_balanca'],'peso')
data_plot.plot_time_data_2(dati['data'],dati['peso_balanca'],'peso')
#def work_2():
#    data_in = datetime(2010,6,21,8,00,0)
#    data_fin = datetime(2010,6,26,8,00,0)
#    dati_station = df.query_db('greenhouse.db','station_data',data_in,data_fin)
#
#    dati = df.query_db('greenhouse.db','data',data_in,data_fin)
#    return dati_station,dati
#if (__name__=="__main__"):
#    station_dati,dati = work_2()
#    Is_green = np.array(df.avg_(dati['rad_int_sup_solar'],12))
#    Is_station = station_dati['net_eadiation']
#    print len(Is_green)
#    print len(Is_station)
#    model,R2 = df.linear_reg(Is_station[:-1],Is_green,True)
#    print model
#    print R2
#    data_plot.plot_time_data_2_y_same_axis(station_dati['data'][:-1],Is_station,'Is_station',Is_green,'greenhouse')
    