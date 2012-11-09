# -*- coding: utf-8 -*-
"""
Created on Thu Nov 08 15:05:49 2012

@author: dpiscia
"""

import datetime
from matplotlib.pyplot import figure, show
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange, date2num
from matplotlib.ticker import MaxNLocator

def plot_time_data(date_in,date_end,delta,data_y):
    ''' plot data against detetime values, provide date_initial and final
    '''
    date1 = date_in
    date2 = date_end
    delta= datetime.timedelta(minutes=5)
    
    dates = drange(date1, date2, delta)
    fig = figure()
    ax = fig.add_subplot(111)
    if (len(dates)<>len(data_y[0:len(dates)])):
        print "error, len dates", len(dates)
        print "len dati ", len(data_y[0:len(dates)])
    ax.plot_date(dates, data_y[0:len(dates)],'-')
    ax.set_xlim( dates[0], dates[-1] )
    ax.xaxis.set_major_locator( DayLocator() )
    ax.xaxis.set_minor_locator( HourLocator())
    ax.xaxis.set_minor_formatter( DateFormatter('%H') )
    ax.xaxis.set_major_formatter( DateFormatter('%Y-%m-%d') )
    
    ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M')
    
    fig.autofmt_xdate()
    show()
    
def plot_time_data_2(data,data_y,label1):
    ''' plot data against detetime values, provide all datetime array
    '''

    
    date = data.astype(object)
    dates= date2num(date)
    fig = figure()
    ax = fig.add_subplot(111)
    ax.plot_date(dates, data_y[0:len(dates)],'-')
    ax.set_xlim( dates[0], dates[-1] )
    ax.xaxis.set_major_locator( DayLocator() )
    ax.xaxis.set_minor_locator( MaxNLocator(nbins = 20, prune = 'lower'))
    ax.xaxis.set_minor_formatter( DateFormatter('%H') )
    ax.xaxis.set_major_formatter( DateFormatter('%Y-%m-%d') )
    ax.set_ylabel(label1, color='b')
    ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M')
    
    fig.autofmt_xdate()
    show()
    
def plot_time_data_2_y_axis(data,data_y1,label1,data_y2,label2):
    ''' plot 2 variables data series against detetime values, provide all datetime array
    '''

    print "date", data
    date = data.astype(object)
    dates= date2num(date)
    fig = figure()
    ax = fig.add_subplot(111)
    ax.plot_date(dates, data_y1[0:len(dates)],'b-')
    ax.set_xlim( dates[0], dates[-1] )
    ax.xaxis.set_major_locator( DayLocator() )
    ax.xaxis.set_minor_locator( MaxNLocator(nbins = 20, prune = 'lower'))
    ax.xaxis.set_minor_formatter( DateFormatter('%H') )
    ax.xaxis.set_major_formatter( DateFormatter('%Y-%m-%d') )
    ax.set_ylabel(label1, color='b')
    ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M')
    ax2 = ax.twinx()
    ax2.plot_date(dates, data_y2[0:len(dates)],'r-')
    ax2.set_ylabel(label2, color='r')
    fig.autofmt_xdate()
    show()