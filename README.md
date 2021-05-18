

This project is responsible for getting stock data based on algorithm.

# Use full Query and logic we build ###
1) Get All BANKNIFTY--> Like  (BANKNIFTY03AUG1723000PE)--single record for day one
2) Based on day one date we need to get search in ALGO-1-->Result_Data
3) In Result_Data we need to round nearest 100 of closing price. --->9:22:59(only)

we got rounded_value --> rounded_value we need to search inside All BANKNIFTY(same date)

we got the BANKNIFTY_RESULT based on rounded value -> BANKNIFTY03AUG1723000PE

we need to find out PE and CE for 9:22 and 3:10---> both closing we need to add X_9 and Y_3---> (X_9-Y_3) 

1)SELECT * FROM MERN_PLUS.BACKTEST_2016 where ticker LIKE 'BANKNIFTY%' AND ticker NOT LIKE 'BANKNIFTY-%' LIMIT 10;

+----+-----------------------------+------------+----------+------+------+------+-------+--------+-----------------+
| Id | ticker                      | date       | time     | open | high | low  | close | volume | option_interest |
+----+-----------------------------+------------+----------+------+------+------+-------+--------+-----------------+
|  0 | BANKNIFTY06OCT1617000PE.NFO | 05/10/2016 | 10:22:59 |  0.3 |  0.3 |  0.3 |   0.3 |   1040 |            2000 | 
+----+-----------------------------+------------+----------+------+------+------+-------+--------+-----------------+


2)SELECT * FROM MERN_PLUS.BACKTEST_2016 where (ticker LIKE '%BANKNIFTY-I' OR ticker LIKE '%BANKNIFTY-I.NFO') and  date='05/10/2016' and time='09:22:59';

| Id | ticker          | date       | time     | open    | high    | low   | close | volume | option_interest |
+----+-----------------+------------+----------+---------+---------+-------+-------+--------+-----------------+
|  0 | BANKNIFTY-I.NFO | 05/10/2016 | 09:22:59 | 19808.4 | 19808.4 | 19792 | 19805 |  18760 |         1988880 |
+----+-----------------+------------+----------+---------+---------+-------+-------+--------+-----------------+

--------------------
-close_round= 19800-
--------------------

3)SELECT * FROM MERN_PLUS.BACKTEST_2016 where ticker LIKE 'BANKNIFTY%' AND ticker NOT LIKE 'BANKNIFTY-%' and  date='05/10/2016' and ticker LIKE '%19800%' and time='09:22:59';

+----+-----------------------------+------------+----------+--------+--------+-------+--------+--------+-----------------+
| Id | ticker                      | date       | time     | open   | high   | low   | close  | volume | option_interest |
+----+-----------------------------+------------+----------+--------+--------+-------+--------+--------+-----------------+
|  0 | BANKNIFTY06OCT1619800CE.NFO | 05/10/2016 | 09:22:59 |   62.8 |   63.3 | 57.35 |  62.35 |  47360 |          383720 |
|  0 | BANKNIFTY06OCT1619800PE.NFO | 05/10/2016 | 09:22:59 |  124.4 | 135.55 |   124 | 126.95 |  32520 |           87320 |
|  0 | BANKNIFTY27OCT1619800CE.NFO | 05/10/2016 | 09:22:59 | 333.45 |  337.6 | 329.5 | 330.35 |    480 |           39560 |
|  0 | BANKNIFTY27OCT1619800PE.NFO | 05/10/2016 | 09:22:59 |  327.5 |    332 | 327.5 |    332 |     40 |           15240 |
+----+-----------------------------+------------+----------+--------+--------+-------+--------+--------+-----------------+

4)SELECT * FROM MERN_PLUS.BACKTEST_2016 where ticker LIKE 'BANKNIFTY%' AND ticker NOT LIKE 'BANKNIFTY-%' and  date='05/10/2016' and ticker LIKE '%19800%' and time='15:09:59';

+----+-----------------------------+------------+----------+-------+-------+--------+--------+--------+-----------------+
| Id | ticker                      | date       | time     | open  | high  | low    | close  | volume | option_interest |
+----+-----------------------------+------------+----------+-------+-------+--------+--------+--------+-----------------+
|  0 | BANKNIFTY06OCT1619800CE.NFO | 05/10/2016 | 15:09:59 | 11.25 |  11.4 |   10.4 |   10.5 |  23200 |          662000 |
|  0 | BANKNIFTY06OCT1619800PE.NFO | 05/10/2016 | 15:09:59 | 217.2 |   226 |  217.2 |  225.1 |   4960 |           39920 |
|  0 | BANKNIFTY13OCT1619800CE.NFO | 05/10/2016 | 15:09:59 |  94.2 | 97.15 |   94.2 |  96.15 |    160 |           18600 |
|  0 | BANKNIFTY27OCT1619800CE.NFO | 05/10/2016 | 15:09:59 | 259.8 | 259.8 | 257.25 | 257.25 |    160 |           54840 |
+----+-----------------------------+------------+----------+-------+-------+--------+--------+--------+-----------------+


