from informations import Information
import pandas as pd
from pmdarima import auto_arima
import matplotlib.pyplot as plt

from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

from sklearn.metrics import mean_squared_error

def is_stationnary(data):
    adf_test = adfuller(data['Day-ahead Price [EUR/MWh]'])
    # Output the results
    print('ADF Statistic: %f' % adf_test[0])
    print('p-value: %f' % adf_test[1])
    if adf_test[1] < 0.05:
        print('The data is stationary')

def plot_autocorrelation(data):
    plot_acf(data['Day-ahead Price [EUR/MWh]'], lags=40)
    plot_pacf(data['Day-ahead Price [EUR/MWh]'], lags=40)
    plt.show()

def test(data):
    # Split the data into train and test
    train_size = int(len(data) * 0.9)
    train, test = data[0:train_size], data[train_size:len(data)]

    # Fit the ARIMA model on the training dataset
    model_train = ARIMA(train['Day-ahead Price [EUR/MWh]'], order=(24, 0, 1))
    model_train_fit = model_train.fit()

    # Forecast on the test dataset
    test_forecast = model_train_fit.get_forecast(steps=len(test))
    print(test_forecast.summary_frame())
    test_forecast_series = pd.Series(test_forecast.predicted_mean, index=test.index)

    # Calculate the mean squared error
    mse = mean_squared_error(test['Day-ahead Price [EUR/MWh]'], test_forecast_series)
    rmse = mse**0.5

    # Create a plot to compare the forecast with the actual test data
    plt.figure(figsize=(14,7))
    plt.plot(train['Day-ahead Price [EUR/MWh]'], label='Training Data')
    plt.plot(test['Day-ahead Price [EUR/MWh]'], label='Actual Data', color='orange')
    plt.plot(test_forecast_series, label='Forecasted Data', color='green')
    plt.fill_between(test.index,
                    test_forecast.conf_int().iloc[:, 0],
                    test_forecast.conf_int().iloc[:, 1],
                    color='k', alpha=.15)
    plt.title('ARIMA Model Evaluation')
    plt.xlabel('Date')
    plt.ylabel('Electricity Price')
    plt.legend()
    plt.show()

    print('RMSE:', rmse)

if __name__ == "__main__":
    information = Information()
    df = information.data
    df.to_csv("df.csv", index=False)

    is_stationnary(df)
    plot_autocorrelation(df)
    test(df)