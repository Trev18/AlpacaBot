import requests, json
import config
#import stream

API_KEY = 'XXXXXXXXXXX'
SECRET_KEY =  'XXXXXXXXXXXX'

BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
ORDERS_URL = "{}/v2/orders".format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID' : API_KEY, 'APCA-API-SECRET-KEY' : SECRET_KEY}
STOCK_1 = "BA"
def get_account(): 
    r = requests.get(ACCOUNT_URL, headers=HEADERS)
 
    return json.loads(r.content)

def create_order(symbol, qty, side, type, time_in_force): #order_class, take_profit.limit_price, stop_price  ): 
    data = {
        "symbol": symbol,
        "qty": qty, 
        "side": side,
        "type": type,
        "time_in_force": time_in_force,
        #"order_class" : order_class,
        #"take_profit" : take_profit,
        #"limit_price": limit_price,
        #"stop_loss" : stop_loss,
        #"stop_price": stop_price,
    }

    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)

    return json.loads(r.content)

response = create_order("MSFT", 1, "buy", "market", "gtc")
#response = create_order("BA", 1, "buy", "market", "gtc")


print(response)
