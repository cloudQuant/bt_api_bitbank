from __future__ import annotations

import hashlib
import hmac
import time
from typing import Any

from bt_api_base.containers.requestdatas.request_data import RequestData
from bt_api_base.feeds.capability import Capability
from bt_api_base.feeds.feed import Feed
from bt_api_base.feeds.http_client import HttpClient
from bt_api_base.logging_factory import get_logger

from bt_api_bitbank.exchange_data import BitbankExchangeDataSpot


class BitbankRequestData(Feed):
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
        self.data_queue = data_queue
        self.exchange_name = kwargs.get("exchange_name", "BITBANK___SPOT")
        self.asset_type = kwargs.get("asset_type", "SPOT")
        self._params = BitbankExchangeDataSpot()
        self._params.api_key = kwargs.get("public_key") or kwargs.get("api_key")
        self._params.api_secret = (
            kwargs.get("private_key") or kwargs.get("secret_key") or kwargs.get("api_secret")
        )
        self.request_logger = get_logger("bitbank_feed")
        self.async_logger = get_logger("bitbank_feed")
        self._http_client = HttpClient(venue=self.exchange_name, timeout=10)

    def _get_base_url(self, path: str) -> str:
        if path.startswith("/v1/"):
            return self._params.rest_private_url
        return self._params.rest_url

    def _generate_signature(self, timestamp: str, time_window: str, message: str) -> str:
        secret = getattr(self._params, "api_secret", None)
        if secret:
            signature = hmac.new(
                secret.encode("utf-8"), message.encode("utf-8"), hashlib.sha256
            ).hexdigest()
            return signature
        return ""

    def _get_headers(
        self,
        method: str,
        request_path: str,
        params: dict[str, Any] | None = None,
        body: str = "",
    ) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}

        api_key = getattr(self._params, "api_key", None)
        if api_key:
            timestamp = str(int(time.time() * 1000))
            time_window = "5000"

            if method == "GET":
                full_path = request_path
                if params:
                    query_string = "&".join(f"{k}={v}" for k, v in params.items())
                    full_path = f"{request_path}?{query_string}"
                message = timestamp + time_window + full_path
            else:
                message = timestamp + time_window + body

            signature = self._generate_signature(timestamp, time_window, message)

            headers.update(
                {
                    "ACCESS-KEY": api_key,
                    "ACCESS-SIGNATURE": signature,
                    "ACCESS-REQUEST-TIME": timestamp,
                    "ACCESS-TIME-WINDOW": time_window,
                }
            )

        return headers

    def request(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        body: Any = None,
        extra_data: dict[str, Any] | None = None,
        timeout: int = 10,
    ) -> RequestData:
        method = path.split()[0] if " " in path else "GET"
        request_path = "/" + path.split()[1] if " " in path else path

        headers = self._get_headers(method, request_path, params, body)

        try:
            response = self._http_client.request(
                method=method,
                url=self._get_base_url(request_path) + request_path,
                headers=headers,
                json_data=body if method == "POST" else None,
                params=params,
            )
            return self._process_response(response, extra_data)
        except Exception as e:
            self.request_logger.error(f"Request failed: {e}")
            raise

    async def async_request(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        body: Any = None,
        extra_data: dict[str, Any] | None = None,
        timeout: int = 5,
    ) -> RequestData:
        method = path.split()[0] if " " in path else "GET"
        request_path = "/" + path.split()[1] if " " in path else path

        headers = self._get_headers(method, request_path, params, body)

        try:
            response = await self._http_client.async_request(
                method=method,
                url=self._get_base_url(request_path) + request_path,
                headers=headers,
                json_data=body if method == "POST" else None,
                params=params,
            )
            return self._process_response(response, extra_data)
        except Exception as e:
            self.async_logger.error(f"Async request failed: {e}")
            raise

    def async_callback(self, future: Any) -> None:
        try:
            result = future.result()
            if result is not None:
                self.push_data_to_queue(result)
        except Exception as e:
            self.async_logger.error(f"Async callback error: {e}")

    def _process_response(
        self, response: dict[str, Any], extra_data: dict[str, Any] | None = None
    ) -> RequestData:
        if extra_data is None:
            extra_data = {}
        return RequestData(response, extra_data)

    def push_data_to_queue(self, data: Any) -> None:
        if self.data_queue is not None:
            self.data_queue.put(data)

    def connect(self) -> None:
        pass

    def disconnect(self) -> None:
        super().disconnect()

    def is_connected(self) -> bool:
        return True
