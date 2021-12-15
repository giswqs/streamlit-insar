import folium
import altair as alt
import leafmap.foliumap as leafmap
import pandas as pd
import streamlit as st


def app():

    st.title("InSAR")

    option = st.radio("Choose an option", ("Circle Marker", "Marker Cluster"))

    m = leafmap.Map(
        center=[29.7029, -95.3335], latlon_control=False, zoom=16, height=600
    )

    data = "data/insar_data.csv"

    if option == "Circle Marker":

        df = pd.read_csv(data, skiprows=0).head(100)
        df.columns = [col.replace(" ", "_").replace(".", "_") for col in df.columns]
        columns = df.columns.values.tolist()
        tooltip_cols = [
            "ID",
            "LAT",
            "LON",
            "HEIGHT",
            "HEIGHT_WRT_DEM",
            "SIGMA_HEIGHT",
            "COHER",
        ]
        ts_cols = columns[16:82]
        ts_df = df[ts_cols]

        min_width = 100
        max_width = 200
        x = ("LON",)
        y = ("LAT",)
        radius = 5
        i = 0
        for row in df.itertuples():
            html = ""
            for p in tooltip_cols:
                html = (
                    html
                    + "<b>"
                    + p
                    + "</b>"
                    + ": "
                    + str(eval(str("row." + p)))
                    + "<br>"
                )

            i_df = ts_df.iloc[[i]].transpose()
            i_df.columns = ["value"]
            i_df["date"] = i_df.index
            i_df = i_df.reset_index()
            graph = line = (
                alt.Chart(i_df)
                .mark_line(interpolate="basis")
                .encode(
                    x="date",
                    y="value",
                )
            )

            popup_html = folium.Popup(html, min_width=min_width, max_width=max_width)
            tooltip_str = folium.Tooltip(html)
            popup = folium.Popup().add_child(
                folium.features.VegaLite(graph, width="50%")
            )

            folium.CircleMarker(
                location=[row.LAT, row.LON],
                radius=radius,
                popup=popup,
                tooltip=tooltip_str,
            ).add_to(m)

            i += 1

    elif option == "Marker Cluster":
        df = pd.read_csv(data)
        columns = [
            "ID",
            "LAT",
            "LON",
            "HEIGHT",
            "HEIGHT_WRT_DEM",
            "SIGMA_HEIGHT",
            "COHER",
        ]
        df = df[columns]
        m.add_points_from_xy(df, x="LON", y="LAT", radius=5)

    m.to_streamlit(height=600)
