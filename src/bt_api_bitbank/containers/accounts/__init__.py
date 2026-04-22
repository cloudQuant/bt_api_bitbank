from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base.containers.accounts.account import AccountData


class BitbankAccountData(AccountData):
    def __init__(
        self,
        account_info: Any,
        symbol_name: str | None = None,
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(account_info, has_been_json_encoded)
        self.exchange_name = "BITBANK"
        self.symbol_name = symbol_name
        self.account_data: dict[str, Any] | str | None = (
            account_info if has_been_json_encoded else None
        )
        self.account_id: str | None = None
        self.account_type: str | None = None
        self.can_deposit: bool | None = None
        self.can_trade: bool | None = None
        self.can_withdraw: bool | None = None
        self.local_update_time = time.time()
        self.has_been_init_data = False

    def init_data(self) -> BitbankAccountData:
        if not self.has_been_json_encoded:
            self.account_data = (
                json.loads(self.account_info) if isinstance(self.account_info, str) else {}
            )
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self
        if isinstance(self.account_data, dict):
            self.account_id = "BITBANK_SPOT"
            self.account_type = "SPOT"
            self.can_deposit = True
            self.can_trade = True
            self.can_withdraw = True
        self.has_been_init_data = True
        return self

    def get_all_data(self) -> dict[str, Any]:
        self.init_data()
        return {
            "exchange_name": self.exchange_name,
            "symbol_name": self.symbol_name,
            "account_id": self.account_id,
            "account_type": self.account_type,
            "can_deposit": self.can_deposit,
            "can_trade": self.can_trade,
            "can_withdraw": self.can_withdraw,
            "local_update_time": self.local_update_time,
        }

    def __str__(self) -> str:
        return json.dumps(self.get_all_data())

    def __repr__(self) -> str:
        return self.__str__()

    def get_exchange_name(self) -> str:
        return self.exchange_name or ""

    def get_asset_type(self) -> str:
        return "SPOT"

    def get_local_update_time(self) -> float:
        return float(self.local_update_time or 0.0)

    def get_account_id(self) -> str | None:
        return self.account_id

    def get_account_type(self) -> str | None:
        return self.account_type

    def get_can_deposit(self) -> bool | None:
        return self.can_deposit

    def get_can_trade(self) -> bool | None:
        return self.can_trade

    def get_can_withdraw(self) -> bool | None:
        return self.can_withdraw


class BitbankRequestAccountData(BitbankAccountData):
    pass


class BitbankWssAccountData(BitbankAccountData):
    pass
