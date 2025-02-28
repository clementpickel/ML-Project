from informations import Information
import pandas as pd
from pmdarima import auto_arima
import matplotlib.pyplot as plt
import warnings
# warnings.filterwarnings(
#     "ignore",
#     category=FutureWarning,
#     message=".*'force_all_finite'.*",  # Regex to match the specific message
#     module="sklearn.utils.deprecation"
# )

if __name__ == "__main__":
    information = Information()
    df = information.data


    # print(df.to_string())
    # information.draw(df, startdate="2024-01-01 00:00:00")


    # # Convert to datetime and set as index
    # df['StartTime'] = pd.to_datetime(df['StartTime'])
    # df.set_index('StartTime', inplace=True)

    # # Check for duplicates
    # if df.index.has_duplicates:
    #     print("Found duplicate timestamps. Removing duplicates...")
    #     df = df[~df.index.duplicated(keep='first')]  # Keep first occurrence

    # # Ensure hourly frequency (fill missing values)
    # df = df.asfreq('h')
    # df['Day-ahead Price [EUR/MWh]'] = df['Day-ahead Price [EUR/MWh]'].interpolate()
    # train = df.iloc[:-336]
    # test = df.iloc[-336:]

    # model = auto_arima(
    #     train['Day-ahead Price [EUR/MWh]'],  # Use train if splitting
    #     seasonal=True,
    #     stepwise=True,
    #     suppress_warnings=True,
    #     trace=True
    # )
    # print(model.summary())

    # try:
    #     # Fit the model on the entire dataset (or train)
    #     model.fit(df['Day-ahead Price [EUR/MWh]'])  # Use df or train

    #     # Generate forecast
    #     forecast, conf_int = model.predict(
    #         n_periods=336,
    #         return_conf_int=True
    #     )

    #     # Create future datetime index
    #     future_dates = pd.date_range(
    #         df.index[-1] + pd.Timedelta(hours=1),
    #         periods=336,
    #         freq='H'
    #     )

    #     last_4_weeks_start = df.index[-1] - pd.Timedelta(weeks=4)

    #     # Filter historical data to show only the last 4 weeks

    #     # Plot
    #     plt.figure(figsize=(12, 6))
    #     plt.plot(df_last_4_weeks.index, df_last_4_weeks['Day-ahead Price [EUR/MWh]'], label='Historical (Last 4 Weeks)')
    #     plt.plot(future_dates, forecast, label='Forecast (Next 2 Weeks)', color='orange')
    #     plt.fill_between(
    #         future_dates,
    #         conf_int[:, 0],
    #         conf_int[:, 1],
    #         color='pink',
    #         alpha=0.3
    #     )
    #     plt.title('Last 4 Weeks vs Next 2 Weeks Forecast')
    #     plt.legend()
    #     plt.show()
    # except Exception as e:
    #     print(e)
