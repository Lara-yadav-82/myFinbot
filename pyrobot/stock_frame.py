import numpy as np
import pandas as pd

from datetime import datetime
from typing import List, Dict, Union
from pandas.core.groupby import DataFrameGroupBy
from pandas.core.window import RollingGroupby

class StockFrame:
    
    def __init__(self, data) -> None:
        self._data = data
        # print(data)
        self._frame: pd.DataFrame = self.create_frame()
        self._symbol_groups: DataFrameGroupBy = None
        self._symbol_rolling_groups: RollingGroupby = None

    @property
    def frame(self) -> pd.DataFrame:
        """Returns the stock data frame."""
        return self._frame

    def create_frame(self):
        

        
        raw_data = self._data[0]['AAPL']

        # Convert list of tuples to list of flat dictionaries
        cleaned_data = [dict(entry) for entry in raw_data]

        # Create DataFrame
        df = pd.DataFrame(cleaned_data)

        # Optional: Format timestamp and sort
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.sort_values(by='timestamp', inplace=True)
        df.reset_index(drop=True, inplace=True)

        return df


    def symbol_groups(self) -> DataFrameGroupBy:
        """Groups the DataFrame by 'symbol'."""
        self._symbol_groups = self._frame.groupby(
            by='symbol',
            as_index=False,
            sort=True
        )
        return self._symbol_groups

    def symbol_rolling_groups(self, size: int) -> RollingGroupby:
        """Creates rolling groups for technical analysis indicators."""
        if self._symbol_groups is None:
            self.symbol_groups()
        self._symbol_rolling_groups = self._symbol_groups.rolling(size)
        return self._symbol_rolling_groups

    # def create_frame(self) -> pd.DataFrame:
    #     """Creates a DataFrame from the raw data and formats it."""
    #     all_records = []

    #     for entry in self._data:  # self._data is a list
    #         data_dict = entry['data']  # Each dict has a 'data' key
    #         for symbol, bars in data_dict.items():
    #             for bar in bars:
    #                 bar_copy = dict(bar)  # Make sure it's mutable
    #                 bar_copy['symbol'] = symbol
    #                 all_records.append(bar_copy)

    # # Create DataFrame
    #     df = pd.DataFrame(all_records)


        
    #     print(df)
    #     price_df = self._parse_datetime_column(df)
    #     # price_df = self._set_multi_index(price_df)
    #     return price_df

    def _parse_datetime_column(self, price_df: pd.DataFrame) -> pd.DataFrame:
        """Converts the 'datetime' column to proper timestamp format."""
        price_df.rename(columns={'timestamp': 'datetime'}, inplace=True)
        return price_df

    def _set_multi_index(self, price_df: pd.DataFrame) -> pd.DataFrame:
        """Sets 'symbol' and 'datetime' as a multi-index."""
        
        
        return price_df.set_index(keys=['symbol','datetime'])

    def add_rows(self, data: Dict) -> None:
        """Adds new rows to the existing DataFrame."""
        column_names = ['open', 'close', 'high', 'low', 'volume']

        for symbol in data:
            time_stamp = pd.to_datetime(
                data[symbol]['quoteTimeInLong'],
                unit='ms',
                origin='unix'
            )

            # Define row index
            row_id = (symbol, time_stamp)

            # Define row values
            row_values = [
                data[symbol]['openPrice'],
                data[symbol]['closePrice'],
                data[symbol]['highPrice'],
                data[symbol]['lowPrice'],
                data[symbol]['askSize'] + data[symbol]['bidSize']
            ]

            # Create a Series for the new row
            new_row = pd.Series(data=row_values, index=column_names)

            # Add row to DataFrame
            self._frame.loc[row_id, column_names] = new_row.values
            self._frame.sort_index(inplace=True)

    def do_indicators_exist(self, column_names: List[str]) -> bool:
        """Checks if specified indicator columns exist."""
        return all(col in self._frame.columns for col in column_names)
    

    def _check_signals(self,indicators:dict)->Union[pd.Series,None]:
        pass