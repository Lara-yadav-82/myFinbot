from datetime import datetime
from typing import List, Optional
from alpaca.trading.client import TradingClient
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.data.historical.corporate_actions import CorporateActionsClient
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.trading.stream import TradingStream
from alpaca.data.live.stock import StockDataStream

from enum import Enum
from alpaca.trading.requests import (

    LimitOrderRequest,
    MarketOrderRequest,
    StopLimitOrderRequest,
    StopOrderRequest,

)
from alpaca.trading.enums import (
    OrderSide,
    OrderType,
    TimeInForce,
)
class Trade:
    def __init__(self):
        self.order = {}  # Stores the order details
        self.trade_id = ""  # Unique trade ID
        
        self.side = ""  # Trade direction (long/short)
        self.side_opposite = ""  # Opposite trade direction
        self.enter_or_exit = ""  # Enter or exit trade
        self.enter_or_exit_opposite = ""  # Opposite of trade action
        
        self._order_response = {}  # Store order response
        self._triggered_added = False  # Track if stop-loss is added
        self._multi_leg = False  # Check if multiple trade legs exist

    def new_trade(self, symbol: str, order_type: str, side: str,
                  order_time='day', session= None,limit_price=None,stop_price = None) -> dict:
    
        order_parm = {
            "symbol": symbol,
            "notional": 30000,  # Ensure qty is correctly formatted
            "side": OrderSide.BUY.value,
            "type": OrderType.MARKET.value,
            "time_in_force":TimeInForce.DAY.value,
            
        }
        print(order_parm)
       

        if order_type == "LIMIT" and limit_price is not None:
            order_parm["limit_price"] = limit_price

        if order_type in ["STOPORDERREQ", "STOPLIMITORDERREQ"] and stop_price is not None:
            order_parm["stop_price"] = stop_price

        if order_type == "SIMPLE":
            req = MarketOrderRequest(**order_parm)
        elif order_type == "LIMIT":
            req = LimitOrderRequest(**order_parm)
        elif order_type == "STOPORDERREQ":
            req = StopOrderRequest(**order_parm)
        elif order_type == "STOPLIMITORDERREQ":
            req = StopLimitOrderRequest(**order_parm)
        else:
            raise ValueError(f"Invalid order_type: {order_type}")

        req_dict = req.model_dump()
        for key, value in req_dict.items():
            if isinstance(value, Enum):  # Convert enums to their string values
                req_dict[key] = value.value

        print(req_dict)  # Check before sending

    # Submit the cleaned order
        cleaned_req_dict = {k: v for k, v in req_dict.items() if v is not None}

        print(cleaned_req_dict)  # Debugging step

# Submit the cleaned order
        res = session.submit_order(cleaned_req_dict) 
        
        

   
