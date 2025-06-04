import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf


def download_data(ticker: str, start: str = "2018-01-01") -> pd.DataFrame:
    """Download daily data for a ticker using yfinance."""
    df = yf.download(ticker, start=start)
    if df.empty:
        raise ValueError(f"No data downloaded for {ticker}")
    return df


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["MA50"] = df["Adj Close"].rolling(window=50).mean()
    df["MA200"] = df["Adj Close"].rolling(window=200).mean()
    return df


def simulate_strategy(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Signal: 1 if 50 MA is above 200 MA
    df["Signal"] = 0
    df.loc[df["MA50"] > df["MA200"], "Signal"] = 1

    # Position is previous day's signal
    df["Position"] = df["Signal"].shift(1).fillna(0)

    # Daily returns
    df["Return"] = df["Adj Close"].pct_change()
    df["Strategy"] = df["Position"] * df["Return"]

    # Cumulative performance
    df["BuyHold_Cum"] = (1 + df["Return"]).cumprod()
    df["Strategy_Cum"] = (1 + df["Strategy"]).cumprod()

    return df


def plot_performance(df: pd.DataFrame, ticker: str) -> None:
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df["BuyHold_Cum"], label="Buy & Hold")
    plt.plot(df.index, df["Strategy_Cum"], label="MA Crossover")
    plt.title(f"{ticker} - Moving Average Crossover vs Buy & Hold")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.legend()
    plt.tight_layout()
    plt.show()


def main() -> None:
    ticker = "IWDA.DE"
    df = download_data(ticker)
    df = add_indicators(df)
    df = simulate_strategy(df)
    plot_performance(df, ticker)


if __name__ == "__main__":
    main()
