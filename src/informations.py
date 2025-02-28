import matplotlib.pyplot as plt
import pandas as pd
import glob
import os

class Information:
    data = None
    csv_to_get = [f"data/SE3_modified_csv/SE3_{year}_entsoe.csv" for year in range(2016, 2025)]

    # get param 1/4/10
    # Hourly data
    # 1  = Air temperature, once/hour (mean), not enough data
    # 4  = Wind speed,      once/hour (mean), not enough data
    # 10 = Sunshine time,   once/hour

    # Daily data
    # 2  = Air temperature, once/day (mean), at 00:00 hrs.
    # 5  = Precipitation,   once/day (sum of 24 hours), at 06:00 a.m.
    # 8	 = Snow depth,      once/day, at 06:00 am
    weather_csv = [
        "data/smhi_data_2022-today/parameter_2",
        "data/smhi_data_2022-today/parameter_5",
        "data/smhi_data_2022-today/parameter_8",
        "data/smhi_data_2022-today/parameter_10",
    ]

    def __init__(self):
        self.data = self.getElectrcityData()
        self.data = self.handleElectricityMissing(self.data)

    def getElectrcityData(self):
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

    def getHourlyWeatherData(self):
        folder_path = "data/smhi_data_2022-today/parameter_1"

        csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
        df_list = [pd.read_csv(file) for file in csv_files]
        merged_df = pd.concat(df_list, ignore_index=True)
    
        data_column = merged_df.columns[2]
        merged_df['Datetime'] = pd.to_datetime(merged_df['Datum'] + " " + merged_df['Tid (UTC)'])
        merged_df = (
            merged_df.groupby(['Datum', 'Tid (UTC)'], as_index=False)
            .agg({data_column: 'mean'})
        )
        merged_df.to_csv("merged_data.csv", index=False)
        return merged_df

if __name__ == "__main__":
    information = Information()
    df = information.getHourlyWeatherData()