from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base.containers.orderbooks.orderbook import OrderBookData


class BitbankOrderBookData(OrderBookData):
    def __init__(
        self,
        orderbook_info: Any,
        symbol_name: str | None = None,
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(orderbook_info, has_been_json_encoded)
        self.exchange_name = "BITBANK"
        self.symbol_name = symbol_name
        self.orderbook_data: dict[str, Any] | str | None = (
            orderbook_info if has_been_json_encoded else None
        )
        self.bids: list[list[float]] = []
        self.asks: list[list[float]] = []
        self.timestamp: int | None = None
        self.local_update_time = time.time()
        self.has_been_init_data = False

    def init_data(self) -> BitbankOrderBookData:
        if not self.has_been_json_encoded:
            self.orderbook_data = (
                json.loads(self.orderbook_info) if isinstance(self.orderbook_info, str) else {}
            )
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self
        if isinstance(self.orderbook_data, dict):
            data = self.orderbook_data.get("data", self.orderbook_data)
            bids_raw = data.get("bids", []) if isinstance(data, dict) else []
            asks_raw = data.get("asks", []) if isinstance(data, dict) else []
            self.bids = [
                [float(x[0]), float(x[1])] for x in bids_raw if isinstance(x, list) and len(x) >= 2
            ]
            self.asks = [
                [float(x[0]), float(x[1])] for x in asks_raw if isinstance(x, list) and len(x) >= 2
            ]
        self.has_been_init_data = True
        return self

    def get_all_data(self) -> dict[str, Any]:
        self.init_data()
        return {
            "exchange_name": self.exchange_name,
            "symbol_name": self.symbol_name,
            "bids": self.bids,
            "asks": self.asks,
            "timestamp": self.timestamp,
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

    def get_bids(self) -> list[list[float]]:
        self.init_data()
        return self.bids

    def get_asks(self) -> list[list[float]]:
        self.init_data()
        return self.asks

    def get_best_bid(self) -> float | None:
        self.init_data()
        return self.bids[0][0] if self.bids else None

    def get_best_ask(self) -> float | None:
        self.init_data()
        return self.asks[0][0] if self.asks else None

    def get_spread(self) -> float | None:
        best_bid = self.get_best_bid()
        best_ask = self.get_best_ask()
        if best_bid is not None and best_ask is not None:
            return best_ask - best_bid
        return None


class BitbankRequestOrderBookData(BitbankOrderBookData):
    pass


class BitbankWssOrderBookData(BitbankOrderBookData):
    pass
