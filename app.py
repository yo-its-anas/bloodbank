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

# Inject custom CSS for fade-in animations
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

# Sample blood banks in Karachi
blood_banks = pd.DataFrame([
    {"name": "Central Blood Bank", "location": "Saddar", "coordinates": (24.8607, 67.0011), "blood_groups": ["A+", "O+"]},
    {"name": "City Blood Bank", "location": "Clifton", "coordinates": (24.8138, 67.0300), "blood_groups": ["B+", "AB+"]},
    {"name": "Fatimid Foundation", "location": "North Nazimabad", "coordinates": (24.9425, 67.0728), "blood_groups": ["A-", "O+"]},
    {"name": "Indus Hospital", "location": "Korangi", "coordinates": (24.8205, 67.1279), "blood_groups": ["O-", "B+"]},
    {"name": "Liaquat National Hospital", "location": "Gulshan-e-Iqbal", "coordinates": (24.9215, 67.0954), "blood_groups": ["A+", "AB-"]},
    {"name": "SIUT", "location": "Garden", "coordinates": (24.8723, 67.0356), "blood_groups": ["O-", "B-"]},
    {"name": "Aga Khan Hospital", "location": "Stadium Road", "coordinates": (24.8948, 67.0822), "blood_groups": ["A+", "B+"]},
    {"name": "Jinnah Hospital", "location": "Rafiqui Road", "coordinates": (24.8673, 67.0409), "blood_groups": ["AB+", "O-"]},
    {"name": "OMI Hospital", "location": "Teen Talwar", "coordinates": (24.8130, 67.0262), "blood_groups": ["A-", "B+"]},
    {"name": "Patel Hospital", "location": "Gulshan", "coordinates": (24.9136, 67.1093), "blood_groups": ["O+", "AB+"]},
    {"name": "Civil Hospital", "location": "M.A. Jinnah Road", "coordinates": (24.8602, 67.0103), "blood_groups": ["A+", "B+"]},
    {"name": "PNS Shifa", "location": "Defence", "coordinates": (24.8099, 67.0357), "blood_groups": ["O+", "B-"]},
    {"name": "Ziauddin Hospital", "location": "North Nazimabad", "coordinates": (24.9466, 67.0724), "blood_groups": ["A-", "AB+"]},
    {"name": "Taj Medical Complex", "location": "Saddar", "coordinates": (24.8635, 67.0268), "blood_groups": ["B-", "O+"]},
    {"name": "NIBD", "location": "PECHS", "coordinates": (24.8622, 67.0747), "blood_groups": ["AB-", "A+"]}
])

# Streamlit App Title
st.title("Karachi Blood Bank Finder")

# User Inputs
with st.form("blood_bank_form"):
    location = st.selectbox("Select Your Location", blood_banks["location"].unique())
    blood_group = st.selectbox("Select Required Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
    submit_button = st.form_submit_button("Find Blood Bank")

# Process Form
if submit_button:
    user_coords = blood_banks[blood_banks["location"] == location]["coordinates"].values[0]
    filtered_banks = blood_banks[blood_banks["blood_groups"].apply(lambda bg: blood_group in bg)]

    if not filtered_banks.empty:
        filtered_banks["distance"] = filtered_banks["coordinates"].apply(lambda coords: geopy_distance.distance(user_coords, coords).km)
        nearest = filtered_banks.loc[filtered_banks["distance"].idxmin()]
        
        # Output Nearest Blood Bank
        st.markdown(f"""
            <div class="fade-in">
                <h3>Nearest Blood Bank Found!</h3>
                <p>📍 <strong>{nearest['name']}</strong> ({nearest['location']})</p>
                <p>🩸 Blood Types Available: {', '.join(nearest['blood_groups'])}</p>
                <p>📏 Distance: {nearest['distance']:.2f} km</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.error("No matching blood bank found.")
