from typing import List, Dict, Optional
import alpaca_trade_api as tradeapi

class Portfolio:
    def __init__(self, account_number: Optional[str] = None):
        self.positions = {}
        self.position_count = 0
        self.market_value = 0.0
        self.profit_loss = 0.0
        self.risk_tolerance = 0.0
        self.account_number = account_number

    def add_position(self, symbol: str, asset_type: str, purchase_date: Optional[str], quantity: int = 0, purchase_price: float = 0.0) -> Dict:
        self.positions[symbol] = {
            'symbol': symbol,
            'quantity': quantity,
            'purchase_date': purchase_date,
            'purchase_price': purchase_price,
            'asset_type': asset_type
        }
        return self.positions

    def add_positions(self, positions: List[Dict]) -> Dict:
        if isinstance(positions, list):
            for position in positions:
                self.add_position(
                    symbol=position['symbol'],
                    asset_type=position['asset_type'],
                    purchase_date=position.get('purchase_date', None),
                    purchase_price=position.get('purchase_price', 0.0),
                    quantity=position.get('quantity', 0)
                )
            return self.positions
        else:
            raise TypeError("Positions must be a list of dictionaries.")

    def remove_position(self, symbol: str) -> tuple[bool, str]:
        if symbol in self.positions:
            del self.positions[symbol]
            return True, f"{symbol} was successfully removed."
        else:
            return False, f"{symbol} was not found."

    def in_portfolio(self, symbol: str) -> bool:
        return symbol in self.positions

    def is_profitable(self, symbol: str, current_price: float) -> bool:
        if symbol in self.positions:
            purchase_price = self.positions[symbol]['purchase_price']
            return current_price > purchase_price
        return False

    def get_market_value(self) -> float:
        total_value = 0.0
        for symbol, details in self.positions.items():
            try:
                position = self.api.get_position(symbol)
                total_value += float(position.market_value)
            except Exception:
                continue
        self.market_value = total_value
        return self.market_value

    def get_total_profit_loss(self) -> float:
        total_pl = 0.0
        for symbol, details in self.positions.items():
            try:
                position = self.api.get_position(symbol)
                total_pl += float(position.unrealized_pl)
            except Exception:
                continue
        self.profit_loss = total_pl
        return self.profit_loss
