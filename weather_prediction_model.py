from meteostat import Hourly, Stations
from datetime import datetime
import pandas as pd
import keras
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from keras.models import Model
from keras.layers import LSTM, Dense, Bidirectional, Dropout, Input, Attention, Concatenate
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping

#Start and end dates for data collection 
start_date = datetime(2023, 11, 21)
end_date = datetime(2025, 5, 21)

#Coordinates of current location
lat = 42.36
lon = -71.05

stations = Stations()

boston_station = stations.nearby(lat, lon).fetch(1)

data = Hourly(boston_station, start_date, end_date)
df = data.fetch()

modified_df = df[['temp', 'prcp', 'rhum', 'wspd', 'pres', 'dwpt']].copy()

#Interpolate missing values for percipitation using a spline method
modified_df.loc[:, 'prcp'] = modified_df['prcp'].interpolate(method='spline', order=3)

#Log transformation on precipitation
modified_df['prcp'] = np.log1p(modified_df['prcp'])

#Normalize the data
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(modified_df)

def create_sequences(data, input_len=96, output_len=6):
    X, y = [], []
    for i in range(len(data) - input_len - output_len):
        X.append(data[i:i+input_len])
        y.append(data[i+input_len:i+input_len+output_len])
    return np.array(X), np.array(y)

X, y = create_sequences(scaled_data, 168, 6)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Early stopping to prevent overfitting 
early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=10,
    min_delta = 1e-4,
    restore_best_weights=True
)

"""
model = Sequential([
    Input(shape=(168, X.shape[2])),
    Bidirectional(LSTM(128, return_sequences=True)),
    Dropout(0.2),
    Bidirectional(LSTM(64, return_sequences=True)),
    Dropout(0.2),
    Bidirectional(LSTM(32)),
    Dense(128, activation='relu'),
    Dropout(0.2),
    Dense(6 * X.shape[2])
])
"""
input_sequence = Input(shape=(168, X.shape[2]))
x = Bidirectional(LSTM(128, return_sequences = True))(input_sequence)
x = Dropout(0.2)(x)
lstm_output = Bidirectional(LSTM(64, return_sequences = True))(x)

attention = Attention()([lstm_output, lstm_output])
context_vector = Concatenate(axis = -1)([lstm_output, attention])
context_vector = Dropout(0.2)(context_vector)

context_vector = LSTM(32)(context_vector)
x = Dense(128, activation = 'relu')(context_vector)
x = Dropout(0.2)(x)
output = Dense(6 * X.shape[2])(x)

model = Model(inputs = input_sequence, outputs = output)
model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
model.summary()

history = model.fit(X_train, y_train.reshape(y_train.shape[0], -1), 
                    epochs=100, batch_size=64, 
                    validation_split=0.2, callbacks = [early_stopping], verbose=1)

loss = model.evaluate(X_test, y_test.reshape(y_test.shape[0], -1))
print(f"Test MSE: {loss:.4f}")

plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title("Model Loss Over Epochs")
plt.xlabel("Epoch")
plt.ylabel("MSE Loss")
plt.legend()
plt.show()

#Predict using the last 96 hours from test set
pred = model.predict(X_test)

#Reshape predictions and actual values
pred_reshaped = pred.reshape(-1, 6, X.shape[2])
actual_reshaped = y_test

#Inverse transform on predictions and actuals
pred_inv = scaler.inverse_transform(pred_reshaped.reshape(-1, X.shape[2])).reshape(-1, 6, X.shape[2])
actual_inv = scaler.inverse_transform(actual_reshaped.reshape(-1, X.shape[2])).reshape(-1, 6, X.shape[2])

#Undo the log transformation done earlier on precipitation
pred_inv[:, :, 1] = np.expm1(pred_inv[:, :, 1])
actual_inv[:, :, 1] = np.expm1(actual_inv[:, :, 1])

sample_idx = 0
hours = range(6)
plt.figure(figsize=(12,5))
plt.subplot(1, 2, 1)
plt.plot(hours, actual_inv[sample_idx, :, 0], label='Actual Temp')
plt.plot(hours, pred_inv[sample_idx, :, 0], label='Predicted Temp')
plt.title('Temperature (°C) - Next 2 Hours')
plt.xlabel('Hours Ahead')
plt.ylabel('Temperature')
plt.legend()
plt.show()

#Check the mse of each feature
feature_names = modified_df.columns.tolist()
for i, name in enumerate(feature_names):
    mse = np.mean((pred_inv[:, :, i] - actual_inv[:, :, i]) ** 2)
    print(f"MSE for {name}: {mse:.4f}")

model.save("model.keras")
model.save_weights("model_weights.weights.h5")
