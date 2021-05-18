
import flask
from flask import request
import mysql.connector
import json
import os
import pandas as pd
import datetime
import calendar
import csv
import math
from utils import *



"""
1) Mention ATM combined premium at 9.20 AM
2) Also write down day high, day Low and day close of combined  premium  of the strike price mentioned in point 1.
3) Then mention the ATM combined premium at 3.28 PM 
4) last, please mention the day open, high, low and close for Bank Nifty -I
5) please run this query on all days from 2016 to 2020.
   ATM combined premium means the total value of CE and PE for the strike price around which the Bank Nifty-I is reflecting at that point of time.
   Eg, if BN is at 29943 at 9.20AM
Then ATM Strike price will be 29900 (nearest to multiple of 100), so combined premium will be addition of 29900 CE and 29900 PE at 9.20 AM.

--->

1. Take all days:- At 9:20 am, take the close price. Round it off. Search that price in BANKNIFTY14SEP1722300PE as strike price
2. On that particular strike price find the ce and pe of open, high, low, close
3. Open:- At 9:15 am find ce and pe and add it.
4. High:- highest price of  combined ce and pe of high
5. Low:- lowest  price of  combined ce and pe of high
6. Close:- at 3:15 pm combine ce and pe
"""

def operation_on_highest_combined_price():

    #Data base connectors
    db = mysql.connector.connect(host="localhost", user="abhi", passwd="test",database="MERN_PLUS") 
    cursor = db.cursor(dictionary=True)

    #Store final result..
    final_list_data = []

    #Prepare query..
    query = "SELECT time, close, date FROM MERN_PLUS.BACKTEST_2020 where ticker LIKE '%BANKNIFTY-I' OR ticker LIKE '%BANKNIFTY-I.NFO'"
    fetch_query_data_1 = get_query_data(cursor, query)  

    count = 0
    is_store = False 
     #Preapre result dict...
    set_dict_data = {}
    set_dict_data['INSTRUMENT_NAME'] = 'BANKNIFTY'
    set_dict_data['DATE'] = ''

    set_dict_data['STRIKE_PRICE_AT_9_20'] = 0
    set_dict_data['OPEN_AT_9_19_SE_9_15'] = 0
    set_dict_data['CLOSE_AT_9_19_SE_3_14'] = 0
    set_dict_data['HIGH_AT_9_19'] = 0
    set_dict_data['LOW_AT_9_19'] = 0

    set_dict_data['STRIKE_PRICE_AT_3_15'] = 0
    set_dict_data['OPEN_AT_3_14_SE_9_15'] = 0
    set_dict_data['CLOSE_AT_3_14_SE_3_14'] = 0
    for i_row in fetch_query_data_1:
        i_time_is = str(i_row['time'])
        close_price = get_near_100(float(i_row['close']))
        search_date =  i_row['date']


       

        
        if i_time_is == '9:19:59':
            set_dict_data['STRIKE_PRICE_AT_9_20'] = close_price
            query = "SELECT ticker, date, time, open, close, low, high FROM MERN_PLUS.BACKTEST_2020 where ticker LIKE 'BANKNIFTY%' AND  date='"+str(search_date)+"'  AND ticker NOT LIKE 'BANKNIFTY-%'  and ticker LIKE '%"+str(close_price)+"%'"
            fetch_query_data_2 = get_query_data(cursor, query)  
            set_dict_data = get_open_value(fetch_query_data_2, set_dict_data)
            set_dict_data = get_high_and_low(fetch_query_data_2, set_dict_data)

        if i_time_is == '15:14:59':
            set_dict_data['STRIKE_PRICE_AT_3_15'] = close_price
            is_store = True
            query = "SELECT ticker, date, time, open, close FROM MERN_PLUS.BACKTEST_2020 where ticker LIKE 'BANKNIFTY%' AND  date='"+str(search_date)+"'  AND ticker NOT LIKE 'BANKNIFTY-%'  and ticker LIKE '%"+str(close_price)+"%'"
            fetch_query_data_2 = get_query_data(cursor, query)  
            set_dict_data = get_close_value(fetch_query_data_2, set_dict_data)
            set_dict_data['DATE'] = search_date

            

      
        if is_store:
            count = count + 1
            set_dict_data['TIME'] = i_time_is
            final_list_data.append(set_dict_data)
            is_store = False

                #Preapre result dict...
            set_dict_data = {}
            set_dict_data['INSTRUMENT_NAME'] = 'BANKNIFTY'
            set_dict_data['DATE'] = search_date

            set_dict_data['STRIKE_PRICE_AT_9_20'] = 0
            set_dict_data['OPEN_AT_9_19_SE_9_15'] = 0
            set_dict_data['CLOSE_AT_9_19_SE_3_14'] = 0
            set_dict_data['HIGH_AT_9_19'] = 0
            set_dict_data['LOW_AT_9_19'] = 0

            set_dict_data['STRIKE_PRICE_AT_3_15'] = 0
            set_dict_data['OPEN_AT_3_14_SE_9_15'] = 0
            set_dict_data['CLOSE_AT_3_14_SE_3_14'] = 0
            print('2020-->',count)
      
    #save file as csv..
    save_as_csv_file('hi_combine_2020',final_list_data)

    return str(final_list_data).replace("'","\"")

