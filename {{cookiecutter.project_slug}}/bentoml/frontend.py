{% if cookiecutter.frontend == "streamlit" %}
import streamlit as st
import numpy as np
import requests

# Define the backend service URLs
BASE_URL = "http://localhost:3000"
MODEL_A_URL = f"{BASE_URL}/model_a_predict"
MODEL_B_URL = f"{BASE_URL}/model_b_predict"
AB_TEST_URL = f"{BASE_URL}/predict_ab_test"

{% elif cookiecutter.frontend == "vite-react" %}

import git

# Replace with the repository URL you want to clone
REPO_URL = 'https://github.com/IbLahlou/ml_api_frontend.git'
CLONE_DIR = '.'

# Clone the repository
git.Repo.clone_from(REPO_URL, CLONE_DIR)

print(f'Repository cloned from {REPO_URL} to {CLONE_DIR}')


{% endif %}

# Other script template are on going