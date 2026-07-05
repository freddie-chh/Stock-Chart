"""Stub routes for future features (indicators, strategies, backtesting)."""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(tags=["future-stubs"])


class IndicatorDefinition(BaseModel):
    """Placeholder indicator definition."""

    id: str
    name: str
    type: str


class IndicatorsResponse(BaseModel):
    """Placeholder indicators list response."""

    definitions: list[IndicatorDefinition]
    coming_soon: bool = True


@router.get("/indicators/definitions", response_model=IndicatorsResponse)
async def list_indicator_definitions() -> IndicatorsResponse:
    """Return indicator definitions (stub — not yet implemented)."""
    return IndicatorsResponse(definitions=[], coming_soon=True)


@router.post("/indicators/custom", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def create_custom_indicator() -> None:
    """Create a custom indicator (stub — not yet implemented)."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Custom indicators are not yet implemented.",
    )


@router.get("/strategies", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def list_strategies() -> None:
    """List saved strategies (stub — not yet implemented)."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Strategy storage is not yet implemented.",
    )


@router.post("/strategies", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def create_strategy() -> None:
    """Save a strategy (stub — not yet implemented)."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Strategy storage is not yet implemented.",
    )


@router.post("/backtest/run", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def run_backtest() -> None:
    """Run a backtest (stub — not yet implemented)."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Backtesting is not yet implemented.",
    )


@router.get("/backtest/{backtest_id}/metrics", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def get_backtest_metrics(backtest_id: str) -> None:
    """Get backtest performance metrics (stub — not yet implemented)."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=f"Backtest metrics for '{backtest_id}' are not yet implemented.",
    )
