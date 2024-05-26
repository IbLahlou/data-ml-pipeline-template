# Depending on the data location
{% if cookiecutter.data_load == "example" %}

    
from prefect import task
import pandas as pd
import os
import zipfile
import requests


# this is just simple example for churn modeling
@task
def load_data(filename: str):
    print("load_data task executed")
    bank_df = pd.read_csv(filename, index_col="id", nrows=1000)
    bank_df = bank_df.drop(["CustomerId", "Surname"], axis=1)
    bank_df = bank_df.sample(frac=1)
    return bank_df
# Add your task execution logic here


{% elif cookiecutter.data_load == "secure download" %}

from prefect import task
import pandas as pd
import os
import zipfile
import requests


# Waiting for implementation
@task
def secure_download_file(url: str, local_file: str):
    pass

{% elif cookiecutter.data_load == "local load" %}

from prefect import task
import pandas as pd
import os
import zipfile
import requests


@task
def load_data(filename: str):
    print("load_data task executed")
    df = pd.read_csv(filename, index_col="id", nrows=1000)
    # Data preprocessing (resampling , filtering , join data )
    return df
# Add your task execution logic here

{% elif cookiecutter.data_load == "download" %}


from prefect import task
import pandas as pd
import os
import zipfile
import requests


@task
def download_file(url: str, local_file: str):
    if not os.path.exists(local_file):
        os.makedirs(os.path.dirname(local_file), exist_ok=True)
        response = requests.get(url)
        with open(local_file, 'wb') as file:
            file.write(response.content)
        print(f"{local_file} downloaded!")
    else:
        print(f"File already exists of size: {os.path.getsize(local_file)} bytes")

@task
def extract_zip_file(zip_file: str, extract_to: str):
    os.makedirs(extract_to, exist_ok=True)
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Extracted to {extract_to}")


{% else %}

from prefect import task
import pandas as pd
import os
import zipfile
import requests


@task
def load_data(filename: str):
    print("load_data task executed")
    df = pd.read_csv(filename, index_col="id", nrows=1000)
    # Data preprocessing (resampling , filtering , join data )
    return df
# Add your task execution logic here

@task
def download_file(url: str, local_file: str):
    if not os.path.exists(local_file):
        os.makedirs(os.path.dirname(local_file), exist_ok=True)
        response = requests.get(url)
        with open(local_file, 'wb') as file:
            file.write(response.content)
        print(f"{local_file} downloaded!")
    else:
        print(f"File already exists of size: {os.path.getsize(local_file)} bytes")

@task
def extract_zip_file(zip_file: str, extract_to: str):
    os.makedirs(extract_to, exist_ok=True)
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Extracted to {extract_to}")

{% endif %}
