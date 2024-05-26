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

@task
def start_mlflow_server():
    mlflow_url = "http://localhost:5000"  # Update with your MLflow server URL if different
    try:
        response = requests.get(mlflow_url)
        if response.status_code != 200:
            raise ConnectionError("Could not connect to MLflow server.")
    except requests.ConnectionError:
        print("Starting MLflow server...")
        import subprocess
        subprocess.Popen(["mlflow", "server", "--host", "localhost", "--port", "5000"])

@task
def load_data(filename: str):
    bank_df = pd.read_csv(filename, index_col="id", nrows=1000)
    bank_df = bank_df.drop(["CustomerId", "Surname"], axis=1)
    bank_df = bank_df.sample(frac=1)
    return bank_df

@task
def preprocessing(bank_df: pd.DataFrame):
    cat_col = [1, 2]
    num_col = [0, 3, 4, 5, 6, 7, 8, 9]

    # Filling missing categorical values
    cat_impute = SimpleImputer(strategy="most_frequent")
    bank_df.iloc[:, cat_col] = cat_impute.fit_transform(bank_df.iloc[:, cat_col])

    # Filling missing numerical values
    num_impute = SimpleImputer(strategy="median")
    bank_df.iloc[:, num_col] = num_impute.fit_transform(bank_df.iloc[:, num_col])

    # Encode categorical features as an integer array.
    cat_encode = OrdinalEncoder()
    bank_df.iloc[:, cat_col] = cat_encode.fit_transform(bank_df.iloc[:, cat_col])

    # Scaling numerical values.
    scaler = MinMaxScaler()
    bank_df.iloc[:, num_col] = scaler.fit_transform(bank_df.iloc[:, num_col])
    return bank_df

@task
def data_split(bank_df: pd.DataFrame):
    # Splitting data into training and testing sets
    X = bank_df.drop(["Exited"], axis=1)
    y = bank_df.Exited

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=125
    )
    return X_train, X_test, y_train, y_test

@task
def train_model(X_train, X_test, y_train, y_test):
    mlflow.set_tracking_uri("http://localhost:5000")

    # Create or set the experiment
    experiment_name = "Bank Model Experiment"
    if not mlflow.get_experiment_by_name(experiment_name):
        mlflow.create_experiment(experiment_name)

    mlflow.set_experiment(experiment_name)

    # Selecting the best features
    KBest = SelectKBest(chi2, k="all")
    X_train = KBest.fit_transform(X_train, y_train)
    X_test = KBest.transform(X_test)

    model = LogisticRegression(max_iter=1000, random_state=125)

    with mlflow.start_run():
        model.fit(X_train, y_train)
        train_predictions = model.predict(X_train)
        train_loss = log_loss(y_train, train_predictions)
        train_accuracy = accuracy_score(y_train, train_predictions)

        mlflow.log_metric("train_loss", train_loss)
        mlflow.log_metric("train_accuracy", train_accuracy)

        return model

@task
def get_prediction(X_test, model: LogisticRegression):
    return model.predict(X_test)

@task
def evaluate_model(y_test, prediction: pd.DataFrame):
    accuracy = accuracy_score(y_test, prediction)
    f1 = f1_score(y_test, prediction, average="macro")

    print("Accuracy:", str(round(accuracy, 2) * 100) + "%", "F1:", round(f1, 2))

    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("f1_score", f1)

@task
def save_model(model: LogisticRegression):
    bentoml.sklearn.save_model("bank_model", model)


import os
import socket

def serve_model(port):
    # Check if the specified port is already in use
    def is_port_in_use(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0

    # Serve the model on the specified port if it is not already in use
    if not is_port_in_use(port):
        # Running the service in the background using '&' in the command
        os.system(f"bentoml serve service:svc --reload --port {port} &")
        print(f"Service started on port {port} in the background.")
    else:
        print(f"Port {port} is already in use. Service not started.")



@flow(log_prints=True)
def ml_workflow(filename: str = "train.csv"):
    start_mlflow_server()
    data = load_data(filename)
    prep_data = preprocessing(data)
    X_train, X_test, y_train, y_test = data_split(prep_data)
    model = train_model(X_train, X_test, y_train, y_test)
    predictions = get_prediction(X_test, model)
    evaluate_model(y_test, predictions)
    save_model(model=model)
    

if __name__ == "__main__":
    ml_workflow()
    serve_model(port=3000)
