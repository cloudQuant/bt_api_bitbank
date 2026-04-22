from __future__ import annotations

import json
import time
from typing import TYPE_CHECKING, Any

from bt_api_base.containers.tickers.ticker import TickerData
from bt_api_base.functions.utils import from_dict_get_float

if TYPE_CHECKING:
    from bt_api_base._compat import Self


class BitbankRequestTickerData(TickerData):
    def __init__(
        self,
        ticker_info: str | dict[str, Any],
        symbol_name: str,
        asset_type: str,
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(ticker_info, has_been_json_encoded)
        self.exchange_name = "BITBANK"
        self.local_update_time = time.time()
        self.ticker_data: dict[str, Any] | None = (
            ticker_info if has_been_json_encoded and isinstance(ticker_info, dict) else None
        )
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.ticker_symbol_name: str | None = None
        self.last_price: float | None = None
        self.bid_price: float | None = None
        self.ask_price: float | None = None
        self.high_24h: float | None = None
        self.low_24h: float | None = None
        self.volume_24h: float | None = None
        self.open_24h: float | None = None
        self.timestamp: int | None = None
        self.has_been_init_data = False

    def init_data(self) -> Self:
        if not self.has_been_json_encoded:
            self.ticker_data = json.loads(self.ticker_info)
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        data = (self.ticker_data or {}).get("data", {})
        if data:
            self.ticker_symbol_name = self.symbol_name
            self.last_price = from_dict_get_float(data, "last")
            self.bid_price = from_dict_get_float(data, "buy")
            self.ask_price = from_dict_get_float(data, "sell")
            self.high_24h = from_dict_get_float(data, "high")
            self.low_24h = from_dict_get_float(data, "low")
            self.volume_24h = from_dict_get_float(data, "vol")
            self.open_24h = from_dict_get_float(data, "open")
            self.timestamp = int(from_dict_get_float(data, "timestamp") or 0)

        self.has_been_init_data = True
        return self

    def get_all_data(self) -> dict[str, Any]:
        self.init_data()
        return {
            "exchange_name": self.exchange_name,
            "symbol_name": self.symbol_name,
            "asset_type": self.asset_type,
            "ticker_symbol_name": self.ticker_symbol_name,
            "last_price": self.last_price,
            "bid_price": self.bid_price,
            "ask_price": self.ask_price,
            "high_24h": self.high_24h,
            "low_24h": self.low_24h,
            "volume_24h": self.volume_24h,
            "open_24h": self.open_24h,
            "timestamp": self.timestamp,
            "local_update_time": self.local_update_time,
        }

    def __str__(self) -> str:
        self.init_data()
        return json.dumps(self.get_all_data())

    def __repr__(self) -> str:
        return self.__str__()

    def get_exchange_name(self) -> str:
        return self.exchange_name

    def get_symbol_name(self) -> str:
        return self.symbol_name

    def get_asset_type(self) -> str:
        return self.asset_type

    def get_last_price(self) -> float | None:
        self.init_data()
        return self.last_price

    def get_bid_price(self) -> float | None:
        self.init_data()
        return self.bid_price

    def get_ask_price(self) -> float | None:
        self.init_data()
        return self.ask_price

    def get_high_24h(self) -> float | None:
        self.init_data()
        return self.high_24h

    def get_low_24h(self) -> float | None:
        self.init_data()
        return self.low_24h

    def get_volume_24h(self) -> float | None:
        self.init_data()
        return self.volume_24h

    def get_timestamp(self) -> int | None:
        self.init_data()
        return self.timestamp

    def get_local_update_time(self) -> float:
        return self.local_update_time
