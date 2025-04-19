import pandas as pd
import alpaca_trade_api as trade_api
import alpaca

from datetime import datetime, timezone, timedelta
from typing import List, Dict, Union, Optional

import pathlib 
import json


from pyrobot.portfolio import Portfolio
from pyrobot.stock_frame import StockFrame
from pyrobot.trades import Trade
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.requests import (
    CorporateActionsRequest,
    StockBarsRequest,
    StockQuotesRequest,
    StockTradesRequest,
)
from alpaca.data.timeframe import TimeFrame 

class PyRobot:
    def __init__(
        self,
        api_key: str,
        sercet_key: str,
        base_url: str = None,
        trading_account: str = "123456",
    ) -> None:
        self.trading_account: str = trading_account
        self.client_id = api_key
        self.credentials_path = sercet_key
        self.trades: Dict[str, Trade] = {}
        self.historical_prices: Dict = {}
        self.stock_frame: Optional[StockFrame] = None
        self.session: Optional[trade_api.REST] = self._create_session()

        self._create_session()

    def _create_session(self):
        """Creates a session with Alpaca Trade API."""
        self.session = trade_api.REST(self.client_id, self.credentials_path, base_url="https://paper-api.alpaca.markets")
        print(self.session)

    def is_market_open(self) -> bool:
        """Checks if the market is currently open."""
        clock = self.session.get_clock()
        return clock.is_open

    def create_portfolio(self):
        """Initializes a new Portfolio object."""
        self.portfolio = Portfolio(account_number=self.trading_account)
        print(self.portfolio)
        return self.portfolio

    def create_trade(
        self,
        symbol,
        order_type,
        side,
        order_time='day',
        limit_price=None,
        stop_price=None,
        
    ) -> Trade:
        """Creates a trade object."""
        trade_id = symbol
        trade = Trade()

        trade.new_trade(
            symbol=symbol,
            order_type=order_type,
            side = side,
            order_time= order_time,
            limit_price=limit_price,
            stop_price=stop_price,
            session = self.session,
            )

        self.trades[trade_id] = trade
        return trade

    def grab_current_quotes(self) -> Dict:
        """Gets the latest stock prices."""
        if not self.session:
            raise ValueError("Session is not initialized. Call _create_session() first.")

        symbols = list(self.portfolio.positions.keys())
        return self.session.get_latest_trade(symbols)

    def grab_historical_prices(self, symbols=None, start=None, end=None):
        stock_historical_data_client = StockHistoricalDataClient(self.client_id,self.credentials_path)

        newprice = []

        # if not symbols:
        #     kk = self.portfolio.add_positions()  # Ensure this returns a list
        #     for i in kk:


        if not isinstance(start, datetime):
            start = datetime.now() - timedelta(days=100)

        if not isinstance(end, datetime):
            end = datetime.now()

        req = StockBarsRequest(
            symbol_or_symbols=symbols,
            timeframe=TimeFrame.Day,
            start=start,
            end=end,
            feed="iex"
        )

        temp = stock_historical_data_client.get_stock_bars(req)  # FIXED

        # print(temp)

        newprice.append(temp)  # FIXED

        print(symbols)
        self.historical_prices['aggregated'] = newprice

        return newprice

      


    def create_stock_frame(self, data) :
        """Creates a StockFrame from historical data."""
        # print(data)
        self.stock_frame = StockFrame(data=data)
        return self.stock_frame
    
    def milliseconds_since_epoch(self,dt_object):

        return int(dt_object.timestamp() * 1000)


    # def get_latest_bar(self)-> list[dict]:
    #     stock_historical_data_client = StockHistoricalDataClient(self.client_id,self.credentials_path)

    #     bar_size = self._bar_size
    #     bar_type = self._bar_type

    #     end_date = datetime.today()
    #     start_date = end_date - timedelta(minutes=15)

    #     start = str(milliseconds_since_epoch(start_date))
    #     end = str(milliseconds_since_epoch(end_date))

    #     latest_price = []

    #     for symbols in self.portfolio.positions:
    #             if not isinstance(start, datetime):
    #                 start = datetime.now() - timedelta(days=6)

    #             if not isinstance(end, datetime):
    #                 end = datetime.now()

    #             req = StockBarsRequest(
    #                 symbol_or_symbols=symbols,
    #                 timeframe=TimeFrame.Minute,
    #                 start=start,
    #                 end=end,
    #                 feed="iex"
    #             )

    #             temp = stock_historical_data_client.get_stock_bars(req)  # FIXED

    #             # print(temp)

    #             latest_price.append(temp)  # FIXED

    #             print(symbols)
    #             self.historical_prices['aggregated'] = latest_price
    #             # here i got the last bar how it done i donot know 

    # def wait_till_next_bar(self,last_bar_timestamp :pd.DatetimeIndex)-> None:

    #     last_bar_time = last_bar_timestamp.to_pydatetime()[0].replace(tzinfo = timezone.utc)
    #     next_bar_time= last_bar_time + timedelta(second = 60)  
    #     curr_bar_time = datetime.now(tz = timezone.utc)

    #     last_bar_timestamp = int(last_bar_time.timestamp())
    #     next_bar_timestamp = int(next_bar_time.timestamp())
    #     curr_bar_timestamp = int(curr_bar_time.timestamp())

    #     _time_to_wait_bar = next_bar_timestamp - last_bar_timestamp
    #     time_to_wait_now = next_bar_timestamp - curr_bar_timestamp

    #     time_true.sleep() 




             


