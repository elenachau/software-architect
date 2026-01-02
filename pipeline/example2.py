import sqlite3
import pandas as pd


# 1. read data from csv file
def read_csv(file_name: str) -> pd.DataFrame:
    df = pd.read_csv(file_name)
    return df


# 2. data cleaning
def clean_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    # remove rows where Age or Salary is missing
    dataframe.dropna(subset=["Age", "Salary"], inplace=True)
    return dataframe


# 3. data transformation
def transform_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    # add new column
    dataframe["Salary_per_Age"] = dataframe["Salary"] / dataframe["Age"]
    return dataframe


# 4. store in SQLite db
def store_in_sqlite(dataframe: pd.DataFrame, db_name: str, table_name: str) -> None:
    conn = sqlite3.connect(db_name)
    dataframe.to_sql(table_name, conn, if_exists="replace", index=False)


# pipeline func
def data_processing_pipeline(file_name: str, db_name: str, table_name: str) -> None:
    data = read_csv(file_name)
    steps = [clean_data, transform_data]

    for step in steps:
        data = step(data)

    print(data)

    store_in_sqlite(data, db_name, table_name)


def main() -> None:
    file_name = "data.csv"
    db_name = "sample.db"
    table_name = "EmployeeData"

    data_processing_pipeline(file_name, db_name, table_name)


if __name__ == "__main__":
    main()
