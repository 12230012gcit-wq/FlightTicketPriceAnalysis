import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# =============================
# 🔹 Page Configuration
# =============================
st.set_page_config(
    page_title="Air Ticket Price Analysis Dashboard",
    page_icon="✈️",
    layout="wide",
)

# =============================
# 🔹 Load Data
# =============================
@st.cache_data
def load_data():
    df = pd.read_csv("dataSet/cleaned_airlines_flights_data.csv")
    return df

df = load_data()

# =============================
# 🔹 Sidebar Styling
# =============================

st.markdown("""
<style>
    /* --- SIDEBAR WIDTH --- */
    [data-testid="stSidebar"] {
        width: 260px !important;
        min-width: 260px !important;
        background-color: #f7f9fc;
        padding-top: 20px;
    }

    .sidebar-title {
        font-size: 22px;
        font-weight: 700;
        color: #0056D2;
        margin-bottom: 15px;
    }

    /* --- REMOVE ONLY THE RADIO DOT --- */
    [data-testid="stRadioOption"] > div:first-child {
        display: none !important;
    }

    /* --- STYLE RADIO LABEL BLOCKS --- */
    div[role="radiogroup"] > label {
        width: 100% !important;
        background: #ffffff !important;
        padding: 12px 16px !important;
        margin: 6px 0 !important;
        border-radius: 10px !important;
        border: 1px solid #dce3ee !important;
        cursor: pointer !important;
        transition: all 0.25s ease !important;

        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        gap: 10px !important;
    }

    /* --- TEXT STYLING --- */
    div[role="radiogroup"] > label p {
        margin: 0 !important;
        padding: 0 !important;
        color: #1a1a1a !important;
        font-size: 15px !important;
        font-weight: 600 !important;
    }

    /* --- HOVER EFFECT --- */
    div[role="radiogroup"] > label:hover {
        background-color: #eef4ff !important;
        border-color: #b7c8ff !important;
        color: #003b91 !important;
    }

    /* --- ACTIVE / SELECTED ITEM --- */
    div[role="radiogroup"] > label[aria-checked="true"] {
        background-color: #0056D2 !important;
        color: white !important;
        border: 1px solid #0041a8 !important;
    }

    div[role="radiogroup"] > label[aria-checked="true"] p {
        color: white !important;
        font-weight: 700 !important;
    }

    /* 1) Force collapse button to always be visible */
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapseButton"] button,
    [data-testid="stSidebarCollapseButton"] button[class*="st-emotion-cache-"] {
        opacity: 1 !important;
        background: transparent !important;
        color: #000 !important;
        box-shadow: none !important;
        border: none !important;
    }

    /* 2) Force the arrow icon (svg + path) to be BLACK */
    [data-testid="stSidebarCollapseButton"] svg,
    [data-testid="stSidebarCollapseButton"] svg path {
        stroke: #000 !important;
        opacity: 1 !important;
    }

    /* 3) Disable hover fade or highlight */
    [data-testid="stSidebarCollapseButton"]:hover,
    [data-testid="stSidebarCollapseButton"] button:hover {
        background: transparent !important;
        opacity: 1 !important;
        box-shadow: none !important;
    }

</style>
""", unsafe_allow_html=True)

# =============================
# 🔹 Sidebar Navigation
# =============================
st.sidebar.markdown("<div class='sidebar-title'>📊 Browse Analysis</div>", unsafe_allow_html=True)

page = st.sidebar.radio(
    "",
    [
        "Overview",
        "Research Question 1",
        "Research Question 2",
        "Research Question 3",
        "Research Question 4",
        "Research Question 5",
        "Summary & Conclusion",
    ]
)