5) 09_22_59-->
 09_22_59_close_ce = 62.35
 09_22_59_close_pe = 126.95
 09_22_59_close_ce = 330.35
 09_22_59_close_pe = 332
 

sub_of_ce_and_pe_5th = 09_22_59_close_ce + 09_22_59_close_pe

6) 15_09_5-->
 15_09_59_close_ce = 10.5
 15_09_59_close_pe = 225.1
 15_09_59_close_ce = 96.15
 15_09_59_close_pe = 257.25


sub_of_ce_and_pe_6th = 15_09_59_close_ce + 15_09_59_close_pe



7)
minus_of_5th_and_6th = sub_of_ce_and_pe_5th + sub_of_ce_and_pe_6th


1)SELECT * FROM MERN_PLUS.BACKTEST_2016 where ticker LIKE 'BANKNIFTY%' AND ticker NOT LIKE 'BANKNIFTY-%' and date='01/09/2016';
+----+-------------------------+------------+----------+------+------+------+-------+--------+-----------------+
| Id | ticker                  | date       | time     | open | high | low  | close | volume | option_interest |
+----+-------------------------+------------+----------+------+------+------+-------+--------+-----------------+
|  0 | BANKNIFTY01SEP1615800PE | 01/09/2016 | 09:35:59 |  0.1 |  0.1 |  0.1 |   0.1 |   1600 |            1960 |



2)SELECT * FROM MERN_PLUS.BACKTEST_2016 where (ticker LIKE '%BANKNIFTY-I' OR ticker LIKE '%BANKNIFTY-I.NFO') and  date='01/09/2016' and time='09:22:59';

+----+-------------+------------+----------+---------+---------+-------+----------+--------+-----------------+
| Id | ticker      | date       | time     | open    | high    | low   | close    | volume | option_interest |
+----+-------------+------------+----------+---------+---------+-------+----------+--------+-----------------+
|  0 | BANKNIFTY-I | 01/09/2016 | 09:22:59 | 19893.9 | 19893.9 | 19870 | 19879.85 |  17800 |         2907680 |
+----+-------------+------------+----------+---------+---------+-------+----------+--------+-----------------+


--------------------
-close_round= 19900-
--------------------

3)SELECT * FROM MERN_PLUS.BACKTEST_2016 where ticker LIKE 'BANKNIFTY%' AND ticker NOT LIKE 'BANKNIFTY-%' and  date='01/09/2016' and ticker LIKE '%19900%' and time='09:22:59';
+----+-------------------------+------------+----------+--------+--------+--------+--------+--------+-----------------+
| Id | ticker                  | date       | time     | open   | high   | low    | close  | volume | option_interest |
+----+-------------------------+------------+----------+--------+--------+--------+--------+--------+-----------------+
|  0 | BANKNIFTY01SEP1619900CE | 01/09/2016 | 09:22:59 |   23.2 |  23.55 |     18 |     20 |  97160 |          541640 |
|  0 | BANKNIFTY01SEP1619900PE | 01/09/2016 | 09:22:59 | 112.15 |  123.8 | 111.15 |  119.4 |  14120 |           72400 |
|  0 | BANKNIFTY08SEP1619900CE | 01/09/2016 | 09:22:59 |    100 |    100 |     95 |     95 |    200 |           11200 |
|  0 | BANKNIFTY08SEP1619900PE | 01/09/2016 | 09:22:59 | 189.55 | 190.05 | 189.55 | 190.05 |     40 |            2000 |
|  0 | BANKNIFTY29SEP1619900CE | 01/09/2016 | 09:22:59 |  308.4 |  308.4 |  297.7 |  297.7 |    960 |           22720 |
|  0 | BANKNIFTY29SEP1619900PE | 01/09/2016 | 09:22:59 | 316.95 |  329.6 | 316.95 |  329.6 |    200 |            9800 |
+----+-------------------------+------------+----------+--------+--------+--------+--------+--------+-----------------+


4)SELECT * FROM MERN_PLUS.BACKTEST_2016 where ticker LIKE 'BANKNIFTY%' AND ticker NOT LIKE 'BANKNIFTY-%' and  date='14/07/2016' and ticker LIKE '%18700%' and time='15:09:59';
 +----+-------------------------+------------+----------+--------+--------+--------+--------+--------+-----------------+
