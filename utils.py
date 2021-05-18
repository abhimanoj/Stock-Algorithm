
import json
import os
import datetime
import calendar
import csv
import math

def get_query_data(cursor, query_is_1):

    cursor.execute(query_is_1)
    result = cursor.fetchall()

    return result

def save_as_csv_file(file_name, list_data):
    keys = list_data[0].keys()
    with open(file_name+'.csv', 'w', newline='')  as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(list_data)
    
    return True

def get_near_100(x_val):
    f1_in = int(math.ceil(x_val / 100.0)) * 100
    f1_d = f1_in - x_val

    if f1_d > 50:
        f1_in = f1_in - 100
    
    return f1_in

from datetime import datetime as dt
from datetime import date

def compare_date(source_date, ticker):
    
    status = False

    date_holder = ticker.replace("BANKNIFTY","").replace(".NFO","").replace("CE","").replace("PE","")
    date_split = source_date.split("/")
    
    date_2 =  date_holder[:2]
    month_2 = get_month_name(date_holder[:7])
    year_2 =  (date_holder[:7])[-2:]

    date_1st = date_split[1]+'/'+date_split[0]+'/'+(date_split[2])[-2:]
    date_2nd = month_2+'/'+date_2+'/'+year_2

    a = dt.strptime(date_2nd, "%m/%d/%y")
    b = dt.strptime(date_1st, "%m/%d/%y")

    days = -1
    if a >= b:

        d0 = date(int(date_split[2]), int(date_split[1]), int(date_split[0]))
        d1 = date(int(date_split[2]), int(month_2), int(date_2))
       
        delta = d1 - d0
        days = delta.days
        status = True
    else:
        status = False

    return days


def get_month_name(date_is):

    if "JAN" in str(date_is):
        return "01"
    elif "FEB" in str(date_is):
        return "02"
    elif "MAR" in str(date_is):
        return "03"
    elif "APR" in str(date_is):
        return "04"
    elif "MAY" in str(date_is):
        return "05"
    elif "JUN" in str(date_is):
        return "06"
    elif "JUL" in str(date_is):
        return "07"
    elif "AUG" in str(date_is):
        return "08"
    elif "SEP" in str(date_is):
        return "09"
    elif "OCT" in str(date_is):
        return "10"
    elif "NOV" in str(date_is):
        return "11"
    elif "DEC" in str(date_is):
        return "12"

is_status = compare_date('01/01/2020', 'BANKNIFTY30JAN2032500CE.NFO')

def get_month(date_is):
    index_val = ''
    prefix = ''
    sufix = ''
    if len(date_is) > 0:
        date_split = date_is.split("/")
        index_val = date_split[1]
        prefix = date_split[0]
        sufix = (date_split[2])[-2:]

    if str(index_val) == '01':
        return prefix+"JAN"+sufix
    elif str(index_val) == '02':
        return prefix+"FEB"+sufix
    elif str(index_val) == '03':
        return prefix+"MAR"+sufix
    elif str(index_val) == '04':
        return prefix+"APR"+sufix
    elif str(index_val) == '05':
        return prefix+"MAY"+sufix
    elif str(index_val) == '06':
        return prefix+"JUN"+sufix
    elif str(index_val) == '07':
        return prefix+"JUL"+sufix
    elif str(index_val) == '08':
        return prefix+"AUG"+sufix
    elif str(index_val) == '09':
        return prefix+"SEP"+sufix
    elif str(index_val) == '10':
        return prefix+"OCT"+sufix
    elif str(index_val) == '11':
        return prefix+"NOV"+sufix
    elif str(index_val) == '12':
        return prefix+"DEC"+sufix
