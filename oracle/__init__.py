from data import DAILY
from keras.callbacks import ModelCheckpoint
from keras.layers import Dense, Dropout, LSTM
from keras.models import Sequential
import os
import numpy

_oracle_path_ = os.path.dirname(os.path.realpath(__file__))
_oracle_checkpoint_format_ = "weights-{epoch:02d}-{loss:.4f}.hdf5"

SEQUENCE_LEN = 20
HIDDEN_LAYER = 2048
EPOCHS = 100
BATCH_SIZE = 64


def _format_daily_data_(raw_json):
    """
    formats the time series data for a ticker symbol into the X and Y for a LSTM model
    :param raw_json: {
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
    print("formatting time series data for LSTM model")
    x, y = list(), list()

    for symbol, dates in raw_json.items():
        _x, _y = list(), list()
        for date, data in dates.items():
            if len(_x) < SEQUENCE_LEN:
                _x += [[float(data["1. open"]) / 25.00,
                       float(data["2. high"]) / 25.00,
                       float(data["3. low"]) / 25.00,
                       float(data["4. close"]) / 25.00,
                       int(data["5. volume"]) / 1000000000.0]]
                if len(_x) > 1:
                    _y += [[float(data["1. open"]) / 25.00,
                           float(data["2. high"]) / 25.00,
                           float(data["3. low"]) / 25.00,
                           float(data["4. close"]) / 25.00,
                           int(data["5. volume"]) / 1000000000.0]]

            else:
                x += [_x]

                _y += [[float(data["1. open"]) / 25.00,
                       float(data["2. high"]) / 25.00,
                       float(data["3. low"]) / 25.00,
                       float(data["4. close"]) / 25.00,
                       int(data["5. volume"]) / 1000000000.0]]
                y += [_y]

                _x = [[float(data["1. open"]) / 25.00,
                      float(data["2. high"]) / 25.00,
                      float(data["3. low"]) / 25.00,
                      float(data["4. close"]) / 25.00,
                      int(data["5. volume"]) / 1000000000.0]]
                _y = list()

    return numpy.array(x), numpy.array(y)


def _build_model_(x, y):
    """
    define the LSTM model. Load the network weights from a previous run if available
    :param x:
    :param y:
    :return:
    """
    print("building LSTM model")
    model = Sequential()
    model.add(LSTM(HIDDEN_LAYER, input_shape=(x.shape[1], x.shape[2]), return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(HIDDEN_LAYER, return_sequences=True))
    model.add(LSTM(HIDDEN_LAYER, return_sequences=True))
    model.add(Dense(y.shape[2], activation='softmax'))

    # load previous network weights
    loss = 10
    filename = ""
    for f in os.listdir(_oracle_path_):
        if f.endswith('.hdf5'):
            if float(os.path.splitext(f)[0].split('-')[2]) < loss:
                filename = f
    if filename != "":
        print("checkpoint file: " + filename)
        model.load_weights(filename)

    model.compile(loss='categorical_crossentropy', optimizer='adam')

    return model


def train():
    """

    :return:
    """
    x, y = _format_daily_data_(DAILY)
    model = _build_model_(x, y)

    # define the checkpoint
    checkpoint = ModelCheckpoint(os.path.join(_oracle_path_, _oracle_checkpoint_format_),
                                 monitor='loss',
                                 verbose=2,  # This gives you one output per epoch.
                                 save_best_only=True,
                                 mode='min')
    callbacks_list = [checkpoint]

    # fit the model
    model.fit(x, y, epochs=EPOCHS, batch_size=BATCH_SIZE, callbacks=callbacks_list)  # Tune the batch size
