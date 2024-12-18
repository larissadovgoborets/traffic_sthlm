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
    
    
    st.header("Traffic Stockholm")			
    map = folium.Map(location=STOCKHOLM_CENTER,zoom_start=9,)
    cols = st.columns([0.12, 0.88],vertical_alignment="top")
    
    # Filter on means of transport
    with cols[0]:
        car_selected = st.checkbox("Car")
        bus_selected = st.checkbox("Bus")
        metro_selected = st.checkbox("Metro")
        train_selected = st.checkbox("Train")
        tram_selected = st.checkbox("Tram")
        ferry_selected = st.checkbox("Ferry")

    # Filter dataframe on traffic deviations that are relevant to the means of transport
    if car_selected or bus_selected:
        car_traffic_deviation = ["Vägarbete","Hastighetsbegränsning gäller","Vägen avstängd","Fordonshaveri",
                                 "Olycka","Följ omledningsskyltar","Körfältsavstängningar","Bärgning","Trafiksignal fungerar ej"]
        df = df.query(f"MESSAGE_CODE in {car_traffic_deviation}")
    if metro_selected:
        pass
    if train_selected:
        pass
    if tram_selected:
        pass
    if ferry_selected:
        ferry_traffic_deviations = ["Färja"]
        df = df.query(f"MESSAGE_CODE in {ferry_traffic_deviations}")

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