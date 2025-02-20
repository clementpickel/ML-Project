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
        combined_df = pd.concat(
            [pd.read_csv(file, na_values=["n/e"]) for file in self.csv_to_get],
            ignore_index=True
        )
        return combined_df
    
    def handleMissing(self, data):
        data["Currency"] = data["Currency"].fillna("EUR") # replace missing value by EUR in Currency
        data["Day-ahead Price [EUR/MWh]"] = data["Day-ahead Price [EUR/MWh]"].interpolate(method="linear", limit_area="inside") # replace missing values
        data = data.dropna(subset=["Day-ahead Price [EUR/MWh]"]) # remove column with missing values
        return data
    
if __name__ == "__main__":
    information = Information()
    df = information.data
    print(df.to_string())
