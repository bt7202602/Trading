import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

TICKER = "URTH"  # iShares MSCI World ETF
START_DATE = "2018-01-01"
END_DATE = None  # up to today
SHORT_WINDOW = 50
LONG_WINDOW = 200


def download_data(ticker: str, start: str, end: str = None) -> pd.DataFrame:
    """Download daily historical data for a ticker using yfinance."""
    t = yf.Ticker(ticker)
    df = t.history(start=start, end=end)
    # Remove timezone information for easier handling
    df.index = df.index.tz_localize(None)
    return df


def generate_signals(df: pd.DataFrame) -> pd.DataFrame:
    """Create moving average crossover signals."""
    df = df.copy()
    df["short_ma"] = df["Close"].rolling(window=SHORT_WINDOW).mean()
    df["long_ma"] = df["Close"].rolling(window=LONG_WINDOW).mean()
    df["position"] = (df["short_ma"] > df["long_ma"]).astype(int)
    return df


def apply_strategy(df: pd.DataFrame) -> pd.DataFrame:
    """Simulate strategy and buy & hold returns."""
    df = df.copy()
    df["returns"] = df["Close"].pct_change()
    df["strategy_returns"] = df["returns"] * df["position"].shift(1)
    df.dropna(subset=["short_ma", "long_ma"], inplace=True)
    df["buy_hold"] = (1 + df["returns"].fillna(0)).cumprod()
    df["strategy"] = (1 + df["strategy_returns"].fillna(0)).cumprod()
    base = 1000 / df[["buy_hold", "strategy"]].iloc[0]
    df["buy_hold"] *= base["buy_hold"]
    df["strategy"] *= base["strategy"]
    return df


def plot_results(df: pd.DataFrame) -> None:
    """Plot price, moving averages, and cumulative returns."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    ax1.plot(df.index, df["Close"], label="Close")
    ax1.plot(df.index, df["short_ma"], label=f"{SHORT_WINDOW}-day MA")
    ax1.plot(df.index, df["long_ma"], label=f"{LONG_WINDOW}-day MA")
    ax1.set_title(f"{TICKER} Price and Moving Averages")
    ax1.legend()

    ax2.plot(df.index, df["buy_hold"], label="Buy & Hold")
    ax2.plot(df.index, df["strategy"], label="MA Strategy")
    ax2.set_title("Cumulative Returns (rebased to 1000)")
    ax2.legend()

    plt.tight_layout()
    plt.show()


def print_table(df: pd.DataFrame) -> None:
    table = df[["strategy", "buy_hold"]].copy()
    table.index.name = "Date"
    print(table)


def main() -> None:
    data = download_data(TICKER, START_DATE, END_DATE)
    if data.empty:
        print("No data downloaded.")
        return

    data = generate_signals(data)
    data = apply_strategy(data)

    print_table(data)
    plot_results(data)


if __name__ == "__main__":
    main()
