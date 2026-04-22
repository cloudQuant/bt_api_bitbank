from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base.containers.orders.order import OrderData
from bt_api_base.functions.utils import from_dict_get_float, from_dict_get_string


class BitbankOrderData(OrderData):
    def __init__(
        self,
        order_info: Any,
        symbol_name: str | None = None,
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(order_info, has_been_json_encoded)
        self.exchange_name = "BITBANK"
        self.symbol_name = symbol_name
        self.order_data: dict[str, Any] | str | None = order_info if has_been_json_encoded else None
        self.order_id: str | None = None
        self.client_order_id: str | None = None
        self.order_type: str | None = None
        self.side: str | None = None
        self.price: float | None = None
        self.amount: float | None = None
        self.filled_amount: float | None = None
        self.remaining_amount: float | None = None
        self.status: str | None = None
        self.created_at: int | None = None
        self.updated_at: int | None = None
        self.local_update_time = time.time()
        self.has_been_init_data = False

    def init_data(self) -> BitbankOrderData:
        if not self.has_been_json_encoded:
            self.order_data = (
                json.loads(self.order_info) if isinstance(self.order_info, str) else {}
            )
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self
        if isinstance(self.order_data, dict):
            data = self.order_data.get("data", self.order_data)
            self.order_id = from_dict_get_string(data, "order_id")
            self.order_type = from_dict_get_string(data, "type")
            self.side = from_dict_get_string(data, "side")
            self.price = from_dict_get_float(data, "price")
            self.amount = from_dict_get_float(data, "start_amount")
            self.filled_amount = from_dict_get_float(data, "executed_amount")
            self.remaining_amount = from_dict_get_float(data, "remaining_amount")
            self.status = from_dict_get_string(data, "status")
            created = from_dict_get_float(data, "ordered_at")
            if created:
                self.created_at = int(created * 1000)
        self.has_been_init_data = True
        return self

    def get_all_data(self) -> dict[str, Any]:
        self.init_data()
        return {
            "exchange_name": self.exchange_name,
            "symbol_name": self.symbol_name,
            "order_id": self.order_id,
            "client_order_id": self.client_order_id,
            "order_type": self.order_type,
            "side": self.side,
            "price": self.price,
            "amount": self.amount,
            "filled_amount": self.filled_amount,
            "remaining_amount": self.remaining_amount,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
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

    def get_order_id(self) -> str | None:
        return self.order_id

    def get_order_type(self) -> str | None:
        return self.order_type

    def get_side(self) -> str | None:
        return self.side

    def get_price(self) -> float | int:
        return self.price or 0.0

    def get_amount(self) -> float | int:
        return self.amount or 0.0

    def get_filled_amount(self) -> float | int:
        return self.filled_amount or 0.0

    def get_remaining_amount(self) -> float | int:
        return self.remaining_amount or 0.0

    def get_status(self) -> str | None:
        return self.status

    def is_order_type(self) -> bool:
        return self.order_type in ("limit", "market")

    def is_side(self) -> bool:
        return self.side in ("buy", "sell")


class BitbankRequestOrderData(BitbankOrderData):
    pass


class BitbankWssOrderData(BitbankOrderData):
    pass
