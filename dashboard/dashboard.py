import folium.features
import folium.map
import streamlit as st
import folium
import pandas as pd
from folium import IFrame
from streamlit_folium import st_folium
from connect_data_warehouse import query_traffic_messages
from datetime import datetime

STOCKHOLM_CENTER = (59.325,18.05)

def get_date(df):
    start_date = datetime.fromisoformat(str(df['START_TIME'])).strftime("%Y-%m-%d %H:%M")

    if pd.isnull(df['END_TIME']):
        end_date = "tid ej angiven"
    else:
        end_date = datetime.fromisoformat(str(df['END_TIME'])).strftime("%Y-%m-%d %H:%M")
    return (start_date,end_date)

def build_html_string(df,start_date,end_date)-> str:
    deviation = df['MESSAGE_CODE']
    if deviation == "Färja":
        html_content = f"""
        <div style="width: 301px; box-sizing: border-box;">
        <h4>{deviation}</h4>
        <pre>Giltlig från:       {start_date}<br>Beräknas pågå till: {end_date}</pre>
        </div>

        """
    elif deviation == "vägarbete":
        html_content = f"""
                <div style="width: 301px; box-sizing: border-box;">
                    <h4>{deviation}</h4>
                    <pre>Giltlig från:       {start_date}<br>Beräknas pågå till: {end_date}</pre>
                </div>
                """
    elif deviation == "Vägen avstängd":
        html_content = f"""
                <div style="width: 301px; box-sizing: border-box;">
                    <h4>{deviation}</h4>
                    <pre>Giltlig från:       {start_date}<br>Beräknas pågå till: {end_date}</pre>
                </div>
                """
    elif deviation == "Hastighetsbegränsning gäller":
        html_content = f"""
                <h4>{deviation}</h4>
                <p>{df['ROAD_NUMBER']}</p>
                <p>Tillfälliga begränsningar:<br>
                {df['TEMPORARY_LIMIT']}<br>
                {df['AFFECTED_DIRECTION']}
                </p>
                <pre>Giltlig från:       {start_date}<br>Beräknas pågå till: {end_date}</pre>
                """
    else:
        html_content = f"""
                <div style="width: 301px; box-sizing: border-box;">
                    <h4>{deviation}</h4>
                    <pre>Giltlig från:       {start_date}<br>Beräknas pågå till: {end_date}</pre>
                </div>
                """
    return html_content
def create_marker_tooltip(df) -> str:  
   
    start_date,end_date = get_date(df)
    html_content = build_html_string(df,start_date,end_date)
    return html_content 

def layout():
    df = query_traffic_messages().dropna(subset=['LONGITUDE'])
    
    traffic_deviation_icons = {"Färja":"./map_icons/ferry.png",
                        "Vägarbete":"./map_icons/road_work.png",
                        "Vägen avstängd":"./map_icons/default_icon.png",
                        "Körfältsavstängningar":"./map_icons/default_icon.png",
                        "Hastighetsbegränsning gäller":{"Hastighet: 50km/h":"./map_icons/speed_limit_50.png",
                                                        "Hastighet: 40km/h":"./map_icons/speed_limit_40.png",
                                                        "Hastighet: 30km/h":"./map_icons/speed_limit_30.png"},
                        "Vägren":"./map_icons/default_icon.png",
                        "Följ omledningsskyltar":"./map_icons/default_icon.png",
                        "Broöppning":"./map_icons/default_icon.png",
                        "Bärgning":"./map_icons/default_icon.png",
                        "Trafiksignal fungerar ej":"./map_icons/default_icon.png",
                        "Olycka":"./map_icons/default_icon.png",
                        "Fordonshaveri":"./map_icons/default_icon.png"}

    
    #st.markdown("<h1 style='text-align: center; color: red;'>Traffic Stockholm</h1>", unsafe_allow_html=True)
    #st.set_page_config(layout="wide")	
    st.header("Traffic Stockholm")			
    map = folium.Map(location=STOCKHOLM_CENTER,zoom_start=9,)
    for index, row in df.iterrows():
        location = row['LATITUDE'],row['LONGITUDE']
        deviation = row['MESSAGE_CODE']
        html_string = create_marker_tooltip(row)
        
        if deviation == "Hastighetsbegränsning gäller":
            speed_limit = row['TEMPORARY_LIMIT']
            image_path = traffic_deviation_icons[deviation][speed_limit]
        else:
            image_path = traffic_deviation_icons[deviation]
        folium.Marker(location,
                        icon=folium.CustomIcon(icon_image=image_path),
                        popup=folium.Popup(html_string,max_width=None)).add_to(map)
    
    st_folium(map,use_container_width=True)

    

if __name__ == "__main__":
    layout()