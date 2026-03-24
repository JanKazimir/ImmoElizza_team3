# 🏠 Immo-Eliza: Belgian Real Estate Price Predictor

A complete data science pipeline designed to scrape, clean, analyze, and predict property prices in the Belgian real estate market using data from **Immovlan.be**.

## 🚀 Project Overview

This project follows a full-cycle data workflow:
1.  **Data Extraction**: Industrial-scale scraping of 30,000+ property listings.
2.  **Preprocessing**: Advanced cleaning, feature engineering, and outlier removal.
3.  **Machine Learning**: Multi-model comparison to find the most accurate regressor.
4.  **Deployment**: A user-friendly dashboard for real-time price estimation.

---

## 🛠️ Tech Stack
*   **Data Processing**: Pandas, NumPy
*   **Visualization**: Matplotlib, Seaborn
*   **Machine Learning**: Scikit-Learn, XGBoost
*   **Model Deployment**: Streamlit, Joblib

---

## 📂 Project Structure

text
├── immo_eliza_scraper/    # Scrapy project folder
│   └── results.csv        # Raw scraped data
├── src/
│   ├── preprocessing.py   # Data cleaning & outlier removal logic
│   ├── train.py           # Model training & evaluation (XGBoost/RF/LR)
│   ├── predict.py         # Inference logic for single inputs
│   └── app.py             # Streamlit web application
├── models/
│   ├── best_model.pkl     # Trained XGBoost model
│   └── model_columns.pkl  # Required feature structure for the model
└── README.md

---

## 🚀 Installation and Usage

1. **Data Collection**

Run the Scrapy spider to fetch the latest property data:
scrapy crawl immo_eliza_spider -o results.csv --set CLOSESPIDER_ITEMCOUNT=30000

2. **Preprocessing & EDA**

Clean the raw data and generate statistical insights:
python src/preprocessing.py

**Key features:**
Removes statistical outliers using IQR.
Extracts provinces and zip codes from URLs.
Handles missing values and performs One-Hot Encoding for categorical variables.

3. **Model Training**

Train and compare Linear Regression, Random Forest, and XGBoost:

python src/train.py

The script automatically selects and saves the model with the highest R² Score .

4. **Interactive Dashboard**

Launch the web interface to predict prices:

streamlit run src/app.py

---

## 📊  Data Insights & Features

The model relies on several key features to estimate property value:
* **Location :** Zipcode and Province.
* **Space :** Living area, Plot surface, and Number of bedrooms.
* **Amenities :** Presence of a garden, terrace, or swimming pool.
* **Type :** Categorization (House, Apartment, Villa, etc.).

## 📈 Model Performance

* **Target Metric:** R² Score (aiming for > 0.70) and Mean Absolute Error (MAE).
* **Top Model:** XGBoost currently provides the best performance for handling non-linear real estate trends.




## 🌐 API Documentation

The API is deployed on Render and provides real-time property price estimations.

### Endpoints


| Route | Method | Description |
| :--- | :--- | :--- |
| `/` | `GET` | Health check. Returns `"alive"`. |
| `/predict` | `GET` | Returns instructions on how to use the prediction tool. |
| `/predict` | `POST` | Accepts property data and returns a price prediction. |

### Data Format (POST `/predict`)

**Required Fields:**
* `living_area` (int): Total indoor area in m².
* `rooms_number` (int): Number of bedrooms.
* `zip_code` (int): Belgian postal code.

**Optional Fields:**
* `garden` (bool), `terrace` (bool), `swimming_pool` (bool), `building_state` (string).


**Example Request Body:**
json
{
  "living_area": 120,
  "rooms_number": 2,
  "zip_code": 1000,
  "garden": true
}


## 🚀 Deployment & API Usage

The API is hosted on **Render**. You can interact with it using the following details:

### Base URL
`https://your-app-name.onrender.com`

### Interactive API Docs (Swagger)
You can test the API directly at: `https://your-app-name.onrender.com`

### Example Request (POST)
To get a prediction, send a JSON object to `/predict`:
```json
{
  "living_area": 120,
  "rooms_number": 3,
  "zip_code": 1000,
  "garden": true
}
