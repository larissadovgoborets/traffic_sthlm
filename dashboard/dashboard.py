import folium.features
import folium.map
import streamlit as st
import folium
from connect_data_warehouse import query_traffic_messages
from folium_map_utility_functions import create_marker_tooltip, get_deviation_icon_image_path
from streamlit.components.v1 import html
from present_sl_data import display_sl_data
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

    query = st.text_input("Sök på väg")
    deviation_types = df["MESSAGE_CODE"].unique()
    # Filter on deviation
    selected_types = st.multiselect('Välj avvikelse', deviation_types, default=deviation_types)
    filtered_df = df[df['MESSAGE_CODE'].isin(selected_types)]
    
    #Filter on search query
    if query:
        filtered_df = filtered_df[df["LOCATION_DESCRIPTOR"].str.contains(rf'\b{query}\b', case=False, na=False) |
                                  df["ROAD_NUMBER"].str.contains(rf'\b{query}\b', case=False, na=False)]
    
    deviation_map = folium.Map(location=STOCKHOLM_CENTER,zoom_start=9)   
    # Loop over dataframe to place markers on the map for every Traffic deviation
    for index, row in filtered_df.iterrows():
        # Coordinates for traffic deviation
        location = row['LATITUDE'],row['LONGITUDE']
        
        # Returns HTML code for marker tooltip
        html_string = create_marker_tooltip(row)
        
        # Returns the image associated with the Traffic deviation
        image_path = get_deviation_icon_image_path(row)
        
        #Create a marker on the map
        folium.Marker(location,
                        icon=folium.CustomIcon(icon_image=image_path, icon_size=(30,30)),
                        popup=folium.Popup(html_string,max_width=None)).add_to(deviation_map)
       
    
    deviation_map = deviation_map._repr_html_()
    html(deviation_map,height=450)


if __name__ == "__main__":
    layout()
    display_sl_data()