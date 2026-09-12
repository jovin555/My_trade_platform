# My Trade Platform

A trading bot scaffold supporting Alpaca (paper trading) and Interactive Brokers (paper + live).

## Setup Workflow

**Paper trade first.** Register an account on [Alpaca](https://alpaca.markets/) and generate Paper Trading API keys before connecting any real capital.

> **Canadian residents:** Alpaca does not offer live brokerage accounts in Canada due to regulatory restrictions, but its Paper Trading API is free and available for sandbox testing / running automated strategies with no real money. For a live account, **Interactive Brokers (IBKR Canada)** is the recommended path.

1. Install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and fill in your settings:
   ```bash
   cp .env.example .env
   ```

### Alpaca (paper trading)

3. Add your Alpaca paper API keys to `.env`, then verify the connection:
   ```bash
   python -m src.main
   ```

### IBKR (paper or live)

IBKR has no static API key. Instead you run **IB Gateway** or **Trader Workstation** locally, log in with your IBKR credentials, and your bot connects to that running instance over a local socket:

3. Download and install [IB Gateway](https://www.interactivebrokers.com/en/trading/ibgateway-stable.php) (lightweight, recommended) or TWS.
4. Log in with your IBKR account credentials. Use a **paper trading account** first — request one free from Account Management if you don't already have one.
5. In IB Gateway/TWS: **Configuration → API → Settings** → enable "Enable ActiveX and Socket Clients", note the socket port, and add `127.0.0.1` to trusted IPs.
6. Set `IBKR_HOST` / `IBKR_PORT` / `IBKR_CLIENT_ID` in `.env` to match (defaults assume Gateway paper trading on port 4002).
7. Verify the connection:
   ```bash
   python -m src.main_ibkr
   ```

## Project Structure

- `src/config.py` — environment-driven configuration
- `src/broker.py` — Alpaca trading client wrapper (paper by default)
- `src/main.py` — Alpaca entry point / connection check
- `src/ibkr_broker.py` — IBKR (`ib_async`) trading client wrapper, connects to a running IB Gateway/TWS
- `src/main_ibkr.py` — IBKR entry point / connection check

## Status

Early scaffold — account connection and order submission only. Strategy, backtesting, and live-data ingestion are not yet implemented.
