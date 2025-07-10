import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

# 포트폴리오 구성
tickers = {
    'VTI': 0.30,  # US Stocks
    'TLT': 0.40,  # Long-term Treasuries
    'IEF': 0.15,  # Intermediate-term Treasuries
    'GLD': 0.075, # Gold
    'DBC': 0.075  # Commodities
}

start_date = '2006-01-01'  # DBC 데이터는 2006년부터 이용 가능
end_date = '2024-12-31'

# S&P 500 ETF
spy = yf.download("SPY", start=start_date, end=end_date, progress=False)["Adj Close"]

# All Weather Portfolio
price_data = pd.DataFrame()

for ticker in tickers:
    price_data[ticker] = yf.download(ticker, start=start_date, end=end_date, progress=False)["Adj Close"]

# 월별 리턴 -> 연도별 리턴
returns = price_data.resample('Y').last().pct_change().dropna()
spy_returns = spy.resample('Y').last().pct_change().dropna()

# 포트폴리오 수익률 계산
awp_returns = (returns * pd.Series(tickers)).sum(axis=1)

# 누적 수익률
awp_cum = (1 + awp_returns).cumprod()
spy_cum = (1 + spy_returns).cumprod()

# 그래프
plt.figure(figsize=(12, 6))
plt.plot(awp_cum.index.year, awp_cum.values, label='All Weather Portfolio', linewidth=2)
plt.plot(spy_cum.index.year, spy_cum.values, label='S&P 500 (SPY)', linewidth=2)
plt.title('All Weather Portfolio vs S&P 500 (Yearly Cumulative Return)')
plt.xlabel('Year')
plt.ylabel('Cumulative Growth (Base = 1.0)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
