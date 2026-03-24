## Imports
import numpy as np
import pandas as pd
import json
import csv
from pathlib import Path


input_test = {
    "livable_surface_m2": 100,
    "number_of_bedrooms": 2,
    "zip_code": 1000, # The model can see it and still run.
    "land_area_m2": None,
    "build_year": 1978,
    "energy_KWh_m2_year": 256.0,
    "has_garden": None,
    "has_terrace": None,
    "has_garage": None,
    "number_of_garages": None,
    "has_elevator": None,
    "has_swimming_pool": None,
    "furnished": None,
    "number_of_facades": None,
    'building_state' : None,
    'property_type': 'house',
    'prop_group_penthouse': 'potato',
    'prop_group_other': False ,
    'prop_group_house' : 'test',
    'prop_group_villa': True ,
    'prop_group_flat': True,
    'prop_group_mixed_building' : False, 
    'province': 1
}

## Need to
# - fill in some nulls? not necessary for the xgboost
# - check data types? pydantic should do that
# - ensure property types is correct


def preprocess(data):
    # print(data)
    zip_code = data["zip_code"] # getting the zip_code from the input
    data['province'] = set_province(zip_code) # turning that into a province, putting it into the data
    data.pop("zip_code", None) # removing the zipcode from the data
    data = set_property_type(data)

    data_array = pd.DataFrame([data]) # converting the dict to a array for the model
    print(data)
    # print(data_array)


def set_property_type(data):
    prop_type = data['property_type'].lower()
    
    ## Set everything to false:
    data['prop_group_penthouse'] = False
    data['prop_group_other'] = False
    data['prop_group_house'] = False
    data['prop_group_villa'] = False
    data['prop_group_flat'] = False
    data['prop_group_mixed_building'] = False
    
    if prop_type == 'house':
      data['prop_group_house'] = True # true

    elif prop_type == "flat":
      data['prop_group_flat'] = True # true
    
    elif prop_type == "other":
      data['prop_group_other'] = True #true

    print(f"+++++++++++++ {data}")
    return data


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


preprocess(input_test)


## For filling:
# build_year : 1978
# "energy_KWh_m2_year": 256.0,
# "has_garden": true or leave empty


# "building_state": Optional{'1' :'To demolish', "2" : 'To renovate', "3" : 'To restore', '4' : 'Normal', '5' : 'Excellent', '6' : 'Fully renovated' , '7' : 'New'},

## Output
{
    # "prediction": Optional[float],
    # "status_code": Optional[int]
}


## The XGboost model is using:

numeric_features = [
    "livable_surface_m2",
    "land_area_m2",
    "build_year",
    "energy_KWh_m2_year",
]

categorical_features = [
    "province",
    "building_state",
]

binary_features = [
    "number_of_bedrooms",
    "furnished",
    "has_terrace",
    "has_garden",
    "number_of_facades",
    "has_swimming_pool",
    "has_garage",
    "number_of_garages",
    "has_elevator",
    "prop_group_flat",
    "prop_group_house",
    "prop_group_mixed_building",
    "prop_group_other",
    "prop_group_penthouse",
    "prop_group_villa",
]


""" 

# Our Data from api:
{
  "data": {
    "livable_surface_m2": int,
    "property-type":  "prop_group_flat" | "prop_group_house" | "prop_group_other",
    "number_of_bedrooms": int,
    "zip-code": int, # Province encoding ❗
    "land_area_m2": Optional[int],
    "build_year": Optional[int],
    "energy_KWh_m2_year": Optional[int],
    "has_garden": Optional[bool],
    "has_terrace": Optional[bool],
    "has_garage": Optional[bool],
    "number_of_garages" : Optional[int],
    "has_elevator": Optional[bool],
    "has_swimming_pool": Optional[bool],
    "furnished": Optional[bool],
    "number_of_facades": Optional[int],
    "building_state": Optional{'1' :'To demolish', "2" : 'To renovate', "3" : 'To restore', '4' : 'Normal', '5' : 'Excellent', '6' : 'Fully renovated' , '7' : 'New'}
  }
}
 """
