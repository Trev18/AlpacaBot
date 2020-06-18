import alpaca_trade_api as tradeapi
from alpaca_trade_api import StreamConn
import threading
import time
import datetime
import logging
import argparse
import websocket
import json
import requests

#import yahoo_stream
#import stream

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

# API KEYS

API_KEY = "XXXXXXXXX"
API_SECRET = "XXXXXXXXXX"
BASE_URL = "https://paper-api.alpaca.markets"
ORDERS_URL = "{}/v2/orders".format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': API_SECRET}

class BracketOrder:
  ws = None
  average = None
  sumOfRanges = None
  total = None
  previous_range = None
  previous_high = None
  def __init__(self):
    self.alpaca = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')
    
  def run(self):
    socket = "wss://data.alpaca.markets/stream"

    #Connect to get streaming market data
    def on_open(ws):
        #print("opened")
        auth_data = {
        "action": "authenticate",
        "data": {"key_id": "XXXXXXXXXXX", "secret_key": "XXXXXXXXXXXX"}
        }

        ws.send(json.dumps(auth_data))

        listen_message = {"action": "listen", "data": {"streams": ["AM.BA"]}}

        ws.send(json.dumps(listen_message))

    def is_bar1(high,low,average):
        if(high - low > average):
            return True
        else return False
    def is_bar2(previous_range,high,low,previous_high):
        if(high - low > previous_range*.5 and previous_high - high < 1):
            return True
        else return False

    def on_message(ws, message):
        #print("received a message")
        print(message)
        volume = message.v
        open_price = message.o
        close_price = message.c
        high_price = message.h
        low_price = message.l
        average_price = message.a
        ticker = message.T   
        sumOfRanges += high_price - low_price
        total += 1
        average = sumOfRanges/total
        if(is_bar1(high_price, low_price, average) and is_bar2(previous_range, high_price, low_price, previous_high)):
            data = {
            "symbol": "BA",
            "qty": 1,
            "side": "buy",
            "type": "market",
            "time_in_force": "gtc",
            "order_class": "bracket",
            "take_profit": {
                "limit_price": close_price*1.02
                },
            "stop_loss": {
                "stop_price": close_price(0.98),
                }
            }
            r = requests.post(ORDERS_URL, json=data, headers=HEADERS)
            response = json.loads(r.content)
        #print(response, "order has been placed")
        previous_range = high_price - low_price
        previous_high = high_price
    def on_close(ws):
        print("")

    ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)
    ws.run_forever()
        

ls = BracketOrder()
ls.run()
