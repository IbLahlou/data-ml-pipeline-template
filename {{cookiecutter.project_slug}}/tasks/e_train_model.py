from prefect import task
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, log_loss
import mlflow


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
