from prefect import task
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score
from sklearn.linear_model import LogisticRegression
import mlflow


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
