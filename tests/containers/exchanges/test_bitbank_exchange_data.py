"""Tests for BitbankExchangeData container."""

from __future__ import annotations

from bt_api_bitbank.exchange_data import BitbankExchangeData


class TestBitbankExchangeData:
    """Tests for BitbankExchangeData."""

    def test_init(self):
        """Test initialization."""
        exchange = BitbankExchangeData()

        assert exchange.exchange_name == "BITBANK"
        assert "bitbank.cc" in exchange.rest_url
