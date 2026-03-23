## Imports
from sklearn.model_selection import train_test_split
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler # for the standardisation
from sklearn.preprocessing import PolynomialFeatures
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Lasso  # for the lasso regression
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error

import joblib

import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.cm as cm
import numpy as np
import pandas as pd

import csv
from pathlib import Path


## Importing data
data_file = Path(__file__).resolve().parents[2] / "data" / "clean_data_for_model.csv"
df = pd.read_csv(data_file)
df['furnished'] = df['furnished'].astype('bool') # not sure why that got eaten
df = df.drop(columns=['price_by_m2'])

 
## Creating and encoding provinces:
### Setting provinces : 
def set_province(): # repeating some like hainaut is easier than conditionals
    conditions = [
        df['zip_code'].between(1000, 1299), # 1 bxl_cap
        df['zip_code'].between(1300, 1499), # 2 brabant_wallon
        df['zip_code'].between(1500, 1999), # 3 brabant_flamand
        df['zip_code'].between(2000, 2999), # 4 anvers
        df['zip_code'].between(3000, 3499), # 3 brabant_flamand #
        df['zip_code'].between(3500, 3999), # 5 limbourg
        df['zip_code'].between(4000, 4999), # 6 liège
        df['zip_code'].between(5000, 5680), # 7 namur
        df['zip_code'].between(6000, 6599), # 8 hainaut
        df['zip_code'].between(6600, 6999), # 9 luxembourg
        df['zip_code'].between(7000, 7999), # 8 hainaut
        df['zip_code'].between(8000, 8999), # 10 flandre_occidentale
        df['zip_code'].between(9000, 9999), # 11 flandre_orientale
    ] 
    
    choices = [1, 2, 3, 4, 3, 5, 6, 7, 8, 9, 8, 10, 11]  # one per condition
    df['province'] = np.select(conditions, choices, default=0)
    print("Provinces created and set")
   
set_province()
#df = df.drop(columns=['zip_code']) # we do this in the drop_features now

## One hot Encode of Provinces
#df = pd.get_dummies(df, columns=['province'], drop_first=True) # doing this in the feature management
#print("Provinces One Hot Encoded")


## Feature Management
numeric_features = ["livable_surface_m2" , "land_area_m2", "build_year", "energy_KWh_m2_year"]
categorical_features = ["number_of_bedrooms", "furnished", "has_terrace", "has_garden", "number_of_facades", "has_swimming_pool", "has_garage", "number_of_garages", "has_elevator", "prop_group_flat", "prop_group_house", "prop_group_mixed_building", "prop_group_other", "prop_group_penthouse", "prop_group_villa"]
hot_features = ['province', "building_state"]
drop_features = ["zip_code"] 

# for col in numeric_features:  # if a data type problem occurs
#     df[col] = pd.to_numeric(df[col], errors="coerce")

## Preprocess pipes:
numeric_pipe = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    #("scaler", StandardScaler()),
])

cat_pipe = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    #("scaler", StandardScaler()),
])

hot_pipe = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore")),
])

preprocess = ColumnTransformer(
    transformers=[
        ("num", numeric_pipe, numeric_features),
        ("hot", hot_pipe, hot_features),
        ("cat",  cat_pipe, categorical_features)
    ],
    remainder="drop"  # or "passthrough" to keep untouched columns
)


## Importing data:
X = df.drop(columns=["price"] + drop_features) #.to_numpy()  # We need to drop the target column
y = df["price"].to_numpy()  #.reshape(-1 , 1)    # here we do the reshaping in place.

## Spliting the data
X_train, X_test, y_train, y_test = train_test_split(X,y, random_state=None, test_size=0.2)
print("Data set split into: X_train, X_test, y_train, y_test")

## Checking the shapes:
print("Shape of X: ", X.shape)  
print("Shape of y: ", y.shape)




## Model Pipeline: Lasso regression
degree = 2 # for the polynomial expansion
pipe_LR2 = Pipeline(steps=[
                ("preprocess", preprocess),
                ('polynomial expansion', PolynomialFeatures(degree=degree)),
                ('scaler', StandardScaler()),
                ('lasso', Lasso(max_iter= 20000, alpha=10.0, tol=1e-3)),
                  ])

""" 

## Calling Lasso regression:
pipe_LR2.fit(X_train, y_train) 
print(pipe_LR2.named_steps["lasso"].n_iter_) 
predictions = pipe_LR2.predict(X_test)
## Printing results
#print("R² train:", pipe.score(X_train, y_train))
#print("R² test:", pipe.score(X_test, y_test))

y_pred_train = pipe_LR2.predict(X_train)
y_pred_test = pipe_LR2.predict(X_test)

r2_train = round(r2_score(y_train, y_pred_train),4)
r2_test = round(r2_score(y_test, y_pred_test), 4)
MAE_train = round(mean_absolute_error(y_train, y_pred_train), 2)
MAE_test = round(mean_absolute_error(y_test, y_pred_test), 2)

RMSE_train = round(np.sqrt(mean_squared_error(y_train, y_pred_train)), 2)
RMSE_test = round(np.sqrt(mean_squared_error(y_test, y_pred_test)), 2)

mape_test = round(mean_absolute_percentage_error(y_test, y_pred_test) *100 , 2)


print(f"""
#| Regression | degree | R² train | R² test | MAE test | RMSE test| MAPE test (%)|
#|------------|:-------|----------|---------|----------|---------:| -------------|
#| Lasso      |   {degree}    |  {r2_train}  |  {r2_test} | {MAE_test} |  {RMSE_test}| {mape_test}%      |

""")

## Exporting the model:
LR2_model_path = Path(__file__).resolve().parents[2] / "data" / "models" / "LR2_model.pkl"
joblib.dump(pipe_LR2, LR2_model_path)


 """

