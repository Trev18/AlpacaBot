import pandas as pd
import numpy as np 
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr
import requests
from pandas.util.testing import assert_frame_equal
yf.pdr_override()
start = dt.datetime(2015,12,1)
now = dt.datetime.now()
stock1 = 'BA'
stock2 = 'AAL'
stock3 ='MSFT'
stock4 = 'JPM'
stocks = ["BA", "AAL", "JPM"]

for stock in stocks:
    print(stock)
    df =pdr.get_data_yahoo(stock, start, now)

    dfmonth = df.groupby(pd.Grouper(freq="M"))["High"].max()

    for index, value in dfmonth.items():
        print(round(value, 2))
