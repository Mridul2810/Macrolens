def add_regime_features(df):
    df = df.copy()

    df["inflation_yoy"] = df["cpi"].pct_change(12)
    df["yield_spread"] = df["gs10"] - df["gs2"]

    df["high_inflation"] = (
        df["inflation_yoy"] > df["inflation_yoy"].rolling(24).median()
    ).astype(int)

    df["inverted_curve"] = (df["yield_spread"] < 0).astype(int)

    df["high_rates"] = (
        df["fedfunds"] > df["fedfunds"].rolling(24).median()
    ).astype(int)

    return df


def classify_regime(row):
    if row["inverted_curve"] == 1 and row["high_inflation"] == 1:
        return "Defensive"
    elif row["high_inflation"] == 1 and row["high_rates"] == 1:
        return "Inflationary"
    elif row["inverted_curve"] == 0 and row["high_rates"] == 0:
        return "Growth"
    else:
        return "Mixed"


def assign_regimes(df):
    df = df.copy()
    df["regime"] = df.apply(classify_regime, axis=1)
    return df