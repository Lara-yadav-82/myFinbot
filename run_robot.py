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
stock_frame = trading_robot.create_stock_frame(data=historical_prices['aggregated'][0]['AAPL'])

# Print StockFrame Head
pprint.pprint(stock_frame._frame)

# # Create a New Trade
new_trade = trading_robot.create_trade(
   symbol='AAPL',
   order_type="SIMPLE",
   side = 'BUY',

)

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
