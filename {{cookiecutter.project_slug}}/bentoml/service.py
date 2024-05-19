import bentoml
from bentoml.io import NumpyNdArray
import numpy as np

# Framework-specific imports
{% if cookiecutter.ml_framework == "tensorflow" %}
import tensorflow as tf
model = bentoml.tensorflow.load_model("path/to/your/model")
{% elif cookiecutter.ml_framework == "torch" %}
import torch
model = bentoml.torch.load_model("path/to/your/model")
{% elif cookiecutter.ml_framework == "sklearn" %}
from sklearn.externals import joblib
model = bentoml.sklearn.load_model("path/to/your/model")
{% else %}
# Add your custom model lowading here
model = None  # Replace with actual model loading
{% endif %}

service = bentoml.Service("{{cookiecutter.project_slug}}", runners=[
    bentoml.Runner(model)
])

@service.api(input=NumpyNdArray(), output=NumpyNdArray())
def predict(input_data: np.ndarray) -> np.ndarray:
    results = model.predict(input_data)
    return results
