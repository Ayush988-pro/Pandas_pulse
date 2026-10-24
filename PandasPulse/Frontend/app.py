# app.py

import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.title("Library App")

menu = st.sidebar.selectbox(
    "Choose",
    ["Signup", "Login"]
)

# ---------------- SIGNUP ----------------

# ---------------- SIGNUP ----------------

if menu == "Signup":

    st.header("Create Account")

    email = st.text_input("Email")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Signup"):

        payload = {
            "email": email,
            "password": password
        }

        response = requests.post(
            f"{BASE_URL}/signup",
            json=payload
        )

        if response.status_code in [200, 201]:
            st.success("Account created")
        else:
            st.error(response.json())


# ---------------- LOGIN ----------------

if menu == "Login":

    st.header("Login")

    username = st.text_input("Username")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        response = requests.post(
            f"{BASE_URL}/login",
            data={
                "username": username,
                "password": password
            }
        )

        if response.status_code == 200:

            token = response.json()["access_token"]

            st.session_state["token"] = token
            st.session_state["logged_in"] = True

            st.switch_page("pages/Dashboard.py")
        else:
            st.write("Status:", response.status_code)
            st.json(response.json())

if "token" in st.session_state:

    st.subheader("Profile")

    headers = {
        "Authorization":
        f"Bearer {st.session_state['token']}"
    }

    response = requests.get(
        f"{BASE_URL}/profile",
        headers=headers
    )

    if response.status_code == 200:
        st.json(response.json())