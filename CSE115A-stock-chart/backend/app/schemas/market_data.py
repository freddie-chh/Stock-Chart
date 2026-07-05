"""Pydantic schemas for market data API."""

from enum import Enum

from pydantic import BaseModel, Field


class Timeframe(str, Enum):
    """Supported chart timeframes."""

    M1 = "1m"
    M5 = "5m"
    M15 = "15m"
    M30 = "30m"
    D1 = "1D"
    MO1 = "1M"
    Y1 = "1Y"
    MAX = "Max"


# Yahoo Finance history limits per timeframe (for integration metadata).
TIMEFRAME_LIMITS: dict[str, str] = {
    "1m": "7 days",
    "5m": "60 days",
    "15m": "60 days",
    "30m": "60 days",
    "1D": "6 months",
    "1M": "max history",
    "1Y": "1 year",
    "Max": "max history",
}


class OHLCVBar(BaseModel):
    """Single OHLCV candle."""

    time: str
    open: float
    high: float
    low: float
    close: float
    volume: float


class MarketDataMeta(BaseModel):
    """Metadata about a market data response."""

    bar_count: int
    start_time: str | None = None
    end_time: str | None = None
    provider: str = "yahoo_finance"


class MarketDataResponse(BaseModel):
    """Market data response for a ticker."""

    ticker: str
    timeframe: str
    data: list[OHLCVBar]
    meta: MarketDataMeta


class IntegrationInfo(BaseModel):
    """Connection info for Stock-Chart-Strategy-Developer."""

    companion_repo: str
    market_data_endpoint: str
    supported_timeframes: list[str]
    timeframe_limits: dict[str, str]
    strategy_dev_api_url: str | None = None
    future_endpoints: dict[str, str] = Field(
        default_factory=lambda: {
            "indicators": "/indicators/definitions",
            "custom_indicators": "/indicators/custom",
            "strategies": "/strategies",
            "backtest_run": "/backtest/run",
            "backtest_metrics": "/backtest/{id}/metrics",
        }
    )
