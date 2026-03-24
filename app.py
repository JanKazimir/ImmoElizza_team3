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
    zip_code: int
    number_of_bedrooms: int
    livable_surface_m2: int
    furnished: bool = None
    has_terrace: bool = None
    has_garden: bool = None
    land_area_m2 : int = None 
    number_of_facades: Optional[int] = None
    has_swimming_pool: bool = None
    build_year: int = None 
    has_garage: bool = None
    number_of_garages: Optional[int] = None
    has_elevator: bool = None
    energy_KWh_m2_year: Optional[int] = None
    building_state: Optional[int] = None
    property_type: Optional[str] # e.g., "New", "Good", "To renovate"



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

# 1.Load your trained model (ensure the path is correct)
model = joblib.load("model/model.pkl")

# 2. Update de POST route
@app.post("/predict")
def predict_price(data: HouseData):
    # Convert the JSON data to a Pandas DataFrame (as your model expects)
    input_df = pd.DataFrame([data.dict()])
    
    # Run the prediction
    prediction = model.predict(input_df)
    
    # Return the price (we take the first result from the list)
    return {"prediction": float(prediction)}




"""
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
