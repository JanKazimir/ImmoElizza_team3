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
# 1.Load your trained model (ensure the path is correct)
model = joblib.load("models/best_model.pkl")

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
