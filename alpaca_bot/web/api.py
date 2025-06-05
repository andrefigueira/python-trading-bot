from __future__ import annotations

from pathlib import Path

import yaml
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

from ..config import Settings

app = FastAPI(title="alpaca-bot")

CONFIG_PATH = Path("config.yaml")
PORTFOLIO = {"balance": 0.0, "pnl": 0.0}
ORDERS = {"open": [], "closed": [], "pending": []}


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
async def dashboard() -> HTMLResponse:
    settings = Settings.load(CONFIG_PATH)
    symbols = ", ".join(settings.execution.symbols)
    html = f"""
    <html>
        <head><title>Alpaca Bot Dashboard</title></head>
        <body>
            <h1>Dashboard</h1>
            <p><strong>Balance:</strong> {PORTFOLIO['balance']}</p>
            <p><strong>P&amp;L:</strong> {PORTFOLIO['pnl']}</p>
            <h2>Configure Symbols</h2>
            <form action='/update_symbols' method='post'>
                <input type='text' name='symbols' value='{symbols}'>
                <button type='submit'>Update</button>
            </form>
            <h2>Orders</h2>
            <h3>Open</h3>
            <ul>{''.join(f'<li>{o}</li>' for o in ORDERS['open'])}</ul>
            <h3>Closed</h3>
            <ul>{''.join(f'<li>{o}</li>' for o in ORDERS['closed'])}</ul>
            <h3>Pending</h3>
            <ul>{''.join(f'<li>{o}</li>' for o in ORDERS['pending'])}</ul>
        </body>
    </html>
    """
    return HTMLResponse(html)


@app.post("/update_symbols")
async def update_symbols(symbols: str = Form(...)) -> dict[str, list[str] | str]:
    settings = Settings.load(CONFIG_PATH)
    parsed = [s.strip().upper() for s in symbols.split(",") if s.strip()]
    settings.execution.symbols = parsed
    CONFIG_PATH.write_text(
        yaml.safe_dump(settings.dict(), sort_keys=False)
    )
    return {"status": "updated", "symbols": parsed}


@app.get("/api/portfolio")
async def get_portfolio() -> dict[str, float]:
    return PORTFOLIO


@app.get("/api/orders")
async def get_orders() -> dict[str, list]:
    return ORDERS
