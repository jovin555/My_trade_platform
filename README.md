# My Trade Platform

A trading bot scaffold built on Alpaca's Paper Trading API.

## Setup Workflow

**Paper trade first.** Register an account on [Alpaca](https://alpaca.markets/) and generate Paper Trading API keys before connecting any real capital.

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
