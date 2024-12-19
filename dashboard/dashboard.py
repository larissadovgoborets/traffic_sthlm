import folium.features
import folium.map
import streamlit as st
import folium
import pandas as pd
from streamlit_folium import st_folium
from connect_data_warehouse import query_traffic_messages
from datetime import datetime
from folium_map_utility_functions import create_marker_tooltip, get_deviation_icon_image_path

STOCKHOLM_CENTER = (59.325,18.05)

def layout():
    df = query_traffic_messages().dropna(subset=['LONGITUDE'])
    

    map = folium.Map(location=STOCKHOLM_CENTER,zoom_start=9,)
    cols = st.columns([0.12, 0.88],vertical_alignment="top")
    
    traffic_deviation_map = {
        "Car": ["Vägarbete", "Hastighetsbegränsning gäller", "Vägen avstängd", "Fordonshaveri",
                "Olycka", "Följ omledningsskyltar", "Körfältsavstängningar", "Bärgning", "Trafiksignal fungerar ej"],
        "Bus": ["Vägarbete", "Hastighetsbegränsning gäller", "Vägen avstängd", "Fordonshaveri",
                "Olycka", "Följ omledningsskyltar", "Körfältsavstängningar", "Bärgning", "Trafiksignal fungerar ej"],
        "Metro": [],  
        "Train": [],  
        "Tram": [],  
        "Ferry": ["Färja"]
    }

    selected_deviations = []
    with cols[0]:
        if st.checkbox("Car"):
            selected_deviations.extend(traffic_deviation_map["Car"])
        if st.checkbox("Bus"):
            selected_deviations.extend(traffic_deviation_map["Bus"])
        if st.checkbox("Metro"):
            selected_deviations.extend(traffic_deviation_map["Metro"])
        if st.checkbox("Train"):
            selected_deviations.extend(traffic_deviation_map["Train"])
        if st.checkbox("Tram"):
            selected_deviations.extend(traffic_deviation_map["Tram"])
        if st.checkbox("Ferry"):
            selected_deviations.extend(traffic_deviation_map["Ferry"])

    # filter dataframe for seleceted deviations
    if selected_deviations:
        df = df[df["MESSAGE_CODE"].isin(selected_deviations)]

    # Loop over dataframe to place markers on the map for every Traffic deviation
    for index, row in df.iterrows():
        # Coordinates for traffic deviation
        location = row['LATITUDE'],row['LONGITUDE']
       
        # Returns HTML code for marker tooltip
        html_string = create_marker_tooltip(row)
        
        # Returns the image associated with the Traffic deviation
        image_path = get_deviation_icon_image_path(row)
        
        #Create a marker on the map
        folium.Marker(location,
                        icon=folium.CustomIcon(icon_image=image_path),
                        popup=folium.Popup(html_string,max_width=None)).add_to(map)
    with cols[1]:
        st_folium(map,height=450,use_container_width=True)

    

if __name__ == "__main__":
    layout()