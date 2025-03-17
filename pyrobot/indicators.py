import operator
import numpy as np
import pandas as pd
from typing import List, Dict, Union, Optional, Tuple, Any
from pyrobot.stock_frame import StockFrame

class Indicators:
    def __init__(self, price_data_frame: StockFrame) -> None:
        self._stock_frame: StockFrame = price_data_frame
        self._price_groups = price_data_frame.symbol_groups
        self._current_indicators = {}
        self._indicator_signals = {}
        self._frame = self._stock_frame.frame

    def set_indicator_signals(self, indicator: str, buy: float, sell: float, condition_buy: Any, condition_sell: Any) -> None:
        """Sets buy/sell conditions for an indicator."""
        if indicator not in self._indicator_signals:
            self._indicator_signals[indicator] = {}
        self._indicator_signals[indicator]['buy'] = buy
        self._indicator_signals[indicator]['sell'] = sell
        self._indicator_signals[indicator]['buy_operator'] = condition_buy
        self._indicator_signals[indicator]['sell_operator'] = condition_sell

    def get_indicator_signals(self, indicator: Optional[str] = None) -> dict:
        """Gets stored indicator signals."""
        if indicator:
            return self._indicator_signals.get(indicator, {})
        return self._indicator_signals

    @property
    def price_data_frame(self) -> pd.DataFrame:
        """Returns the stored price DataFrame."""
        return self._frame

    @price_data_frame.setter
    def price_data_frame(self, price_data_frame: pd.DataFrame) -> None:
        """Sets a new price DataFrame."""
        self._frame = price_data_frame

    def change_in_price(self) -> pd.DataFrame:
        """Calculates daily price change."""
        column_name = 'change_in_price'
        self._current_indicators[column_name] = {'func': self.change_in_price}
        self._frame[column_name] = self._price_groups['close'].transform(lambda x: x.diff())
        return self._frame

    def rsi(self, period: int, method: str = 'wilders') -> pd.DataFrame:
        """Computes the Relative Strength Index (RSI)."""
        column_name = 'rsi'
        self._current_indicators[column_name] = {'func': self.rsi, 'args': {'period': period, 'method': method}}

        if 'change_in_price' not in self._frame.columns:
            self.change_in_price()

        self._frame['up_day'] = self._price_groups['change_in_price'].transform(lambda x: np.where(x >= 0, x, 0))
        self._frame['down_day'] = self._price_groups['change_in_price'].transform(lambda x: np.where(x < 0, -x, 0))

        self._frame['ewma_up'] = self._price_groups['up_day'].transform(lambda x: x.ewm(span=period).mean())
        self._frame['ewma_down'] = self._price_groups['down_day'].transform(lambda x: x.ewm(span=period).mean())

        relative_strength = self._frame['ewma_up'] / self._frame['ewma_down']
        self._frame[column_name] = 100 - (100 / (1 + relative_strength))

        self._frame.drop(['ewma_up', 'ewma_down', 'down_day', 'up_day', 'change_in_price'], axis=1, inplace=True)
        return self._frame

    def sma(self, period: int) -> pd.DataFrame:
        """Computes the Simple Moving Average (SMA)."""
        column_name = f'sma_{period}'
        self._current_indicators[column_name] = {'func': self.sma, 'args': {'period': period}}
        self._frame[column_name] = self._price_groups['close'].transform(lambda x: x.rolling(window=period).mean())
        return self._frame

    def ema(self, period: int, alpha: float = 0.0) -> pd.DataFrame:
        """Computes the Exponential Moving Average (EMA)."""
        column_name = f'ema_{period}'
        self._current_indicators[column_name] = {'func': self.ema, 'args': {'period': period, 'alpha': alpha}}
        self._frame[column_name] = self._price_groups['close'].transform(lambda x: x.ewm(span=period).mean())
        return self._frame

    def refresh(self) -> None:
        """Recalculates all indicators when new data is received."""
        self._price_groups = self._stock_frame.symbol_groups
        for indicator, details in self._current_indicators.items():
            func = details["func"]
            args = details.get("args", {})
            func(**args)

    def check_signals(self) -> Union[pd.DataFrame, None]:
        """Checks buy/sell signals."""
        return self._stock_frame._check_signals(indicators=self._indicator_signals)
