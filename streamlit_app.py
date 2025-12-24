import streamlit as st
from common.hello import say_hello


st.title(f"Example streamlit app using snowpark session. {say_hello()}")



def get_snowpark_session():
    """Get Snowpark session, works everywhere"""
    try:
        # This ONLY works when running INSIDE Snowflake
        from snowflake.snowpark.context import get_active_session

        return get_active_session()
    except:
        # This works LOCALLY with credentials

        st.text("not running inside snowflake")

        from snowflake.snowpark import Session

        # NB This uses .streamlit/secrets.toml

        session = Session.builder.configs({
            "account": st.secrets["connections"]["snowflake"]["account"],
            "user": st.secrets["connections"]["snowflake"]["user"],
            "password": st.secrets["connections"]["snowflake"]["password"],
            "warehouse": st.secrets["connections"]["snowflake"]["warehouse"],
            "database": st.secrets["connections"]["snowflake"]["database"],
            "schema":  st.secrets["connections"]["snowflake"]["schema"]
        }).create()


        # Hard coded connection details:
        # session = Session.builder.configs({
        #     "account": "ES10286-MARKETPLACE",
        #     "user": "richard_mp",
        #     "password": "xxxxxxxx",
        #     "warehouse": "DEV_DEVELOPER_WH",
        #     "database": "DEV_STREAMLIT_DEMO",
        #     "schema":  "schema1"
        # }).create()


        # Other way to get connection details: Use non-snowflake streamlit connection method just to get access to connection details
        # This feels a bit hacky but works, and is only used when running locally for dev testing:
        # conn = st.connection("snowflake")  
        # password = st.secrets["connections"]["snowflake"]["password"] # however we have to get password this way as conn._instance._password is always empty
        # session = Session.builder.configs({
        #     "account": conn._instance._account,
        #     "user": conn._instance._user,
        #     "password": password,
        #     "warehouse": conn._instance._warehouse,
        #     "database": conn._instance._database,
        #     "schema":  conn._instance._schema
        # }).create()
        


        return session
 
    

# Get session (works in both environments)
session = get_snowpark_session()

query = "SELECT COL1, COL2 FROM DAFT_TABLE;"
df = session.sql(query).collect()

# Iterate through the rows
for row in df:
    st.write(f"{row.COL1} has a :{row.COL2}:")
