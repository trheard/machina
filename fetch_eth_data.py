import ccxt
import pandas as pd
import time

def fetch_ohlcv_data(exchange, symbol, timeframe='1d', since=None, limit=None):
    data = []
    while True:
        try:
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=since, limit=limit)
            data += ohlcv
            break
        except Exception as e:
            print(f"Error fetching data: {e}, retrying...")
            time.sleep(exchange.rateLimit / 1000)

    return data

def save_to_csv(data, filename):
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.to_csv(filename, index=False)

if __name__ == "__main__":
    exchange = ccxt.kraken({
        'rateLimit': 1200,
        'enableRateLimit': True,
    })

    symbol = 'ETH/USD'
    timeframe = '1h'
    filename = 'eth_usdt_data.csv'

    data = fetch_ohlcv_data(exchange, symbol, timeframe)
    save_to_csv(data, filename)
    print(f"Saved historical data to {filename}")
