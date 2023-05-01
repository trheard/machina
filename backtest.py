import pandas as pd
import backtrader as bt

filename = 'eth_usdt_data.csv'

data = pd.read_csv(filename, index_col='timestamp', parse_dates=True)
data = data.rename(columns={'timestamp': 'datetime', 'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'})

class BollingerStochRSIStrategy(bt.Strategy):
    params = (('bb_period', 20), ('bb_std', 2), ('stoch_rsi_period', 14), ('stoch_rsi_smooth', 3), ('sma50_period', 50), ('sma200_period', 200))

    def __init__(self):
        self.bollinger = bt.indicators.BollingerBands(self.data.close, period=self.params.bb_period, devfactor=self.params.bb_std)
        self.rsi = bt.indicators.RSI(self.data.close, period=self.params.stoch_rsi_period)
        self.stoch_rsi = bt.indicators.StochasticFast(self.rsi, period=self.params.stoch_rsi_smooth, period_dfast=self.params.stoch_rsi_smooth)
        self.sma50 = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.sma50_period)
        self.sma200 = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.sma200_period)

    def next(self):
        if not self.position:
            if self.stoch_rsi.lines.percK[-1] < 0.2 and self.data.close[-1] < self.bollinger.lines.bot[-1] and self.sma50[-1] > self.sma200[-1]:
                self.buy()
        elif self.stoch_rsi.lines.percK[-1] > 0.8 and self.data.close[-1] > self.bollinger.lines.top[-1] and self.sma50[-1] < self.sma200[-1]:
            self.sell()

cerebro = bt.Cerebro()
cerebro.addstrategy(BollingerStochRSIStrategy)

data_feed = bt.feeds.PandasData(dataname=data)
cerebro.adddata(data_feed)

cerebro.broker.setcash(10000.0)
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

result = cerebro.run()
final_portfolio_value = cerebro.broker.getvalue()
print('Final Portfolio Value: %.2f' % final_portfolio_value)

print("\nTrade Analyzer:")
print(f"Total Trades: {trade_analyzer.total.total}")
print(f"Total Profit: {trade_analyzer.pnl.net.total:.2f}")
print(f"Total Open Trades: {trade_analyzer.total.open}")
print(f"Total Closed Trades: {trade_analyzer.total.closed}")

print("\nProfitable Trades:")
if trade_analyzer.won.total:
    print(f"Total Profitable Trades: {trade_analyzer.won.total}")
    print(f"Total Profit: {trade_analyzer.pnl.won.total:.2f}")
    print(f"Average Profit per Trade: {trade_analyzer.pnl.won.average:.2f}")
else:
    print("No profitable trades.")

print("\nLosing Trades:")
if trade_analyzer.lost.total:
    print(f"Total Losing Trades: {trade_analyzer.lost.total}")
    print(f"Total Loss: {trade_analyzer.pnl.lost.total:.2f}")
    print(f"Average Loss per Trade: {trade_analyzer.pnl.lost.average:.2f}")
else:
    print("No losing trades.")

   
