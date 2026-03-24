import os
import uvicorn
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional
from src.deploying.preprocessing.cleaning_data import preprocess, set_property_type, set_province
from src.deploying.predict.prediction import make_prediction

app = FastAPI()

# Define the data format for the POST request
class HouseData(BaseModel):
    zip_code: int
    number_of_bedrooms: int
    livable_surface_m2: int
    furnished: Optional[bool] = Field(default=None, examples=[None])
    has_terrace: Optional[bool] = Field(default=None, examples=[None])
    has_garden: Optional[bool] = Field(default=None, examples=[None])
    land_area_m2: Optional[int] = Field(default=None, examples=[None])
    number_of_facades: Optional[int] = Field(default=None, examples=[None])
    has_swimming_pool: Optional[bool] = Field(default=None, examples=[None])
    build_year: Optional[int] = Field(default=None, examples=[None])
    has_garage: Optional[bool] = Field(default=None, examples=[None])
    number_of_garages: Optional[int] = Field(default=None, examples=[None])
    has_elevator: Optional[bool] = Field(default=None, examples=[None])
    energy_KWh_m2_year: Optional[int] = Field(default=None, examples=[None])
    building_state: Optional[int] = Field(default=None, examples=[None])
    property_type: str = Field(default="house", examples=["house"])  # "house", "flat", or "other"



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

# 2. Update de POST route
@app.post("/predict")
def predict_price(data: HouseData):
    # Convert the JSON data to a Pandas DataFrame (as your model expects)
    #input_df = pd.DataFrame([data.dict()])
    processed_df = preprocess(data)
    
    # Run the prediction
    prediction = make_prediction(processed_df)
    
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
