# Weather Trading Tools Setup

## Data Pipeline: poly_data

```bash
# Clone
git clone https://github.com/warproxxx/poly_data.git
cd poly_data

# Download pre-built snapshot (saves 2+ days)
wget https://polydata-archive.s3.us-east-1.amazonaws.com/archive.tar.xz
tar -xf archive.tar.xz

# Install deps (uses uv)
uv sync

# Run data pipeline
uv run python update_all.py
```

**Output files:**
- `markets.csv` — All Polymarket markets with metadata
- `goldsky/orderFilled.csv` — Raw order events
- `processed/trades.csv` — Structured trade data

## AI Agent Framework: Polymarket/agents

```bash
# Clone
git clone https://github.com/Polymarket/agents.git
cd polymarket-agents

# Virtual env
virtualenv --python=python3.9 .venv
source .venv/bin/activate

# Install
pip install -r requirements.txt

# Config
cp .env.example .env
# Add: POLYGON_WALLET_PRIVATE_KEY, OPENAI_API_KEY

# CLI
python scripts/python/cli.py get-all-markets --limit 10
```

## API Libraries

```bash
# Read-only market data
pip install py-clob-client

# Full API with validation  
pip install polymarket-apis
```

## Weather Data

```bash
# Open-Meteo (no key needed)
curl "https://api.open-meteo.com/v1/forecast?latitude=40.78&longitude=-73.97&daily=temperature_2m_max&temperature_unit=fahrenheit&timezone=America/New_York"
```

## HuggingFace Datasets

- `tsinviking/polymarket_data_with_comments` — Historical Polymarket data
- `CK0607/polymarket_10000` — 10k market sample

## Build Order

1. Set up poly_data → Get historical trades for backtesting
2. Filter to weather markets → Build accuracy database
3. Compare forecast vs actual vs market → Quantify edge
4. Paper trade with refined model → Prove strategy
5. Deploy with Polymarket/agents → Live trading

---

*Clawdine 1.0 used these. Time to rebuild.*
