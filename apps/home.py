import pandas as pd
import streamlit as st
import leafmap.foliumap as leafmap


def app():
    st.title("Home")

    # m = leafmap.Map(locate_control=True)
    # m.add_basemap("ROADMAP")
    # m.to_streamlit(height=700)

    st.header("Data")
    df = pd.read_csv("data/insar_data.csv")
    st.dataframe(df)

    st.header("Demo")
    st.text("Click on the left sidebar menu to explore data interactively.")
    st.image("https://i.imgur.com/KEzE0W3.gif")
