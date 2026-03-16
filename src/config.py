SECTOR_ETFS = [
    "XLF",  # Financials
    "XLK",  # Technology
    "XLE",  # Energy
    "XLV",  # Healthcare
    "XLI",  # Industrials
    "XLP",  # Consumer Staples
    "XLU",  # Utilities
    "XLY"   # Consumer Discretionary
]

BENCHMARK = "SPY"

START_DATE = "2013-01-01"
END_DATE = "2026-01-01"

FRED_SERIES = {
    "cpi": "CPIAUCSL",       # Consumer Price Index
    "unrate": "UNRATE",      # Unemployment Rate
    "fedfunds": "FEDFUNDS",  # Federal Funds Rate
    "gs10": "GS10",          # 10-Year Treasury Rate
    "gs2": "GS2"             # 2-Year Treasury Rate
}

TRANSACTION_COST = 0.001
REBALANCE_FREQ = "M"