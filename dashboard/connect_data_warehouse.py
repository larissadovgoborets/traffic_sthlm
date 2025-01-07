import os
from dotenv import load_dotenv
import snowflake.connector
import pandas as pd 
import streamlit as st

@st.cache_data
def query_traffic_messages(query='SELECT * FROM mart_trafikverket_traffic_messages_dgstr'):

    load_dotenv()

    with snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        role=os.getenv("SNOWFLAKE_ROLE"),
    ) as conn:

        # Execute the query
        df = pd.read_sql(query, conn)

        return df

def query_sl_announcements(query="""SELECT * FROM MART_SL_DEVIATIONS
                           WHERE publish_upto > CURRENT_TIMESTAMP() 
                           ORDER BY priority DESC"""): # Order by priority to show the most important announcements first

    load_dotenv()

    with snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        role=os.getenv("SNOWFLAKE_ROLE"),
    ) as conn:

        # Execute the query
        df = pd.read_sql(query, conn)

        return df
    
if __name__ == "__main__":
    print(query_traffic_messages())
    df = query_traffic_messages()
    print(df.info())
    sl_df = query_sl_announcements()
    print(sl_df.head())