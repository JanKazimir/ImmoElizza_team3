## Imports
import numpy as np
import pandas as pd
import json
import csv
from pathlib import Path


# Incoming data from api:
{
  "data": {
    "area": int,
    "property-type": "APARTMENT" | "HOUSE" | "OTHERS",
    "rooms-number": int,
    "zip-code": int,
    "land-area": Optional[int],
    "garden": Optional[bool],
    "garden-area": Optional[int],
    "equipped-kitchen": Optional[bool],
    "full-address": Optional[str],
    "swimming-pool": Optional[bool],
    "furnished": Optional[bool],
    "open-fire": Optional[bool],
    "terrace": Optional[bool],
    "terrace-area": Optional[int],
    "facades-number": Optional[int],
    "building-state": Optional[
      "NEW" | "GOOD" | "TO RENOVATE" | "JUST RENOVATED" | "TO REBUILD"
    ]
  }
}

## Output
{
  "prediction": Optional[float],
  "status_code": Optional[int]
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


## Notes:
# ❗ Model doesn't have the zipcode, so we'll need to reuse teh province encode function
# ❓ Nonsense to remove: open fire, terrace area was dropped

# correspondance between api input and model names:
{
    "area": "livable_surface_m2",
    "property-type":     "prop_group_flat" | "prop_group_house" | "prop_group_other",
    "rooms-number": "number_of_bedrooms",
    "zip-code": "province" # ❗ needs encoding
    "land-area": "land_area_m2",
    "garden": "has_garden",
    "garden-area": Optional[int], ## We don't have that.
    "equipped-kitchen": Optional[bool],
    "full-address": Optional[str],
    "swimming-pool": Optional[bool],
    "furnished": Optional[bool],
    "open-fire": Optional[bool],
    "terrace": Optional[bool],
    "terrace-area": Optional[int],
    "facades-number": Optional[int],
    "building-state": Optional[
      "NEW" | "GOOD" | "TO RENOVATE" | "JUST RENOVATED" | "TO REBUILD"
    ]
  }


###
### The actual function:
###

def preprocess():
    pass
