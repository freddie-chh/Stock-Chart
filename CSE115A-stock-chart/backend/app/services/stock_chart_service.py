"""Stock chart service — orchestrates market data fetching."""

import logging
import re

from app.providers.yahoo_finance import (
    NoDataError,
    ProviderError,
    fetch_historical_daily,
    fetch_ohlcv,
)
from app.schemas.market_data import MarketDataMeta, MarketDataResponse, OHLCVBar, Timeframe

logger = logging.getLogger(__name__)

TICKER_PATTERN = re.compile(r"^[A-Z0-9][A-Z0-9.\-^=]{0,14}$")


class InvalidTickerError(ValueError):
    """Raised when a ticker symbol is malformed."""


class InvalidTimeframeError(ValueError):
    """Raised when a timeframe is not supported."""


def normalize_ticker(ticker: str) -> str:
    """Normalize and validate a ticker symbol."""
    normalized = ticker.strip().upper()
    if not normalized or not TICKER_PATTERN.match(normalized):
        raise InvalidTickerError(
            f"Invalid ticker '{ticker}'. Use 1-15 alphanumeric characters (e.g. AAPL, BTC-USD)."
        )
    return normalized


def validate_timeframe(timeframe: str) -> str:
    """Validate and return a supported timeframe value."""
    valid = {tf.value for tf in Timeframe}
    if timeframe not in valid:
        raise InvalidTimeframeError(
            f"Invalid timeframe '{timeframe}'. Choose from: {', '.join(sorted(valid))}"
        )
    return timeframe


def _build_meta(bars: list[OHLCVBar]) -> MarketDataMeta:
    """Build metadata from OHLCV bars."""
    return MarketDataMeta(
        bar_count=len(bars),
        start_time=bars[0].time if bars else None,
        end_time=bars[-1].time if bars else None,
        provider="yahoo_finance",
    )


def get_market_data(ticker: str, timeframe: str = "1D") -> MarketDataResponse:
    """Fetch OHLCV market data for a ticker and timeframe."""
    normalized_ticker = normalize_ticker(ticker)
    validated_timeframe = validate_timeframe(timeframe)

    logger.info("Fetching market data for %s (%s)", normalized_ticker, validated_timeframe)

    try:
        bars = fetch_ohlcv(normalized_ticker, validated_timeframe)
    except NoDataError:
        raise
    except ProviderError:
        raise

    return MarketDataResponse(
        ticker=normalized_ticker,
        timeframe=validated_timeframe,
        data=bars,
        meta=_build_meta(bars),
    )


def get_historical_daily(ticker: str, start_date: str, end_date: str) -> list[OHLCVBar]:
    """Fetch daily OHLCV data for a date range (for future backtesting)."""
    normalized_ticker = normalize_ticker(ticker)
    logger.info(
        "Fetching historical daily data for %s (%s to %s)",
        normalized_ticker,
        start_date,
        end_date,
    )
    return fetch_historical_daily(normalized_ticker, start_date, end_date)
