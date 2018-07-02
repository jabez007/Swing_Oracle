# Swing_Oracle
Using Python and Machine Learning to identify trends in small cap stocks
under $25 and possible [swing trades](https://www.eatsleeptrade.net/my-swing-trading-strategies)

## Resources
* [Intrinio Stock Screener API](http://docs.intrinio.com/?shell#securities-search-screener)
    for identifying stocks to train on and also make predictions on.
  * [Python source](https://github.com/intrinio/python-sdk)
* [Alpha Vantage](https://www.alphavantage.co/) for gathering data on
    identified stocks.
  * [Python source](https://github.com/RomelTorres/alpha_vantage)
* [Deep Learning with Keras](https://app.pluralsight.com/library/courses/keras-deep-learning/table-of-contents)
  * [TensorFlow: Getting Started](https://app.pluralsight.com/library/courses/tensorflow-getting-started/table-of-contents)

## Outline

### Training
We will use the screener API to search for securities that have 
a `52 Week Low` >= $1.00 and a `52 Week High` <= $25.00, 
with a `Market Capitalization` between $300,000,000 and
$2,000,000,000, and an `Average Daily Volume` over 500,000
```
https://api.intrinio.com/securities/search?conditions=52_week_low~gte~1.00,52_week_high~lte~25.00,marketcap~gte~300000000,marketcap~lte~2000000000,average_daily_volume~gte~500000
```
to get out our list of ticker symbols.
With that list of tickers, we will go through each one to pull the last
100 days worth of data from Alpha Vantage
```
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={apikey}
```
And those 100 days will then be split on a `Sequence Size` of 20 to
train our Recurrent Neural Network [LSTM](https://dashee87.github.io/deep%20learning/python/predicting-cryptocurrency-prices-with-deep-learning/) model

### Forecasting
Here we will again use the screener API to search for securities that 
have a `52 Week Low` >= $1.00 and a `52 Week High` <= $25.00 with
a `Market Capitalization` between $300,000,000 and $2,000,000,000, and 
an `Average Daily Volume` over 500,000
```
https://api.intrinio.com/securities/search?conditions=52_week_low~gte~1.00,52_week_high~lte~25.00,marketcap~gte~300000000,marketcap~lte~2000000000,average_daily_volume~gte~500000
```
to get out our list of ticker symbols, and with that list of tickers
pull the last 100 days worths of data from Alpha Vantage
```
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={apikey}
```
From there, we will take only the last 20 days of data from each ticker
to seed our model and run a forecast for the next 20 days. We will then
plot and analyze the forecasts looking for potential [long term swing trades](http://www.swing-trade-stocks.com/trading-strategy.html).

## Technical

### Training
* [Predict Bitcoin and Ethereum price with LSTM in Keras](https://medium.com/@siavash_37715/how-to-predict-bitcoin-and-ethereum-price-with-rnn-lstm-in-keras-a6d8ee8a5109)

#### [Number of Layers](https://www.heatonresearch.com/2017/06/01/hidden-layers.html)
* 2 -> Can represent an arbitrary decision boundary to arbitrary accuracy with rational activation functions and can approximate any smooth mapping to any accuracy.
* **>2 -> Additional layers can learn complex representations (sort of automatic feature engineering) for layer layers.**

#### [Number of Neurons](https://www.heatonresearch.com/2017/06/01/hidden-layers.html)
* The number of hidden neurons should be between the size of the input layer and the size of the output layer.
* The number of hidden neurons should be 2/3 the size of the input layer, plus the size of the output layer.
* The number of hidden neurons should be less than twice the size of the input layer.

Since our input is going to be (20, 5) and our output is (1, 5), it seems like our number of neurons should be in the 128 to 256 range.
We can bump up the number of neurons to the 512 to 1024 range as long as we include `Dropout` layers to avoid overfitting.

#### [Activation Function](https://datascience.stackexchange.com/questions/14349/difference-of-activation-functions-in-neural-networks-in-general)
* linear
* tanh -> squashes a real-valued number to the range [-1, 1] so its output is zero-centered.
* ReLU ([leaky Rectified Linear Unit](https://medium.com/@huangkh19951228/predicting-cryptocurrency-price-with-tensorflow-and-keras-e1674b0dc58a)) -> this function computes f(x)=1(x<0)(αx)+1(x>=0)(x) where α is a small constant.

#### [loss](https://keras.io/losses/)
* mean squared error (mse) ->
* mean absolute error (mae) ->
* mean absolute percentage error (mape) -> we want to minimize the percentages that our true is off from our prediction

#### [optimizer](https://keras.io/optimizers/)
* adam
