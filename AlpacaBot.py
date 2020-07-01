import alpaca_trade_api as tradeapi
from alpaca_trade_api import StreamConn
import threading
import time
import datetime as dt
import logging
import argparse
import websocket
import json
import requests
import pandas as pd
import numpy as np 
import yfinance as yf
from pandas_datareader import data as pdr
import ta

historical_5minute = None
slowMa = None
fastMa = None

yf.pdr_override()

stocks= "BA"

startyear=2010
startmonth=1
startday=1

start=dt.datetime(startyear,startmonth,startday)
now=dt.datetime.now()

df=pdr.get_data_yahoo(stocks,start,now)



# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

# API KEYS

API_KEY = "PK1X4W2RZG5TB15V0QGM"
API_SECRET = "dYUMhwHitUflmI6cWNRu2sQHHwwu1LOh9y5DVBa9"
BASE_URL = "https://paper-api.alpaca.markets"
ORDERS_URL = "{}/v2/orders".format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': API_SECRET}

class BracketOrder:
  ws = None
  average = None
  sumOfRanges = 0
  total = 0
  previous_range = 0
  previous_high = 0
  
  #Calculate Simple Moving Average
  def calculateSMA(self, candles, update):
    for entry in candles:
        print(entry.c)
    open_time = [entry.t for entry in candles]
    close = [entry.c for entry in candles]
    print(close)
    close_array = pd.Series(np.asarray(close))
    inTrade = False
    #Calculate SMA
    self.slowMa = ta.trend.sma_indicator(close_array, n=20, fillna=True)
    self.fastMa = ta.trend.sma_indicator(close_array, n=5, fillna=True) 
    #Delete first SMA value to make room for latest
    if (update):
        self.fivemin_candles.pop(0)
    print(self.fastMa)  


  def __init__(self):
    self.alpaca = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')
    fivemin_candles = None
    slowMa = None
    fastMa = None 
    barset = self.alpaca.get_barset('BA', '5Min', limit=5)
    self.fivemin_candles = barset['BA']
    self.calculateSMA( self.fivemin_candles,False)

             
  def run(self):
    socket = "wss://data.alpaca.markets/stream"

    #Connect to get streaming market data
    def on_open(ws):
        #print("opened")
        auth_data = {
        "action": "authenticate",
        "data": {"key_id": "PK1X4W2RZG5TB15V0QGM", "secret_key": "dYUMhwHitUflmI6cWNRu2sQHHwwu1LOh9y5DVBa9"}
        }

        ws.send(json.dumps(auth_data))

        #AM = Subscribe to minute .* Stock symbol e.g AM.BA
        listen_message = {"action": "listen", "data": {"streams": ["AM.BA", "AM.MSFT"]}}
        
        
        ws.send(json.dumps(listen_message))

    def is_bar1(high,low,average):
        if(high - low > average):
            return True
        else: return False
    def is_bar2(previous_range,high,low,previous_high):
        if(high - low > previous_range*.5 and previous_high - high < 1):
            return True
        else: return False
    #On Message, ever minute bar data we get for the stock we subscribe to 
    def on_message(ws, message):
        #Convert our message to dictionary
        convertedMessage = json.loads(message)
        try: 
            #Store vars for candlestick
            volume = convertedMessage["data"]["v"]
            open_price = convertedMessage["data"]["o"]
            close_price = convertedMessage["data"]["c"]
            high_price = convertedMessage["data"]["h"]
            low_price = convertedMessage["data"]["l"]
            average_price = convertedMessage["data"]["a"]
            ticker = convertedMessage["data"]["T"]  
            #TODO: Confirm
            time = convertedMessage["data"]["t"]  
            print("Current Volume : ", volume)
            print("Current Open Price : ", open_price)
            print("Current Close Price : ", close_price)
            print("Current High Price : ", high_price)
            print("Current Low : ", low_price)
            print("Current Average : ", average_price)
            print("Symbol : ", ticker)
            self.fivemin_candles.append([{'t': time, 'c':close_price}])
            self.calculateSMA(self.fivemin_candles, True)
            # if(is_bar1(high_price, low_price, average) and is_bar2(self.previous_range, high_price, low_price, self.previous_high)):
            #     data = {
            #     "symbol": "BA",
            #     "qty": 1,
            #     "side": "buy",
            #     "type": "market",
            #     "time_in_force": "gtc",
            #     "order_class": "bracket",
            #     "take_profit": {
            #         "limit_price": close_price*1.02
            #         },
            #     "stop_loss": {
            #         "stop_price": close_price*0.98,
            #         }
            #     }
            #     r = requests.post(ORDERS_URL, json=data, headers=HEADERS)
            #     response = json.loads(r.content)
            # #print(response, "order has been placed")
            # previous_range = high_price - low_price
            # previous_high = high_price
        except:
            pass
    def on_close(ws):
        print("Market is closed")

    ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)
    ws.run_forever()
        

ls = BracketOrder()
ls.run()
