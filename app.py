import streamlit as st
from dbhelper import DB
import plotly.graph_objects as go
import plotly.express as px

db = DB()

st.sidebar.title('Flights Analytics')

user_option = st.sidebar.selectbox('Menu', ['Select One', 'Check Flights', 'Analytics'])

if user_option == 'Check Flights':
    st.title('Check Flights')

    col1, col2 = st.columns(2)

    city = db.fetch_city_names()

    with col1:
        source = st.selectbox('Source', sorted(city))
    with col2:
        destination = st.selectbox('Destination', sorted(city))

    if st.button('Search'):
        results = db.fetch_all_flights(source, destination)
        st.dataframe(results)

elif user_option == 'Analytics':
    st.header("Airline Frequency")
    airline, frequency = db.fetch_airline_frequency()
    fig = go.Figure(
        go.Pie(
            labels=airline,
            values=frequency,
            hoverinfo="label+percent",
            textinfo="value"
        )
    )
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    st.header("Busy Airports")
    city, frequency1 = db.busy_airport()
    fig = px.bar(
        x=city,
        y=frequency1,
        labels={'x': 'City', 'y': 'Frequency'},
        title='Busy Airports'
    )
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    st.header("Daily Flight Frequency")
    date, frequency2 = db.daily_frequency()
    fig = px.line(
        x=date,
        y=frequency2,
        labels={'x': 'Date', 'y': 'Frequency'},
        title='Daily Flight Frequency'
    )
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

else:
    st.title('Please select an option from the sidebar.')
