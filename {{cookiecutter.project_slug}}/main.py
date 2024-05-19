from prefect import flow
from tasks import (
    start_mlflow_server,
    load_data,
    data_preprocessing,
    data_split,
    get_prediction,
    train_model,
    evaluate_model,
    save_model
)
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
        os.chdir("bentoml")
        os.system(f"bentoml serve service:svc --reload --port {port} &")
        print(f"Service started on port {port} in the background.")
    else:
        print(f"Port {port} is already in use. Service not started.")



@flow(log_prints=True)
def ml_workflow(filename: str = "data/train.csv"):
    start_mlflow_server()
    data = load_data(filename)
    prep_data = data_preprocessing(data)
    X_train, X_test, y_train, y_test = data_split(prep_data)
    model = train_model(X_train, X_test, y_train, y_test)
    predictions = get_prediction(X_test, model)
    evaluate_model(y_test, predictions)
    save_model(model=model)

if __name__ == "__main__":
    ml_workflow()
