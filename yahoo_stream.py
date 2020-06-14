import pandas as pd
import numpy as np 
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr


yf.pdr_override()

stocks= "BA"

print(stocks)

startyear=1999
startmonth=1
startday=1

start=dt.datetime(startyear,startmonth,startday)
now=dt.datetime.now()

df=pdr.get_data_yahoo(stocks,start,now)

ma=50
smaString="Sma_"+str(ma)

df[smaString]=df.iloc[:,4].rolling(window=ma).mean()

df=df.iloc[ma:]

print(df) 

# for i in df.index:
#     print(df["Adj Close"][i])
# numH=0
# numC=0
# for i in df.index:
#     if(df["Adj Close"][i]>df[smaString][i]):
#         print('The close is higher')
#         numH+=1
#     else:
#         print('The close is lower')
#         numC+=1
# print(str(numH))
# print(str(numC))