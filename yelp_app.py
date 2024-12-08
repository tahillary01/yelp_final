import sys
st.write("Python Executable:", sys.executable)
st.write("Python Version:", sys.version)

# Import libraries
import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Load the trained model
model = joblib.load('best_knn_model.pkl')

# Streamlit App UI Title
st.title("Restaurant Review Rating Predictor")

# Instructions
st.write("""
This app predicts the restaurant review score based on the user and restaurant information you input.
Please fill in the fields below and click **Predict Rating**.
""")

# Input Fields - User Information
st.header("User Information")
review_count_x = st.number_input("Review Count (User)", min_value=0, value=10)
average_stars = st.number_input("Average Stars", min_value=0.0, max_value=5.0, value=3.5)
user_AvgRestaurantCat_rating = st.number_input("User Avg for Restaurant Category Rating", min_value=0.0, max_value=5.0, value=3.0)

# Feature Input
# User-friendly slider for sentiment score
st.write("""
How would you rate the sentiment of the user review?  
Slide toward **negative** (-1) if the review was poor, toward **positive** (+1) if the review was great.
""")

sentiment_score_slider = st.slider(
    "Sentiment Score", 
    min_value=-1.0,  # -1 represents very negative sentiment
    max_value=1.0,   # +1 represents very positive sentiment
    value=0.0,       # Default to neutral sentiment
    step=0.1         # Adjust step for fine control
)

# Set this value directly for predictions
sentiment_score = sentiment_score_slider

# User-friendly slider for hour of day
st.write("""
Select the hour of the day when the review was made.  
Hours are based on a 24-hour clock (military time).
""")

# Create a list of hours for the dropdown menu
hours = [str(i) for i in range(0, 24)]  # Create a list of strings from '0' to '23'

# Dropdown selection
hour_of_day = st.selectbox(
    "Select the Hour", 
    options=hours, 
    index=12  # Default to 12 (noon)
)

# Convert selected value to int
hour_of_day = int(hour_of_day)

is_weekend = st.selectbox("Is the review written on a weekend?", ["Yes", "No"])
is_weekend = 1 if is_weekend == "Yes" else 0

# Input Fields - Restaurant Information
st.header("Restaurant Information")
restaurant_review_count = st.number_input("Restaurant Review Count", min_value=0, value=20)
latitude = st.number_input("Latitude", value=37.7749)  # Default value for San Francisco coordinates
longitude = st.number_input("Longitude", value=122.4194)  # Default value for San Francisco coordinates
is_open = st.selectbox("Is the restaurant still in business?", ["Yes", "No"])
is_open = 1 if is_open == "Yes" else 0

# Restaurant Features
st.write("Select the following restaurant features:")
Alcohol_full_bar = st.selectbox("Is there a full bar?", ["Yes", "No"])
Alcohol_full_bar = 1 if Alcohol_full_bar == "Yes" else 0

Alcohol_beer_and_wine = st.selectbox("Is beer and wine served?", ["Yes", "No"])
Alcohol_beer_and_wine = 1 if Alcohol_beer_and_wine == "Yes" else 0

RestaurantsDelivery = st.selectbox("Does the restaurant offer delivery?", ["Yes", "No"])
RestaurantsDelivery = 1 if RestaurantsDelivery == "Yes" else 0

HasTV = st.selectbox("Does the restaurant have a TV?", ["Yes", "No"])
HasTV = 1 if HasTV == "Yes" else 0

RestaurantsReservations = st.selectbox("Does the restaurant take reservations?", ["Yes", "No"])
RestaurantsReservations = 1 if RestaurantsReservations == "Yes" else 0

RestaurantsTableService = st.selectbox("Is table service available?", ["Yes", "No"])
RestaurantsTableService = 1 if RestaurantsTableService == "Yes" else 0

RestaurantsGoodForGroups = st.selectbox("Good for groups?", ["Yes", "No"])
RestaurantsGoodForGroups = 1 if RestaurantsGoodForGroups == "Yes" else 0

st.write("""
US News Top 15 Best Food Cities:
- New Orleans, LA
- New York City, NY
- Chicago, IL
- Los Angeles, CA
- San Francisco, CA
- Philadelphia, PA
- Las Vegas, NV
- Houston, TX
- Portland, ME
- Austin, TX
- Honolulu, HI
- Boston, MA
- Denver, CO
- Atlanta, GA
- Louisville, KY
""")
is_in_best_food_city = st.selectbox("Is the restaurant located in one of these cities?", ["Yes", "No"])
is_in_best_food_city = 1 if is_in_best_food_city == "Yes" else 0

# Input Feature Array
user_input_features = pd.DataFrame([{
    'review_count_x': review_count_x,
    'average_stars': average_stars,
    'user_AvgRestaurantCat_rating': user_AvgRestaurantCat_rating,
    'restaurant_review_count': restaurant_review_count,
    'latitude': latitude,
    'longitude': longitude,
    'is_open': is_open,
    'Alcohol_full_bar': Alcohol_full_bar,
    'Alcohol_beer_and_wine': Alcohol_beer_and_wine,
    'RestaurantsDelivery': RestaurantsDelivery,
    'HasTV': HasTV,
    'RestaurantsReservations': RestaurantsReservations,
    'RestaurantsTableService': RestaurantsTableService,
    'RestaurantsGoodForGroups': RestaurantsGoodForGroups,
    'sentiment_score': sentiment_score,
    'hour_of_day': hour_of_day,
    'is_weekend': is_weekend,
    'is_in_best_food_city': is_in_best_food_city
}])

# Predict Button
if st.button("Predict Rating"):
    with st.spinner("Calculating..."):
        # Perform Prediction
        prediction = model.predict(user_input_features)

        # Output result
        st.success(f"Predicted Review Rating: {prediction[0]:.2f}")