def get_high_and_low(fetch_query_data_2, set_dict_data):

    last_days_1 = -1
    last_days_2 = -1
    unique_time = {}
    unique_time_local_ce = {}
    unique_time_local_pe = {}
    final_high = []
    final_low = []
    is_status = True
    for j_row in fetch_query_data_2:

        time_is = str(j_row['time'])
        
        opening_stike_price = j_row['ticker'].replace("BANKNIFTY","").replace(".NFO","")
        last_char = opening_stike_price[-2:]

        get_days = compare_date(j_row['date'], j_row['ticker'])

        if time_is not in unique_time_local_ce:
            tmp_dict = {'days':-1,'high': 0,'low':0}
            unique_time_local_ce[time_is] =  tmp_dict

        if time_is not in unique_time_local_pe:
            tmp_dict = {'days':-1,'high': 0,'low':0}
            unique_time_local_pe[time_is] =  tmp_dict


        if 'CE' == last_char and get_days >= 0:

            if get_days < (unique_time_local_ce[time_is])['days'] or (unique_time_local_ce[time_is])['days'] == -1:
                tmp_dict = {'days':get_days,'high': j_row['close'],'low':j_row['close']}
                unique_time_local_ce[time_is] =  tmp_dict

        if 'PE' == last_char and get_days >= 0:
            
            if get_days < (unique_time_local_pe[time_is])['days'] or (unique_time_local_pe[time_is])['days'] == -1:
                tmp_dict = {'days':get_days,'high': j_row['close'],'low':j_row['close']}
                unique_time_local_pe[time_is] =  tmp_dict
 

    
        high = (unique_time_local_pe[time_is])['high'] + (unique_time_local_ce[time_is])['high']
        low = (unique_time_local_pe[time_is])['low'] + (unique_time_local_ce[time_is])['low']
        
        final_high.append(high)
        final_low.append(low)


    set_dict_data['HIGH_AT_9_19'] = max(final_high)
    set_dict_data['LOW_AT_9_19'] = min(final_low)
 
    return set_dict_data


def get_close_value(fetch_query_data_2, set_dict_data):

    is_status_1 = True
    is_status_2 = True
 

    is_status_3 = True
    is_status_4 = True
 
    ce_open_price_1 = 0
    pe_open_price_1 = 0
 
    ce_open_price_2 = 0
    pe_open_price_2 = 0
 
    for j_row in fetch_query_data_2:

        time_is = str(j_row['time'])
        
        opening_stike_price = j_row['ticker'].replace("BANKNIFTY","").replace(".NFO","")
        last_char = opening_stike_price[-2:]
    
        if 'CE' == last_char and is_status_1 and time_is == '9:19:59':
            ce_open_price_1 = j_row['close']
            is_status_1 = False

        if 'PE' == last_char and is_status_2 and time_is == '9:19:59':
            pe_open_price_1 = j_row['close']
            is_status_2 = False
     
        if 'CE' == last_char and is_status_3 and time_is == '15:14:59':
            ce_open_price_2 = j_row['close']
            is_status_3 = False

        if 'PE' == last_char and is_status_4 and time_is == '15:14:59':
            pe_open_price_2 = j_row['close']
            is_status_4 = False

    set_dict_data['OPEN_AT_9_19_SE_9_15'] = ce_open_price_1 + pe_open_price_1
    set_dict_data['CLOSE_AT_9_19_SE_3_14'] = ce_open_price_2 + pe_open_price_2

    return set_dict_data

def get_open_value(fetch_query_data_2, set_dict_data):

    is_status_1 = True
    is_status_2 = True
 
    is_status_3 = True
    is_status_4 = True
 
    ce_open_price_1 = 0
    pe_open_price_1 = 0
 
    ce_open_price_2 = 0
    pe_open_price_2 = 0

    for j_row in fetch_query_data_2:

        time_is = str(j_row['time'])
        
        opening_stike_price = j_row['ticker'].replace("BANKNIFTY","").replace(".NFO","")
        last_char = opening_stike_price[-2:]
    
        if 'CE' == last_char and is_status_1 and time_is == '9:19:59':
            ce_open_price_1 = j_row['close']
            is_status_1 = False

        if 'PE' == last_char and is_status_2 and time_is == '9:19:59':
            pe_open_price_1 = j_row['close']
            is_status_2 = False

        if 'CE' == last_char and is_status_3 and time_is == '15:14:59':
            ce_open_price_2 = j_row['close']
            is_status_3 = False

        if 'PE' == last_char and is_status_4 and time_is == '15:14:59':
            pe_open_price_2 = j_row['close']
            is_status_4 = False

    set_dict_data['OPEN_AT_3_14_SE_9_15'] = ce_open_price_1 + pe_open_price_1
    set_dict_data['CLOSE_AT_3_14_SE_3_14'] = ce_open_price_2 + pe_open_price_2

    return set_dict_data
