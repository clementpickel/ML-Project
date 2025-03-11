import matplotlib.pyplot as plt
import pandas as pd
import glob
import os

class Information:
    data = None
    csv_to_get = [f"data/SE3_modified_csv/SE3_{year}_entsoe.csv" for year in range(2024, 2025)]

    # get param 1/4/10
    # Hourly data
    # 1  = Air temperature, once/hour (mean), not enough data
    # 4  = Wind speed,      once/hour (mean), not enough data
    # 10 = Sunshine time,   once/hour
    # 21 = Wind speed town,  once/hour

    # Daily data
    # 2  = Air temperature, once/day (mean), at 00:00 hrs.
    # 5  = Precipitation,   once/day (sum of 24 hours), at 06:00 a.m.
    # 8	 = Snow depth,      once/day, at 06:00 am
    hourly_weather_csv = [
        "data/smhi_data_2022-today/parameter_1",
        "data/smhi_data_2022-today/parameter_10",
        "data/smhi_data_2022-today/parameter_21",
    ]

    daily_weather_csv = [
        "data/smhi_data_2022-today/parameter_2",
        "data/smhi_data_2022-today/parameter_5",
        "data/smhi_data_2022-today/parameter_8",
    ]

    def __init__(self):
        self.data = self.getElectricityData()
        self.data = self.handleElectricityMissing(self.data)

    def getElectricityData(self):
        df = pd.concat(
            [pd.read_csv(file, na_values=["n/e"]) for file in self.csv_to_get],
            ignore_index=True
        )

        # divide Time in two column
        df['StartTime'] = df['MTU (CET/CEST)'].apply(lambda x: x.split(" - ")[0])
        df['EndTime'] = df['MTU (CET/CEST)'].apply(lambda x: x.split(" - ")[1])
        df['StartTime'] = pd.to_datetime(df['StartTime'], format="%d.%m.%Y %H:%M")
        df['EndTime'] = pd.to_datetime(df['EndTime'], format="%d.%m.%Y %H:%M")
        return df
    
    def handleElectricityMissing(self, data):
        data["Currency"] = data["Currency"].fillna("EUR") # replace missing value by EUR in Currency
        data["Day-ahead Price [EUR/MWh]"] = data["Day-ahead Price [EUR/MWh]"].interpolate(method="linear", limit_area="inside") # replace missing values
        data = data.dropna(subset=["Day-ahead Price [EUR/MWh]"]) # remove column with missing values
        return data
    
    def draw(self, df, startdate="2016-01-01 00:00:00"):
        import pandas as pd
        startdate = pd.to_datetime(startdate)
        df_filtered = df[df['StartTime'] >= startdate]
        
        plt.figure(figsize=(15, 9))
        plt.plot(df_filtered['StartTime'], df_filtered['Day-ahead Price [EUR/MWh]'], marker='.', linestyle='-')
        plt.xlabel('Time')
        plt.ylabel('Day-ahead Price [EUR/MWh]')
        plt.title('Day-ahead Electricity Price Over Time')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def getWeatherData(self):
        df = pd.DataFrame()

        for csv_folder in self.hourly_weather_csvweather_csv:
            csv_files = glob.glob(os.path.join(csv_folder, "*.csv"))
            df_list = [pd.read_csv(file) for file in csv_files]
            if not df_list:
                continue
            merged_df = pd.concat(df_list, ignore_index=True)
                
            data_col = merged_df.columns[2]
            merged_df['Datetime'] = pd.to_datetime(
                merged_df['Datum'] + " " + merged_df['Tid (UTC)'], errors='coerce'
            )
            merged_df = merged_df.dropna(subset=['Datetime'])
            merged_df = merged_df.groupby('Datetime', as_index=False)[data_col].mean()

            if df.empty:
                df = merged_df
            else:
                df = pd.merge(df, merged_df, on='Datetime', how='outer')

        df.sort_values('Datetime', inplace=True)
        df.to_csv("df.csv", index=False)
        return df

if __name__ == "__main__":
    information = Information()
    df = information.getWeatherData()
    df.to_csv("df.csv")