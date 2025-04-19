from alpaca.trading.requests import (
    LimitOrderRequest,
    MarketOrderRequest,
    StopLimitOrderRequest,
    StopOrderRequest,
)
from enum import Enum
from alpaca.trading.enums import OrderSide, OrderType, TimeInForce

class Trade:
    def __init__(self):
        self.order = {}
        self.trade_id = ""
        self.side = ""
        self.side_opposite = ""
        self.enter_or_exit = ""
        self.enter_or_exit_opposite = ""
        self._order_response = {}
        self._triggered_added = False
        self._multi_leg = False

    def new_trade(self, symbol: str, order_type: str, side: str,
                  order_time='day', session=None, limit_price=None, stop_price=None) -> dict:
        
        if session is None:
            raise ValueError("Session object cannot be None")

        try:
            order_type_enum = OrderType(order_type)
            order_side_enum = OrderSide(side)
            time_in_force_enum = TimeInForce(order_time)
        except ValueError as e:
            raise ValueError(f"Invalid order parameters: {e}")

        order_parm = {
            "symbol": symbol,
            "notional": "30000",
            "side": order_side_enum.value,
            "type": order_type_enum.value,
            "time_in_force": time_in_force_enum.value,
        }

        if order_type_enum == OrderType.LIMIT and limit_price is not None:
            order_parm["limit_price"] = limit_price

        if order_type_enum in [OrderType.STOP, OrderType.STOP_LIMIT] and stop_price is not None:
            order_parm["stop_price"] = stop_price

        order_request = None
        if order_type_enum == OrderType.MARKET:
            order_request = MarketOrderRequest(**order_parm)
        elif order_type_enum == OrderType.LIMIT:
            order_request = LimitOrderRequest(**order_parm)
        elif order_type_enum == OrderType.STOP:
            order_request = StopOrderRequest(**order_parm)
        elif order_type_enum == OrderType.STOP_LIMIT:
            order_request = StopLimitOrderRequest(**order_parm)

        if order_request is None:
            raise ValueError(f"Invalid order_type: {order_type}")

        req_dict = order_request.model_dump()

        
        for key, value in req_dict.items():
            if isinstance(value, Enum):  # Convert enums to their string values
                req_dict[key] = value.value

        cleaned_req_dict = {k: v for k, v in req_dict.items() if v is not None}

        print(cleaned_req_dict)  # Debugging step

        res = session.submit_order(**cleaned_req_dict)
        print(res)
        return res
