"""Tests for stock chart API."""

from datetime import datetime
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.providers.yahoo_finance import format_time
from app.schemas.market_data import OHLCVBar, Timeframe
from app.services.stock_chart_service import (
    InvalidTickerError,
    InvalidTimeframeError,
    normalize_ticker,
    validate_timeframe,
)

client = TestClient(app)

SAMPLE_BARS = [
    OHLCVBar(
        time="2026-01-02",
        open=100.0,
        high=105.0,
        low=99.0,
        close=103.0,
        volume=1000000.0,
    ),
    OHLCVBar(
        time="2026-01-03",
        open=103.0,
        high=108.0,
        low=102.0,
        close=107.0,
        volume=1200000.0,
    ),
]


class TestTimeframeValidation:
    def test_valid_timeframes(self):
        for tf in Timeframe:
            assert validate_timeframe(tf.value) == tf.value

    def test_invalid_timeframe_raises(self):
        with pytest.raises(InvalidTimeframeError, match="Invalid timeframe"):
            validate_timeframe("1h")


class TestTickerNormalization:
    def test_normalizes_uppercase(self):
        assert normalize_ticker("aapl") == "AAPL"

    def test_strips_whitespace(self):
        assert normalize_ticker("  AAPL  ") == "AAPL"

    def test_accepts_crypto_ticker(self):
        assert normalize_ticker("BTC-USD") == "BTC-USD"

    def test_rejects_empty(self):
        with pytest.raises(InvalidTickerError):
            normalize_ticker("")

    def test_rejects_invalid_chars(self):
        with pytest.raises(InvalidTickerError):
            normalize_ticker("AA@PL")


class TestFormatTime:
    def test_intraday_format(self):
        ts = datetime(2026, 1, 2, 14, 30, 0)
        assert format_time(ts, "5m") == "2026-01-02 14:30:00"

    def test_daily_format(self):
        ts = datetime(2026, 1, 2, 14, 30, 0)
        assert format_time(ts, "1d") == "2026-01-02"


class TestMarketDataRoute:
    @patch("app.services.stock_chart_service.fetch_ohlcv", return_value=SAMPLE_BARS)
    def test_returns_ohlcv_with_meta(self, mock_fetch):
        response = client.get("/market-data/AAPL?timeframe=1D")
        assert response.status_code == 200
        body = response.json()
        assert body["ticker"] == "AAPL"
        assert body["timeframe"] == "1D"
        assert len(body["data"]) == 2
        assert body["meta"]["bar_count"] == 2
        assert body["meta"]["start_time"] == "2026-01-02"
        assert body["meta"]["end_time"] == "2026-01-03"
        assert body["meta"]["provider"] == "yahoo_finance"
        mock_fetch.assert_called_once_with("AAPL", "1D")

    def test_invalid_timeframe_returns_400(self):
        response = client.get("/market-data/AAPL?timeframe=1h")
        assert response.status_code == 400
        assert "Invalid timeframe" in response.json()["detail"]

    def test_invalid_ticker_returns_400(self):
        response = client.get("/market-data/INVALID@?timeframe=1D")
        assert response.status_code == 400
        assert "Invalid ticker" in response.json()["detail"]

    @patch("app.services.stock_chart_service.fetch_ohlcv", side_effect=Exception("No data"))
    def test_no_data_returns_404(self, mock_fetch):
        from app.providers.yahoo_finance import NoDataError

        mock_fetch.side_effect = NoDataError("No data found for ticker 'FAKE'")
        response = client.get("/market-data/FAKE?timeframe=1D")
        assert response.status_code == 404

    @patch("app.services.stock_chart_service.fetch_ohlcv")
    def test_provider_error_returns_502(self, mock_fetch):
        from app.providers.yahoo_finance import ProviderError

        mock_fetch.side_effect = ProviderError("Market data provider failed")
        response = client.get("/market-data/AAPL?timeframe=1D")
        assert response.status_code == 502


class TestIntegrationRoute:
    def test_returns_all_timeframes(self):
        response = client.get("/integration/strategy-developer")
        assert response.status_code == 200
        body = response.json()
        expected = [tf.value for tf in Timeframe]
        assert body["supported_timeframes"] == expected
        assert "1h" not in body["supported_timeframes"]
        assert body["timeframe_limits"]["1m"] == "7 days"
        assert "future_endpoints" in body


class TestStubRoutes:
    def test_indicator_definitions_returns_empty(self):
        response = client.get("/indicators/definitions")
        assert response.status_code == 200
        body = response.json()
        assert body["definitions"] == []
        assert body["coming_soon"] is True

    def test_custom_indicator_returns_501(self):
        response = client.post("/indicators/custom")
        assert response.status_code == 501

    def test_strategies_returns_501(self):
        response = client.get("/strategies")
        assert response.status_code == 501

    def test_backtest_run_returns_501(self):
        response = client.post("/backtest/run")
        assert response.status_code == 501

    def test_backtest_metrics_returns_501(self):
        response = client.get("/backtest/test-id/metrics")
        assert response.status_code == 501
