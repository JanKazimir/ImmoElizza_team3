from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import OneHotEncoder


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

## Importing data:
X = df.drop(columns=["price", "zip_code"]) #.to_numpy()  # We need to drop the target column
y = df["price"].to_numpy()  #.reshape(-1 , 1)    # here we do the reshaping in place.

## Spliting the data
X_train, X_test, y_train, y_test = train_test_split(X,y, random_state=None, test_size=0.2)
print("Data set split into: X_train, X_test, y_train, y_test")


###
### XG BOOST
###


### Columns Management:
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

## Pipelines:

### Preprocess:
numeric_pipe = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
])

categorical_pipe = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore")),
])

binary_pipe = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
])

preprocess = ColumnTransformer(
    transformers=[
        ("num", numeric_pipe, numeric_features),
        ("cat", categorical_pipe, categorical_features),
        ("bin", binary_pipe, binary_features),
    ],
    remainder="drop",
)

## Model pipeline :
xgb_pipe = Pipeline(steps=[
    ("preprocess", preprocess),
    ("model", XGBRegressor(
        objective="reg:squarederror",
        n_estimators=300,
        learning_rate=0.05,
        max_depth=5,
        subsample=0.7,
        colsample_bytree=0.7,
        random_state=42,
        n_jobs=-1,
    )),
])


## Train model

print("Begin model training")
xgb_pipe.fit(X_train, y_train)
y_pred = xgb_pipe.predict(X_test)

xgb_pipe.fit(X_train, y_train)
y_pred_train = xgb_pipe.predict(X_train)
y_pred_test = xgb_pipe.predict(X_test)
mape_test = round(mean_absolute_percentage_error(y_test, y_pred_test) *100 , 2)

# print("R2 train:", r2_score(y_train, y_pred_train))
# print("R2 test:", r2_score(y_test, y_pred_test))
# print("MAE test:", mean_absolute_error(y_test, y_pred_test))
# print("RMSE test:", np.sqrt(mean_squared_error(y_test, y_pred_test)))

print(
    f"""
| Regression | R² train | R² test | MAE test | RMSE test| MAPE test (%)|
|------------|----------|---------|----------|---------:| -------------|
| Xgboost    |  {round(r2_score(y_train, y_pred_train), 2)}    |  {round(r2_score(y_test, y_pred_test), 2)}  | {round(mean_absolute_error(y_test, y_pred_test), 2)} | {round(np.sqrt(mean_squared_error(y_test, y_pred_test)), 2)}  | {mape_test}%      |
"""
)

## Exporting the model:
XGB_model_path = Path(__file__).resolve().parents[2] / "model" / "model.pkl"
joblib.dump(xgb_pipe, XGB_model_path)


# Save the column names (needed for the dashboard to match the input)
joblib.dump(X_train.columns.tolist(), 'model/model_columns.pkl')
