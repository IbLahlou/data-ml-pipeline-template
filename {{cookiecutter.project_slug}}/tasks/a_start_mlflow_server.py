from prefect import task
import mlflow
import requests
import subprocess

@task
def start_mlflow_server():
    mlflow_url = "http://localhost:5000"
    try:
        response = requests.get(mlflow_url)
        if response.status_code != 200:
            raise ConnectionError("Could not connect to MLflow server.")
    except requests.ConnectionError:
        print("Starting MLflow server...")
        subprocess.Popen(["mlflow", "server", "--host", "localhost", "--port", "5000"])
    print("start_mlflow_server task executed")
