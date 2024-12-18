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
    
    # Loop over dataframe to place markers on the map for every Traffic deviation
    for index, row in df.iterrows():
        # Coordinates for traffic deviation
        location = row['LATITUDE'],row['LONGITUDE']
       
        # Returns HTML code for marker tooltip
        html_string = create_marker_tooltip(row)
        
        # Returns the image associated with the Traffic deviation
        image_path = get_deviation_icon_image_path(row)
        
        #Creates a marker on the map
        folium.Marker(location,
                        icon=folium.CustomIcon(icon_image=image_path),
                        popup=folium.Popup(html_string,max_width=None)).add_to(map)
    
    st_folium(map,use_container_width=True)

    

if __name__ == "__main__":
    layout()