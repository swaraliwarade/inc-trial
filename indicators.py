import pandas as pd
import ta

def compute_indicators(candles):
    df = pd.DataFrame(candles, columns=["time", "open", "high", "low", "close", "volume"])
    df["close"] = df["close"].astype(float)

    # RSI
    df["rsi"] = ta.momentum.RSIIndicator(df["close"], window=14).rsi()

    # EMA 12 & 26
    df["ema12"] = ta.trend.EMAIndicator(df["close"], window=12).ema_indicator()
    df["ema26"] = ta.trend.EMAIndicator(df["close"], window=26).ema_indicator()

    return df
