REGIME_WEIGHTS = {
    "Growth": {
        "XLK": 0.25,
        "XLY": 0.20,
        "XLI": 0.15,
        "XLF": 0.15,
        "XLE": 0.05,
        "XLV": 0.10,
        "XLP": 0.05,
        "XLU": 0.05
    },
    "Inflationary": {
        "XLE": 0.30,
        "XLF": 0.20,
        "XLI": 0.15,
        "XLP": 0.10,
        "XLU": 0.10,
        "XLV": 0.05,
        "XLK": 0.05,
        "XLY": 0.05
    },
    "Defensive": {
        "XLV": 0.25,
        "XLP": 0.25,
        "XLU": 0.20,
        "XLF": 0.10,
        "XLI": 0.08,
        "XLE": 0.05,
        "XLK": 0.04,
        "XLY": 0.03
    },
    "Mixed": {
        "XLK": 0.15,
        "XLF": 0.15,
        "XLE": 0.10,
        "XLV": 0.15,
        "XLI": 0.15,
        "XLP": 0.10,
        "XLU": 0.10,
        "XLY": 0.10
    }
}


def get_weights_for_regime(regime):
    return REGIME_WEIGHTS[regime]