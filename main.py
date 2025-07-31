import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


##### Child UI  ###########



def show_child_ui():
    # Load data
    @st.cache_data
    def load_data():
        return pd.read_csv("data/child.csv")  # Replace with actual data if different

    df = load_data()

    # Sidebar
    st.sidebar.title("Navigation")
    section = st.sidebar.radio("Go to", [
        "Home",
        "Diarrhea & Pneumonia",
        "Wealth Analysis",
        "Risk Trends",
        "Malaria Analysis",
        "Sub-sector Risk Analysis",
        "Diarrhea Time Trends",
        "Top Indicators",
        "Indicator Metadata"
    ])

    st.sidebar.title("Filters")
    countries = st.sidebar.multiselect("Select Country", df['geographic_area'].unique(), default=df['geographic_area'].unique())
    years = st.sidebar.multiselect("Select Year", sorted(df['time_period'].unique()), default=df['time_period'].unique())
    indicators = st.sidebar.multiselect("Select Indicator", df['indicator'].unique(), default=df['indicator'].unique())

    # Filtered data
    filtered = df[
        df['geographic_area'].isin(countries) &
        df['time_period'].isin(years) &
        df['indicator'].isin(indicators)
    ]

    if section == "Home":
        st.title("👶 Child Health Risk Analysis Dashboard")
        st.write("Welcome to the Child Health Risk Analysis Dashboard. Use the sidebar to navigate through different sections and filter data.")
        
    elif section == "Diarrhea & Pneumonia":
        st.title("💧 Diarrhea & Pneumonia Analysis")

        diar = filtered[filtered['sub_sector'] == 'DIAR']
        pneu = filtered[filtered['sub_sector'] == 'PNEU']

        st.subheader("Average Diarrhea Rate by Residence")
        diar_plot = diar.groupby(['geographic_area', 'residence'])['obs_value'].mean().unstack()
        st.dataframe(diar_plot)

        st.subheader("Pneumonia Vaccination by Residence")
        pneu_plot = pneu.groupby(['geographic_area', 'residence'])['obs_value'].mean().unstack()
        st.dataframe(pneu_plot)

    elif section == "Wealth Analysis":
        st.title("💰 Wealth Disparity in Diarrhea Rates")

        wealth = filtered[filtered['sub_sector'] == 'DIAR']
        wealth = wealth[wealth['wealth_quintile'] != 'total']

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(data=wealth, x='wealth_quintile', y='obs_value', hue='geographic_area', ax=ax)
        plt.title("Diarrhea Rate by Wealth Quintile")
        st.pyplot(fig)

    elif section == "Risk Trends":
        st.title("📈 Risk Category Trends Over Time")

        risk = filtered.groupby(['time_period', 'risk_category']).size().unstack().fillna(0)

        fig, ax = plt.subplots(figsize=(12, 6))
        risk.plot(kind='line', ax=ax)
        plt.title("Risk Category Count Over Time")
        plt.ylabel("Count")
        st.pyplot(fig)

    elif section == "Sub-sector Risk Analysis":
        st.title("📊 Risk Category Breakdown by Sub-sector")
        
        subsector_risk = filtered.groupby(['sub_sector', 'risk_category']).size().unstack(fill_value=0)
        
        st.subheader("Risk Category Distribution by Sub-sector")
        st.dataframe(subsector_risk)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        subsector_risk.plot(kind='bar', stacked=True, ax=ax)
        plt.title("Risk Categories by Sub-sector")
        plt.ylabel("Count")
        plt.xticks(rotation=45)
        st.pyplot(fig)

    elif section == "Diarrhea Time Trends":
        st.title("⏳ Diarrhea Rate Time Trend by Country")
        
        diar = filtered[filtered['sub_sector'] == 'DIAR']
        diar_time_trend_all = diar.groupby(['geographic_area', 'time_period'])['obs_value'].mean().unstack()
        
        st.subheader("Mean Diarrhea Rates Over Time by Country")
        st.dataframe(diar_time_trend_all)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        for country in diar_time_trend_all.index:
            ax.plot(diar_time_trend_all.columns, diar_time_trend_all.loc[country], label=country)
        plt.title("Diarrhea Rate Trends Over Time")
        plt.xlabel("Year")
        plt.ylabel("Mean Diarrhea Rate")
        plt.legend()
        st.pyplot(fig)

    elif section == "Top Indicators":
        st.title("🏆 Top Indicators by Mean Observed Value")
        
        top_indicators = filtered.groupby('indicator')['obs_value'].mean().sort_values(ascending=False).head(10)
        
        st.subheader("Top 10 Indicators with Highest Mean Values")
        st.dataframe(top_indicators)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        top_indicators.plot(kind='barh', ax=ax)
        plt.title("Top Indicators by Mean Observed Value")
        plt.xlabel("Mean Observed Value")
        st.pyplot(fig)

    elif section == "Malaria Analysis":
        st.title("🦟 Malaria (MALA) Sub-Sector Analysis")

        mala_df = df[df['sub_sector'] == 'MALA']

        st.subheader("1. Malaria Risk Category Distribution")
        mala_risk = mala_df['risk_category'].value_counts()
        st.write(mala_risk)

        st.subheader("2. Average Malaria Observation by Country and Year")
        mala_geo_time = mala_df.groupby(['geographic_area', 'time_period'])['obs_value'].mean().reset_index()
        st.dataframe(mala_geo_time)

        st.subheader("3. Urban vs Rural Malaria Rates")
        mala_residence = mala_df[mala_df['residence'] != 'total'] \
            .groupby(['geographic_area', 'time_period', 'residence'])['obs_value'].mean().reset_index()
        st.dataframe(mala_residence)

        st.subheader("4. Malaria Rate by Wealth Quintile")
        mala_wealth = mala_df[mala_df['wealth_quintile'] != 'total'] \
            .groupby(['geographic_area', 'time_period', 'wealth_quintile'])['obs_value'].mean().reset_index()
        st.dataframe(mala_wealth)

        st.subheader("5. Top 5 Malaria Indicators by Mean Observed Value")
        top_mala_indicators = mala_df.groupby('indicator')['obs_value'].mean() \
            .sort_values(ascending=False).head(5).reset_index()
        st.dataframe(top_mala_indicators)

        if st.checkbox("Show Malaria Indicator Bar Plot"):
            top10 = mala_df.groupby(['indicator', 'geographic_area'])['obs_value'] \
                .mean().reset_index().sort_values(by='obs_value', ascending=False).head(10)

            fig, ax = plt.subplots(figsize=(14, 6))
            sns.barplot(data=top10, x='indicator', y='obs_value', hue='geographic_area', ax=ax)
            plt.xticks(rotation=45)
            plt.title("Top 10 Malaria Indicators by Country")
            st.pyplot(fig)
    elif section == "Indicator Metadata":
        st.title("ℹ️ Indicator Metadata")
        met = pd.read_csv("../data/metadata.csv")
        met.drop(columns=['Unnamed: 0', 'category', 'Unnamed: 0.1'], inplace=True, errors='ignore')
        st.dataframe(met)

        st.markdown(
                """
                <hr>
                <div style='text-align:center;'>
                    <p style='font-family:Verdana; color:#555555;'>Developed by Jomo|Victoria|Taoheed</p>
                </div>
                """, unsafe_allow_html=True
            )


