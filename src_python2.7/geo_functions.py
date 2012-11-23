# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 09:03:40 2012

@author: dpiscia
"""
import re

class geometry:
    """ read a text file and return geometry fields"""
    def __init__(self,folder):
        """ try to open the green_in file located in given folder
        
            the file is called green_in 
                   
        """
        try:
            f = open(folder+'/green_in','r')
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)    
        else:            
            self.properties = {}
            for line in f:
                line_new=line.split('=')
         
                try:
                    self.properties[re.sub(" ","",line_new[0])]=float(line_new[1])
                except :
                    print "error with line ", line
     
            f.close()

def dictionary_set():
    ''' return the dictionary where element names are associated to number
    i.e. elements['cover_out'] = 4'''
    elements = {'cover_out':0}
    elements['sky'] = 1
    elements['ext_soil'] = 2
    elements['sidewall_out'] = 3
    elements['cover_in'] = 4
    elements['sidewall_in'] = 5
    elements['soil'] = 6
    elements['SA*PO'] = 7
    return elements