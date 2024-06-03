{% if cookiecutter.data_load == "example" %}
import pandas as pd
import numpy as np
from prefect import flow, task
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, log_loss
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, OrdinalEncoder
import bentoml
from bentoml.io import NumpyNdarray
import mlflow
import requests
import os
import json

@task
def evaluate_model(y_test, prediction: pd.DataFrame, metrics_file: str = 'artifacts/metrics.json'):
    accuracy = accuracy_score(y_test, prediction)
    f1 = f1_score(y_test, prediction, average="macro")

    metrics = {
        "accuracy": accuracy,
        "f1_score": f1
    }

    # Ensure the artifacts directory exists
    os.makedirs(os.path.dirname(metrics_file), exist_ok=True)

    with open(metrics_file, 'w') as file:
        json.dump(metrics, file)

    print("Accuracy:", str(round(accuracy, 2) * 100) + "%", "F1:", round(f1, 2))

    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("f1_score", f1)

@task
def get_prediction(X_test, model: LogisticRegression):
    return model.predict(X_test)


{% endif %}

'''
@task
def evaluate_model(y_test, prediction: pd.DataFrame, metrics_file: str = 'artifacts/metrics.json'):
    accuracy = accuracy_score(y_test, prediction)
    f1 = f1_score(y_test, prediction, average="macro")

    metrics = {
        "accuracy": accuracy,
        "f1_score": f1
    }

    # Ensure the artifacts directory exists
    os.makedirs(os.path.dirname(metrics_file), exist_ok=True)

    with open(metrics_file, 'w') as file:
        json.dump(metrics, file)

    print("Accuracy:", str(round(accuracy, 2) * 100) + "%", "F1:", round(f1, 2))

    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("f1_score", f1)
'''
