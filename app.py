import streamlit as st
from multiapp import MultiApp
from apps import home, insar  # import your app modules here

st.set_page_config(layout="wide")

app = MultiApp()

# Add all your application here
app.add_app("Home", home.app)
app.add_app("InSAR", insar.app)


# The main app
app.run()
