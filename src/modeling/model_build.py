## Imports
from sklearn.model_selection import train_test_split
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler # for the standardisation
from sklearn.preprocessing import PolynomialFeatures
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
def set_province():
    conditions = [
        df['zip_code'].between(1000, 1299), # 1 bxl_cap
        df['zip_code'].between(1300, 1499), # 2 brabant_wallon
        df['zip_code'].between(1300, 1499), # 3 brabant_flamand
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
    ] # repeating some like hainaut is easier than conditionals
    
    choices = [1, 2, 3, 4, 3, 5, 6, 7, 8, 9, 8, 10, 11]  # one per conditio
    df['province'] = np.select(conditions, choices, default=0)
    print("Provinces created and set")
   
set_province()
df = df.drop(columns=['zip_code'])

## One hot Encode of Provinces
df = pd.get_dummies(df, columns=['province'], drop_first=True)
print("Provinces One Hot Encoded")



## Importing and Splitting data:
X = df.drop(columns=["price"]) #.to_numpy()  # We need to drop the target column
y = df["price"].to_numpy().reshape(-1 , 1)    # here we do the reshaping in place.
X_train, X_test, y_train, y_test = train_test_split(X,y, random_state=None, test_size=0.2)
print("Data set split into: X_train, X_test, y_train, y_test")

## Checking the shapes:
print("Shape of X: ", X.shape)  
print("Shape of y: ", y.shape)



## Pipeline: 

### Filling nulls with median or modes:
class NullFiller(BaseEstimator, TransformerMixin):
    
    def fit(self, X, y=None):
        ## Getting medians
        self.build_year_median = X['build_year'].median()
        self.energy_median = X['energy_KWh_m2_year'].median()
        self.land_area_median = X['land_area_m2'].median() 
        
        ## Getting modes
        self.build_state_mode = X['building_state'].mode()[0]
        self.num_beds_mode = X['number_of_bedrooms'].mode()[0]
        self.furnished_mode = X['furnished'].mode()[0]
        self.num_facades_mode = X['number_of_facades'].mode()[0]
        self.num_garage_mode = X['number_of_garages'].mode()[0]
    
        return self


    
    def transform(self, X):
        X = X.copy() # this is good practice
        # Writing medians
        X['build_year'] = X['build_year'].fillna(self.build_year_median)
        X['energy_KWh_m2_year'] = X['energy_KWh_m2_year'].fillna(self.energy_median)
        X['land_area_m2'] = X['land_area_m2'].fillna(self.land_area_median)
        
        # Writing modes
        X['building_state'] = X['building_state'].fillna(self.build_state_mode)
        X['number_of_bedrooms'] = X['number_of_bedrooms'].fillna(self.num_beds_mode)
        X['furnished'] = X['furnished'].fillna(self.furnished_mode)
        X['number_of_facades'] = X['number_of_facades'].fillna(self.num_facades_mode)
        X['number_of_garages'] = X['number_of_garages'].fillna(self.num_garage_mode)
        
        ## changing type:
        df['furnished'] = df['furnished'].astype('int')
        

        return X


# retry in simpler way:




### Lasso regression:
degree = 2 # for the polynomial expansion

pipe_LR2 = Pipeline([('fill_nulls', NullFiller()),
                 ('polynomial expansion', PolynomialFeatures(degree=degree)),
                ('scaler', StandardScaler()),
                ('lasso', Lasso(max_iter= 1000, alpha=1.0)),
                  ])



## Training the model: 

## Calling Lasso regression:
pipe_LR2.fit(X_train, y_train)  
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
| Regression | degree | R² train | R² test | MAE test | RMSE test| MAPE test (%)|
|------------|:-------|----------|---------|----------|---------:| -------------|
| Lasso      |   {degree}    |  {r2_train}  |  {r2_test} | {MAE_test} |  {RMSE_test}| {mape_test}%|

""")

## Exporting the model:
LR2_model_path = Path(__file__).resolve().parents[2] / "data" / "models" / "LR2_model.pkl"
joblib.dump(pipe_LR2, LR2_model_path)

