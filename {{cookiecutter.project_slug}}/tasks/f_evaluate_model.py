{% if cookiecutter.data_load == "example" %}
import json
import os
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score
from prefect import task
import mlflow

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