# =============================
# 🔹 1. Overview
# =============================
if page == "Overview":
    st.title("✈️ Air Ticket Price Analysis Dashboard")
    st.markdown("""
    This dashboard provides insights into air ticket pricing patterns using data from **Kaggle**.
    We explore various factors like **airline**, **class**, **stops**, and **days_left** before departure to understand
    how they influence ticket prices.
    """)

    # -----------------------------
    # 📥 DATA DOWNLOAD DROPDOWN
    # -----------------------------
    st.subheader("📥 Download Dataset")

    download_option = st.selectbox(
        "Choose a dataset to download:",
        ["Select an option", "Raw Dataset", "Cleaned Dataset"]
    )

    if download_option == "Raw Dataset":
        st.download_button(
            label="Download Raw Dataset",
            data=open("dataSet/raw_airlines_flights_data.csv", "rb").read(),
            file_name="raw_airlines_flights_data.csv",
            mime="text/csv"
        )

    elif download_option == "Cleaned Dataset":
        st.download_button(
            label="Download Cleaned Dataset",
            data=df.to_csv(index=False),
            file_name="cleaned_airlines_flights_data.csv",
            mime="text/csv"
        )


    #CUSTOM CSS FOR CARDS
    st.markdown("""
    <style>
    .metric-card {
        background-color: #ffffff;
        padding: 20px 25px;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.07);
        text-align: center;

        height: 150px;              
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;

        margin-bottom: 20px;        
    }
    .metric-card h3 {
        font-size: 18px;
        margin-bottom: 6px;
        color: #333;
    }
    .metric-card p {
        font-size: 22px;
        font-weight: 600;
        color: #1a73e8;
        margin: 0;
    }
    </style>
    """, unsafe_allow_html=True)


    # 📊 METRIC CARDS
  
    st.subheader("Overview")

    # Calculations
    avg_price = df['price'].mean()
    avg_duration = df['duration'].mean()
    avg_day_left = df['days_left'].mean()

    df['route'] = df['source_city'] + " → " + df['destination_city']
    unique_routes = df['route'].nunique()

    airline_avg = df.groupby('airline')['price'].mean()
    cheapest_airline = airline_avg.idxmin()
    cheapest_price = airline_avg.min()
    expensive_airline = airline_avg.idxmax()
    expensive_price = airline_avg.max()

    # Display Metric Cards
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    with col1:
        # Total Records
        st.markdown(f"""
        <div class="metric-card">
            <h3>📊 Total Records</h3>
            <p>{len(df):,}</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Average Ticket Price (moved from col1 to col2)
        st.markdown(f"""
        <div class="metric-card">
            <h3>💸 Average Ticket Price</h3>
            <p>₹{avg_price:,.0f}</p>
        </div>
        """, unsafe_allow_html=True)


    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📅 Average Days Left</h3>
            <p>{avg_day_left:.1f}</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🛣️ Unique Routes</h3>
            <p>{unique_routes}</p>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <h3>💰 Cheapest Airline</h3>
            <p>{cheapest_airline}<br>₹{cheapest_price:,.0f}</p>
        </div>
        """, unsafe_allow_html=True)

    with col6:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🔥 Pricest Airline</h3>
            <p>{expensive_airline}<br>₹{expensive_price:,.0f}</p>
        </div>
        """, unsafe_allow_html=True)


    # -----------------------------
    # 📂 Overview Visualization
    # -----------------------------

    st.subheader("Overview Visualizations")

    # Dropdown selection
    pie_option = st.selectbox(
        "Select a Pie Chart to View:",
        ["Flights by Airline", "Flight Classes", "Number of Stops"]
    )

    # ---------------------- AIRLINE PIE CHART ----------------------
    if pie_option == "Flights by Airline":
        airline_counts = df['airline'].value_counts().reset_index()
        airline_counts.columns = ['Airline', 'Count']

        fig = px.pie(
            airline_counts,
            names='Airline',
            values='Count',
            title='Distribution of Flights by Airline',
            hole=0.3
        )

        fig.update_traces(
            hovertemplate="<b>%{label}</b><br>Flights: %{value}<br>Percentage: %{percent}"
        )

        st.plotly_chart(fig, use_container_width=True)


    # ---------------------- CLASS PIE CHART ----------------------
    elif pie_option == "Flight Classes":
        class_counts = df['class'].value_counts().reset_index()
        class_counts.columns = ['Class', 'Count']

        fig = px.pie(
            class_counts,
            names='Class',
            values='Count',
            title='Distribution of Flight Classes',
            hole=0.3
        )

        fig.update_traces(
            hovertemplate="<b>%{label}</b><br>Total Flights: %{value}<br>Percentage: %{percent}"
        )

        st.plotly_chart(fig, use_container_width=True)


    # ---------------------- STOPS PIE CHART ----------------------
    elif pie_option == "Number of Stops":
        stops_counts = df['stops'].value_counts().reset_index()
        stops_counts.columns = ['Stops', 'Count']
        stops_counts['Stops'] = stops_counts['Stops'].astype(str)

        fig = px.pie(
            stops_counts,
            names='Stops',
            values='Count',
            title='Distribution of Number of Stops',
            hole=0.3
        )

        fig.update_traces(
            hovertemplate="<b>%{label} Stops</b><br>Total Flights: %{value}<br>Percentage: %{percent}"
        )

        st.plotly_chart(fig, use_container_width=True)

    # Dropdown options for ticket price and day_left distribution
    # Pre-compute metrics for hover tooltips  

    price_mean = df['price'].mean()
    price_min = df['price'].min()
    price_max = df['price'].max()

    days_mean = df['days_left'].mean()
    days_min = df['days_left'].min()
    days_max = df['days_left'].max()

    # Dropdown  
    chart_option = st.selectbox(
        "📊 Select Distribution to View",
        ["Ticket Price Distribution", "Days Left Distribution"]
    )

    # -------------------------------
    # 1️⃣ Ticket Price Histogram
    # -------------------------------
    if chart_option == "Ticket Price Distribution":
        fig = px.histogram(
            df,
            x='price',
            nbins=40,
            title='Distribution of Ticket Prices',
            color_discrete_sequence=['#1f77b4'],  # blue
            opacity=0.85,
        )

        # Add visible bar boundaries
        fig.update_traces(
            marker_line_width=1.2,
            marker_line_color='black',
            hovertemplate=(
                "<b>Price: %{x}</b><br>"
                "Count: %{y}<br><br>"
                f"Avg Price: ₹{price_mean:,.0f}<br>"
                f"Min Price: ₹{price_min:,.0f}<br>"
                f"Max Price: ₹{price_max:,.0f}<br>"
            )
        )

        st.plotly_chart(fig, use_container_width=True)


    # -------------------------------
    # 2️⃣ Days Left Histogram
    # -------------------------------
    elif chart_option == "Days Left Distribution":
        fig = px.histogram(
            df,
            x='days_left',
            nbins=40,
            title='Distribution of Days Left Before Departure',
            color_discrete_sequence=['#2ca02c'],  # green
            opacity=0.85,
        )

        # Add visible bar boundaries  
        fig.update_traces(
            marker_line_width=1.2,
            marker_line_color='black',
            hovertemplate=(
                "<b>Days Left: %{x}</b><br>"
                "Count: %{y}<br><br>"
                f"Avg Days Left: {days_mean:.1f}<br>"
                f"Min Days Left: {days_min}<br>"
                f"Max Days Left: {days_max}<br>"
            )
        )

        st.plotly_chart(fig, use_container_width=True)


# =============================
# 🔹 2. Research Question 1

elif page == "Research Question 1":

    # ===============================
    # 1️⃣ STYLE THE RESEARCH QUESTION HEADER

    st.markdown("""
    <style>
        .rq-header {
            display: flex;
            align-items: center;
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 15px;
        }
        .rq-number {
            background-color: #0056D2;
            color: white;
            font-size: 20px;
            font-weight: bold;
            padding: 6px 14px;
            border-radius: 50%;
            margin-right: 10px;
        }
        .hyp-card {
            background-color: #f8f9fb;
            border: 1px solid #d1d9e6;
            padding: 18px 20px;
            border-radius: 12px;
            margin-top: 10px;
            margin-bottom: 20px;
        }
        .hyp-card p {
            color: #333333;      
            font-size: 16px;
            line-height: 1.5;
        }
        .hyp-title {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 8px;
            color: #000000;      
        }
        .hyp-status {
            color: #1BA94C;
            font-weight: 600;
            margin-top: 15px;
            display: flex;
            align-items: center;
        }
        .hyp-status-icon {
            font-size: 20px;
            margin-right: 6px;
        }
    </style>
    """, unsafe_allow_html=True)


    # ===============================
    # 2️⃣ HEADER BLOCK (Fix: ensure no stray characters)
    # ===============================
    st.markdown("""
        <div class='rq-header'>
            <div class='rq-number'>1</div>
            How does the number of days left before departure affect flight ticket?
        </div>
    """, unsafe_allow_html=True)


    # ===============================
    # 3️⃣ FIXED HYPOTHESIS DISPLAY
    # ===============================
    st.markdown("""
        <div class="hyp-card">
            <div class="hyp-title">Hypothesis</div>
            <p>Flights booked closer to the departure date are significantly more expensive than those booked well in advance.</p>
            <div class="hyp-status">
                <span class="hyp-status-icon">✔️</span>
                Hypothesis Supported
            </div>
        </div>
    """, unsafe_allow_html=True)


    # ===============================
    # 4️⃣ VISUALIZATIONS
    # ===============================
    tab1, tab2, tab3 = st.tabs([
        "Booking Time vs Ticket Price",
        "How Price Changes as the Trip Gets Closer",
        "Price Distribution by Booking Window"
    ])

    # ---------------------------
    # ⭐ TAB 1: SCATTER (All Airlines)
    # ---------------------------
    with tab1:

        df_filtered = df.copy()   # Always all airlines

        fig = px.scatter(
            df_filtered,
            x='days_left',
            y='price',
            color='airline',
            title="Days Left vs Ticket Price (All Airlines)",
            opacity=0.7,
            hover_data=['airline', 'source_city', 'destination_city']
        )

        fig.update_traces(marker=dict(size=8, line=dict(width=0.5, color='black')))
        fig.update_layout(xaxis_title="Days Left", yaxis_title="Ticket Price")

        st.plotly_chart(fig, use_container_width=True)


    # ---------------------------
    # ⭐ TAB 2: LINE TREND (All Airlines)
    # ---------------------------
    with tab2:

        st.subheader("Average Price Trend as Departure Gets Closer")

        df1 = df.copy()

        df1['Days_Bin'] = pd.cut(
            df1['days_left'],
            bins=np.arange(0, df1['days_left'].max() + 5, 5)
        )

        avg_price_by_bin = df1.groupby('Days_Bin')['price'].mean().reset_index()
        avg_price_by_bin['Days_Bin'] = avg_price_by_bin['Days_Bin'].astype(str)

        fig = px.line(
            avg_price_by_bin,
            x='Days_Bin',
            y='price',
            markers=True,
            title="Price Trend Across All Airlines (5-Day Booking Windows)"
        )

        fig.update_traces(line=dict(width=3), marker=dict(size=8))
        fig.update_xaxes(showline=True, linewidth=2)
        fig.update_yaxes(showline=True, linewidth=2)
        fig.update_layout(
            xaxis_title="Days Left (5-Day Bins)",
            yaxis_title="Average Ticket Price",
            xaxis_tickangle=45
        )

        st.plotly_chart(fig, use_container_width=True)


    # ---------------------------
    # ⭐ TAB 3: BOX PLOT (All Airlines)
    # ---------------------------

    with tab3:

        st.subheader("Ticket Price Distribution by Booking Window")

        df1 = df.copy()

        max_day = df1['days_left'].max()
        bins = [0, 5, 10, 20, 30, 60, 90, 120, max(121, max_day)]
        labels = ['0-5','6-10','11-20','21-30','31-60','61-90','91-120','120+']

        df1['Booking_Window'] = pd.cut(
            df1['days_left'],
            bins=bins,
            labels=labels,
            include_lowest=True
        )

        fig = px.box(
            df1,
            x='Booking_Window',
            y='price',
            color='Booking_Window',
            title="Price Distribution Across All Airlines by Booking Window",
            points='all'
        )

        fig.update_traces(
            marker=dict(opacity=0.5, size=4),
            jitter=0.3,
            boxmean=True
        )

        fig.update_layout(
            xaxis_title="Days Left Category",
            yaxis_title="Ticket Price",
            showlegend=False
        )

        fig.update_xaxes(showline=True, linewidth=2, linecolor="black")
        fig.update_yaxes(showline=True, linewidth=2, linecolor="black")

        st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        "**Insight:** Ticket prices rise sharply when fewer days are left — supporting the hypothesis."
    )

# =============================
# 🔹 3. Research Question 2
# =============================
elif page == "Research Question 2":

    # ===============================
    # 1️⃣ STYLE THE RESEARCH QUESTION HEADER
    # ===============================
    st.markdown("""
    <style>
        .rq-header {
            display: flex;
            align-items: center;
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 15px;
        }
        .rq-number {
            background-color: #0056D2;
            color: white;
            font-size: 20px;
            font-weight: bold;
            padding: 6px 14px;
            border-radius: 50%;
            margin-right: 10px;
        }
        .hyp-card {
            background-color: #f8f9fb;
            border: 1px solid #d1d9e6;
            padding: 18px 20px;
            border-radius: 12px;
            margin-top: 10px;
            margin-bottom: 20px;
        }
        .hyp-card p {
            color: #333333;      
            font-size: 16px;
            line-height: 1.5;
        }
        .hyp-title {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 8px;
            color: #000000;      
        }
        .hyp-status {
            color: #1BA94C;
            font-weight: 600;
            margin-top: 15px;
            display: flex;
            align-items: center;
        }
        .hyp-status-icon {
            font-size: 20px;
            margin-right: 6px;
        }
    </style>
    """, unsafe_allow_html=True)


    # ===============================
    # 2️⃣ HEADER BLOCK (Fix: ensure no stray characters)
    # ===============================
    st.markdown("""
        <div class='rq-header'>
            <div class='rq-number'>2</div>
            Does the effect of days left on ticket prices vary across different airlines?
        </div>
    """, unsafe_allow_html=True)


    # ===============================
    # 3️⃣ FIXED HYPOTHESIS DISPLAY
    # ===============================
    st.markdown("""
        <div class="hyp-card">
            <div class="hyp-title">Hypothesis</div>
            <p>Airlines differ in their pricing strategies, with some showing sharper increases in ticket prices as departure approaches compared to others.</p>
            <div class="hyp-status">
                <span class="hyp-status-icon">✔️</span>
                Hypothesis Supported
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs([
        "How Booking Time Affects Ticket Prices",
        "Price Trend as the Trip Gets Closer (by Airline)",
        "Price Distribution Across Booking Windows (by Airline)"
    ])    

    with tab1:

        st.subheader("How Booking Time Affects Ticket Price for Each Airline")

        # Build dropdown options: first item = "All Airlines"
        airline_options = ["All Airlines"] + sorted(df['airline'].unique())

        # Default selection: first actual airline (index 1, not "All Airlines")
        default_index = 1 if len(airline_options) > 1 else 0

        selected_airline = st.selectbox(
            "Select Airline:",
            airline_options,
            index=default_index
        )

        # Filter dataframe
        if selected_airline == "All Airlines":
            df_filtered = df.copy()
        else:
            df_filtered = df[df["airline"] == selected_airline]

        # Scatter plot
        fig = px.scatter(
            df_filtered,
            x='days_left',
            y='price',
            color=None if selected_airline != "All Airlines" else "airline",
            title=(
                f"Days Left vs Ticket Price ({selected_airline})"
                if selected_airline != "All Airlines"
                else "Days Left vs Ticket Price (All Airlines)"
            ),
            opacity=0.7,
            hover_data=['airline', 'source_city', 'destination_city']
        )

        fig.update_traces(
            marker=dict(size=8, line=dict(width=0.5, color='black'))
        )

        fig.update_layout(
            xaxis_title="Days Left Before Departure",
            yaxis_title="Ticket Price"
        )

        fig.update_xaxes(showline=True, linewidth=2)
        fig.update_yaxes(showline=True, linewidth=2)

        st.plotly_chart(fig, use_container_width=True)

    with tab2:

        st.subheader("How Ticket Prices Change as the Departure Date Gets Closer")

        df1 = df.copy()

        # Dropdown
        airline_options = ["All Airlines"] + sorted(df1['airline'].unique())
        default_index = 1 if len(airline_options) > 1 else 0

        selected_airline_2 = st.selectbox(
            "Select Airline:",
            airline_options,
            index=default_index,
            key="rq2_tab2_airline"
        )

        # Apply filter
        if selected_airline_2 != "All Airlines":
            df1 = df1[df1['airline'] == selected_airline_2]

        # Create 5-day bins
        df1['Days_Bin'] = pd.cut(
            df1['days_left'],
            bins=np.arange(0, df1['days_left'].max() + 5, 5)
        )

        # Compute average price
        avg_price_by_bin = df1.groupby('Days_Bin')['price'].mean().reset_index()
        avg_price_by_bin['Days_Bin'] = avg_price_by_bin['Days_Bin'].astype(str)

        # Line plot
        fig = px.line(
            avg_price_by_bin,
            x='Days_Bin',
            y='price',
            markers=True,
            title=(
                f"Price Trend for {selected_airline_2} (5-Day Booking Windows)"
                if selected_airline_2 != "All Airlines"
                else "Price Trend Across All Airlines (5-Day Booking Windows)"
            )
        )

        fig.update_traces(line=dict(width=3), marker=dict(size=8))
        fig.update_xaxes(showline=True, linewidth=2, linecolor="black")
        fig.update_yaxes(showline=True, linewidth=2, linecolor="black")

        fig.update_layout(
            xaxis_title="Days Left (5-Day Bins)",
            yaxis_title="Average Ticket Price",
            xaxis_tickangle=45
        )

        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:

        st.subheader("How Ticket Prices Vary Across Booking Windows for Each Airline")

        df1 = df.copy()

        # --------------------------
        # AIRLINE DROPDOWN (DEFAULT = FIRST AIRLINE)
        # --------------------------
        airline_options = ["All Airlines"] + sorted(df1["airline"].unique())

        default_index = 1 if len(airline_options) > 1 else 0   # not "All Airlines"

        selected_airline_3 = st.selectbox(
            "Select Airline:",
            airline_options,
            index=default_index,
            key="rq2_tab3_airline"
        )

        # Apply filter
        if selected_airline_3 != "All Airlines":
            df1 = df1[df1["airline"] == selected_airline_3]

        # --------------------------
        # Create Booking Window Bins
        # --------------------------
        max_day = df1["days_left"].max()

        bins = [0, 5, 10, 20, 30, 60, 90, 120, max(121, max_day)]
        labels = ["0-5","6-10","11-20","21-30","31-60","61-90","91-120","120+"]

        df1["Booking_Window"] = pd.cut(
            df1["days_left"],
            bins=bins,
            labels=labels,
            include_lowest=True
        )

        # --------------------------
        # PLOTLY BOXPLOT
        # --------------------------
        fig = px.box(
            df1,
            x="Booking_Window",
            y="price",
            color="Booking_Window",
            points="all",
            title=(
                f"Price Distribution for {selected_airline_3} Across Booking Windows"
                if selected_airline_3 != "All Airlines"
                else "Price Distribution Across All Airlines by Booking Window"
            )
        )

        fig.update_traces(
            jitter=0.3,
            boxmean=True,
            marker=dict(size=4, opacity=0.45)
        )

        fig.update_layout(
            xaxis_title="Days Left Category",
            yaxis_title="Ticket Price",
            showlegend=False
        )

        # Clear axis lines
        fig.update_xaxes(showline=True, linewidth=2, linecolor="black")
        fig.update_yaxes(showline=True, linewidth=2, linecolor="black")

        st.plotly_chart(fig, use_container_width=True)


    st.markdown(
        "**Insight:** Some airlines show steeper price increases as the departure date approaches, "
        "indicating different pricing strategies and supporting the hypothesis."
    )


