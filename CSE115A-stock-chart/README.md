# Stock-Chart

Backend API for interactive stock charts. Serves OHLCV candle data to a chart frontend.

## Quick start

```bash
bash run-backend.sh
```

- API: http://localhost:8000
- Docs: http://localhost:8000/docs

## Timeframes

`1m` · `5m` · `15m` · `30m` · `1D` · `1M` · `1Y` · `Max`

## Frontend integration

Point your chart app at:

```
GET /market-data/{ticker}?timeframe=1D
```

Response includes OHLCV `data` and a `meta` block. Set `CORS_ORIGINS` in `.env` to your frontend URL (e.g. `http://localhost:5173`).

See [`backend/README.md`](backend/README.md) for full API details and tests.
