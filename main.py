import data
import screener

print(screener.TICKERS[0]["ticker"])
print(len(screener.TICKERS))

print(data._download_daily_full_("AMD").items())
