import alpaca_trade_api as tradeapi
from datetime import datetime
import csv

if __name__ == '__main__':
    

    # First, open the API connection
    api = tradeapi.REST(
        'API_KEY',
        'SECRET_KEY',
        'https://paper-api.alpaca.markets'
    )

    # Get account info
    account = api.get_account()

    # Check our current balance vs. our balance at the last market close
    todays_date = datetime.date(datetime.now())
    portfolio = api.list_positions()
    total_value = 0
    for position in portfolio:
        total_value += float(position.market_value)
    filename = 'Portfolio_History.csv'
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([todays_date, total_value])
