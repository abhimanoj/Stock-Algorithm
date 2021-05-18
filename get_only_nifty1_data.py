
import mysql.connector
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

def nifty_operation_on_highest_combined_price():

    #Data base connectors
    db = mysql.connector.connect(host="localhost", user="abhi", passwd="test",database="MERN_PLUS") 
    cursor = db.cursor(dictionary=True)

    #Store final result..
    final_list_data = []

    #Prepare query..
    query = "SELECT time, close, date, high, low FROM MERN_PLUS.BACKTEST_2020 where ticker LIKE '%BANKNIFTY-I' OR ticker LIKE '%BANKNIFTY-I.NFO'"
    fetch_query_data_1 = get_query_data(cursor, query)  
    get_date_high_low = get_high_and_low(fetch_query_data_1)

    count = 0
    is_store = False 

    is_status_1 = True
    is_status_3 = True
 
    open_price_1 = 0
    open_price_2 = 0

    set_dict_data = {}
    set_dict_data['INSTRUMENT_NAME'] = 'BANKNIFTY-I' 
    set_dict_data['DATE'] = ''

    set_dict_data['OPEN_9_15'] = 0
    set_dict_data['CLOSE_3_14'] = 0 

    set_dict_data['HIGH_IN_BANKNIFTY_I'] = 0
    set_dict_data['LOW_IN_BANKNIFTY_I'] = 0
    for i_row in fetch_query_data_1:
        time_is = str(i_row['time'])
        search_date =  i_row['date']

        #Preapre result dict...
    
        set_dict_data = get_close_value(i_row, set_dict_data)

        if is_status_1 and time_is == '9:19:59':
            open_price_1 = i_row['close']
            is_status_1 = False

        if is_status_3 and time_is == '15:14:59':
            open_price_2 = i_row['close']
            is_status_3 = False
            is_store = True
            set_dict_data['DATE'] = search_date

        if is_store:
            count = count + 1
            set_dict_data['TIME'] = time_is

            set_dict_data['OPEN_9_15'] = open_price_1
            set_dict_data['CLOSE_3_14'] = open_price_2

            open_price_1 = 0
            open_price_2 = 0

            set_dict_data['HIGH_IN_BANKNIFTY_I'] = (get_date_high_low['high'])[str(i_row['date']).replace("/","_")]
            set_dict_data['LOW_IN_BANKNIFTY_I'] = (get_date_high_low['low'])[str(i_row['date']).replace("/","_")]

            print(str(set_dict_data).replace("'","\""))
            final_list_data.append(set_dict_data)
            is_store = False
            is_status_1 = True
            is_status_3 = True
            print('2020-->',count)


            set_dict_data = {}
            set_dict_data['INSTRUMENT_NAME'] = 'BANKNIFTY-I' 
            set_dict_data['DATE'] = ''

            set_dict_data['OPEN_9_15'] = 0
            set_dict_data['CLOSE_3_14'] = 0 

            set_dict_data['HIGH_IN_BANKNIFTY_I'] = 0
            set_dict_data['LOW_IN_BANKNIFTY_I'] = 0
    
    #save file as csv..
    save_as_csv_file('nifty1_combine_2020',final_list_data)

    return str(final_list_data).replace("'","\"")

def get_high_and_low(fetch_query_data_1):

    unique_time = {}
    unique_high_local = {} 
    unique_low_local = {} 
    final_high = []
    final_low = []
    is_status = True
    high = 0
    low = 0
    for j_row in fetch_query_data_1:
        time_is = str(j_row['time'])
        date_is = str(j_row['date']).replace("/","_")
         
        if date_is not in unique_high_local:
            unique_high_local[date_is] =  high

        if date_is not in unique_low_local:
            unique_low_local[date_is] =  j_row['close']

        if float((unique_high_local[date_is])) < float(j_row['close']):
            unique_high_local[date_is] =  j_row['close']
        
        if float((unique_low_local[date_is])) > float(j_row['close']):
            unique_low_local[date_is] =  j_row['close']
   
    return {'high':unique_high_local,'low':unique_low_local}


def get_close_value(j_row, set_dict_data):

    is_status_1 = True
    is_status_3 = True
 
    open_price_1 = 0
    open_price_2 = 0
  
    
    time_is = str(j_row['time'])
    
   
    if is_status_1 and time_is == '9:19:59':
        open_price_1 = j_row['close']
        is_status_1 = False
    
    if is_status_3 and time_is == '15:14:59':
        open_price_2 = j_row['close']
        is_status_3 = False
 

    set_dict_data['OPEN_9_15'] = open_price_1
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
