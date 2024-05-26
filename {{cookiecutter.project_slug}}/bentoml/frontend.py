{% if cookiecutter.frontend == "streamlit" %}
import streamlit as st
import numpy as np
import requests

# Define the backend service URLs
BASE_URL = "http://localhost:3000"
MODEL_A_URL = f"{BASE_URL}/model_a_predict"
MODEL_B_URL = f"{BASE_URL}/model_b_predict"
AB_TEST_URL = f"{BASE_URL}/predict_ab_test"

{% endif %}