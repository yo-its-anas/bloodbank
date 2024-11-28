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

# Custom CSS for enhanced UI
st.markdown("""
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
        }
        .card {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            animation: slide-in 0.8s ease-out;
        }
        .card h3 {
            margin-top: 0;
            color: #3b82f6;
        }
        .card p {
            margin: 5px 0;
        }
        .icon {
            font-size: 1.2em;
            margin-right: 5px;
            color: #f87171;
        }
        .btn-find {
            background-color: #3b82f6;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .btn-find:hover {
            background-color: #2563eb;
        }
        @keyframes slide-in {
            from {
                transform: translateY(10px);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
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
])

# Streamlit App Title
st.title("Karachi Blood Bank Finder 🩸")

# User Inputs
with st.form("blood_bank_form"):
    location = st.selectbox("📍 Select Your Location", blood_banks["location"].unique())
    blood_group = st.selectbox("🩸 Select Required Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
    submitted = st.form_submit_button("🔍 Find Blood Bank", use_container_width=True)

# Process Form
if submitted:
    user_coords = blood_banks[blood_banks["location"] == location]["coordinates"].values[0]
    filtered_banks = blood_banks[blood_banks["blood_groups"].apply(lambda bg: blood_group in bg)]

    if not filtered_banks.empty:
        filtered_banks["distance"] = filtered_banks["coordinates"].apply(lambda coords: geopy_distance.distance(user_coords, coords).km)
        nearest = filtered_banks.loc[filtered_banks["distance"].idxmin()]

        # Enhanced Output with Cards
        st.markdown(f"""
        <div class="card">
            <h3>📍 {nearest['name']} - {nearest['location']}</h3>
            <p><span class="icon">🩸</span><strong>Blood Types Available:</strong> {', '.join(nearest['blood_groups'])}</p>
            <p><span class="icon">📏</span><strong>Distance:</strong> {nearest['distance']:.2f} km</p>
            <p><span class="icon">🏥</span><strong>Location:</strong> {nearest['location']}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("❌ No matching blood bank found.")
