import streamlit as st
import pandas as pd
import geopy.distance as geopy_distance
from streamlit_lottie import st_lottie
import requests
import random
import string

# Function to load Lottie animation
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_animation = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_tfb3estd.json")

# Persistent User Storage (In-Memory for now)
users_db = {}

# Generate Random Username
def generate_username(name):
    return name.lower().replace(" ", "") + ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))

# Set page configuration
st.set_page_config(page_title="Karachi Blood Bank Finder", layout="wide")

# Custom CSS
st.markdown("""
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f0f0f0;
        }
        .card {
            background-color: #ffffff;
            padding: 20px;
            margin: 10px;
            border-radius: 8px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        .header {
            text-align: center;
            color: #1e90ff;
            font-size: 36px;
            margin-top: 20px;
        }
        .stylish-box {
            background-color: #ffffff;
            padding: 15px;
            margin: 10px;
            border-radius: 8px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            border-left: 4px solid #1e90ff;
        }
    </style>
""", unsafe_allow_html=True)

# Main App Page - Blood Bank Finder
st.title("Find Blood Banks in Karachi")
st_lottie(lottie_animation, height=200)

# Data for Blood Banks
blood_banks = pd.DataFrame([
    {"name": "Central Blood Bank", "location": "Saddar", "coordinates": (24.8607, 67.0011), "blood_groups": ["A+", "O+"]},
    {"name": "Fatimid Foundation", "location": "North Nazimabad", "coordinates": (24.9425, 67.0728), "blood_groups": ["A-", "O+"]},
    {"name": "Indus Hospital", "location": "Korangi", "coordinates": (24.8205, 67.1279), "blood_groups": ["O-", "B+"]},
    {"name": "Liaquat National Hospital", "location": "Gulshan-e-Iqbal", "coordinates": (24.9215, 67.0954), "blood_groups": ["A+", "AB-"]},
    {"name": "The Blood Bank", "location": "Ferozabad", "coordinates": (24.8880, 67.0708), "blood_groups": ["A-", "B-"]},
    {"name": "JPMC Blood Bank", "location": "Saddar", "coordinates": (24.8556, 67.0092), "blood_groups": ["B+", "O+"]},
    {"name": "Karachi Blood Bank", "location": "Korangi", "coordinates": (24.8321, 67.0731), "blood_groups": ["O-", "A+"]},
    {"name": "Holy Family Blood Bank", "location": "Naya Nazimabad", "coordinates": (24.9271, 67.0505), "blood_groups": ["O+", "AB-"]},
    {"name": "Ziauddin Blood Bank", "location": "North Karachi", "coordinates": (24.9644, 67.0599), "blood_groups": ["AB+", "B+"]},
    {"name": "National Blood Bank", "location": "Hassan Square", "coordinates": (24.8552, 67.0564), "blood_groups": ["O-", "A+"]},
    {"name": "Sindh Blood Transfusion Authority", "location": "Clifton", "coordinates": (24.8138, 67.0300), "blood_groups": ["AB-", "O+"]},
])

# Karachi's Locations
karachi_locations = ["Saddar", "Gulshan-e-Iqbal", "North Nazimabad", "Clifton", "Garden", "Korangi", "Ferozabad", "Naya Nazimabad", "North Karachi", "Hassan Square"]

# User Input for Blood Bank Finder
with st.form("blood_search"):
    user_location = st.selectbox("Select Your Location in Karachi", karachi_locations)
    blood_group_needed = st.selectbox("Select Required Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
    submit_button = st.form_submit_button("Search Blood Banks")

if available_blood_banks:
    st.success("Available Blood Banks:")
    for bank in available_blood_banks:
        st.write(f"Name: {bank['name']} - Location: {bank['location']}")
else:
    st.error("No blood banks found matching your criteria.")

    # Calculate nearest available blood banks
    available_banks = blood_banks.copy()
    available_banks['distance'] = available_banks['coordinates'].apply(
        lambda x: geopy_distance.distance((24.8607, 67.0011), x).km
    )
    nearest_banks = available_banks.sort_values("distance").head(3)
    
    for _, bank in nearest_banks.iterrows():
        st.markdown(f"### {bank['name']}")
        st.markdown(f"📍 Location: {bank['location']}")
        st.markdown(f"🩸 Available Blood Groups: {', '.join(bank['blood_groups'])}")
        st.markdown(f"📞 Contact: +92-{random.randint(3000000000, 3999999999)}")
        st.markdown(f"🌐 Website: [Visit]({bank['name'].lower().replace(' ', '')}.domain.com)")
        st.markdown(f"📍 Distance: {round(bank['distance'], 2)} km")
        st.markdown("---")
else:
    for _, bank in available_banks.iterrows():
        st.markdown(
            f"""
            <div class="stylish-box" style="
                border: 1px solid #ccc;
                padding: 15px;
                margin: 10px 0;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                transition: transform 0.3s ease;
            " onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
                <h3 style="color: #007BFF;">{bank['name']}</h3>
                <p>📍 Location: {bank['location']}</p>
                <p>🩸 Available Blood Groups: {', '.join(bank['blood_groups'])}</p>
                <p>📞 Contact: +92-{random.randint(3000000000, 3999999999)}</p>
                <p>🌐 Website: <a href="http://{bank['name'].lower().replace(' ', '')}.domain.com" target="_blank" style="text-decoration: none; color: #007BFF;">Visit</a></p>
            </div>
            """, 
            unsafe_allow_html=True
        )
else:
    st.warning("Please enter a location.")
