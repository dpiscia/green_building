# -*- coding: utf-8 -*-
"""
Created on Thu Nov 08 15:05:49 2012

@author: dpiscia
"""

import datetime
from matplotlib.pyplot import figure, show
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
from numpy import arange

def plot_time_data(date_in,date_end,delta,data_y):
    ''' plot data against detetime values
    '''
    date1 = date_in
    date2 = date_end
    delta= datetime.timedelta(minutes=5)
    dates = drange(date1, date2, delta)
    fig = figure()
    ax = fig.add_subplot(111)
    ax.plot_date(dates, data_y[0:len(dates)],'-')
    ax.set_xlim( dates[0], dates[-1] )
    ax.xaxis.set_major_locator( DayLocator(5, prune='both') )
    ax.xaxis.set_minor_locator( HourLocator())
    ax.xaxis.set_minor_formatter( DateFormatter('%H') )
    ax.xaxis.set_major_formatter( DateFormatter('%Y-%m-%d') )
    
    ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M')
    
    fig.autofmt_xdate()
    show()