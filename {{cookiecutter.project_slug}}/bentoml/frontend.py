import streamlit as st
import numpy as np
import requests

# Define the backend service URLs
BASE_URL = "http://localhost:3000"
MODEL_A_URL = f"{BASE_URL}/model_a_predict"
MODEL_B_URL = f"{BASE_URL}/model_b_predict"
AB_TEST_URL = f"{BASE_URL}/predict_ab_test"

st.title("Bank Model Prediction Service")

st.header("Input Features")

# Collect inputs for each column
id = st.number_input("ID", value=165034)
customer_id = st.number_input("Customer ID", value=15773898)
surname = st.text_input("Surname", value="Lucchese")  # This will not be included in the input data array
credit_score = st.number_input("Credit Score", value=586)
geography = st.selectbox("Geography", options=["France", "Spain", "Germany"], index=0)
gender = st.selectbox("Gender", options=["Male", "Female"], index=1)
age = st.number_input("Age", value=23.0)
tenure = st.number_input("Tenure", value=2)
balance = st.number_input("Balance", value=0.0)
num_of_products = st.number_input("Number of Products", value=2)
has_cr_card = st.selectbox("Has Credit Card", options=[0.0, 1.0], index=0)
is_active_member = st.selectbox("Is Active Member", options=[0.0, 1.0], index=1)
estimated_salary = st.number_input("Estimated Salary", value=160976.75)

# Convert inputs to numpy array (excluding 'surname')
input_data = np.array([
    [
        id, customer_id, credit_score, geography, gender,
        age, tenure, balance, num_of_products, has_cr_card,
        is_active_member, estimated_salary
    ]
])

# Encode categorical variables
def encode_input_data(data):
    geography_map = {"France": 0, "Spain": 1, "Germany": 2}
    gender_map = {"Male": 0, "Female": 1}
    
    data[0][3] = geography_map[data[0][3]]
    data[0][4] = gender_map[data[0][4]]
    return data

input_data = encode_input_data(input_data)

st.write("Input Data:", input_data)

# Define function to send request and get prediction
def get_prediction(url, data):
    try:
        response = requests.post(url, json=data.tolist())
        response.raise_for_status()  # Raise an exception for HTTP errors
        st.write("Response status code:", response.status_code)
        st.write("Response content:", response.content)
        prediction = np.array(response.json())
        return prediction
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        return None
    except ValueError as e:
        st.error(f"JSON decode failed: {e}")
        st.error(f"Response content: {response.text}")
        return None

if st.button("Predict with Model A"):
    prediction = get_prediction(MODEL_A_URL, input_data)
    if prediction is not None:
        st.write("Model A Prediction:", prediction)

if st.button("Predict with Model B"):
    prediction = get_prediction(MODEL_B_URL, input_data)
    if prediction is not None:
        st.write("Model B Prediction:", prediction)

if st.button("Predict with AB Test"):
    prediction = get_prediction(AB_TEST_URL, input_data)
    if prediction is not None:
        st.write("AB Test Prediction:", prediction)
