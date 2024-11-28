import streamlit as st
import pandas as pd
import geopy.distance as geopy_distance
from streamlit_lottie import st_lottie
import requests
import random
import string

# Load Lottie animation
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

# UI Enhancements
st.set_page_config(page_title="Karachi Blood Bank Finder", layout="wide")

st.sidebar.title("🔒 User Authentication")
auth_option = st.sidebar.radio("Navigate", ["Sign In", "Sign Up"])

if auth_option == "Sign Up":
    st.sidebar.header("Create Your Account")
    with st.sidebar.form("signup_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        password = st.text_input("Password", type="password")
        signup_submit = st.form_submit_button("Sign Up")

    if signup_submit:
        if email and password and name and blood_group:
            username = generate_username(name)
            if email in users_db:
                st.sidebar.error("📧 Email already registered!")
            else:
                users_db[email] = {"name": name, "username": username, "blood_group": blood_group, "password": password}
                st.sidebar.success(f"🎉 Account created! Your username is **{username}**")
        else:
            st.sidebar.error("❌ Please fill in all fields!")

elif auth_option == "Sign In":
    st.sidebar.header("Log In to Your Account")
    with st.sidebar.form("signin_form"):
        username_input = st.text_input("Username")
        password_input = st.text_input("Password", type="password")
        signin_submit = st.form_submit_button("Sign In")

    if signin_submit:
        valid_user = any(user["username"] == username_input and user["password"] == password_input for user in users_db.values())
        if valid_user:
            st.session_state["logged_in_user"] = username_input
            st.sidebar.success(f"👋 Welcome back, {username_input}!")
            st.sidebar.button("Log Out", on_click=lambda: st.session_state.pop("logged_in_user"))
        else:
            st.sidebar.error("❌ Invalid Username or Password!")

# Main Blood Bank App
if "logged_in_user" in st.session_state:
    st.markdown(f"### Welcome, **{st.session_state['logged_in_user']}**! 🎉")
    st_lottie(lottie_animation, height=200)

st.title("Karachi Blood Bank Finder 🩸")

blood_banks = pd.DataFrame([
    {"name": "Central Blood Bank", "location": "Saddar", "coordinates": (24.8607, 67.0011), "blood_groups": ["A+", "O+"]},
    {"name": "City Blood Bank", "location": "Clifton", "coordinates": (24.8138, 67.0300), "blood_groups": ["B+", "AB+"]},
    {"name": "Fatimid Foundation", "location": "North Nazimabad", "coordinates": (24.9425, 67.0728), "blood_groups": ["A-", "O+"]},
    {"name": "Indus Hospital", "location": "Korangi", "coordinates": (24.8205, 67.1279), "blood_groups": ["O-", "B+"]},
    {"name": "Liaquat National Hospital", "location": "Gulshan-e-Iqbal", "coordinates": (24.9215, 67.0954), "blood_groups": ["A+", "AB-"]},
])

with st.form("blood_bank_form"):
    location = st.selectbox("📍 Select Your Location", blood_banks["location"].unique())
    blood_group = st.selectbox("🩸 Select Required Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
    submitted = st.form_submit_button("🔍 Find Blood Bank")

if submitted:
    user_coords = blood_banks[blood_banks["location"] == location]["coordinates"].values[0]
    filtered_banks = blood_banks[blood_banks["blood_groups"].apply(lambda bg: blood_group in bg)]
    if not filtered_banks.empty:
        filtered_banks["distance"] = filtered_banks["coordinates"].apply(lambda coords: geopy_distance.distance(user_coords, coords).km)
        nearest = filtered_banks.loc[filtered_banks["distance"].idxmin()]

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
