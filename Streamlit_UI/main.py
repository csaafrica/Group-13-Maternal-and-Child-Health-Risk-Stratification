import streamlit as st
from streamlit.components.v1 import iframe
from child import show_child_ui
from mother import show_mother_ui

st.set_page_config(page_title="Health Dashboard", layout="centered")

st.title("👪 Maternal and Child Health Dashboard")
st.markdown("This dashboard combines data analysis for **child health** and **maternal health** indicators across Kenya, Uganda, and Tanzania.")
st.image("https://cdn-icons-png.flaticon.com/512/3559/3559784.png", width=200)
st.markdown("Use the dropdown to switch between analyses for **Child** or **Mother** datasets.")

section = st.selectbox("Choose a Dashboard", ["-- Select --", "Child", "Mother"])


    
    
if section == "Child":
    show_child_ui()
elif section == "Mother":
    show_mother_ui()
else:
    st.warning("Please select a valid dashboard from the dropdown.")
    st.markdown("You can analyze child health indicators or maternal health indicators by selecting the respective options.")
    st.markdown("Use the sidebar to filter data by country, year, and indicator.")