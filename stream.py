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

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

# API KEYS

API_KEY = "XXXXXXXXXXXXXXXXXX"
API_SECRET = "XXXXXXXXXXXXXXXXXX"
BASE_URL = "https://paper-api.alpaca.markets"
ORDERS_URL = "{}/v2/orders".format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': API_SECRET}
import websocket, json

class live_stream:
  ws = None
  
  def __init__(self):
    self.alpaca = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')
    
  def run(self):
    socket = "wss://data.alpaca.markets/stream"

    #Connect to get streaming market data
    def on_open(ws):
        #print("opened")
        auth_data = {
        "action": "authenticate",
        "data": {"key_id": "XXXXXXXXXXX", "secret_key": "XXXXXXXXXXXXXXX"}
        }

        ws.send(json.dumps(auth_data))

        #AM = Subscribe to minute .* Stock symbol e.g AM.BA
        listen_message = {"action": "listen", "data": {"streams": ["AM.BA", "AM.MSFT"]}}
        
        
        ws.send(json.dumps(listen_message))

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
            print("Current Volume : ", volume)
            print("Current Open Price : ", open_price)
            print("Current Close Price : ", close_price)
            print("Current High Price : ", high_price)
            print("Current Low : ", low_price)
            print("Current Average : ", average_price)
            print("Symbol : ", ticker)
           
        except:
            pass
    def on_close(ws):
        print("Market is closed")

    ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)
    ws.run_forever()
        

ls = live_stream()
ls.run()
