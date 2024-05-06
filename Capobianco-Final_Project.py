"""
Name: Sam Capobianco
CS230-5
Data: Open_Pubs (Sample of 10,000)
URL:

Description: This application displays information on pubs in England using a sample of 10,000 open pubs. There are 4
tabs including a home page, maps, pub density, and name commonality. Each tab tells a story about England's renowned
pub culture.

"""

import streamlit as st
import pydeck as pdk
import pandas as pd
import matplotlib.pyplot as plt
import emoji

path = "C:/Users/samca/PycharmProjects/Capobianco-Final_Project/open_pubs_10000_sample.csv"

df_pubs = pd.read_csv(path)
df_pubs.rename(columns={"latitude":"lat", "longitude": "lon"}, inplace= True)

# Data Cleaning [DA1]
df_pubs['lat'] = pd.to_numeric(df_pubs['lat'], errors='coerce')
df_pubs['lon'] = pd.to_numeric(df_pubs['lon'], errors='coerce')
df_pubs = df_pubs.dropna(subset=['lat', 'lon'])  # Remove rows with NaN in lat or lon
df_pubs = df_pubs.reset_index(drop=True)  # Reset index after removing rows

# Creates a sidebar menu [ST4]
st.sidebar.header("Menu")
tabs = ["Home Page", "Maps", "Pub Density", "Name Commonality"]
selected_tab = st.sidebar.radio("", tabs)

if selected_tab == "Home Page":

    st.markdown((emoji.emojize(":beer:" * 35)))

    st.title("Welcome to English Pub Insights")
    st.write("\nHere, you will learn about England's Renowned Pub Culture and the statistics behind it. The stats gathered "
            "are from a sample of 10,000 pubs around England. Please watch the video below or select a tab to get "
            "started...")

    youtube_video_url = "https://www.youtube.com/watch?v=qxzcIRzfb04"
    st.video(youtube_video_url)

if selected_tab == "Maps":
    st.title("Maps of English Pubs")

    ICON_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Emoji_u1f37a.svg/2048px-Emoji_u1f37a.svg.png"

    # Format icon
    icon_data = {
        "url": ICON_URL,
        "width": 100,
        "height": 100,
        "anchorY": 1
    }

    # Add icons to dataframe
    df_pubs["icon_data"] = None
    for i in df_pubs.index:
        df_pubs.at[i, "icon_data"] = icon_data

    # Create a layer with your custom icon
    icon_layer = pdk.Layer(type="IconLayer",
                           data=df_pubs,
                           get_icon="icon_data",
                           get_position='[lon,lat]',
                           get_size=40,
                           pickable=True)

    # Create default view state
    view_state = pdk.ViewState(
        latitude=df_pubs["lat"].mean(),
        longitude=df_pubs["lon"].mean(),
        zoom=5.5,
        pitch=3
        )

    # Creates tool tip for map
    tool_tip = {"html": "Pub Name:<br/> <b>{name}</b>",
                "style": {"backgroundColor": "gold",
                          "color": "white"}
                }

    # Compiles the map and adds style/layers
    icon_map = pdk.Deck(
        map_style='mapbox://styles/mapbox/navigation-day-v1',
        layers=[icon_layer],
        initial_view_state=view_state,
        tooltip=tool_tip
        )

    # Displays Map title and simple map
    map1_title = '<p style="text-align: center; font-size: 30px;"> Simple Map'
    st.markdown(map1_title, unsafe_allow_html=True)
    st.map(df_pubs)

    # Displays icon/detailed map [VIZ1]
    map2_title = '<p style="text-align: center; font-size: 30px;"> Emoji Map with Pub Names'
    st.markdown(map2_title, unsafe_allow_html=True)
    st.pydeck_chart(icon_map)



