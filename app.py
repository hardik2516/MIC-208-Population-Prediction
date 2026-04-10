import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Ensure wide mode and premium dark setup by default
st.set_page_config(
    page_title="India Population Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

    /* Hide Streamlit default components */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {
        padding-top: 2rem !important;
    }

    /* Global Typography & Background */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Animated Gradient Background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(-45deg, #090B10, #161224, #0A1128, #0a0a0a);
        background-size: 400% 400%;
        animation: gradientBG 20s ease infinite;
        color: #e6edf3;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Elegant Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(10, 10, 15, 0.4) !important;
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Modern Dashboard Headers with Text Gradients */
    h1, h2, h3 {
        background: linear-gradient(to right, #ffffff, #d2a8ff, #58a6ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        margin-bottom: 5px;
        letter-spacing: -0.5px;
    }
    
    /* Ultra Glassmorphism KPI Cards */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0.01) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-top: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255,255,255,0.1);
        transition: all 0.5s cubic-bezier(0.2, 0.8, 0.2, 1);
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 30px 60px rgba(163, 113, 247, 0.15), inset 0 1px 0 rgba(255,255,255,0.2);
        border-color: rgba(163, 113, 247, 0.4);
    }

    /* Metric Label Styling */
    div[data-testid="stMetricLabel"] > div > div > p {
        font-size: 1.1rem !important;
        font-weight: 400 !important;
        color: #aeb5be !important;
        letter-spacing: 0.5px;
    }
    div[data-testid="stMetricValue"] > div {
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        letter-spacing: -1px;
        color: #ffffff;
        text-shadow: 0px 0px 30px rgba(255, 255, 255, 0.2);
    }
    
    /* Custom divider */
    hr {
        border-color: rgba(255, 255, 255, 0.05);
        margin-top: 1em;
        margin-bottom: 2em;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- Data Loading -----------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("india_population_complete_1950_2050.csv")
        return df
    except FileNotFoundError:
        st.error("Data file not found. Ensure 'india_population_complete_1950_2050.csv' is in the root directory.")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

# ----------------- Sidebar & Filtering -----------------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3233/3233483.png", width=60) # A general trend icon
st.sidebar.title("Configuration")

min_year = int(df['Year'].min())
max_year = int(df['Year'].max())

year_range = st.sidebar.slider(
    "Select Year Range:",
    min_value=min_year,
    max_value=max_year,
    value=(2020, max_year),
    step=1
)

st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Specific Year Insights")
insight_year = st.sidebar.slider(
    "Select Year for Insights:",
    min_value=min_year,
    max_value=max_year,
    value=max_year,
    step=1
)

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info(
    "This dashboard predicts the Total, Male, and Female population of India up to 2050 "
    "using Ridge Polynomial Regression. The 'Female Population' is structurally sound (Derived mathematically as Total - Male)."
)

# Filter dataframe based on slider
filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])].copy()

# ----------------- KPIs (Top Bar) -----------------
st.title("📈 India Population Forecast Dashboard")
st.markdown("Interactive analysis of historical data and future population projections.")

# Extract values for the specific insight year selected
insight_data = df[df['Year'] == insight_year].iloc[0]
total_pop = insight_data['Predicted Total Population']
male_pop = insight_data['Predicted Male Population']
female_pop = insight_data['Predicted Female Population']

# Calculate YoY Growth for Insights if not the first year
yoy_growth = 0
if insight_year > min_year:
    prev_year_data = df[df['Year'] == insight_year - 1].iloc[0]
    yoy_growth = total_pop - prev_year_data['Predicted Total Population']

def format_number(num):
    if num >= 1e9:
        return f"{num / 1e9:.2f} B"
    elif num >= 1e6:
        return f"{num / 1e6:.2f} M"
    else:
        return f"{num:,.0f}"

st.subheader(f"💡 Key Insights for {insight_year}")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label=f"Total Pop.", value=format_number(total_pop), delta=format_number(yoy_growth) if yoy_growth else None)
with col2:
    st.metric(label=f"Male Pop.", value=format_number(male_pop))
with col3:
    st.metric(label=f"Female Pop.", value=format_number(female_pop))
with col4:
    male_ratio = (male_pop / total_pop) * 100
    st.metric(label=f"Male/Female Ratio", value=f"{male_ratio:.1f}% M")

st.markdown("---")

# ----------------- Visualizations -----------------

# 1. Main Population Trend (Line Chart)
st.markdown("<h3 style='margin-bottom: 0px;'>📊 Population Trajectory</h3>", unsafe_allow_html=True)
st.markdown("<p style='color: #8b949e; margin-bottom: 20px;'>Macro trends spanning exactly a century of data.</p>", unsafe_allow_html=True)