# =============================
# 🔹 4. Research Question 3
# =============================
elif page == "Research Question 3":

    # ===============================
    # 1️⃣ STYLE THE RESEARCH QUESTION HEADER
    # ===============================
    st.markdown("""
    <style>
        .rq-header {
            display: flex;
            align-items: center;
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 15px;
        }
        .rq-number {
            background-color: #0056D2;
            color: white;
            font-size: 20px;
            font-weight: bold;
            padding: 6px 14px;
            border-radius: 50%;
            margin-right: 10px;
        }
        .hyp-card {
            background-color: #f8f9fb;
            border: 1px solid #d1d9e6;
            padding: 18px 20px;
            border-radius: 12px;
            margin-top: 10px;
            margin-bottom: 20px;
        }
        .hyp-card p {
            color: #333333;      /* ✅ dark gray text for readability */
            font-size: 16px;
            line-height: 1.5;
        }
        .hyp-title {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 8px;
            color: #000000;      /* optional: stronger title color */
        }
        .hyp-status {
            color: #1BA94C;
            font-weight: 600;
            margin-top: 15px;
            display: flex;
            align-items: center;
        }
        .hyp-status-icon {
            font-size: 20px;
            margin-right: 6px;
        }
    </style>
    """, unsafe_allow_html=True)


    # ===============================
    # 2️⃣ HEADER BLOCK (Fix: ensure no stray characters)
    # ===============================
    st.markdown("""
        <div class='rq-header'>
            <div class='rq-number'>3</div>
            How does the relationship between days left and ticket price differ between economy and business class flights?
        </div>
    """, unsafe_allow_html=True)


    # ===============================
    # 3️⃣ FIXED HYPOTHESIS DISPLAY
    # ===============================
    st.markdown("""
        <div class="hyp-card">
            <div class="hyp-title">Hypothesis</div>
            <p>Business class tickets increase in price more steeply than economy class tickets as the departure date approaches.</p>
            <div class="hyp-status">
                <span class="hyp-status-icon">✔️</span>
                Hypothesis Supported
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs([
        "Average Price by Class", 
        "Price Trend: Economy vs Business",
        "Booking Window Price Trend"
        ])

    with tab1:

        st.subheader("Average Ticket Price: Economy vs Business Class")

        # Compute average price by class (sorted)
        avg_price_class = (
            df.groupby('class')['price']
            .mean()
            .sort_values(ascending=False)
            .reset_index()
        )

        # Plotly bar chart
        fig = px.bar(
            avg_price_class,
            x='class',
            y='price',
            color='class',
            title="Average Ticket Price by Flight Class",
            text_auto='.2s'
        )

        # Improve bar styling
        fig.update_traces(
            marker_line_width=1.2,
            marker_line_color="black"
        )

        # Layout adjustments
        fig.update_layout(
            xaxis_title="Flight Class",
            yaxis_title="Average Ticket Price",
            showlegend=False
        )

        # Clear axis lines
        fig.update_xaxes(showline=True, linewidth=2)
        fig.update_yaxes(showline=True, linewidth=2)

        st.plotly_chart(fig, use_container_width=True)

    with tab2:

        st.subheader("How Booking Time Affects Ticket Prices by Flight Class")

        # Dropdown options for class
        class_options = ["All Classes"] + sorted(df['class'].unique())

        # Default = first real class (not "All Classes")
        default_class_index = 1 if len(class_options) > 1 else 0

        selected_class = st.selectbox(
            "Select Flight Class:",
            class_options,
            index=default_class_index,
            key="rq3_tab2_class"
        )

        # Filter data
        if selected_class == "All Classes":
            df_filtered = df.copy()
        else:
            df_filtered = df[df["class"] == selected_class]

        # Plotly scatter
        fig = px.scatter(
            df_filtered,
            x='days_left',
            y='price',
            color="class" if selected_class == "All Classes" else None,
            title=(
                f"Days Left vs Ticket Price ({selected_class})"
                if selected_class != "All Classes"
                else "Days Left vs Ticket Price (All Flight Classes)"
            ),
            opacity=0.7,
            hover_data=['airline', 'source_city', 'destination_city', 'class'],
        )

        # Marker styling
        fig.update_traces(
            marker=dict(
                size=8,
                line=dict(width=0.5, color='black')
            )
        )

        # Layout polish
        fig.update_layout(
            xaxis_title="Days Left Before Departure",
            yaxis_title="Ticket Price",
        )

        # Clean axis lines
        fig.update_xaxes(showline=True, linewidth=2, linecolor="black")
        fig.update_yaxes(showline=True, linewidth=2, linecolor="black")

        st.plotly_chart(fig, use_container_width=True)

    with tab3:

        st.subheader("How Ticket Prices Change as Departure Gets Closer (By Class)")

        df1 = df.copy()

        # --------------------------
        # Dropdown for selecting class
        # --------------------------
        class_options = ["All Classes"] + sorted(df1['class'].unique())

        # Default index = first actual class
        default_class_index = 1 if len(class_options) > 1 else 0

        selected_class_line = st.selectbox(
            "Select Flight Class:",
            class_options,
            index=default_class_index,
            key="rq3_tab3_class"
        )

        # --------------------------
        # Create 5-day bins
        # --------------------------
        df1['Days_Bin'] = pd.cut(
            df1['days_left'],
            bins=np.arange(0, df1['days_left'].max() + 5, 5)
        )

        # --------------------------
        # Filter by class (if needed)
        # --------------------------
        if selected_class_line != "All Classes":
            df1 = df1[df1["class"] == selected_class_line]

        # --------------------------
        # Compute mean per bin + class
        # --------------------------
        avg_price_bin = (
            df1.groupby(['Days_Bin', 'class'])['price']
            .mean()
            .reset_index()
        )

        # Convert intervals to readable strings
        avg_price_bin['Days_Bin'] = avg_price_bin['Days_Bin'].astype(str)

        # --------------------------
        # Plotly line graph
        # --------------------------
        fig = px.line(
            avg_price_bin,
            x='Days_Bin',
            y='price',
            color='class' if selected_class_line == "All Classes" else None,
            markers=True,
            title=(
                f"Price Trend for {selected_class_line} (5-Day Booking Windows)"
                if selected_class_line != "All Classes"
                else "Price Trend Across Flight Classes (5-Day Booking Windows)"
            )
        )

        fig.update_traces(line=dict(width=3), marker=dict(size=8))

        # Clean axis styling
        fig.update_xaxes(showline=True, linewidth=2, tickangle=45)
        fig.update_yaxes(showline=True, linewidth=2)

        fig.update_layout(
            xaxis_title="Days Left (5-Day Bins)",
            yaxis_title="Average Ticket Price",
            legend_title="Flight Class"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Insight:** Business class fares are consistently higher, confirming the hypothesis.")

# =============================
# 🔹 5. Research Question 4
# =============================
elif page == "Research Question 4":

    # ===============================
    # 1️⃣ STYLE THE RESEARCH QUESTION HEADER
    # ===============================
    st.markdown("""
    <style>
        .rq-header {
            display: flex;
            align-items: center;
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 15px;
        }
        .rq-number {
            background-color: #0056D2;
            color: white;
            font-size: 20px;
            font-weight: bold;
            padding: 6px 14px;
            border-radius: 50%;
            margin-right: 10px;
        }
        .hyp-card {
            background-color: #f8f9fb;
            border: 1px solid #d1d9e6;
            padding: 18px 20px;
            border-radius: 12px;
            margin-top: 10px;
            margin-bottom: 20px;
        }
        .hyp-card p {
            color: #333333;      
            font-size: 16px;
            line-height: 1.5;
        }
        .hyp-title {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 8px;
            color: #000000;      
        }
        .hyp-status {
            color: #1BA94C;
            font-weight: 600;
            margin-top: 15px;
            display: flex;
            align-items: center;
        }
        .hyp-status-icon {
            font-size: 20px;
            margin-right: 6px;
        }
    </style>
    """, unsafe_allow_html=True)


    # ===============================
    # 2️⃣ HEADER BLOCK (Fix: ensure no stray characters)
    # ===============================
    st.markdown("""
        <div class='rq-header'>
            <div class='rq-number'>4</div>
            Do non-stop flights show different price trends compared to flights with one or more stops as departure approaches?
        </div>
    """, unsafe_allow_html=True)


    # ===============================
    # 3️⃣ FIXED HYPOTHESIS DISPLAY
    # ===============================
    st.markdown("""
        <div class="hyp-card">
            <div class="hyp-title">Hypothesis</div>
            <p>Non-stop flights exhibit stronger price increases closer to departure than connecting flights.</p>
            <div class="hyp-status">
                <span class="hyp-status-icon">❌</span>
                Hypothesis Not Supported
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs([
        "Average Ticket Price by Number of Stops", 
        "Booking Time vs Ticket Price (By Number of Stops)",
        "Price Trend Across Booking Windows (By Stops)"
        ])

    with tab1:

        st.subheader("Average Ticket Price by Number of Stops")

        # Aggregate average prices by stops
        avg_price_stops = (
            df.groupby('stops')['price']
            .mean()
            .sort_values(ascending=False)
            .reset_index()
        )

        # Create bar chart
        fig = px.bar(
            avg_price_stops,
            x='stops',
            y='price',
            color='stops',
            title="Average Ticket Price by Number of Stops",
            text_auto='.2s'
        )

        # Improve bar appearance
        fig.update_traces(
            marker_line_width=1.2,
            marker_line_color="black"
        )

        # Layout styling
        fig.update_layout(
            xaxis_title="Number of Stops",
            yaxis_title="Average Price",
            showlegend=False
        )

        # Sharp axis lines for clarity
        fig.update_xaxes(showline=True, linewidth=2, tickangle=0)
        fig.update_yaxes(showline=True, linewidth=2)

        st.plotly_chart(fig, use_container_width=True)

    with tab2:

        st.subheader("Booking Time vs Ticket Price (By Number of Stops)")

        df2 = df.copy()

        # Dropdown for stop categories
        stop_options = ["All Stops"] + sorted(df2["stops"].unique().tolist())

        selected_stop = st.selectbox(
            "Select Number of Stops:",
            stop_options,
            index=0,
            key="rq4_tab2_stops"
        )

        # Filter based on selection
        if selected_stop == "All Stops":
            df_plot = df2
            title_text = "Days Left vs Ticket Price (All Stop Categories)"
        else:
            df_plot = df2[df2["stops"] == selected_stop]
            title_text = f"Days Left vs Ticket Price ({selected_stop} Stop(s))"

        # Scatter plot
        fig = px.scatter(
            df_plot,
            x="days_left",
            y="price",
            color="stops",
            title=title_text,
            opacity=0.6,
            hover_data=["airline", "class", "source_city", "destination_city"]
        )

        fig.update_traces(
            marker=dict(size=7, line=dict(width=0.4, color="black"))
        )

        fig.update_xaxes(showline=True, linewidth=2)
        fig.update_yaxes(showline=True, linewidth=2)

        fig.update_layout(
            xaxis_title="Days Left Before Departure",
            yaxis_title="Ticket Price",
            legend_title="Stops"
        )

        st.plotly_chart(fig, use_container_width=True)


    with tab3:

        st.subheader("Price Trend Across Booking Windows (By Stops)")

        df3 = df.copy()

        # Create 5-day bins
        df3["Days_Bin"] = pd.cut(
            df3["days_left"],
            bins=np.arange(0, df3["days_left"].max() + 5, 5)
        )

        # Compute average price per bin per stop category
        avg_price_bins = (
            df3.groupby(["Days_Bin", "stops"])["price"]
            .mean()
            .reset_index()
        )

        # Convert interval bins to string labels
        avg_price_bins["Days_Bin"] = avg_price_bins["Days_Bin"].astype(str)

        # Line plot
        fig = px.line(
            avg_price_bins,
            x="Days_Bin",
            y="price",
            color="stops",
            markers=True,
            title="Average Ticket Price by Booking Window (By Stops)"
        )

        fig.update_traces(marker=dict(size=8), line=dict(width=3))

        fig.update_xaxes(showline=True, linewidth=2, tickangle=45)
        fig.update_yaxes(showline=True, linewidth=2)

        fig.update_layout(
            xaxis_title="Days Left (5-Day Bins)",
            yaxis_title="Average Ticket Price",
            legend_title="Number of Stops"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Insight:**
                
    - **0-stop (non-stop) flights are the cheapest overall**, consistently showing the lowest ticket prices across booking windows.
    - **1-stop flights are the most expensive**, with prices noticeably higher than both non-stop and 2+ stop flights.
    - **Flights with 2 or more stops fall in between**, generally more expensive than non-stop flights but cheaper than 1-stop flights.
    - As the departure date approaches, **prices increase for all stop categories**, but the rise is **steeper for 1-stop flights**.
    - Non-stop flights also increase in price closer to departure, but **not as sharply** as 1-stop flights.
    """)

# =============================
# 🔹 6. Research Question 5
# =============================
elif page == "Research Question 5":

    # ===============================
    # 1️⃣ STYLE THE RESEARCH QUESTION HEADER
    # ===============================
    st.markdown("""
    <style>
        .rq-header {
            display: flex;
            align-items: center;
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 15px;
        }
        .rq-number {
            background-color: #0056D2;
            color: white;
            font-size: 20px;
            font-weight: bold;
            padding: 6px 14px;
            border-radius: 50%;
            margin-right: 10px;
        }
        .hyp-card {
            background-color: #f8f9fb;
            border: 1px solid #d1d9e6;
            padding: 18px 20px;
            border-radius: 12px;
            margin-top: 10px;
            margin-bottom: 20px;
        }
        .hyp-card p {
            color: #333333;      /* ✅ dark gray text for readability */
            font-size: 16px;
            line-height: 1.5;
        }
        .hyp-title {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 8px;
            color: #000000;      /* optional: stronger title color */
        }
        .hyp-status {
            color: #1BA94C;
            font-weight: 600;
            margin-top: 15px;
            display: flex;
            align-items: center;
        }
        .hyp-status-icon {
            font-size: 20px;
            margin-right: 6px;
        }
    </style>
    """, unsafe_allow_html=True)


    # ===============================
    # 2️⃣ HEADER BLOCK (Fix: ensure no stray characters)
    # ===============================
    st.markdown("""
        <div class='rq-header'>
            <div class='rq-number'>5</div>
            How do airline, class, and number of stops interact with the booking window (days left) in determining flight ticket prices?
        </div>
    """, unsafe_allow_html=True)


    # ===============================
    # 3️⃣ FIXED HYPOTHESIS DISPLAY
    # ===============================
    st.markdown("""
        <div class="hyp-card">
            <div class="hyp-title">Hypothesis</div>
            <p>The impact of days left on ticket prices is jointly influenced by airline, flight class, and number of stops, leading to complex variations in pricing patterns.</p>
            <div class="hyp-status">
                <span class="hyp-status-icon">✔️</span>
                Hypothesis Supported
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs([
        "Airline vs Class Pricing Comparison",
        "Pricing Differences by Stops and Class",
        "Booking Window Price Trend Across Airlines"
    ])


    with tab1:

        st.subheader("Average Ticket Price by Airline and Flight Class")

        df1 = df.copy()

        # Compute mean price by airline and class
        avg_price_airline_class = (
            df1.groupby(['airline', 'class'])['price']
            .mean()
            .reset_index()
        )

        # Plotly grouped bar chart
        fig = px.bar(
            avg_price_airline_class,
            x='airline',
            y='price',
            color='class',
            barmode='group',
            title="Average Ticket Price by Airline and Class",
            text_auto='.2s'
        )

        # Improve bar appearance
        fig.update_traces(marker_line_width=1.2, marker_line_color="black")

        # Layout polish
        fig.update_layout(
            xaxis_title="Airline",
            yaxis_title="Average Price",
            legend_title="Flight Class"
        )

        # Clear axis lines
        fig.update_xaxes(showline=True, linewidth=2, tickangle=45)
        fig.update_yaxes(showline=True, linewidth=2)

        st.plotly_chart(fig, use_container_width=True)

    with tab2:

        st.subheader("Average Ticket Price by Number of Stops and Flight Class")

        df1 = df.copy()

        # Compute mean price grouped by stops × class
        avg_price_stops_class = (
            df1.groupby(['stops', 'class'])['price']
            .mean()
            .reset_index()
        )

        # Plotly grouped bar chart
        fig = px.bar(
            avg_price_stops_class,
            x='stops',
            y='price',
            color='class',
            barmode='group',
            title="Average Ticket Price by Stops and Class",
            text_auto='.2s',
            color_discrete_sequence=px.colors.qualitative.Set2  # nice soft colors
        )

        # Improve bar appearance
        fig.update_traces(marker_line_width=1.2, marker_line_color="black")

        # Layout polish
        fig.update_layout(
            xaxis_title="Number of Stops",
            yaxis_title="Average Price",
            legend_title="Flight Class"
        )

        # Clear axis lines
        fig.update_xaxes(showline=True, linewidth=2, tickangle=0)
        fig.update_yaxes(showline=True, linewidth=2)

        st.plotly_chart(fig, use_container_width=True)

    with tab3:

        st.subheader("Booking Window Price Trend Across Airlines")

        df1 = df.copy()

        # ----------------------------
        # CLASS DROPDOWN
        # ----------------------------
        class_options =  sorted(df1["class"].unique())
        selected_class = st.selectbox(
            "Select Flight Class:",
            class_options,
            index=0, 
            key="rq5_tab3_class"
        )

        # Filter based on dropdown
        if selected_class != "All Classes":
            df_filtered = df1[df1["class"].str.lower() == selected_class.lower()]
        else:
            df_filtered = df1.copy()

        # ----------------------------
        # CREATE 5-DAY BINS
        # ----------------------------
        df_filtered["Days_Bin"] = pd.cut(
            df_filtered["days_left"],
            bins=np.arange(0, df_filtered["days_left"].max() + 5, 5)
        )

        # ----------------------------
        # COMPUTE AVERAGE PRICE PER AIRLINE × BIN
        # ----------------------------
        avg_price_by_bin = (
            df_filtered.groupby(["airline", "Days_Bin"])["price"]
            .mean()
            .reset_index()
        )
        avg_price_by_bin["Days_Bin"] = avg_price_by_bin["Days_Bin"].astype(str)

        # ----------------------------
        # PLOTLY MULTILINE CHART
        # ----------------------------
        fig = px.line(
            avg_price_by_bin,
            x="Days_Bin",
            y="price",
            color="airline",
            markers=True,
            title=(
                f"Average Ticket Price Trend Across Airlines ({selected_class})"
                if selected_class != "All Classes"
                else "Average Ticket Price Trend Across Airlines (All Classes)"
            )
        )

        fig.update_traces(line=dict(width=3), marker=dict(size=8))

        fig.update_layout(
            xaxis_title="Days Left (5-Day Bins)",
            yaxis_title="Average Ticket Price",
            xaxis_tickangle=45,
            legend_title="Airline"
        )

        # clearer axis lines
        fig.update_xaxes(showline=True, linewidth=2)
        fig.update_yaxes(showline=True, linewidth=2)

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Insight:**

    - **Ticket prices start highest when only a few days are left** (0–5 days), and drop sharply as the booking window widens.
    - After around **15–20 days before departure**, prices stabilize for most airlines.
    - **Airline pricing strategies differ noticeably**:
    - Premium airlines like **Vistara** and **Air India** remain consistently more expensive across all booking windows.
    - Budget carriers such as **AirAsia** and **GO_FIRST** offer the lowest prices throughout.
    - The curves show that some airlines reduce prices more aggressively as the departure date gets farther away, while others show more gradual changes.
    - When multiple classes are included, the lines reflect the **combined influence of Economy and Business**, leading to greater variation due to class mix.

    """)
    

# =============================
# 🔹 7. Summary / Conclusion
# =============================
elif page == "Summary & Conclusion":
    st.header("📘 Summary & Key Insights")

    st.markdown("""
    ### **Overall Findings**

    - **Airline choice strongly influences ticket prices.**  
    Premium airlines like Vistara and Air India consistently charge much higher fares, especially for Business class.

    - **Business class prices vary dramatically across airlines.**  
    Some airlines charge 5–7× more for Business class, while others have smaller class gaps.

    - **Non-stop flights are the cheapest overall**, while **1-stop and 2+ stop flights tend to be more expensive**, especially for Business class.

    - **Price behavior changes as the departure date approaches.**  
    All airlines show higher prices when booked last-minute, with large drops between 0–10 days left and stabilization after ~20 days.

    - **Price sensitivity to booking window differs by airline.**  
    Some airlines show sharp price drops as days_left increases, while others maintain stable pricing.

    - **Stops and Class interact in complex ways.**  
    Multi-stop Business flights are often the most expensive because they correspond to longer, higher-end routes.

    - **Airline, Class, and Stops jointly shape pricing patterns**, confirming that price is not determined by a single factor but by the interaction of multiple ones.

    ---

    ### **Conclusion**

    Across RQ1–RQ5, the results show that:

    - Some hypotheses (RQ1, RQ2, RQ3, RQ5) were **supported**,  
    - while others (such as RQ4) were **not supported**,  
    revealing unexpected patterns in stop-based pricing.

    Overall, the analyses demonstrate that **airline pricing is shaped by interconnected factors** —  
    **airline strategy, number of stops, travel class, and the booking window**.  

    These insights can help travelers make better booking decisions  
    and enable airlines to understand competitor pricing dynamics.
    """)


