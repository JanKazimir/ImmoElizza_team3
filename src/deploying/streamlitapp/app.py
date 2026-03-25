# %%

import streamlit as st
import pandas as pd
import joblib
import numpy as np
import os
from pathlib import Path

## To do :
# - make it actually work. 
#   - It needs to transform things into the right format, 
#   - encode the provinces, 
# - have options for a few more columns, 
# - state of the building, etc...
# - Figure out how to deploy to some actual webpage
# - clean up the repo
# - when returning a price, return the mean predicted price from several models.

# Paths of files and folders
BASE_DIR = Path(__file__).resolve()
PROJECT_ROOT = BASE_DIR.parents[3]
MODEL_PATH = PROJECT_ROOT / 'model' / 'XGB_model.pkl'
COLUMNS_PATH = PROJECT_ROOT / 'model' / 'model_columns.pkl'

# %%
# Now load using the full path
model = joblib.load(MODEL_PATH)
model_columns = joblib.load(COLUMNS_PATH)
print(model_columns)
# %%

# 1. Load the model and the columns list
# model = joblib.load('models/best_model.pkl')
# model_columns = joblib.load('models/model_columns.pkl')

st.set_page_config(page_title="Immo-Eliza Price Predictor", layout="centered")

st.title("🏠 Immo-Eliza: Belgium Real Estate Predictor")
st.markdown("Enter property details below to estimate the **Market Sale Price**.")

# 2. Input Form
with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        zip_code = st.number_input("Zip Code", min_value=1000, max_value=9999, value=1000)
        living_area = st.number_input("Living Area (m²)", min_value=10, max_value=1000, value=100)
        rooms = st.slider("Number of Bedrooms", 1, 10, 3)
        facades = st.slider("Number of Facades", 1, 4, 2)
        
    with col2:
        land_area = st.number_input("Land Area (m²)", min_value=0, max_value=10000, value=0)
        build_year = st.number_input("Build Year", min_value=1800, max_value=2024, value=2000)
        has_garden = st.checkbox("Garden")
        has_terrace = st.checkbox("Terrace")
        has_swimming_pool = st.checkbox("Swimming Pool")

    # Property Type Selection (Dynamic based on your training columns)
    prop_type = st.selectbox("Property Type", ["House", "Flat", "Villa", "Penthouse"])
    
    submit = st.form_submit_button("Estimate Price")



## Set up functions:
def set_province(zip_code):
    province_ranges = [
        (1000, 1299, 1), # 1 bxl_cap
        (1300, 1499, 2), # 2 brabant_wallon
        (1500, 1999, 3), # 3 brabant_flamand
        (2000, 2999, 4), # 4 anvers
        (3000, 3499, 3), # 3 brabant_flamand
        (3500, 3999, 5), # 5 limbourg
        (4000, 4999, 6), # 6 liège
        (5000, 5680, 7), # 7 namur
        (6000, 6599, 8), # 8 hainaut
        (6600, 6999, 9), # 9 luxembourg
        (8000, 8999, 10), # 10 flandre_occidentale
        (9000, 9999, 11), # 11 flandre_orientale
    ]
    for start, end, province in province_ranges:
        if start <= zip_code <= end:
            return province
    return None


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
        'has_garden': bool(has_garden),
        'has_terrace': bool(has_terrace),
        'has_swimming_pool': bool(has_swimming_pool)
    }

    for key, value in mapping.items():
        if key == zip_code:
            input_data[key] = set_province(zip_code)
            
        
        if key in input_data.columns:
            input_data[key] = value
            

    # Handle Property Group Booleans (One-Hot Encoding) # that's not doing it at all.
    type_col = f"prop_group_{prop_type.lower()}"
    if type_col in input_data.columns:
        input_data[type_col] = 1
        


    ## Above is broken:
    # ['number_of_bedrooms', 'livable_surface_m2', 'furnished', 'has_terrace', 'has_garden', 'land_area_m2', 'number_of_facades', 'has_swimming_pool', 'build_year', 'has_garage', 'number_of_garages', 'has_elevator', 'energy_KWh_m2_year', 'building_state', 'prop_group_flat', 'prop_group_house', 'prop_group_mixed_building', 'prop_group_other', 'prop_group_penthouse', 'prop_group_villa', 'province']



    # Predict
    prediction = model.predict(input_data)[0]

    st.success(f"### 💰 Estimated Value: €{prediction:,.2f}")
    st.info("This prediction is based on XGBoost analysis of ~25k listings.")


# %%
# if __name__ == "__main__":


