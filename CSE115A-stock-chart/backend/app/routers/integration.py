"""Integration metadata routes."""

from fastapi import APIRouter

from app.config import get_settings
from app.schemas.market_data import IntegrationInfo, Timeframe, TIMEFRAME_LIMITS

router = APIRouter(tags=["integration"])


@router.get("/integration/strategy-developer", response_model=IntegrationInfo)
async def strategy_developer_info() -> IntegrationInfo:
    """Connection info for Stock-Chart-Strategy-Developer companion repo."""
    settings = get_settings()
    timeframes = [tf.value for tf in Timeframe]

    return IntegrationInfo(
        companion_repo="https://github.com/ryancleary8/Stock-Chart-Strategy-Developer",
        market_data_endpoint="/market-data/{ticker}?timeframe={timeframe}",
        supported_timeframes=timeframes,
        timeframe_limits={tf: TIMEFRAME_LIMITS[tf] for tf in timeframes},
        strategy_dev_api_url=settings.strategy_dev_api_url or None,
    )
