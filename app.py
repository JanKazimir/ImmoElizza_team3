import os
import uvicorn
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


app = FastAPI()

# Define the data format for the POST request
class HouseData(BaseModel):
    living_area: int
    rooms_number: int
    zip_code: int
    land_area: Optional[int] = None
    garden: bool = False
    garden_area: Optional[int] = None
    equipped_kitchen: bool = False
    swimming_pool: bool = False
    furnished: bool = False
    open_fire: bool = False
    terrace: bool = False
    terrace_area: Optional[int] = None
    facades_number: Optional[int] = None
    building_state: Optional[str] = None # e.g., "New", "Good", "To renovate"

@app.get("/")
def read_root():
    """Returns 'alive' if the server is running."""
    return "alive"

@app.get("/predict")
def predict_info():
    """Explains what the POST request expects."""
    return (
        "To get a price prediction, send a POST request with a JSON object containing "
        "property details such as 'living_area', 'rooms_number', and 'zip_code'."
    )

model = joblib.load("model/model.pkl")
model_columns = joblib.load("model/model_columns.pkl")


# 2. Update de POST route
@app.post("/predict")
def predict_price(data: HouseData):
    try:
        # Convert input to DataFrame
        input_df = pd.DataFrame([data.dict()])
        
        # Ensure column order matches training (CRITICAL for XGBoost)
        input_df = input_df.reindex(columns=model_columns, fill_value=0)
        
        # Predict
        prediction = model.predict(input_df)
        return {"prediction": round(float(prediction[0]), 2)}

    except Exception as e:
        # This will return the actual error message in the API response
        return {"error": str(e), "type": str(type(e))}
""""
@app.post("/predict")
def predict_price(data: HouseData):
    
    #Receives house data in JSON format and returns a predicted price.
    #Note: Replace the dummy logic with your actual model.predict()
    
    # Example logic:
    # prediction = model.predict([list(data.dict().values())])
    prediction = 250000 
    return {"prediction": prediction}
"""
if __name__ == "__main__":
    # Render uses the PORT environment variable
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
