"""Stock Chart API — market data for interactive charts."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import integration, market_data, stubs

settings = get_settings()

app = FastAPI(
    title="Stock Chart API",
    description="Market data API for interactive stock charts",
    version="0.3.0",
)

origins = [o.strip() for o in settings.cors_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(market_data.router)
app.include_router(integration.router)
app.include_router(stubs.router)


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "service": "stock-chart-api"}