| Id | ticker                  | date       | time     | open   | high   | low    | close  | volume | option_interest |
+----+-------------------------+------------+----------+--------+--------+--------+--------+--------+-----------------+
|  0 | BANKNIFTY01SEP1619900CE | 01/09/2016 | 15:09:59 |   0.15 |   0.15 |   0.05 |    0.1 | 108520 |         1049800 |
|  0 | BANKNIFTY01SEP1619900PE | 01/09/2016 | 15:09:59 |    102 | 120.45 |    102 | 120.45 |  19720 |          112080 |
|  0 | BANKNIFTY08SEP1619900CE | 01/09/2016 | 15:09:59 |   84.3 |   84.5 |  80.25 |  81.65 |   3880 |           83080 |
|  0 | BANKNIFTY08SEP1619900PE | 01/09/2016 | 15:09:59 | 213.55 | 223.75 | 213.55 | 221.35 |    480 |           52440 |
|  0 | BANKNIFTY29SEP1619900CE | 01/09/2016 | 15:09:59 |  294.6 |  294.6 |  288.5 |  288.5 |    200 |           23800 |
|  0 | BANKNIFTY29SEP1619900PE | 01/09/2016 | 15:09:59 |    360 |    360 | 359.95 | 359.95 |     40 |           13280 |
+----+-------------------------+------------+----------+--------+--------+--------+--------+--------+-----------------+


3)SELECT * FROM MERN_PLUS.BACKTEST_2016 where ticker LIKE 'BANKNIFTY%' AND ticker NOT LIKE 'BANKNIFTY-%' and  date='29/09/2016' and ticker LIKE '%19800%' and time='09:22:59';
 
1)We nee to get all BANKNIFTY data where date is thudays.
2)



+----+-------------------------+------------+----------+-------+-------+--------+-------+--------+-----------------+
| Id | ticker                  | date       | time     | open  | high  | low    | close | volume | option_interest |
+----+-------------------------+------------+----------+-------+-------+--------+-------+--------+-----------------+
|  0 | BANKNIFTY14JUL1618700CE | 14/07/2016 | 15:09:59 | 143.4 |   144 | 142.55 |   144 |   5120 |          124560 |
|  0 | BANKNIFTY21JUL1618700CE | 14/07/2016 | 15:09:59 | 271.9 | 271.9 |    270 |   270 |    360 |           33600 |
|  0 | BANKNIFTY21JUL1618700PE | 14/07/2016 | 15:09:59 | 83.15 |    84 |  82.85 |    83 |   4320 |           84160 |
|  0 | BANKNIFTY28JUL1618700CE | 14/07/2016 | 15:09:59 |   363 | 366.5 | 362.45 | 366.5 |    680 |           59520 |
|  0 | BANKNIFTY28JUL1618700PE | 14/07/2016 | 15:09:59 | 156.4 | 156.4 | 155.05 | 156.1 |   1560 |           45880 |
+----+-------------------------+------------+----------+-------+-------+--------+-------+--------+-----------------+


BANKNIFTY	29/09/2016	19800	36.45	0.05	36.4	72800	19782.3	19150.45	631.85	3.3	9:22:59	BANKNIFTY29SEP1619800CE.NFO	29/09/2016	15:09:59	BANKNIFTY29SEP1619800CE.NFO	29/09/2016

{'INSTRUMENT_NAME': 'BANKNIFTY', 'EXPIRAY_DATE': '29/09/2016', 'STRIKE_PRICE': '', 'COMBINED_PREMIUM_AT_9_23AM': 36.45, 'COMBINED_PREMIUM_AT_3_10PM': '', 'DIFFRENCE_OF_COMBINED_PREMIUM': '', 'PERCENTAGE_OF_COMBINED_PREMIUM': '', 'FUTURE_AT_9_23AM': '19782.3', 'FUTURE_AT_3_10PM': '19150.45', 'DIFFERENCE': '631.85', 'PERCENTAGE': '3.3', 'time_is_1': '9:22:59', 'ticker_1': 'BANKNIFTY29SEP1619800CE.NFO', 'date_1': '29/09/2016'}


pe=53.65
ce=36.45



# Some Query related to logic

SELECT * FROM MERN_PLUS.BACKTEST_2020 where (ticker LIKE '%BANKNIFTY-I' OR ticker LIKE '%BANKNIFTY-I.NFO')'

SELECT ticker, date, time, open, close FROM MERN_PLUS.BACKTEST_2020 where ticker LIKE 'BANKNIFTY%' AND  date='02/01/2020' AND ticker NOT LIKE 'BANKNIFTY-%' and ticker LIKE '%32600%' and time='15:14:59'


SELECT ticker, date, time, open, close FROM MERN_PLUS.BACKTEST_2020 where ticker LIKE 'BANKNIFTY%' AND  date='01/01/2020'  AND ticker NOT LIKE 'BANKNIFTY-%'  and ticker LIKE '%32300%';
 
