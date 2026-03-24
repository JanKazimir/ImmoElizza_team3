import joblib

model = joblib.load("model/XGB_model.pkl")
model_columns = joblib.load("model/model_columns.pkl")

def make_prediction(input_df):
    input_df = input_df[model_columns]
    prediction = model.predict(input_df)
    return prediction[0]
