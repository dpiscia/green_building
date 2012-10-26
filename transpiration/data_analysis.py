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
       

#import os
#os.system("ls *.xls > file_list.txt")

def convert_file_into_list(file_name):
    ''' get a file, containg a list of file, as input and return a
    python list object
    '''
    import csv
    import re
    lista = []
    with open(file_name,'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            lista.append(re.sub("[]''[]","",str(row)))
    return lista            
#check function already dvelopped

