# app.py
import streamlit as st
import pandas as pd
import geopy.distance as geopy_distance

# Sample dataset of blood banks
blood_banks = pd.DataFrame([
    {"name": "City Blood Bank", "address": "Clifton, Karachi", "latitude": 24.8138, "longitude": 67.0294, "blood_types": ["A+", "B+", "O+"]},
    {"name": "Central Blood Bank", "address": "Saddar, Karachi", "latitude": 24.8482, "longitude": 67.0235, "blood_types": ["A-", "B-", "O-", "AB+"]},
    {"name": "Karachi Blood Donation Center", "address": "Gulshan-e-Iqbal, Karachi", "latitude": 24.9236, "longitude": 67.0873, "blood_types": ["A+", "O+", "B+"]},
])

# Function to calculate distance between two locations using geopy
def calculate_distance(user_location, bank_location):
    return geopy_distance.distance(user_location, bank_location).km

# UI for user input
st.title("Karachi Blood Bank Finder")
st.subheader("Find the nearest blood bank based on your location and required blood group")

with st.form("blood_bank_form"):
    st.write("Enter your details:")
    user_latitude = st.number_input("Your Latitude", min_value=24.0, max_value=25.0, format="%.6f")
    user_longitude = st.number_input("Your Longitude", min_value=67.0, max_value=68.0, format="%.6f")
    required_blood_group = st.selectbox("Select Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
    submit_button = st.form_submit_button("Find Blood Bank")

# Logic for finding the nearest blood bank
if submit_button:
    user_location = (user_latitude, user_longitude)
    filtered_banks = blood_banks[blood_banks["blood_types"].apply(lambda x: required_blood_group in x)]
    
    if not filtered_banks.empty:
        filtered_banks["distance"] = filtered_banks.apply(
            lambda row: calculate_distance(user_location, (row["latitude"], row["longitude"])), axis=1
        )
        nearest_blood_bank = filtered_banks.sort_values("distance").iloc[0]
        
        # Display the result with animation
        st.markdown("### Nearest Blood Bank")
        st.write("Loading results... 🎉", unsafe_allow_html=True)
        st.info(
            f"**{nearest_blood_bank['name']}**\n\n"
            f"📍 Address: {nearest_blood_bank['address']}\n\n"
            f"🩸 Available Blood Types: {', '.join(nearest_blood_bank['blood_types'])}\n\n"
            f"📏 Distance: {nearest_blood_bank['distance']:.2f} km"
        )
    else:
        st.warning("No blood banks available with the required blood group nearby.")

