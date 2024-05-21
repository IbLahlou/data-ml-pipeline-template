
from prefect import  task
from sklearn.linear_model import LogisticRegression
import bentoml
import pickle

@task
def save_model(model: LogisticRegression):
    bentoml.sklearn.save_model("bank_model", model)

    model_path = 'artifacts/model/bank_model.pkl'
    
    # Save the model using pickle
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
# Add your task execution logic here
