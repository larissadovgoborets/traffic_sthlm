from typing import Tuple
import pandas as pd
from datetime import datetime

def __get_date(df)-> Tuple[str,str]:
    start_date = datetime.fromisoformat(str(df['START_TIME'])).strftime("%Y-%m-%d %H:%M")
    if pd.isnull(df['END_TIME']):
        end_date = "tid ej angiven"
    else:
        end_date = datetime.fromisoformat(str(df['END_TIME'])).strftime("%Y-%m-%d %H:%M")
    return (start_date,end_date)

def __build_html_string(df,start_date,end_date)-> str:
    deviation = df['MESSAGE_CODE']
    if deviation == "Färja":
        html_content = f"""
        <div style="width: 301px; box-sizing: border-box;">
        <h4>{deviation}</h4>
        <p><b>{df['HEADER']}:</b><br>
        {df['LOCATION_DESCRIPTOR']}
        </p>
        <p><b>Trafikbegränsning:</b><br>
        {df['TRAFFIC_RESTRICTION_TYPE']}
        <p/>
        <pre>Giltlig från:       {start_date}<br>Beräknas pågå till: {end_date}</pre>
        </div>

        """
    elif deviation == "Vägarbete":
        html_content = f"""
                <div style="width: 301px; box-sizing: border-box;">
                    <h4>{deviation}</h4>
                    <p><b>Plats:</b><br>
                    {df['LOCATION_DESCRIPTOR']}
                    </p>
                    <p><b>Trafikmeddelande:</b><br>
                    {df['MESSAGE']}
                    </p>
                    <p><b>Påverkansgrad:</b><br>
                    {df['SEVERITY_TEXT']}
                    </p>
                    <pre>Giltlig från:       {start_date}<br>Beräknas pågå till: {end_date}</pre>
                </div>
                """
    elif deviation == "Körfältsavstängningar":
               html_content = f"""
                <div style="width: 301px; box-sizing: border-box;">
                    <h4>{deviation}</h4>
                    <p><b>Plats:</b><br>
                    {df['LOCATION_DESCRIPTOR']}
                    </p>
                    <p><b>Trafikmeddelande:</b><br>
                    {df['MESSAGE']}
                    </p>
                    <p><b>Trafikbegränsning:</b><br>
                    {df['TRAFFIC_RESTRICTION_TYPE']}<br>
                    {df['AFFECTED_DIRECTION']}
                    <p/>
                    <p><b>Påverkansgrad:</b><br>
                    {df['SEVERITY_TEXT']}
                    </p>
                    <pre>Giltlig från:       {start_date}<br>Beräknas pågå till: {end_date}</pre>
                </div>
                """
    elif deviation == "Hastighetsbegränsning gäller":
        html_content = f"""
            <div style="width: 301px; box-sizing: border-box;">
                <h4>{deviation}</h4>
                <p><b>Plats:</b><br>
                {df['ROAD_NUMBER']}
                </p>
                <p><b>Tillfälliga begränsningar:</b><br>
                {df['TEMPORARY_LIMIT']}<br>
                {df['AFFECTED_DIRECTION']}
                </p>
                <p><b>Orsak:</b><br>
                {df['TRAFFIC_RESTRICTION_TYPE']}
                </p>
                <p><b>Påverkansgrad:</b><br>
                {df['SEVERITY_TEXT']}
                </p>
                <pre>Giltlig från:       {start_date}<br>Beräknas pågå till: {end_date}</pre>
            </div>
                """
            
    elif deviation == 'Vägen avstängd' or deviation == 'Olycka' or deviation == 'Bärgning' or deviation == 'Fordonshaveri':
        html_content = f"""
                <div style="width: 301px; box-sizing: border-box;">
                    <h4>{deviation}</h4>
                    <p><b>Plats:</b><br>
                    {df['LOCATION_DESCRIPTOR']}
                    </p>
                    <p><b>Trafikmeddelande:</b><br>
                    {df['MESSAGE']}
                    </p>
                    <p><b>Påverkansgrad:</b><br>
                    {df['SEVERITY_TEXT']}
                     </p>
                    <pre>Giltlig från:       {start_date}<br>Beräknas pågå till: {end_date}</pre>
                </div>
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
    start_date,end_date = __get_date(df)
    html_content = __build_html_string(df,start_date,end_date)
    return html_content 

def get_deviation_icon_image_path(df) -> str:
    deviation = df['MESSAGE_CODE']
    traffic_deviation_icons = {"Färja":"./map_icons/ferry2.png",
                        "Vägarbete":"./map_icons/road_work.png",
                        "Vägen avstängd":"./map_icons/default_icon.png",
                        "Körfältsavstängningar":"./map_icons/road_work.png",
                        "Hastighetsbegränsning gäller":{"Hastighet: 70km/h":"./map_icons/speed_limit_70.png",
                                                        "Hastighet: 50km/h":"./map_icons/speed_limit_50.png",
                                                        "Hastighet: 40km/h":"./map_icons/speed_limit_40.png",
                                                        "Hastighet: 30km/h":"./map_icons/speed_limit_30.png"},
                        "Vägren":"./map_icons/default_icon.png",
                        "Följ omledningsskyltar":"./map_icons/default_icon.png",
                        "Broöppning":"./map_icons/default_icon.png",
                        "Bärgning":"./map_icons/default_icon.png",
                        "Trafiksignal fungerar ej":"./map_icons/default_icon.png",
                        "Olycka":"./map_icons/default_icon.png",
                        "Fordonshaveri":"./map_icons/default_icon.png"}
    if deviation not in traffic_deviation_icons:
         image_path = "./map_icons/default_icon.png"
         
    elif deviation == "Hastighetsbegränsning gäller":
            speed_limit = df['TEMPORARY_LIMIT']
            image_path = traffic_deviation_icons[deviation][speed_limit]
    else:
            image_path = traffic_deviation_icons[deviation]
    
    return image_path
