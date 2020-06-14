import requests, json

API_KEY = 'PK1X4W2RZG5TB15V0QGM'
SECRET_KEY =  'dYUMhwHitUflmI6cWNRu2sQHHwwu1LOh9y5DVBa9'

BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
ORDERS_URL = "{}/v2/orders".format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}

def get_account():
    r = requests.get(ACCOUNT_URL, headers=HEADERS)

    return json.loads(r.content)

def get_orders():
    r = requests.get(ORDERS_URL, headers=HEADERS)

    return json.loads(r.content)
data = {
    "symbol": "BA",
    "qty": 1,
    "side": "buy",
    "type": "market",
    "time_in_force": "gtc",
    "order_class": "bracket",
    "take_profit": {
        "limit_price": "220"
    },
    "stop_loss": {
        "stop_price": "195",
    }
}

r = requests.post(ORDERS_URL, json=data, headers=HEADERS)

response = json.loads(r.content)

print(response)