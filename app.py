import streamlit as st
import pandas as pd
import geopy.distance as geopy_distance
from streamlit_lottie import st_lottie
import requests

# Load Lottie animation
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_animation = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_tfb3estd.json")
st_lottie(lottie_animation, height=300)

# Inject custom CSS for animations
st.markdown("""
    <style>
        .fade-in {
            animation: fadeIn ease 2s;
        }
        @keyframes fadeIn {
            from {opacity: 0;}
            to {opacity: 1;}
        }
    </style>
""", unsafe_allow_html=True)

# Sample dataset of blood banks
blood_banks = pd.DataFrame([
    {"name": "Central Blood Bank", "location": "Saddar", "coordinates": (24.8607, 67.0011), "blood_groups": ["A+", "O+"]},
    {"name": "City Blood Bank", "location": "Clifton", "coordinates": (24.8138, 67.0300), "blood_groups": ["B+", "AB+"]},
    {"name": "Fatimid Foundation", "location": "North Nazimabad", "coordinates": (24.9425, 67.0728), "blood_groups": ["A-", "O+"]},
    {"name": "Indus Hospital", "location": "Korangi", "coordinates": (24.8205, 67.1279), "blood_groups": ["O-", "B+"]},
    {"name": "Liaquat National Hospital", "location": "Gulshan-e-Iqbal", "coordinates": (24.9215, 67.0954), "blood_groups": ["A+", "AB-"]},
    {"name": "SIUT", "location": "Garden", "coordinates": (24.8723, 67.0356), "blood_groups": ["O-", "B-"]},
    {"name": "Agha Khan University Hospital", "location": "Stadium Road", "coordinates": (24.8948, 67.0822), "blood_groups": ["A+", "B+"]},
    {"name": "Jinnah Hospital", "location": "Rafiqui Shaheed Road", "coordinates": (24.8673, 67.0409), "blood_groups": ["AB+", "O-"]},
    {"name": "OMI Hospital", "location": "Teen Talwar", "coordinates": (24.8130, 67.0262), "blood_groups": ["A-", "B+"]},
    {"name": "Patel Hospital", "location": "Gulshan-e-Iqbal", "coordinates": (24.9136, 67.1093), "blood_groups": ["O+", "AB+"]},
    {"name": "Civil Hospital", "location": "M.A. Jinnah Road", "coordinates": (24.8602, 67.0103), "blood_groups": ["A+", "B+"]},
    {"name": "PNS Shifa", "location": "Defence", "coordinates": (24.8099, 67.0357), "blood_groups": ["O+", "B-"]},
    {"name": "Ziauddin Hospital", "location": "North Nazimabad", "coordinates": (24.9466, 67.0724), "blood_groups": ["A-", "AB+"]},
    {"name": "Taj Medical Complex", "location": "Saddar", "coordinates": (24.8635, 67.0268), "blood_groups": ["B-", "O+"]},
    {"name": "National Institute of Blood Diseases", "location": "PECHS", "coordinates": (24.8622, 67.0747), "blood_groups": ["AB-", "A+"]},
])

# Streamlit UI
st.title("Karachi Blood Bank Finder")

# User input form with location and blood group selection
with st.form("blood_bank_form"):
    user_location = st.selectbox("Select Your Location", blood_banks["location"].unique())
    required_blood_group = st.selectbox("Select Required Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
    submit_button = st.form_submit_button("Find Blood Bank")

# Process and display the result
if submit_button:
    user_coords = blood_banks[blood_banks["location"] == user_location]["coordinates"].values[0]
    filtered_blood_banks = blood_banks[blood_banks["blood_groups"].apply(lambda bg: required_blood_group in bg)]
    
    if not filtered_blood_banks.empty:
        filtered_blood_banks["distance"] = filtered_blood_banks["coordinates"].apply(lambda coords: geopy_distance.distance(user_coords, coords).km)
        nearest_blood_bank = filtered_blood_banks.loc[filtered_blood_banks["distance"].idxmin()]

        # Show result with animation
        st.markdown(f"""
            <div class="fade-in">
                <h3>Nearest Blood Bank Found!</h3>
                <p>📍 <strong>{nearest_blood_bank['name']}</strong>, {nearest_blood_bank['location']}</p>
                <p>🩸 Available Blood Types: {', '.join(nearest_blood_bank['blood_groups'])}</p>
                <p>📏 Distance: {nearest_blood_bank['distance']:.2f} km</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.error("No matching blood bank found.")
