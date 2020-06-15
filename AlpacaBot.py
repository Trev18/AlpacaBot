import alpaca_trade_api as tradeapi
from alpaca_trade_api import StreamConn
import threading
import time
import datetime
import logging
import argparse
import websocket, json
import requests
# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

# API KEYS

API_KEY = "XXXXXXXXX"
API_SECRET = "XXXXXXXXXXX"
BASE_URL = "https://paper-api.alpaca.markets"
ORDERS_URL = "{}/v2/orders".format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': API_SECRET}

class BracketOrder:
  ws = None
  def __init__(self):
    self.alpaca = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')
    
  def run(self):
    socket = "wss://data.alpaca.markets/stream"

    #Connect to get streaming market data
    def on_open(ws):
        print("opened")
        auth_data = {
        "action": "authenticate",
        "data": {"key_id": "XXXXXXXXXXXX", "secret_key": "XXXXXXXXXXXXX"}
        }

        ws.send(json.dumps(auth_data))

        listen_message = {"action": "listen", "data": {"streams": ["AM.BA"]}}

        ws.send(json.dumps(listen_message))


    def on_message(ws, message):
        print("received a message")
        print(message)
        data = {
        "symbol": "BA",
        "qty": 1,
        "side": "buy",
        "type": "market",
        "time_in_force": "gtc",
        "order_class": "bracket",
        "take_profit": {
            "limit_price": "195"
            },
        "stop_loss": {
            "stop_price": "182",
            }
        }   

        r = requests.post(ORDERS_URL, json=data, headers=HEADERS)
        response = json.loads(r.content)
        print(response, "order has been placed")
    def on_close(ws):
        print("closed connection")

    ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)
    ws.run_forever()
        

ls = BracketOrder()
ls.run()
