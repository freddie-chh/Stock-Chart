# Stock Chart API (Backend)

FastAPI market data service for interactive stock charts. Serves OHLCV candle data for multiple timeframes via Yahoo Finance.

Designed to work with a separate chart frontend — merge and wire the frontend when ready.

## Timeframes

`1m` · `5m` · `15m` · `30m` · `1D` · `1M` · `1Y` · `Max`

## Quick start

```bash
bash run-backend.sh
```

API: http://localhost:8000  
Docs: http://localhost:8000/docs

## Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/health` | Health check |
| GET | `/market-data/{ticker}?timeframe=1D` | OHLCV candles + metadata |
| GET | `/integration/strategy-developer` | Supported timeframes and integration info |

## Tests

```bash
cd backend && PYTHONPATH=. python3 -m pytest tests/ -v
```
