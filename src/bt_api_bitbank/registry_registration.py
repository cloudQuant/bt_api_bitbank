from __future__ import annotations

from typing import TYPE_CHECKING, Any

from bt_api_base.balance_utils import nested_balance_handler as _bitbank_balance_handler

from bt_api_bitbank.exchange_data import BitbankExchangeDataSpot
from bt_api_bitbank.feeds.live_bitbank.spot import BitbankRequestDataSpot

if TYPE_CHECKING:
    from bt_api_base.registry import ExchangeRegistry


def _bitbank_spot_subscribe_handler(
    data_queue: Any, exchange_params: Any, topics: Any, bt_api: Any
) -> None:
    topic_list = [i["topic"] for i in topics]
    bt_api.log(f"Bitbank Spot topics requested: {topic_list}")


def register_bitbank(registry: type[ExchangeRegistry]) -> None:
    registry.register_feed("BITBANK___SPOT", BitbankRequestDataSpot)
    registry.register_exchange_data("BITBANK___SPOT", BitbankExchangeDataSpot)
    registry.register_balance_handler("BITBANK___SPOT", _bitbank_balance_handler)
    registry.register_stream("BITBANK___SPOT", "subscribe", _bitbank_spot_subscribe_handler)
