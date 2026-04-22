from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base.containers.bars.bar import BarData


class BitbankBarData(BarData):
    def __init__(
        self,
        bar_info: Any,
        symbol_name: str | None = None,
        period: str | None = None,
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(bar_info, has_been_json_encoded)
        self.exchange_name = "BITBANK"
        self.symbol_name = symbol_name
        self.period = period
        self.bar_data: dict[str, Any] | str | None = bar_info if has_been_json_encoded else None
        self.open_time: int | None = None
        self.open_price: float | None = None
        self.high_price: float | None = None
        self.low_price: float | None = None
        self.close_price: float | None = None
        self.volume: float | None = None
        self.quote_volume: float | None = None
        self.local_update_time = time.time()
        self.has_been_init_data = False

    def init_data(self) -> BitbankBarData:
        if not self.has_been_json_encoded:
            self.bar_data = json.loads(self.bar_info) if isinstance(self.bar_info, str) else {}
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self
        if isinstance(self.bar_data, dict):
            data = self.bar_data.get("data", self.bar_data)
            candlestick = data.get("candlestick", []) if isinstance(data, dict) else []
            if candlestick and isinstance(candlestick[0], dict):
                ohlcv = candlestick[0].get("ohlcv", [])
                if isinstance(ohlcv, list) and len(ohlcv) >= 5:
                    self.open_time = int(float(ohlcv[0]) * 1000) if ohlcv[0] else 0
                    self.open_price = float(ohlcv[1]) if len(ohlcv) > 1 else 0.0
                    self.high_price = float(ohlcv[2]) if len(ohlcv) > 2 else 0.0
                    self.low_price = float(ohlcv[3]) if len(ohlcv) > 3 else 0.0
                    self.close_price = float(ohlcv[4]) if len(ohlcv) > 4 else 0.0
                    self.volume = float(ohlcv[5]) if len(ohlcv) > 5 and ohlcv[5] else 0.0
        self.has_been_init_data = True
        return self

    def get_all_data(self) -> dict[str, Any]:
        self.init_data()
        return {
            "exchange_name": self.exchange_name,
            "symbol_name": self.symbol_name,
            "period": self.period,
            "open_time": self.open_time,
            "open_price": self.open_price,
            "high_price": self.high_price,
            "low_price": self.low_price,
            "close_price": self.close_price,
            "volume": self.volume,
            "quote_volume": self.quote_volume,
            "local_update_time": self.local_update_time,
        }

    def __str__(self) -> str:
        return json.dumps(self.get_all_data())

    def __repr__(self) -> str:
        return self.__str__()

    def get_exchange_name(self) -> str:
        return self.exchange_name or ""

    def get_symbol_name(self) -> str:
        return self.symbol_name or ""

    def get_period(self) -> str | None:
        return self.period

    def get_open_time(self) -> float | int:
        return self.open_time or 0

    def get_open_price(self) -> float | int:
        return self.open_price or 0.0

    def get_high_price(self) -> float | int:
        return self.high_price or 0.0

    def get_low_price(self) -> float | int:
        return self.low_price or 0.0

    def get_close_price(self) -> float | int:
        return self.close_price or 0.0

    def get_volume(self) -> float | int:
        return self.volume or 0.0


class BitbankRequestBarData(BitbankBarData):
    pass


class BitbankWssBarData(BitbankBarData):
    pass
