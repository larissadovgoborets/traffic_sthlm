import streamlit as st
import pandas as pd
from connect_data_warehouse import query_sl_announcements

def display_sl_data():
    
    # Fetch SL announcements data
    df = query_sl_announcements()

    # Choose the columns to display
    display_df = df[['TRANSPORT_MODE', 'LINE_KEY','SCOPE_ALIAS', 'HEADER', 'MESSAGE', 'STOP_POINT_NAME', 'PUBLISH_UPTO']]

    # Translate the column names to Swedish
    display_df.columns = ['Transportmedel','Linje', 'Omfattning', 'Rubrik', 'Meddelande', 'Hållplats', 'Giltigt till']

    #Translate the transport modes to Swedish
    display_df['Transportmedel'] = display_df['Transportmedel'].replace({'BUS':'Buss', 'METRO':'Tunnelbana', 'TRAIN':'Pendeltåg', 'TRAM':'Spårvagn', 'SHIP':'Pendelbåt'})
    # Set up the Streamlit app
    st.title("SL Trafikinformation")

    # Display the total number of deviations for each transport mode
    st.markdown("## Antal störningar just nu") 

    cols = st.columns(6)

    with cols[0]:
        st.metric(label="Totalt", value= df['DEVIATION_CASE_ID'].count())

    with cols[1]:
        st.metric(
            label="Bussar",
            value=df[df["TRANSPORT_MODE"] == "BUS"]["TRANSPORT_MODE"].count(),
        )

    with cols[2]:
        st.metric(
            label="Tunnelbana",
            value=df[df["TRANSPORT_MODE"] == "METRO"]["TRANSPORT_MODE"].count(),
        )

    with cols[3]:
        st.metric(
            label="Pendeltåg",
            value=df[df["TRANSPORT_MODE"] == "TRAIN"]["TRANSPORT_MODE"].count(),
        )

    with cols[4]:
        st.metric(
            label="Spårvagn",
            value=df[df["TRANSPORT_MODE"] == "TRAM"]["TRANSPORT_MODE"].count(),
        )

    with cols[5]:
        st.metric(
            label="Pendelbåt",
            value=df[df["TRANSPORT_MODE"] == "SHIP"]["TRANSPORT_MODE"].count(),
        )

    # Add a filter for the transport mode
    transport_modes = display_df['Transportmedel'].unique()
    selected_modes = st.multiselect('Välj transportmedel:', transport_modes, default=transport_modes)

    # Filter data based on selected transport modes
    filtered_data = display_df[display_df['Transportmedel'].isin(selected_modes)]

    # Add a search bar for a specific line
    search_line = st.text_input('Sök efter linje:', '')

    # Filter data based on the search line
    if search_line:
        filtered_data = filtered_data[filtered_data['Linje']== int(search_line)]

    # Display the dataframe based on the filter
    st.write("SL Announcements Data")
    filtered_data_display = filtered_data[['Transportmedel', 'Omfattning', 'Rubrik', 'Meddelande', 'Giltigt till']]
    
    # Drop duplicates from the filtered data display (because of the station area and point joins)
    filtered_data_display = filtered_data_display.drop_duplicates()

    # Display the filtered data
    st.write(filtered_data_display)

if __name__ == "__main__":
    display_sl_data()

