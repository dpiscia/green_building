# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/home/dpiscia/.spyder2/.temp.py
"""
import functions_green as fg


class zone:
    """ the zone class can represent the greeenhouse """
    def __init__(self, folder):
         """ folder represents the folder where DB data files are located"""
         print "folder passed is ", folder
         self.folder = folder
         self.geometry = fg.geometry(self.folder)
         # geometry instead of being populated by aschii file can be created
         #by chosing from db
         