fig_line = go.Figure()

# Total Population (With shaded area)
fig_line.add_trace(go.Scatter(
    x=filtered_df['Year'], y=filtered_df['Predicted Total Population'],
    mode='lines', name='Total Population',
    line=dict(color='#58a6ff', width=5, shape='spline'),
    fill='tozeroy', fillcolor='rgba(88, 166, 255, 0.08)'
))
# Male
fig_line.add_trace(go.Scatter(
    x=filtered_df['Year'], y=filtered_df['Predicted Male Population'],
    mode='lines', name='Male',
    line=dict(color='#3fb950', width=3, dash='dot', shape='spline')
))
# Female
fig_line.add_trace(go.Scatter(
    x=filtered_df['Year'], y=filtered_df['Predicted Female Population'],
    mode='lines', name='Female',
    line=dict(color='#ff7b72', width=3, dash='dot', shape='spline')
))

# Mark the forecast boundary if within range
border_year = 2025 # Change year
if year_range[0] <= border_year <= year_range[1]:
    fig_line.add_vline(x=border_year, line_width=2, line_dash="dash", line_color="rgba(255,255,255,0.4)")
    fig_line.add_annotation(x=border_year, y=total_pop*0.85, text=" ➔ Model Forecast", showarrow=False, xanchor="left", font=dict(color="rgba(255,255,255,0.8)", size=16, family="Outfit", weight="bold"))

fig_line.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#c9d1d9', family='Outfit'),
    xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.03)', title='Year', showline=False),
    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.03)', title='Population', showline=False),
    hovermode='x unified',
    hoverlabel=dict(bgcolor="rgba(10, 10, 15, 0.95)", font_size=16, font_family="Outfit", bordercolor="rgba(255,255,255,0.1)"),
    legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1, font=dict(size=14)),
    margin=dict(l=0, r=0, t=10, b=0)
)

st.plotly_chart(fig_line, use_container_width=True, config={'displayModeBar': False})


col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    # 2. Gender Ratio
    st.markdown("### ⚖️ Gender Distribution")

    # Ratio over time
    fig_ratio = px.area(
        filtered_df, x="Year", y=["Predicted Male Population", "Predicted Female Population"],
        labels={"value": "Population", "variable": "Gender"},
        color_discrete_map={"Predicted Male Population": "rgba(63, 185, 80, 0.8)", "Predicted Female Population": "rgba(255, 123, 114, 0.8)"}
    )
    
    fig_ratio.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#c9d1d9', family='Outfit'),
        xaxis=dict(showgrid=False, title=''),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.03)', title='Population'),
        hovermode='x unified',
        hoverlabel=dict(bgcolor="rgba(10, 10, 15, 0.95)", font_family="Outfit", font_size=14),
        legend=dict(orientation="h", yanchor="top", y=1.1, xanchor="center", x=0.5, title=''),
        margin=dict(l=0, r=0, t=30, b=0)
    )
    st.plotly_chart(fig_ratio, use_container_width=True, config={'displayModeBar': False})

with col_chart2:
    # 3. Y-o-Y Growth
    st.markdown("### 📈 Annual Total Growth")
    
    # Calculate difference
    filtered_df['YoY Growth'] = filtered_df['Predicted Total Population'].diff()
    
    fig_growth = go.Figure()
    fig_growth.add_trace(go.Bar(
        x=filtered_df['Year'], y=filtered_df['YoY Growth'],
        marker=dict(
            color=filtered_df['YoY Growth'],
            colorscale=[[0, 'rgba(210, 168, 255, 0.4)'], [1, 'rgba(163, 113, 247, 0.9)']],
            line=dict(color='rgba(163, 113, 247, 1)', width=1)
        ),
        name="Growth"
    ))
    fig_growth.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#c9d1d9', family='Outfit'),
        xaxis=dict(showgrid=False, title=''),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.03)', title='Population Increase'),
        hoverlabel=dict(bgcolor="rgba(10, 10, 15, 0.95)", font_family="Outfit", font_size=14),
        margin=dict(l=0, r=0, t=30, b=0)
    )
    st.plotly_chart(fig_growth, use_container_width=True, config={'displayModeBar': False})

st.markdown("<br><br>", unsafe_allow_html=True)
# ----------------- Raw Data Table -----------------
with st.expander("📂 View Raw Data"):
    st.dataframe(filtered_df.style.format({
        'Predicted Total Population': '{:,.0f}',
        'Predicted Male Population': '{:,.0f}',
        'Predicted Female Population': '{:,.0f}',
        'YoY Growth': '{:,.0f}'
    }))

