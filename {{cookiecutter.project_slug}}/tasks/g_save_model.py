{% if cookiecutter.data_load == "example" %}
import asyncio
import pickle
from concurrent.futures import ThreadPoolExecutor
from prefect import task
from sklearn.linear_model import LogisticRegression
import bentoml.sklearn

# Define a blocking function to save the model using BentoML
def blocking_bentoml_save_model(model: LogisticRegression):
    bentoml.sklearn.save_model("bank_model", model)

# Define a blocking function to save the model using pickle
def blocking_pickle_save_model(model: LogisticRegression):
    model_path = 'artifacts/model/bank_model.pkl'
    # Save the model using pickle
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)

# Define your async task using a thread pool executor for the blocking operations
@task
async def save_model(model: LogisticRegression):
    loop = asyncio.get_event_loop()
    executor = ThreadPoolExecutor()

    # Run both blocking functions in parallel
    await asyncio.gather(
        loop.run_in_executor(executor, blocking_bentoml_save_model, model),
        loop.run_in_executor(executor, blocking_pickle_save_model, model)
    )
{% endif %}