
{% if cookiecutter.data_load == "example" %}
import bentoml
import numpy as np
from bentoml.io import NumpyNdarray
from typing import List
import random

# Define the service outside of any function, at the module level
svc = bentoml.Service("bank_model_service")

def get_previous_model(model_name: str) -> str:
    model_versions = bentoml.models.list(model_name)
    sorted_models = sorted(model_versions, key=lambda m: m.info.creation_time)

    if len(sorted_models) < 2:
        raise ValueError("Not enough model versions to select the previous one.")

    return sorted_models[-2].tag  # Get the tag of the second latest model

# Load the models at module level
model_a = bentoml.sklearn.load_model("bank_model:latest")
model_b = bentoml.sklearn.load_model(get_previous_model("bank_model"))

@svc.api(input=NumpyNdarray(), output=NumpyNdarray())
async def model_a_predict(input_data: np.ndarray):
    prediction = model_a.predict(input_data)
    return prediction

@svc.api(input=NumpyNdarray(), output=NumpyNdarray())
async def model_b_predict(input_data: np.ndarray):
    prediction = model_b.predict(input_data)
    return prediction

@svc.api(input=NumpyNdarray(), output=NumpyNdarray())
async def predict_ab_test(input_data: np.ndarray):
    # Define AB testing strategy, e.g., 50% traffic to model_a, 50% to model_b
    if random.random() < 0.5:
        prediction = model_a.predict(input_data)
    else:
        prediction = model_b.predict(input_data)
    return prediction

{% endif %}

'''
# Framework-specific imports
{% if cookiecutter.ml_framework == "tensorflow" %}
import tensorflow as tf
model = bentoml.tensorflow.load_model("bank_model")
{% elif cookiecutter.ml_framework == "torch" %}
import torch
model = bentoml.torch.load_model("bank_model)
{% elif cookiecutter.ml_framework == "sklearn" %}
from sklearn.externals import joblib
model = bentoml.sklearn.load_model("bank_model")
{% else %}
# Add your custom model lowading here
model = None  # Replace with actual model loading
{% endif %}
'''

