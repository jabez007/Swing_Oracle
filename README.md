# Swing_Oracle
Using Python and Machine Learning to identify trends in penny stocks and possible swing trades

## Resources
* [Intrinio Stock Screener API](http://docs.intrinio.com/?shell#securities-search-screener) for identifying stocks to train on and also make predictions on.
  * [Python source](https://github.com/intrinio/intrinio-realtime-python-sdk)
* [Alpha Vantage](https://www.alphavantage.co/) for gathering data on identified stocks.
  * [Python source](https://github.com/RomelTorres/alpha_vantage)

## Training
We will use the screener API to search for securities on the NYSE `Stock Exchange` that have `52 Week Low` >= $1.00 and `52 week high` <= $5.00
```
https://api.intrinio.com/securities/search?conditions=stock_exchange~eq~NYSE,52_week_low~gte~1.00,52_week_high~lte~5.00
```
to get out our list of ticker symbols.
With that list of tickers, we will go through each one to pull the last 100 days worth of data from Alpha Vantage
```
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={apikey}
```
And those 100 days will then be split on a `Sequence Size` of 20 to train our Recurrent Neural Network (LSTM)[https://machinelearningmastery.com/time-series-prediction-lstm-recurrent-neural-networks-python-keras/] model 

## Forecasting
Here we will again use the screener API to search for securities on the NYSE `Stock Exchange` that have `52 Week Low` >= $1.00 and `52 week high` <= $5.00
```
https://api.intrinio.com/securities/search?conditions=stock_exchange~eq~NYSE,52_week_low~gte~1.00,52_week_high~lte~5.00
```
to get out our list of ticker symbols, and with that list of tickers pull the last 100 days worths of data from Alpha Vantage
```
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={apikey}
```
From there, we will take only the last 20 days of data from each ticker to seed our model and run the forecast for the next 60 days. We will run the forecast 30 times for each ticker and create a distribution to then analyze for potential long term swing trades. 
