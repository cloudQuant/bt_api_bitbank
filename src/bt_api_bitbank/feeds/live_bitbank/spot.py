from __future__ import annotations

from datetime import datetime
from typing import Any

from bt_api_base.feeds.capability import Capability

from bt_api_bitbank.feeds.live_bitbank.request_base import BitbankRequestData


class BitbankRequestDataSpot(BitbankRequestData):
    @classmethod
    def _capabilities(cls) -> set[Capability]:
        return {
            Capability.GET_TICK,
            Capability.GET_DEPTH,
            Capability.GET_KLINE,
            Capability.GET_EXCHANGE_INFO,
            Capability.GET_BALANCE,
            Capability.GET_ACCOUNT,
            Capability.MAKE_ORDER,
            Capability.CANCEL_ORDER,
        }

    def __init__(self, data_queue: Any = None, **kwargs: Any) -> None:
        super().__init__(data_queue, **kwargs)
        self.exchange_name = kwargs.get("exchange_name", "BITBANK___SPOT")

    def _normalize_pair(self, symbol: str) -> str:
        symbol = symbol.upper().replace("/", "_").replace("-", "_")
        return symbol.lower()

    def _get_tick(
        self, symbol: str, extra_data: dict[str, Any] | None = None, **kwargs: Any
    ) -> tuple[str, dict[str, Any] | None, dict[str, Any]]:
        pair = self._normalize_pair(symbol)
        path = f"GET /{pair}/ticker"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "request_type": "get_tick",
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_tick_normalize_function,
            }
        )
        return path, None, extra_data

    @staticmethod
    def _get_tick_normalize_function(
        input_data: dict[str, Any], extra_data: Any
    ) -> tuple[list[Any], bool]:
        if not input_data:
            return [], False
        data = input_data.get("data", {})
        if data and input_data.get("success") == 1:
            return [data], True
        return [], False

    def get_tick(self, symbol: str, extra_data: dict[str, Any] | None = None, **kwargs: Any) -> Any:
        path, params, extra = self._get_tick(symbol, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra)

    def async_get_tick(
        self, symbol: str, extra_data: dict[str, Any] | None = None, **kwargs: Any
    ) -> None:
        path, params, extra = self._get_tick(symbol, extra_data, **kwargs)
        self.submit(
            self.async_request(path, params=params, extra_data=extra), callback=self.async_callback
        )

    def _get_depth(
        self,
        symbol: str,
        count: int = 20,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> tuple[str, dict[str, Any] | None, dict[str, Any]]:
        pair = self._normalize_pair(symbol)
        path = f"GET /{pair}/depth"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "request_type": "get_depth",
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_depth_normalize_function,
            }
        )
        return path, None, extra_data

    @staticmethod
    def _get_depth_normalize_function(
        input_data: dict[str, Any], extra_data: Any
    ) -> tuple[list[Any], bool]:
        if not input_data:
            return [], False
        data = input_data.get("data", {})
        if data and input_data.get("success") == 1:
            return [data], True
        return [], False

    def get_depth(
        self,
        symbol: str,
        count: int = 20,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        path, params, extra = self._get_depth(symbol, count, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra)

    def async_get_depth(
        self,
        symbol: str,
        count: int = 20,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        path, params, extra = self._get_depth(symbol, count, extra_data, **kwargs)
        self.submit(
            self.async_request(path, params=params, extra_data=extra), callback=self.async_callback
        )

    def _get_kline(
        self,
        symbol: str,
        period: str,
        count: int = 20,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> tuple[str, dict[str, Any] | None, dict[str, Any]]:
        pair = self._normalize_pair(symbol)
        candle_type = self._params.kline_periods.get(period, period)
        long_periods = ["4hour", "8hour", "12hour", "1day", "1week", "1month"]
        if candle_type in long_periods:
            date_str = datetime.now().strftime("%Y")
        else:
            date_str = datetime.now().strftime("%Y%m%d")

        path = f"GET /{pair}/candlestick/{candle_type}/{date_str}"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "request_type": "get_kline",
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "period": period,
                "normalize_function": self._get_kline_normalize_function,
            }
        )
        return path, None, extra_data

    @staticmethod
    def _get_kline_normalize_function(
        input_data: dict[str, Any], extra_data: Any
    ) -> tuple[list[Any], bool]:
        if not input_data:
            return [], False
        data = input_data.get("data", {})
        if data and input_data.get("success") == 1:
            candlestick = data.get("candlestick", [])
            if candlestick and len(candlestick) > 0:
                ohlcv = candlestick[0].get("ohlcv", [])
                if ohlcv:
                    return [{"ohlcv": ohlcv}], True
        return [], False

    def get_kline(
        self,
        symbol: str,
        period: str,
        count: int = 20,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        path, params, extra = self._get_kline(symbol, period, count, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra)

    def async_get_kline(
        self,
        symbol: str,
        period: str = "1m",
        count: int = 20,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        path, params, extra = self._get_kline(symbol, period, count, extra_data, **kwargs)
        self.submit(
            self.async_request(path, params=params, extra_data=extra), callback=self.async_callback
        )

    def _get_exchange_info(
        self, extra_data: dict[str, Any] | None = None, **kwargs: Any
    ) -> tuple[str, dict[str, Any] | None, dict[str, Any]]:
        path = "GET /spot/pairs"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "request_type": "get_exchange_info",
                "symbol_name": "",
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_exchange_info_normalize_function,
            }
        )
        return path, None, extra_data

    @staticmethod
    def _get_exchange_info_normalize_function(
        input_data: Any, extra_data: Any
    ) -> tuple[list[Any], bool]:
        if not input_data:
            return [], False
        data = input_data.get("data", {})
        if data and input_data.get("success") == 1:
            pairs = data.get("pairs", data) if isinstance(data, dict) else data
            return pairs if isinstance(pairs, list) else [pairs], True
        return [], False

    def get_exchange_info(self, extra_data: dict[str, Any] | None = None, **kwargs: Any) -> Any:
        path, params, extra = self._get_exchange_info(extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra)

    def _make_order(
        self,
        symbol: str,
        volume: Any,
        price: Any,
        order_type: str,
        offset: str = "open",
        post_only: bool = False,
        client_order_id: str | None = None,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> tuple[str, dict[str, Any], dict[str, Any]]:
        path = "POST /v1/user/spot/order"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "exchange_name": self.exchange_name,
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "request_type": "make_order",
            }
        )
        params = {
            "pair": self._normalize_pair(symbol),
            "amount": str(volume),
            "price": str(price),
            "side": offset if offset in ("buy", "sell") else "buy",
            "type": order_type,
        }
        return path, params, extra_data

    def make_order(
        self,
        symbol: str,
        volume: Any,
        price: Any,
        order_type: str,
        offset: str = "open",
        post_only: bool = False,
        client_order_id: str | None = None,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        path, params, extra = self._make_order(
            symbol,
            volume,
            price,
            order_type,
            offset,
            post_only,
            client_order_id,
            extra_data,
            **kwargs,
        )
        return self.request(path, body=params, extra_data=extra)

    def _cancel_order(
        self,
        symbol: str,
        order_id: str | int,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> tuple[str, dict[str, Any], dict[str, Any]]:
        path = "POST /v1/user/spot/cancel_order"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "exchange_name": self.exchange_name,
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "request_type": "cancel_order",
                "order_id": order_id,
            }
        )
        params = {"pair": self._normalize_pair(symbol), "order_id": order_id}
        return path, params, extra_data

    def cancel_order(
        self,
        symbol: str,
        order_id: str | int,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        path, params, extra = self._cancel_order(symbol, order_id, extra_data, **kwargs)
        return self.request(path, body=params, extra_data=extra)

    def _query_order(
        self,
        symbol: str,
        order_id: str | int,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> tuple[str, dict[str, Any], dict[str, Any]]:
        path = "GET /v1/user/spot/order"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "exchange_name": self.exchange_name,
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "request_type": "query_order",
                "order_id": order_id,
            }
        )
        params = {"pair": self._normalize_pair(symbol), "order_id": order_id}
        return path, params, extra_data

    def query_order(
        self,
        symbol: str,
        order_id: str | int,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        path, params, extra = self._query_order(symbol, order_id, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra)

    def _get_open_orders(
        self,
        symbol: str | None = None,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> tuple[str, dict[str, Any], dict[str, Any]]:
        path = "GET /v1/user/spot/active_orders"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "exchange_name": self.exchange_name,
                "symbol_name": symbol or "",
                "asset_type": self.asset_type,
                "request_type": "get_open_orders",
            }
        )
        params = {"pair": self._normalize_pair(symbol)} if symbol else {}
        return path, params, extra_data

    def get_open_orders(
        self,
        symbol: str | None = None,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        path, params, extra = self._get_open_orders(symbol, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra)

    def _get_account(
        self,
        symbol: str | None = None,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> tuple[str, dict[str, Any] | None, dict[str, Any]]:
        path = "GET /v1/user/assets"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "exchange_name": self.exchange_name,
                "symbol_name": symbol or "",
                "asset_type": self.asset_type,
                "request_type": "get_account",
            }
        )
        return path, None, extra_data

    def get_account(
        self,
        symbol: str | None = None,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        path, params, extra = self._get_account(symbol, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra)

    def _get_balance(
        self,
        symbol: str | None = None,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> tuple[str, dict[str, Any] | None, dict[str, Any]]:
        path = "GET /v1/user/assets"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "exchange_name": self.exchange_name,
                "symbol_name": symbol or "",
                "asset_type": self.asset_type,
                "request_type": "get_balance",
            }
        )
        return path, None, extra_data

    def get_balance(
        self,
        symbol: str | None = None,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        path, params, extra = self._get_balance(symbol, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra)
