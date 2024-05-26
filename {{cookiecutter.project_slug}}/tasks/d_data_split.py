{% if cookiecutter.data_load == "example" %}
from prefect import task
import pandas as pd
from sklearn.model_selection import train_test_split


@task
def data_split(bank_df: pd.DataFrame):
    # Splitting data into training and testing sets
    X = bank_df.drop(["Exited"], axis=1)
    y = bank_df.Exited

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=125
    )
    return X_train, X_test, y_train, y_test


{% endif %}
'''
@task
def data_split(bank_df: pd.DataFrame):
    # Splitting data into training and testing sets
    X = df.drop(["y"], axis=1)
    y = df.y
    X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=125
    return X_train, X_test, y_train, y_test
'''