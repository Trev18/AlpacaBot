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
