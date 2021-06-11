
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
1. Take all days:- At 9:20 am, take the close price. Round it off. Search that price in BANKNIFTY14SEP1722300PE as strike price
2. On that particular strike price find the ce and pe of open, high, low, close
3. Open:- At 9:15 am find ce and pe and add it.
4. High:- highest price of  combined ce and pe of high
5. Low:- lowest  price of  combined ce and pe of high
6. Close:- at 3:15 pm combine ce and pe
"""

def golden_ratio_data():

    #Data base connectors
    db = mysql.connector.connect(host="localhost", user="abhi", passwd="test",database="MERN_PLUS") 
    cursor = db.cursor(dictionary=True)

    #Store final result..
    final_list_data = []

    #Prepare query..
    query = "SELECT time, close, date, high, low FROM MERN_PLUS.BACKTEST_2018 where ticker LIKE '%BANKNIFTY-I' OR ticker LIKE '%BANKNIFTY-I.NFO'"
    fetch_query_data_1 = get_query_data(cursor, query)  
    get_date_high_low = get_high_and_low(fetch_query_data_1)

    count = 0
    is_store = False  
    open_price_1 = 0
    open_price_2 = 0

    set_dict_data = {}
    set_dict_data['INSTRUMENT_NAME'] = 'BANKNIFTY-I' 
    set_dict_data['DATE'] = ''
 
    set_dict_data['CLOSE_3_14'] = 0 

    set_dict_data['HIGH_IN_BANKNIFTY_I'] = 0
    set_dict_data['LOW_IN_BANKNIFTY_I'] = 0

    set_dict_data['RANGE_OF_YESTERDAY'] = 0
    set_dict_data['LOW_IN_BANKNIFTY_I'] = 0

    set_dict_data['10_MIN_HIGH'] = 0
    set_dict_data['10_MIN_LOW'] = 0
    set_dict_data['RANGE_OF_10_MIN'] = 0
    set_dict_data['RANGE_FACTOR'] = 0
    set_dict_data['GOLDEN_VALUE'] = 0
    set_dict_data['CLOSE_BUY_LEVEL'] = 0
    set_dict_data['CLOSE_SELL_LEVEL'] = 0

    previous_day = {}
    last_close = 0
    previous_day = {'_one':set_dict_data['HIGH_IN_BANKNIFTY_I'],'_two':set_dict_data['LOW_IN_BANKNIFTY_I']}

   
    for i_row in fetch_query_data_1:
        time_is = str(i_row['time'])
        search_date =  i_row['date']



        if time_is == '15:14:59':
            print(search_date,'---------------------------<<<<<<<<<<')
            set_dict_data = get_close_value(i_row, set_dict_data)
            # print(str(set_dict_data).replace("'","\""))


            count = count + 1
            set_dict_data['TIME'] = time_is

            set_dict_data['RANGE_OF_YESTERDAY'] = previous_day['_one'] - previous_day['_two']
            set_dict_data['HIGH_IN_BANKNIFTY_I'] = (get_date_high_low['high'])[str(i_row['date']).replace("/","_")]
            set_dict_data['LOW_IN_BANKNIFTY_I'] = (get_date_high_low['low'])[str(i_row['date']).replace("/","_")]    
            previous_day = {'_one':set_dict_data['HIGH_IN_BANKNIFTY_I'],'_two':set_dict_data['LOW_IN_BANKNIFTY_I']}


            set_dict_data['10_MIN_HIGH'] = (get_date_high_low['close_high'])[str(i_row['date']).replace("/","_")]
            set_dict_data['10_MIN_LOW'] = (get_date_high_low['close_low'])[str(i_row['date']).replace("/","_")]
            set_dict_data['RANGE_OF_10_MIN'] = set_dict_data['10_MIN_HIGH'] - set_dict_data['10_MIN_LOW'] 
            set_dict_data['RANGE_FACTOR'] = set_dict_data['RANGE_OF_10_MIN'] + set_dict_data['RANGE_OF_YESTERDAY'] 
            set_dict_data['GOLDEN_VALUE'] = set_dict_data['RANGE_FACTOR'] * 0.618
                        
            set_dict_data['CLOSE_BUY_LEVEL'] = set_dict_data['GOLDEN_VALUE'] + last_close
            set_dict_data['CLOSE_SELL_LEVEL'] = set_dict_data['GOLDEN_VALUE'] - last_close
            last_close = set_dict_data['CLOSE_3_14']
            set_dict_data['DATE'] = search_date


            final_list_data.append(set_dict_data)
            set_dict_data = {}
            set_dict_data['INSTRUMENT_NAME'] = 'BANKNIFTY-I' 
            set_dict_data['DATE'] = ''

            set_dict_data['CLOSE_3_14'] = 0 

            set_dict_data['HIGH_IN_BANKNIFTY_I'] = 0
            set_dict_data['LOW_IN_BANKNIFTY_I'] = 0

            set_dict_data['RANGE_OF_YESTERDAY'] = 0
            set_dict_data['LOW_IN_BANKNIFTY_I'] = 0

            set_dict_data['10_MIN_HIGH'] = 0
            set_dict_data['10_MIN_LOW'] = 0
            set_dict_data['RANGE_OF_10_MIN'] = 0
            set_dict_data['RANGE_FACTOR'] = 0
            set_dict_data['GOLDEN_VALUE'] = 0
            set_dict_data['CLOSE_BUY_LEVEL'] = 0
            set_dict_data['CLOSE_SELL_LEVEL'] = 0

       
            print('2020-->',count)


    #save file as csv..
    save_as_csv_file('golden_ratio_trading_2018',final_list_data)

    return str(final_list_data).replace("'","\"")

def get_high_and_low(fetch_query_data_1):

    unique_high_local = {} 
    unique_low_local = {} 

    unique_10_high_local = {} 
    unique_10_low_local = {} 
 
    high = 0
    low = 0
    for j_row in fetch_query_data_1:
        time_is = str(j_row['time'])
        date_is = str(j_row['date']).replace("/","_")

        #Get 10min High..
        if time_is == '9:15:59' or time_is == '9:16:59' or time_is == '9:17:59' or time_is == '9:18:59' or time_is == '9:19:59' or time_is == '9:20:59' or time_is == '9:21:59' or time_is == '9:22:59' or time_is == '9:23:59' or time_is == '9:24:59' or time_is == '9:25:59':
            
            if date_is not in unique_10_high_local:
                unique_10_high_local[date_is] =  high

            if date_is not in unique_10_low_local:
                unique_10_low_local[date_is] =  j_row['close']

            if float((unique_10_high_local[date_is])) < float(j_row['close']):
                unique_10_high_local[date_is] =  j_row['close']
            
            if float((unique_10_low_local[date_is])) > float(j_row['close']):
                unique_10_low_local[date_is] =  j_row['close']
   

         
        if date_is not in unique_high_local:
            unique_high_local[date_is] =  high

        if date_is not in unique_low_local:
            unique_low_local[date_is] =  j_row['close']

        if float((unique_high_local[date_is])) < float(j_row['close']):
            unique_high_local[date_is] =  j_row['close']
        
        if float((unique_low_local[date_is])) > float(j_row['close']):
            unique_low_local[date_is] =  j_row['close']
   
    return {'high':unique_high_local,'low':unique_low_local ,'close_high':unique_10_high_local,'close_low':unique_10_low_local}


def get_close_value(j_row, set_dict_data):

    is_status_1 = True
    is_status_3 = True
 
    open_price_1 = 0
    open_price_2 = 0
  
    
    time_is = str(j_row['time'])
    
    
    if is_status_3 and time_is == '15:14:59':
        open_price_2 = j_row['close']
        is_status_3 = False
 
 
    set_dict_data['CLOSE_3_14'] = open_price_2

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
