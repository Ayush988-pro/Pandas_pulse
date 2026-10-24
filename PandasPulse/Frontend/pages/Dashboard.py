import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

if "token" not in st.session_state:
    st.error("Please login first")
    st.stop()

token = st.session_state["token"]
headers ={"Authorization": f"Bearer {token}"}

st.title("📊 PandasPulse Dashboard")

# -----------------------------
# Profile Section
# -----------------------------

profile_response = requests.get(
    f"{BASE_URL}/profile",
    headers=headers
)

if profile_response.status_code == 200:
    user = profile_response.json()

    st.success(
        f"Welcome {user['email']}"
    )

# -----------------------------
# Upload Dataset
# -----------------------------

st.subheader("Upload Dataset")

uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    if st.button("Upload"):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file,
                "text/csv"
            )
        }

        response = requests.post(
            f"{BASE_URL}/upload",
            files=files,
            headers=headers
        )

        if response.status_code == 200:
            st.success("File uploaded successfully")
            st.rerun()

        else:
            st.error(response.json())

# -----------------------------
# My Datasets
# -----------------------------

st.subheader("My Datasets")

response = requests.get(
    f"{BASE_URL}/datasets",
    headers=headers
)

if response.status_code == 200:

    datasets = response.json()

    if len(datasets) == 0:
        st.info("No datasets uploaded yet")

    else:

        for dataset in datasets:

            col1, col2,col3 = st.columns([5, 1,1])

            with col1:
                st.write(f"📄 {dataset['filename']}")
            with col2:
                if st.button("Analyze",key=f"analyze_{dataset['id']}"):
                    st.session_state["dataset_id"] = dataset["id"]

            with col3:
                if st.button(
                        "Delete",
                        key=f"delete_{dataset['id']}"
                ):

                    delete_response = requests.delete(
                        f"{BASE_URL}/datasets/{dataset['id']}",
                        headers=headers
                    )

                    if delete_response.status_code == 200:
                        st.success("Dataset deleted")
                        st.rerun()
                    else:
                        st.error(delete_response.json())
else:

    st.error("Unable to fetch datasets")

# -----------------------------
# Logout
# -----------------------------

if st.button("Logout"):
    st.session_state.clear()
    st.switch_page("../app.py")
