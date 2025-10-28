import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

import preprocessor
import helper

# Load data
df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)

st.sidebar.title("Olympics Analysis")

st.markdown("---")  # Optional: Add a separator line
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        color: grey;
        text-align: center;
        padding: 5px;
        font-size: 0.8em;
    }
    </style>
    <div class="footer">
        <p>Copyright © Kopila Devkota's Web App | Made By Kopila Devkota.</p>
    </div>
    """,
    unsafe_allow_html=True
)

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete Wise Analysis')
)

# ------------------ Medal Tally ------------------ #
if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox('Select Year', years)
    selected_country = st.sidebar.selectbox('Select Country', country)
    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.title(f"Medal Tally in {selected_year} Olympics")
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.title(f"{selected_country} Overall Performance")
    else:
        st.title(f"{selected_country} Performance in {selected_year} Olympics")

    st.table(medal_tally)

# ------------------ Overall Analysis ------------------ #
elif user_menu == 'Overall Analysis':
    editions = df['Year'].nunique() - 1
    cities = df['City'].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    athletes = df['Name'].nunique()
    nations = df['region'].nunique()

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('Athletes')
        st.title(athletes)

    st.title('Participating Nations Over The Years')
    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x="Year", y="count", labels={"count": "Number of Nations"})
    st.plotly_chart(fig)

    st.title('Number of Events Over The Years')
    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Year", y="count", labels={"count": "Number of Events"})
    st.plotly_chart(fig)

    st.title('Athletes Over The Years')
    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x="Year", y="count", labels={"count": "Number of Athletes"})
    st.plotly_chart(fig)

    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select Sport', sport_list)
    x = helper.most_successful(df, selected_sport)
    st.table(x)

# ------------------ Country-wise Analysis ------------------ #
elif user_menu == 'Country-wise Analysis':
    st.sidebar.title('Country wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select Country', country_list)

    st.title(f"{selected_country} Medal Tally Over The Years")
    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.plotly_chart(fig)

    st.title(f"{selected_country} Excels in the following sports")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(25, 25))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    st.title(f"Top 10 athletes of {selected_country}")
    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)

# ------------------ Athlete Wise Analysis ------------------ #
elif user_menu == 'Athlete Wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    # Distribution of Age
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4],
                             ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    # Distribution of Age wrt Sports
    x = []
    name = []
    famous_sports = [
        'Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics', 'Swimming',
        'Badminton', 'Sailing', 'Gymnastics', 'Art Competitions', 'Handball',
        'Weightlifting', 'Wrestling', 'Water Polo', 'Hockey', 'Rowing', 'Fencing',
        'Equestrianism', 'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving',
        'Canoeing', 'Tennis', 'Modern Pentathlon', 'Golf', 'Softball', 'Archery',
        'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
        'Rhythmic Gymnastics', 'Rugby Sevens', 'Trampolining', 'Beach Volleyball',
        'Triathlon', 'Rugby', 'Lacrosse', 'Polo', 'Cricket', 'Ice Hockey',
        'Racquets', 'Motorboating', 'Croquet', 'Figure Skating', 'Jeu De Paume',
        'Roque', 'Basque Pelota', 'Alpinism', 'Aeronautics'
    ]
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        age_data = temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna()
        if len(age_data) >= 2 and len(age_data.unique()) > 1:
            x.append(age_data)
            name.append(sport)

    if x:
        fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
        fig.update_layout(autosize=False, width=1000, height=600)
        st.title("Distribution of Age wrt Sports")
        st.plotly_chart(fig)
    else:
        st.warning("Not enough valid data to plot the distribution.")

    # Height vs Weight
    st.title('Height Vs Weight')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(x='Weight', y='Height', hue='Medal', style='Sex', data=temp_df)
    st.pyplot(fig)

    # Men vs Women
    st.title('Men Vs Women Over the Years')
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
    # app.py (Add this section to the bottom of the file)
    # ------------------ Footer/Copyright ------------------ #

    # Use an expander to visually separate the footer and keep it clean
    # or just use st.markdown directly.
