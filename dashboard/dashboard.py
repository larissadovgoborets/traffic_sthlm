import folium.features
import folium.map
import streamlit as st
import folium
import pandas as pd
from streamlit_folium import st_folium
from connect_data_warehouse import query_traffic_messages
from folium_map_utility_functions import create_marker_tooltip, get_deviation_icon_image_path
from streamlit.components.v1 import html


STOCKHOLM_CENTER = (59.325,18.05)

def layout():
    df = query_traffic_messages().dropna(subset=['LONGITUDE'])
    cols = st.columns([0.18,0.82],vertical_alignment="center")
    with cols[0]:
        st.image("./map_icons/logga.png")
    with cols [1]:
        st.markdown(
        """
        <h1 style="text-align: left; padding-left: 50px;">Traffic Stockholm</h1>
        """,
        unsafe_allow_html=True
        )

    query = st.text_input("Sök på avvikelser")
    col1, col2, col3 = st.columns(3)

    count = df.duplicated(subset=['LONGITUDE', 'LATITUDE'], keep=False).sum()
    with col1:
        st.markdown(f"""
            <div style="padding: 0px; background-color: #27272f; border-radius: 5px; text-align: center;">
                <h5 style="color: #white;">Antal Störningar</h2>
                <h5 style="color: #white;">{count}</h3>
            </div>
        """, unsafe_allow_html=True)


    with col2:
        st.markdown("""
            <div style="padding: 0px; background-color: #27272f; border-radius: 10px; text-align: center;">
                <h5 style="color: #white;">test2</h2>
                <h5 style="color: #white;">0</h3>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div style="padding: 0px; background-color: #27272f; border-radius: 10px; text-align: center;">
                <h5 style="color: #white;">test3</h2>
                <h5 style="color: #white;">0</h3>
            </div>
        """, unsafe_allow_html=True)
    st.write("")

    cols = st.columns([0.13, 0.87],vertical_alignment="top")
    
    traffic_deviation_map = {
        "Car": ["Vägarbete", "Hastighetsbegränsning gäller", "Vägen avstängd", "Fordonshaveri",
                "Olycka", "Följ omledningsskyltar", "Körfältsavstängningar", "Bärgning", "Trafiksignal fungerar ej"],
        "Bus": ["Vägarbete", "Vägen avstängd", "Fordonshaveri",
                "Olycka", "Följ omledningsskyltar", "Körfältsavstängningar", "Bärgning", "Trafiksignal fungerar ej"],
        "Metro": [],  
        "Train": [],  
        "Tram": [],  
        "Ferry": ["Färja"]
    }
    selected_deviations = []
    with cols[0]:
        st.markdown("""
            <div style="padding: 5px; background-color: #27272f; border-radius: 10px; text-align: center;">
            <pre>Välj Färdmedel</pre>
            </div>
        """, unsafe_allow_html=True)
        st.write("")
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

    deviation_map = folium.Map(location=STOCKHOLM_CENTER,zoom_start=9)   
    
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
                        popup=folium.Popup(html_string,max_width=None)).add_to(deviation_map)
       
    
    with cols[1]:
        #st_folium(deviation_map,height=450,use_container_width=True)
        deviation_map = deviation_map._repr_html_()
        html(deviation_map,height=600)

    

if __name__ == "__main__":
    layout()