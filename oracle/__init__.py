from data import DAILY, TimeSeries
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.layers import Activation, Dense, Dropout, LSTM
from keras.models import Sequential, load_model
import numpy
import os
from . import Plot
from pprint import pprint

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  # disable the verbose output from TensorFlow starting up

_oracle_path_ = os.path.dirname(os.path.realpath(__file__))
_oracle_checkpoint_format_ = "model-{epoch:02d}-{accuracy:.4f}.hdf5"

EPOCHS = 50
BATCH_SIZE = 128


def _format_input_output_(data, input_size=20, output_size=1):
    """
    formats the time series data for a ticker symbol into the X and Y for a LSTM model
    :param data: {
                        "ABC": {
                            "2018-06-17": {
                            },
                            "2018-06-18": {
                            }
                        },
                        "DEF": {
                            "2018-06-17": {
                            },
                            "2018-06-18": {
                            }
                        }
                     }
    :return: x and y for the input and output of a LSTM model
    """
    print("-- Formatting time series data for LSTM model")
    x, y = list(), list()
    for symbol, _data in data.items():
        _x, _y = _data.get_input_output(input_size, output_size)
        x += _x
        y += _y
    return numpy.array(x), numpy.array(y)


def _build_model_(inputs, 
                  output_size=1, neurons=512, activation_function="tanh", dropout=0.3, loss="mape", optimizer="adam"):
    """
    define the LSTM model. Load the network weights from a previous run if available.
    https://www.kaggle.com/pablocastilla/predict-stock-prices-with-lstm
    https://dashee87.github.io/deep%20learning/python/predicting-cryptocurrency-prices-with-deep-learning/
    https://medium.com/@siavash_37715/how-to-predict-bitcoin-and-ethereum-price-with-rnn-lstm-in-keras-a6d8ee8a5109
    :param inputs:
    :param output_size:
    :param neurons:
    :param activation_function:
    :param dropout:
    :param loss:
    :param optimizer:
    :return:
    """
    print("-- Building LSTM model")
    # load previous model if it exists
    accuracy = 0
    filename = ""
    for f in os.listdir(_oracle_path_):
        if f.endswith('.hdf5'):
            if float(os.path.splitext(f)[0].split('-')[2]) > accuracy:
                filename = f
    if filename != "":
        print("checkpoint file: " + filename)
        model = load_model(os.path.join(_oracle_path_, filename))
    else:
        model = Sequential()
        model.add(LSTM(neurons, 
                       input_shape=(inputs.shape[1], inputs.shape[2]), 
                       return_sequences=True,
                       activation=activation_function))
        model.add(Dropout(dropout))
        model.add(LSTM(neurons, 
                       return_sequences=True,
                       activation=activation_function))
        model.add(Dropout(dropout))
        model.add(LSTM(neurons,
                       activation=activation_function))
        model.add(Dropout(dropout))
        model.add(Dense(units=output_size))
        model.add(Activation(activation_function))
        model.compile(loss=loss, optimizer=optimizer, metrics=['accuracy'])
    
    model.summary()
    return model


_x_, _y_ = _format_input_output_(DAILY)
_model_ = _build_model_(_x_)


def train():
    """

    :return:
    """
    # define the checkpoint
    checkpoint = ModelCheckpoint(os.path.join(_oracle_path_, _oracle_checkpoint_format_),
                                 monitor='accuracy',
                                 verbose=2,  # This gives you one output per epoch.
                                 save_best_only=True,
                                 mode='max')
    early_stop = EarlyStopping(monitor='accuracy', 
                               patience=5,
                               mode='max')
    
    callbacks_list = [checkpoint, early_stop]

    # fit the model
    _model_.fit(_x_, _y_, epochs=EPOCHS, batch_size=BATCH_SIZE, callbacks=callbacks_list)  # Tune the batch size

    
def get_forecast(symbol):
    """

    :param symbol:
    :return:
    """
    if symbol in DAILY.keys():
        _seed = DAILY[symbol].get_seed(SEQUENCE_LEN)
        seed = numpy.array([_seed])
        if len(seed.shape) == 3 and seed.shape[1] == 20:
            _forecast = _model_.predict(seed, verbose=0)
            # pprint(_forecast[0])
            return TimeSeries.from_forecast(symbol, _forecast[0])
