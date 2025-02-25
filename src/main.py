from informations import Information

if __name__ == "__main__":
    information = Information()
    df = information.data
    print(df.to_string())
    information.draw(df, startdate="2024-01-01 00:00:00")
