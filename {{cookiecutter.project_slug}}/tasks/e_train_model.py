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


def load_hparams(filename: str):
    with open(filename, 'r') as file:
        hparams = yaml.safe_load(file)
    return hparams

@task
def train_model(X_train, X_test, y_train, y_test, hparams_file: str = "artifacts/hparams.yml"):
    mlflow.set_tracking_uri("http://localhost:5000")

    # Create or set the experiment
    experiment_name = "Bank Model Experiment"
    if not mlflow.get_experiment_by_name(experiment_name):
        mlflow.create_experiment(experiment_name)

    mlflow.set_experiment(experiment_name)

    # Load hyperparameters
    hparams = load_hparams(hparams_file)

    # Selecting the best features
    KBest = SelectKBest(chi2, k=hparams['k_best'])
    X_train = KBest.fit_transform(X_train, y_train)
    X_test = KBest.transform(X_test)

    model = LogisticRegression(max_iter=hparams['max_iter'], random_state=hparams['random_state'])

    with mlflow.start_run():
        model.fit(X_train, y_train)
        train_predictions = model.predict(X_train)
        train_loss = log_loss(y_train, train_predictions)
        train_accuracy = accuracy_score(y_train, train_predictions)

        mlflow.log_metric("train_loss", train_loss)
        mlflow.log_metric("train_accuracy", train_accuracy)

        return model

{% endif %}
'''
import yaml
from prefect import task
import mlflow
#import feature selector
#import model
#import training metrics



@task
def train_model(X_train, X_test, y_train, y_test, hparams_file: str = "artifacts/hparams.yml"):
    mlflow.set_tracking_uri("http://localhost:5000")

    # Create or set the experiment
    experiment_name = "{{cookiecutter.experiment_name}}"
    if not mlflow.get_experiment_by_name(experiment_name):
        mlflow.create_experiment(experiment_name)

    mlflow.set_experiment(experiment_name)

    # Load hyperparameters
    hparams = load_hparams(hparams_file)



    model = The Model
    
    with mlflow.start_run():
        model.fit(X_train, y_train)
        train_predictions = model.predict(X_train)
        train_loss = log_loss(y_train, train_predictions)
        train_accuracy = accuracy_score(y_train, train_predictions)

        mlflow.log_metric("train_loss", train_loss)
        mlflow.log_metric("train_accuracy", train_accuracy)

        return model
'''
