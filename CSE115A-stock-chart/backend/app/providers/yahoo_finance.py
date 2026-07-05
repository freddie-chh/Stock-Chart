"""Yahoo Finance market data provider."""

import logging
from datetime import datetime

import yfinance as yf

from app.schemas.market_data import OHLCVBar, Timeframe

logger = logging.getLogger(__name__)

# Each timeframe maps to Yahoo Finance interval + period.
TIMEFRAME_MAP: dict[str, dict[str, str]] = {
    Timeframe.M1.value: {"period": "7d", "interval": "1m"},
    Timeframe.M5.value: {"period": "60d", "interval": "5m"},
    Timeframe.M15.value: {"period": "60d", "interval": "15m"},
    Timeframe.M30.value: {"period": "60d", "interval": "30m"},
    Timeframe.D1.value: {"period": "6mo", "interval": "1d"},
    Timeframe.MO1.value: {"period": "max", "interval": "1mo"},
    Timeframe.Y1.value: {"period": "1y", "interval": "1d"},
    Timeframe.MAX.value: {"period": "max", "interval": "1d"},
}

INTRADAY_INTERVALS = {"1m", "5m", "15m", "30m"}


class ProviderError(Exception):
    """Raised when the Yahoo Finance provider fails."""


class NoDataError(Exception):
    """Raised when no data is returned for a ticker."""


def format_time(ts: datetime, interval: str) -> str:
    """Format timestamp for chart consumption."""
    if interval in INTRADAY_INTERVALS:
        return ts.strftime("%Y-%m-%d %H:%M:%S")
    return ts.strftime("%Y-%m-%d")


def fetch_ohlcv(ticker: str, timeframe: str) -> list[OHLCVBar]:
    """Fetch OHLCV data from Yahoo Finance for a ticker and timeframe."""
    params = TIMEFRAME_MAP[timeframe]
    interval = params["interval"]

    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=params["period"], interval=interval)
    except Exception as exc:
        logger.error("Yahoo Finance fetch failed for %s (%s): %s", ticker, timeframe, exc)
        raise ProviderError(f"Market data provider failed for '{ticker}'") from exc

    if df.empty:
        raise NoDataError(f"No data found for ticker '{ticker}'")

    bars: list[OHLCVBar] = []
    for ts, row in df.iterrows():
        bars.append(
            OHLCVBar(
                time=format_time(ts.to_pydatetime(), interval),
                open=round(float(row["Open"]), 4),
                high=round(float(row["High"]), 4),
                low=round(float(row["Low"]), 4),
                close=round(float(row["Close"]), 4),
                volume=round(float(row["Volume"]), 2),
            )
        )

    return bars


def fetch_historical_daily(ticker: str, start_date: str, end_date: str) -> list[OHLCVBar]:
    """Fetch daily OHLCV data for a date range (used by backtesting)."""
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(start=start_date, end=end_date, interval="1d")
    except Exception as exc:
        logger.error(
            "Yahoo Finance historical fetch failed for %s (%s to %s): %s",
            ticker,
            start_date,
            end_date,
            exc,
        )
        raise ProviderError(f"Market data provider failed for '{ticker}'") from exc

    if df.empty:
        raise NoDataError(
            f"No historical data for '{ticker}' between {start_date} and {end_date}"
        )

    bars: list[OHLCVBar] = []
    for ts, row in df.iterrows():
        bars.append(
            OHLCVBar(
                time=ts.strftime("%Y-%m-%d"),
                open=round(float(row["Open"]), 4),
                high=round(float(row["High"]), 4),
                low=round(float(row["Low"]), 4),
                close=round(float(row["Close"]), 4),
                volume=round(float(row["Volume"]), 2),
            )
        )

    return bars
