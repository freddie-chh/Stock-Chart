"""Market data API routes."""

from fastapi import APIRouter, HTTPException, Query, status

from app.providers.yahoo_finance import NoDataError, ProviderError
from app.schemas.market_data import MarketDataResponse
from app.services.stock_chart_service import (
    InvalidTickerError,
    InvalidTimeframeError,
    get_market_data,
)

router = APIRouter(tags=["market-data"])


@router.get("/market-data/{ticker}", response_model=MarketDataResponse)
async def get_market_data_route(
    ticker: str,
    timeframe: str = Query(default="1D"),
) -> MarketDataResponse:
    """Return OHLCV market data for a ticker (no auth required)."""
    try:
        return get_market_data(ticker, timeframe)
    except InvalidTickerError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except InvalidTimeframeError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except NoDataError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except ProviderError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc
