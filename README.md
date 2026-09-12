# My Trade Platform

A trading bot scaffold built on Alpaca's Paper Trading API.

## Setup Workflow

**Paper trade first.** Register an account on [Alpaca](https://alpaca.markets/) and generate Paper Trading API keys before connecting any real capital.

> **Canadian residents:** Alpaca does not offer live brokerage accounts in Canada due to regulatory restrictions, but its Paper Trading API is free and available for sandbox testing / running automated strategies with no real money. For a live account, **Interactive Brokers (IBKR Canada)** is the recommended path — it supports Python via `ib_insync` / the TWS API and also offers paper trading. This platform currently targets Alpaca for paper trading; an IBKR broker adapter would be needed before going live from Canada.

1. Install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and fill in your Alpaca paper API keys:
   ```bash
   cp .env.example .env
   ```

3. Verify the connection:
   ```bash
   python -m src.main
   ```

## Project Structure

- `src/config.py` — environment-driven configuration
- `src/broker.py` — Alpaca trading client wrapper (paper by default)
- `src/main.py` — entry point / connection check

## Status

Early scaffold — account connection and order submission only. Strategy, backtesting, and live-data ingestion are not yet implemented.
