from prefect import task
import pandas as pd



@task
def load_data(filename: str):
    print("load_data task executed")
    bank_df = pd.read_csv(filename, index_col="id", nrows=1000)
    bank_df = bank_df.drop(["CustomerId", "Surname"], axis=1)
    bank_df = bank_df.sample(frac=1)
    return bank_df
# Add your task execution logic here