if selected_tab == "Pub Density":
    st.title("Pub Density")

    # Filter data by city to create sub data frame [DA4]
    big_cities = ['City of London', 'Birmingham', "Liverpool", "Manchester"]
    df_big_cities = df_pubs.loc[df_pubs['local_authority'].isin(big_cities)]

    # Count amount of pubs in each city using .size [DA7]
    city_counts = df_big_cities.groupby('local_authority').size()
    city_counts = city_counts.sort_values(ascending=False)  # [DA2]

    # Creates and displays bar chart with title [VIZ2]
    city_bar_chart = city_counts.plot(kind = "bar")
    city_bar_chart.set_xlabel("City")
    chart1_title = '<p style="text-align: center; font-size: 30px;"> Pubs in Britains 4 Largest Cities'
    st.markdown(chart1_title, unsafe_allow_html=True)
    st.pyplot()

    st.write("Birmingham may have the most pubs of the 4 largest cities, but it is important to consider that "
             "this data comes from a sample")

    chart1_title = '<p style="text-align: center; font-size: 30px;"> Top 10 Towns with Most Pubs'
    st.markdown(chart1_title, unsafe_allow_html=True)

    # Gets the top 10 towns with the most pubs and prints [DA3]
    top_10 = df_pubs['local_authority'].value_counts().nlargest(10)
    st.write(top_10)

    # Create a list from the series to allow for user selection
    town_series = df_pubs['local_authority']
    town_list = town_series.tolist()
    town_list = list(set(town_list))  # Remove duplicate town names
    town_list = sorted(town_list)  # Alphabetical order

    # Defines a function that takes user selections & returns a series of counts of pubs in each town [PY1][PY3]
    def user_cities(town_list, select_towns=None):
        if select_towns is None:
            select_towns = big_cities
        town_counts = town_list.value_counts()
        selected_town_counts = town_counts[select_towns]

        return selected_town_counts


    input_title = '<p style="text-align: center; font-size: 30px;"> Amount of Pubs in...'
    st.markdown(input_title, unsafe_allow_html=True)

    # Prompts user to input a town and returns how many pubs in that town [ST1]
    user_town = st.text_input("Please enter a town in England")
    if user_town:
        selected_town = user_cities(town_series, user_town)
        st.write(f"{user_town} has {selected_town} pubs!")
    else:
        st.write("Please enter a valid town name to get the amount of pubs")

    chart2_title = '<p style="text-align: center; font-size: 30px;"> Choose Cities to Compare'
    st.markdown(chart2_title, unsafe_allow_html=True)

    # Displays multiselect allowing user to choose towns from town list [ST2]
    multiselect_towns = st.multiselect("Please select some towns", town_list)

    # Creates and displays bar chart with selected cities [VIZ3]
    if multiselect_towns:
        selected_cities = user_cities(town_series, multiselect_towns)
        selected_cities_bar_chart = selected_cities.plot(kind="bar", stacked=True)
        selected_cities_bar_chart.set_xlabel("Town")
        st.pyplot()
    else:
        st.write(" ")


if selected_tab == "Name Commonality":
    name_series = df_pubs["name"]
    name_list = name_series.tolist()

    search_terms = ["Inn", "Tavern", "Club", "Golf", "Hotel", "Pub"]

    # Defines a function that returns term occurrences. Utilized ChatGPT to help draft logic, complex list comprehension
    def count_term_occurrences(name_list, search_terms):
        # Term counts using list comprehension [PY4]
        term_counts = {term: sum(1 for name in name_list if term in name) for term in search_terms}
        # Count names without any search term using list comprehension
        other_count = sum(1 for name in name_list if not any(term in name for term in search_terms))
        # Adds "Other" key value pair
        term_counts["Other"] = other_count

        # Returns a dictionary storing the terms and their respective counts
        return term_counts

    # Call above function
    term_counts = count_term_occurrences(name_list, search_terms)

    # Utilized chat to help
    plt.figure()

    # Uses term_counts dictionary and key value pairs to help plot pie chart [PY5]
    plt.pie(
        term_counts.values(),
        labels=term_counts.keys(),
        autopct="%1.1f%%",
    )

    chart3_title = '<p style="text-align: center; font-size: 30px;"> Name Prevalence Pie Chart'
    st.markdown(chart3_title, unsafe_allow_html=True)

    # Display Pie Chart [VIZ4]
    st.pyplot(plt)

    search_term_title = '<p style="text-align: center; font-size: 30px;"> Choose a Term!'
    st.markdown(search_term_title, unsafe_allow_html=True)

    # Create a select box to let user choose what search term they want [ST3]
    selected_term = st.selectbox("Pick a search term", search_terms)

    selected_term_count = term_counts.get(selected_term)

    # Performs calculation on data frame to get selected term percentage. No Numeric Data so couldn't do columns [DA9]
    total_pubs = len(df_pubs)
    selected_term_percentage = round((selected_term_count / total_pubs) * 100, 1)

    st.write(f"There are {selected_term_count} pubs in the sample that include the word {selected_term}. This "
             f"represents {selected_term_percentage}% of the sample.")
