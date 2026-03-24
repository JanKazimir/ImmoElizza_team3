
import pandas as pd
import joblib

def load_inference_tools():
    # Load the model and the required column structure.
    model = joblib.load('model/model.pkl')
    model_columns = joblib.load('models/model_columns.pkl')
    return model, model_columns

def make_prediction(input_data):
    """
    Takes a dictionary of house details and returns a price.
    Example input: {'zip_code': 1000, 'livable_surface_m2': 150, ...}
    """
    model, model_columns = load_inference_tools()
    
    # 1. Create a DataFrame with the same structure as training
    # Initialize all columns to 0
    df_input = pd.DataFrame(0, index=[0], columns=model_columns)
    
    # 2. Map the input dictionary to the DataFrame columns
    for key, value in input_data.items():
        if key in df_input.columns:
            df_input[key] = value
            
    # 3. Handle Property Group (One-Hot Encoding)
    # If the user provides 'property_type', map it to 'prop_group_xxx'
    if 'property_type' in input_data:
        type_col = f"prop_group_{input_data['property_type'].lower()}"
        if type_col in df_input.columns:
            df_input[type_col] = 1

    # 4. Predict
    prediction = model.predict(df_input)[0]
    return round(float(prediction), 2)

if __name__ == "__main__":
    # --- Example Usage (Testing the script via terminal) ---
    test_house = {
        'zip_code': 2970,
        'livable_surface_m2': 250,
        'number_of_bedrooms': 4,
        'land_area_m2': 800,
        'build_year': 2010,
        'property_type': 'house',
        'has_garden': 1
    }
    
    price = make_prediction(test_house)
    print(f"--- Prediction Test ---")
    print(f"House Details: {test_house}")
    print(f"Predicted Price: €{price:,}")