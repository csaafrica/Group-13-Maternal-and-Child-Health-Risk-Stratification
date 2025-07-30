import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

def show_mother_ui():

    # Load data
    @st.cache_data
    def load_data():
        return pd.read_csv("../data/mother.csv")  # Replace with actual data if different

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