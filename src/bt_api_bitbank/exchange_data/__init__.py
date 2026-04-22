from __future__ import annotations

from bt_api_base.containers.exchanges.exchange_data import ExchangeData


class BitbankExchangeData(ExchangeData):
    def __init__(self) -> None:
        super().__init__()
        self.exchange_name = "BITBANK"
        self.rest_url = "https://public.bitbank.cc"
        self.rest_private_url = "https://api.bitbank.cc/v1"
        self.wss_url = "wss://stream.bitbank.cc"
        self.kline_periods = {
            "1m": "1min",
            "5m": "5min",
            "15m": "15min",
            "30m": "30min",
            "1h": "1hour",
            "4h": "4hour",
            "8h": "8hour",
            "12h": "12hour",
            "1d": "1day",
            "1w": "1week",
            "1month": "1month",
        }
        self.legal_currency = ["JPY", "BTC", "ETH"]
        self.rest_paths = {}
        self.wss_paths = {}


class BitbankExchangeDataSpot(BitbankExchangeData):
    def __init__(self) -> None:
        super().__init__()
        self.asset_type = "SPOT"
        self.api_key = None
        self.api_secret = None
