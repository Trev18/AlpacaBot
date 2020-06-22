#import config
import websocket, json

def on_open(ws):
    print("opened")
    auth_data = {
        "action": "authenticate",
        "data": {"key_id": "PK1X4W2RZG5TB15V0QGM", "secret_key": "dYUMhwHitUflmI6cWNRu2sQHHwwu1LOh9y5DVBa9"}
    }

    ws.send(json.dumps(auth_data))

    listen_message = {"action": "listen", "data": {"streams": ["T.BA"]}}

    ws.send(json.dumps(listen_message))


def on_message(ws, message):
    print("received a message")
    print(message)
    volume = message.v
    open_price = message.o
    close_price = message.c
    high_price = message.h
    low_price = message.l
    average_price = message.a
    ticker = message.T
    print(open_price)
#def on_close(ws):
    #print("closed connection")

socket = "wss://data.alpaca.markets/stream"

ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message) #on_close=on_close)
ws.run_forever()
