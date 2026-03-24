import streamlit as st
import pandas as pd
import joblib
import numpy as np
import os

# This part automatically finds the correct folder path
# regardless of where you run the terminal from.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'model.pkl')
COLUMNS_PATH = os.path.join(BASE_DIR, 'model', 'model_columns.pkl')

# Now load using the full path
model = joblib.load(MODEL_PATH)
model_columns = joblib.load(COLUMNS_PATH)

# 1. Load the model and the columns list
#model = joblib.load('models/best_model.pkl')
#model_columns = joblib.load('models/model_columns.pkl')

st.set_page_config(page_title="Immo-Eliza Price Predictor", layout="centered")

st.title("🏠 Immo-Eliza: Belgium Real Estate Predictor")
st.markdown("Enter property details below to estimate the **Market Sale Price**.")

# 2. Input Form
with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        zip_code = st.number_input("Zip Code", min_value=1000, max_value=9999, value=1000)
        living_area = st.number_input("Living Area (m²)", min_value=10, max_value=1000, value=150)
        rooms = st.slider("Number of Bedrooms", 1, 10, 3)
        facades = st.slider("Number of Facades", 1, 4, 2)
        
    with col2:
        land_area = st.number_input("Land Area (m²)", min_value=0, max_value=10000, value=500)
        build_year = st.number_input("Build Year", min_value=1800, max_value=2024, value=2000)
        has_garden = st.checkbox("Garden")
        has_terrace = st.checkbox("Terrace")
        has_swimming_pool = st.checkbox("Swimming Pool")

    # Property Type Selection (Dynamic based on your training columns)
    prop_type = st.selectbox("Property Type", ["House", "Flat", "Villa", "Penthouse"])
    
    submit = st.form_submit_button("Estimate Price")

# 3. Prediction Logic
if submit:
    # Create empty DataFrame with same columns as training
    input_data = pd.DataFrame(0, index=[0], columns=model_columns)
    
    # Fill numeric values (using the exact names from your processed_sale.csv)
    mapping = {
        'zip_code': zip_code,
        'livable_surface_m2': living_area,
        'number_of_bedrooms': rooms,
        'land_area_m2': land_area,
        'number_of_facades': facades,
        'build_year': build_year,
        'has_garden': int(has_garden),
        'has_terrace': int(has_terrace),
        'has_swimming_pool': int(has_swimming_pool)
    }
    
    for key, value in mapping.items():
        if key in input_data.columns:
            input_data[key] = value

    # Handle Property Group Booleans (One-Hot Encoding)
    type_col = f"prop_group_{prop_type.lower()}"
    if type_col in input_data.columns:
        input_data[type_col] = 1

    # Predict
    prediction = model.predict(input_data)[0]
    
    st.success(f"### 💰 Estimated Value: €{prediction:,.2f}")
    st.info("This prediction is based on XGBoost analysis of 10,100 listings.")