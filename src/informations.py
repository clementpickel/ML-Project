import matplotlib.pyplot as plt
import pandas as pd

class Information:
    data = None
    csv_to_get = [
        "data/SE3_modified_csv/SE3_2016_entsoe.csv",
        "data/SE3_modified_csv/SE3_2017_entsoe.csv",
        "data/SE3_modified_csv/SE3_2018_entsoe.csv",
        "data/SE3_modified_csv/SE3_2019_entsoe.csv",
        "data/SE3_modified_csv/SE3_2020_entsoe.csv",
        "data/SE3_modified_csv/SE3_2021_entsoe.csv",
        "data/SE3_modified_csv/SE3_2022_entsoe.csv",
        "data/SE3_modified_csv/SE3_2023_entsoe.csv",
        "data/SE3_modified_csv/SE3_2024_entsoe.csv"
    ]

    def __init__(self):
        self.data = self.getData()
        self.data = self.handleMissing(self.data)

    def getData(self):
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
    
    def handleMissing(self, data):
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
    
if __name__ == "__main__":
    information = Information()
    df = information.data
    # print(df.to_string())
    information.draw(df, startdate="2024-09-01 00:00:00")