############################

##### Mother UI  ###########


def show_mother_ui():

    # Load data
    @st.cache_data
    def load_data():
        return pd.read_csv("data/mother.csv")  # Replace with actual data if different

    df = load_data()

    # Sidebar
    st.sidebar.title("Navigation")
    section = st.sidebar.radio("Go to", [
        "Home",
        "Mother's Health Indicators",
        "Wealth Analysis",
        "Risk Trends",
        "Risk Prediction",
        "Sub-sector Risk Analysis",
        "Indicator Time Trends",
        "Top Indicators",
        "Indicator Metadata"
    ])

    st.sidebar.title("Filters")
    countries = st.sidebar.multiselect("Select Country", df['geographic_area'].unique(), default=df['geographic_area'].unique())
    years = st.sidebar.multiselect("Select Year", sorted(df['time_period'].unique()), default=df['time_period'].unique())
    indicators = st.sidebar.multiselect("Select Indicator", df['indicator'].unique(), default=df['indicator'].unique())

    # Filtered data
    filtered = df[df['geographic_area'].isin(countries) & df['time_period'].isin(years) & df['indicator'].isin(indicators)]
    # filtered = filtered[filtered['residence'].str.lower() != 'total']

    if section == "Home":
        st.title("🤰 Mother Health Risk Analysis Dashboard")
        st.write("Welcome to the Mother Health Risk Analysis Dashboard. Use the sidebar to navigate through different sections and filter data.")
        
    elif section == "Mother's Health Indicators":
        st.title("💊 Mother's Health Indicators Analysis")

        st.subheader("Average Health Indicators by Residence")
        
        health_plot = filtered.groupby(['geographic_area', 'residence'])['obs_value'].mean().unstack()
        st.dataframe(health_plot)

        st.subheader("Education Level Impact")
        edu_plot = filtered.groupby(['geographic_area', "mother's_education_level"])['obs_value'].mean().unstack()
        st.dataframe(edu_plot)

    elif section == "Wealth Analysis":
        st.title("💰 Wealth Disparity in Mother's Health")

        wealth = filtered[filtered['wealth_quintile'] != 'total']

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(data=wealth, x='wealth_quintile', y='obs_value', hue='geographic_area', ax=ax)
        plt.title("Mother's Health Indicators by Wealth Quintile")
        st.pyplot(fig)

    elif section == "Risk Trends":
        st.title("📈 Risk Category Trends Over Time")

        risk = filtered.groupby(['time_period', 'risk_category']).size().unstack().fillna(0)

        fig, ax = plt.subplots(figsize=(12, 6))
        risk.plot(kind='line', ax=ax)
        plt.title("Risk Category Count Over Time")
        plt.ylabel("Count")
        st.pyplot(fig)

    elif section == "Risk Prediction":
        st.title("🔮 Risk Category Prediction")

        st.write("Enter details below to predict the mother health risk category:")

        geo = st.selectbox("Geographic Area", df['geographic_area'].unique())
        year = st.selectbox("Year", sorted(df['time_period'].unique()))
        sector = st.selectbox("Sub Sector", df['sub_sector'].unique())
        residence = st.selectbox("Residence", df['residence'].unique())
        wealth = st.selectbox("Wealth Quintile", df['wealth_quintile'].unique())
        indicator = st.selectbox("Indicator", df['indicator'].unique())
        age = st.selectbox("Age Group", df['current_age'].unique())
        education = st.selectbox("Education Level", df["mother's_education_level"].unique())

        if st.button("Predict"):
            # This should call your trained ML model or statistical model
            st.warning("⚠️ This prediction is for informational purposes only and should not be fully relied on for decision-making.")
            st.success("Predicted Risk Category: Medium (example)")  # Replace with real model output

    elif section == "Sub-sector Risk Analysis":
        st.title("📊 Risk Category Breakdown by Sub-sector")
        
        subsector_risk = filtered.groupby(['sub_sector', 'risk_category']).size().unstack(fill_value=0)
        
        st.subheader("Risk Category Distribution by Sub-sector")
        st.dataframe(subsector_risk)
        
        # Visualize with a stacked bar chart
        fig, ax = plt.subplots(figsize=(12, 6))
        subsector_risk.plot(kind='bar', stacked=True, ax=ax)
        plt.title("Risk Categories by Sub-sector")
        plt.ylabel("Count")
        plt.xticks(rotation=45)
        st.pyplot(fig)

    elif section == "Indicator Time Trends":
        st.title("⏳ Health Indicator Trends Over Time")
        
        time_trend_all = filtered.groupby(['geographic_area', 'time_period'])['obs_value'].mean().unstack()
        
        st.subheader("Mean Indicator Values Over Time by Country")
        st.dataframe(time_trend_all)
        
        # Plot time trends
        fig, ax = plt.subplots(figsize=(12, 6))
        for country in time_trend_all.index:
            ax.plot(time_trend_all.columns, time_trend_all.loc[country], label=country)
        plt.title("Health Indicator Trends Over Time")
        plt.xlabel("Year")
        plt.ylabel("Mean Indicator Value")
        plt.legend()
        st.pyplot(fig)

    elif section == "Top Indicators":
        st.title("🏆 Top Indicators by Mean Observed Value")
        
        top_indicators = filtered.groupby('indicator')['obs_value'].mean().sort_values(ascending=False).head(10)
        
        st.subheader("Top 10 Indicators with Highest Mean Values")
        st.dataframe(top_indicators)
        
        # Visualize top indicators
        fig, ax = plt.subplots(figsize=(12, 6))
        top_indicators.plot(kind='barh', ax=ax)
        plt.title("Top Indicators by Mean Observed Value")
        plt.xlabel("Mean Observed Value")
        st.pyplot(fig)
    elif section == "Indicator Metadata":
        st.title("ℹ️ Indicator Metadata")
        met = pd.read_csv("../data/metadata.csv")
        met.drop(columns=['Unnamed: 0', 'category', 'Unnamed: 0.1'], inplace=True, errors='ignore')
        st.dataframe(met)

        st.markdown(
        """
        <hr>
        <div style='text-align:center;'>
            <p style='font-family:Verdana; color:#555555;'>Developed by Jomo|Victoria|Taheed</p>
        </div>
        """, unsafe_allow_html=True
        )

############################




st.set_page_config(page_title="Health Dashboard", layout="centered")

st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://www.rockypointrotary.org/cdn/shop/products/Maternal_ChildHealthLogoWhiteBckgrnd.png?v=1676183856&width=1346" width="200">
    </div>
    """,
    unsafe_allow_html=True
)

st.title("👪 Maternal and Child Health Dashboard")
st.markdown("This dashboard combines data analysis for **child health** and **maternal health** indicators across Kenya, Uganda, and Tanzania.")
# st.image("https://www.rockypointrotary.org/cdn/shop/products/Maternal_ChildHealthLogoWhiteBckgrnd.png?v=1676183856&width=1346", width=200)
st.markdown("Use the dropdown to switch between analyses for **Child** or **Mother** datasets.")

section = st.selectbox("Choose a Dashboard", ["-- Select --", "Child", "Mother"])


    
    
if section == "Child":
    show_child_ui()
elif section == "Mother":
    show_mother_ui()
else:
    st.warning("Please select a valid dashboard from the dropdown.")
    st.markdown("You can analyze child health indicators or maternal health indicators by selecting the respective options.")
    st.markdown("Use the sidebar to filter data by country, year, and indicator.")