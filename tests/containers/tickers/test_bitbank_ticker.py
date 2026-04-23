"""Tests for BitbankRequestTickerData container."""

from __future__ import annotations

from bt_api_bitbank.containers.tickers import BitbankRequestTickerData


class TestBitbankRequestTickerData:
    """Tests for BitbankRequestTickerData."""

    def test_init(self):
        """Test initialization."""
        ticker = BitbankRequestTickerData({}, symbol_name="btc_jpy", asset_type="SPOT")

        assert ticker.exchange_name == "BITBANK"
        assert ticker.symbol_name == "btc_jpy"
        assert ticker.asset_type == "SPOT"
        assert ticker.has_been_init_data is False

    def test_init_data(self):
        """Test init_data with ticker info."""
        data = {"last": "5000000", "buy": "4999000", "sell": "5001000"}
        ticker = BitbankRequestTickerData(
            data, symbol_name="btc_jpy", asset_type="SPOT", has_been_json_encoded=True
        )
        ticker.init_data()

        assert ticker.has_been_init_data is True

    def test_get_all_data(self):
        ticker = BitbankRequestTickerData(
            {}, symbol_name="btc_jpy", asset_type="SPOT", has_been_json_encoded=True
        )
        result = ticker.get_all_data()
        assert result["exchange_name"] == "BITBANK"
        assert result["symbol_name"] == "btc_jpy"

    def test_str_representation(self):
        ticker = BitbankRequestTickerData(
            {}, symbol_name="btc_jpy", asset_type="SPOT", has_been_json_encoded=True
        )
        assert "BITBANK" in str(ticker)
