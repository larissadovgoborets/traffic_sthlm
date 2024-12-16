import streamlit as st
from connect_data_warehouse import query_traffic_messages


def layout():
    df = query_traffic_messages()

    st.title("Trafikmeddelanden")
    st.write(
        "test123 "
    )




if __name__ == "__main__":
    layout()