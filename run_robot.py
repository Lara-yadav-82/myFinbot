import time as true_time
import pprint
import pathlib
import operator
import pandas as pd

from datetime import datetime, timedelta
from configparser import ConfigParser

from pyrobot.robot import PyRobot
from pyrobot.indicators import Indicators

# Load Configuration
config = ConfigParser()
config.read(r'configs/config.ini')
key = config.get('main', 'key')
secret = config.get('main', 'sercet_key')
base_url= config.get('main', 'base_url')

# Initialize Trading Robot
trading_robot = PyRobot(
    api_key=key,
    sercet_key=secret,
    base_url=base_url,
)

# Create Portfolio
trading_robot_portfolio = trading_robot.create_portfolio()

# Define Multiple Positions
multi_positions = [
    {
        'asset_type': 'equity',
        'quantity': 2,
        'purchase_price': 4.00,
        'symbol': 'TSLA',
        'purchase_date': '2025-03-16'
    },
    {
        'asset_type': 'equity',
        'quantity': 2,
        'purchase_price': 4.00,
        'symbol': 'SQ',
        'purchase_date': '2025-03-16'
    }
]

# Add Positions to Portfolio
print(trading_robot_portfolio)
new_positions = trading_robot_portfolio.add_positions(positions=multi_positions)
pprint.pprint(new_positions)

# Define Historical Price Data Range
end_date = datetime.today()
start_date = end_date - timedelta(days=30)

syms =['AAPL']
historical_prices = trading_robot.grab_historical_prices(
    symbols=syms
)


# print(type(historical_prices))
# Convert Data to StockFrame
print((historical_prices))

stock_frame = trading_robot.create_stock_frame(data=historical_prices)

# Print StockFrame Head
print(stock_frame._frame)

# # Create a New Trade
# new_trade = trading_robot.create_trade(
#    symbol='F',
#    order_type="market",
#    side = 'buy',

# )

# # Set Good Till Cancel
# new_trade.good_til_cancel(cancel_time=datetime.now())

# # Modify Trade Session
# new_trade.modify_session(session='am')

# # Define Instrument for Trade (Example with MSFT)
# new_trade.instrument(
#     symbol='MSFT',
#     quantity=10,
#     asset_type='equity'
# )

# the indicator is now o
pprint.pprint(stock_frame._frame.columns)
indicator_cleint = Indicators(price_data_frame=stock_frame)
print(indicator_cleint.change_in_price())
print(indicator_cleint.rsi(period=14))
print(indicator_cleint.sma(period=4))




# indicator_cleint.set_indicator_signals(
#     indicator='rsi',
#     buy =40.0,
#     sell = 20.0,
#     condition_buy=operator.ge,
#     condition_sell=operator.le
# )

# trades_dict={
#     'MSFT':{
#         'trade_func': trading_robot.trades['long_msft'],
#         'trade_id': trading_robot.trades['long_msft'].trade_id
#     }
# }

# while True:
    
#     lastest_bars = trading_robot.get_latest_bar()

#     stock_frame.add_rows(data = lastest_bars)

#     indicator_cleint.refresh()


#     print(' = '*50)
#     print('current stock frame')
#     print('-'*50)
#     print(stock_frame.symbol_groups.tail())
#     print('-'*50)
#     print('')


#     lastest_bar_timestamp = trading_robot.stock_frame.frame.tail(1).index.get_level_value(1)

#     trading_robot.wait_till_next_next_bar(lastest_bar_timestamp = lastest_bar_timestamp)

