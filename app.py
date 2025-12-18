import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION & DARK THEME
# ---------------------------------------------------------
st.set_page_config(
    page_title="Festival Emoji Analytics",
    page_icon="🎉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Force Dark Mode & Neon Styling
st.markdown("""
    <style>
    /* Backgrounds */
    .stApp { background-color: #0E1117; color: white; }
    [data-testid="stSidebar"] { background-color: #161B22; }
    
    /* Metrics Cards */
    div[data-testid="metric-container"] {
        background-color: #1F2937;
        border-left: 5px solid #8B5CF6;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    /* Text Colors */
    h1, h2, h3 { color: #A78BFA !important; }
    p, label { color: #E5E7EB !important; }
    
    /* Upload Box Styling */
    .stFileUploader {
        border: 2px dashed #8B5CF6;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. DATA PROCESSING FUNCTION
# ---------------------------------------------------------
@st.cache_data
def process_data(uploaded_file):
    """
    Reads the uploaded Excel file and generates necessary columns
    to match the dashboard structure.
    """
    try:
        df = pd.read_excel(uploaded_file)
        
        # 1. Tweet IDs (Random ID generation)
        if 'Tweet_ID' not in df.columns:
            df['Tweet_ID'] = np.random.randint(1000000, 9999999, size=len(df))
            
        # 2. Authors (Random Author assignment)
        if 'Author_ID' not in df.columns:
            authors = ['Ananya_Rao', 'Rohan_M', 'Priya_Singh', 'Arjun_K',
                       'Vikram_P', 'Meera_N', 'Suresh_Eats']
            df['Author_ID'] = np.random.choice(authors, size=len(df))
            
        # 3. Dates (Simulate last 30 days if no date column)
        if 'Date' not in df.columns:
            start_date = datetime.now() - timedelta(days=30)
            df['Date'] = [
                start_date + timedelta(days=np.random.randint(0, 30),
                                       hours=np.random.randint(0, 23))
                for _ in range(len(df))
            ]
        else:
            df['Date'] = pd.to_datetime(df['Date'])

        # 4. Handle Text Column Renaming
        if 'Tweet' in df.columns and 'Tweet_Text' not in df.columns:
            df['Tweet_Text'] = df['Tweet']
        elif 'Tweet_Text' not in df.columns:
            df['Tweet_Text'] = "No text available"

        # Ensure Emoji column exists
        if 'Emoji' not in df.columns:
            df['Emoji'] = "🙂"

        return df
        
    except Exception as e:
        st.error(f"Error processing file: {e}")
        return pd.DataFrame()

# ---------------------------------------------------------
# 3. SIDEBAR - FILE UPLOAD & FILTERS
# ---------------------------------------------------------
st.sidebar.title("⚙️ Dashboard Config")

st.sidebar.subheader("1. Upload Data")
uploaded_file = st.sidebar.file_uploader(
    "Upload Excel File (DEV DATASET.xlsx)", type=['xlsx']
)

if uploaded_file is not None:
    df = process_data(uploaded_file)
    
    if not df.empty:
        st.sidebar.success("Data Loaded Successfully!")
        
        # --- Filter Controls ---
        st.sidebar.subheader("2. Filter Controls")
        
        # Festival filter
        festival_options = ["All"]
        if 'Festival' in df.columns:
            festival_options += sorted(df['Festival'].dropna().unique().tolist())
        sel_festival = st.sidebar.selectbox("Filter by Festival", festival_options)
        
        # Sentiment filter
        sentiment_options = ["All"]
        if 'Sentiment' in df.columns:
            sentiment_options += sorted(df['Sentiment'].dropna().unique().tolist())
        sel_sentiment = st.sidebar.selectbox("Filter by Sentiment", sentiment_options)
        
        top_n = st.sidebar.slider("Top Emojis to Show", 5, 50, 10)

        # Apply Filters
        df_filt = df.copy()
        if sel_festival != "All" and 'Festival' in df_filt.columns:
            df_filt = df_filt[df_filt['Festival'] == sel_festival]
        if sel_sentiment != "All" and 'Sentiment' in df_filt.columns:
            df_filt = df_filt[df_filt['Sentiment'] == sel_sentiment]

        # ---------------------------------------------------------
        # 4. MAIN DASHBOARD LAYOUT
        # ---------------------------------------------------------
        st.title("🎉 Festival Emoji Analytics")
        st.markdown(f"### Real-time Sentiment & Emotion Tracking ({sel_festival})")

        # --- A. KPI ROW ---
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Tweets", len(df_filt))

        unique_emoji_count = df_filt['Emoji'].nunique() if 'Emoji' in df_filt.columns else 0
        c2.metric("Unique Emojis", unique_emoji_count)

        top_emotion = "N/A"
        if 'Emotion' in df_filt.columns and not df_filt['Emotion'].mode().empty:
            top_emotion = df_filt['Emotion'].mode()[0]
        c3.metric("Top Emotion", top_emotion)

        # Top Emoji metric
        top_emoji = "N/A"
        if 'Emoji' in df_filt.columns and not df_filt['Emoji'].mode().empty:
            top_emoji = df_filt['Emoji'].mode()[0]
        c4.metric("Top Emoji", top_emoji)

        st.markdown("---")

        # --- B. CHARTS ROW 1 ---
        col_left, col_right = st.columns([2, 1])

        with col_left:
            st.subheader("📊 Emoji Frequency Ranking")
            if 'Emoji' in df_filt.columns:
                emoji_counts = (
                    df_filt['Emoji']
                    .value_counts()
                    .nlargest(top_n)
                    .reset_index()
                )
                emoji_counts.columns = ['Emoji', 'Count']
                
                fig_bar = px.bar(
                    emoji_counts,
                    x='Count',
                    y='Emoji',
                    orientation='h',
                    text='Count',
                    color='Count',
                    color_continuous_scale='Viridis'
                )
                fig_bar.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.warning("Column 'Emoji' not found in dataset.")

        with col_right:
            st.subheader("🍩 Sentiment Split")
            if 'Sentiment' in df_filt.columns:
                fig_pie = px.pie(
                    df_filt,
                    names='Sentiment',
                    hole=0.5,
                    color_discrete_sequence=px.colors.qualitative.Bold
                )
                fig_pie.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.warning("Column 'Sentiment' not found.")

        # --- C. CHARTS ROW 2 (Treemap + Line) ---
        col3, col4 = st.columns(2)

        with col3:
            st.subheader("☁️ Emotion Treemap")
            if 'Emotion' in df_filt.columns and 'Emoji' in df_filt.columns:
                tree_df = (
                    df_filt
                    .groupby(['Emotion', 'Emoji'])
                    .size()
                    .reset_index(name='Count')
                )
                fig_tree = px.treemap(
                    tree_df,
                    path=['Emotion', 'Emoji'],
                    values='Count',
                    color='Emotion'
                )
                fig_tree.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig_tree, use_container_width=True)
            else:
                st.warning("Required columns for Treemap missing.")

        with col4:
            st.subheader("📈 Tweet Trends (Time Series)")
            if 'Date' in df_filt.columns:
                daily = (
                    df_filt
                    .groupby(df_filt['Date'].dt.date)
                    .size()
                    .reset_index(name='Tweets')
                )
                daily.rename(columns={'Date': 'Date'}, inplace=True)

                fig_line = px.line(
                    daily,
                    x='Date',
                    y='Tweets',
                    markers=True,
                    line_shape='spline'
                )
                fig_line.update_traces(line_color='#F472B6', line_width=3)
                fig_line.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig_line, use_container_width=True)
            else:
                st.warning("Date column missing.")

        st.markdown("---")

        # ---------------------------------------------------------
        # 5. EXTRA VISUALIZATIONS (Bar, Violin, Scatter)
        # ---------------------------------------------------------
        st.subheader("📌 Extra Emoji Insights")

        extra_col1, extra_col2 = st.columns(2)

        # 5A. Emoji vs Sentiment bar chart
        with extra_col1:
            st.markdown("#### 🔡 Emoji vs Sentiment (Bar)")
            if 'Emoji' in df_filt.columns and 'Sentiment' in df_filt.columns:
                emoji_sent = (
                    df_filt
                    .groupby(['Emoji', 'Sentiment'])
                    .size()
                    .reset_index(name='Count')
                )
                emoji_sent_top = (
                    emoji_sent
                    .sort_values('Count', ascending=False)
                    .head(top_n * 3)
                )

                fig_emoji_sent = px.bar(
                    emoji_sent_top,
                    x='Emoji',
                    y='Count',
                    color='Sentiment',
                    barmode='group'
                )
                fig_emoji_sent.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig_emoji_sent, use_container_width=True)
            else:
                st.info("Need both 'Emoji' and 'Sentiment' columns for this chart.")

        # 5B. Violin plot: Tweet length by Sentiment
        with extra_col2:
            st.markdown("#### 🎻 Tweet Length Distribution (Violin)")
            if 'Tweet_Text' in df_filt.columns and 'Sentiment' in df_filt.columns:
                temp = df_filt.copy()
                temp['Tweet_Length'] = temp['Tweet_Text'].astype(str).str.len()

                fig_violin = px.violin(
                    temp,
                    x='Sentiment',
                    y='Tweet_Length',
                    color='Sentiment',
                    box=True,
                    points='all'
                )
                fig_violin.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig_violin, use_container_width=True)
            else:
                st.info("Need 'Tweet_Text' and 'Sentiment' columns for violin plot.")

        # 5C. Scatter plot: Time vs Emoji
        st.markdown("#### ✨ Emoji Activity Over Time (Scatter)")
        if 'Date' in df_filt.columns and 'Emoji' in df_filt.columns:
            scat_df = df_filt.copy()
            scat_df['Date_only'] = scat_df['Date'].dt.date

            fig_scatter = px.scatter(
                scat_df,
                x='Date_only',
                y='Emoji',
                color='Sentiment' if 'Sentiment' in scat_df.columns else None,
                size_max=8
            )
            fig_scatter.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.info("Need 'Date' and 'Emoji' for scatter plot.")

        st.markdown("---")

        # ---------------------------------------------------------
        # 6. ADVANCED VISUALS: RADAR, STACKED AREA, GAUGE
        # ---------------------------------------------------------
        st.subheader("🌈 Advanced Festival Analytics")

        adv_col1, adv_col2 = st.columns(2)

        # 6A. Radar Chart (Spider Plot) – Avg tweet length by sentiment
        with adv_col1:
            st.markdown("#### 🕸️ Radar Chart: Tweet Length vs Sentiment")
            if 'Tweet_Text' in df_filt.columns and 'Sentiment' in df_filt.columns:
                radar_df = df_filt.copy()
                radar_df['Tweet_Length'] = radar_df['Tweet_Text'].astype(str).str.len()
                agg_radar = (
                    radar_df
                    .groupby('Sentiment')['Tweet_Length']
                    .mean()
                    .reset_index()
                )

                fig_radar = px.line_polar(
                    agg_radar,
                    r='Tweet_Length',
                    theta='Sentiment',
                    line_close=True
                )
                fig_radar.update_traces(fill='toself')
                fig_radar.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True)
                    ),
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig_radar, use_container_width=True)
            else:
                st.info("Need 'Tweet_Text' and 'Sentiment' for radar chart.")

        # 6B. Stacked Area Chart – Tweets per sentiment over time
        with adv_col2:
            st.markdown("#### 🏔️ Stacked Area: Sentiment Over Time")
            if 'Date' in df_filt.columns and 'Sentiment' in df_filt.columns:
                area_df = df_filt.copy()
                area_df['Date_only'] = area_df['Date'].dt.date
                area_agg = (
                    area_df
                    .groupby(['Date_only', 'Sentiment'])
                    .size()
                    .reset_index(name='Tweets')
                )

                fig_area = px.area(
                    area_agg,
                    x='Date_only',
                    y='Tweets',
                    color='Sentiment',
                    line_group='Sentiment',
                    groupnorm=None
                )
                fig_area.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig_area, use_container_width=True)
            else:
                st.info("Need 'Date' and 'Sentiment' for stacked area chart.")

        # 6C. Gauge Chart – % Positive tweets
        st.markdown("#### 🚀 Sentiment Gauge (Speedometer)")
        if 'Sentiment' in df_filt.columns and len(df_filt) > 0:
            total = len(df_filt)
            positive_count = (df_filt['Sentiment'] == 'Positive').sum()
            positive_rate = (positive_count / total) * 100

            fig_gauge = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=positive_rate,
                    title={'text': "Positive Tweets (%)"},
                    domain={'x': [0, 1], 'y': [0, 1]},
                    gauge={
                        "axis": {"range": [0, 100]},
                        "bar": {"color": "#8B5CF6"},
                        "steps": [
                            {"range": [0, 30], "color": "#DC2626"},
                            {"range": [30, 60], "color": "#F59E0B"},
                            {"range": [60, 100], "color": "#16A34A"},
                        ],
                        "threshold": {
                            "line": {"color": "white", "width": 4},
                            "thickness": 0.75,
                            "value": positive_rate,
                        },
                    },
                )
            )
            fig_gauge.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig_gauge, use_container_width=True)
        else:
            st.info("Need 'Sentiment' column for gauge chart.")

        st.markdown("---")

        # ---------------------------------------------------------
        # 7. ADVANCED FLOW & CORRELATION VISUALS
        # ---------------------------------------------------------
        st.subheader("🔀 Flow & Correlation Visuals")

        flow_col1, flow_col2 = st.columns(2)

        # 7A. Sankey Diagram: Festival -> Sentiment -> Emoji
        with flow_col1:
            st.markdown("#### 🌉 Sankey Diagram: Festival → Sentiment → Emoji")
            if 'Festival' in df_filt.columns and 'Sentiment' in df_filt.columns and 'Emoji' in df_filt.columns:
                # Build nodes: Festivals, Sentiments, Top Emojis
                top_emojis_global = (
                    df_filt['Emoji']
                    .value_counts()
                    .nlargest(top_n)
                    .index
                    .tolist()
                )
                sankey_df = df_filt[df_filt['Emoji'].isin(top_emojis_global)].copy()

                festivals = sankey_df['Festival'].dropna().unique().tolist()
                sentiments = sankey_df['Sentiment'].dropna().unique().tolist()
                emojis = top_emojis_global

                labels = festivals + sentiments + emojis
                label_to_idx = {lab: i for i, lab in enumerate(labels)}

                # Links: Festival -> Sentiment
                fs = (
                    sankey_df
                    .groupby(['Festival', 'Sentiment'])
                    .size()
                    .reset_index(name='Count')
                )
                # Links: Sentiment -> Emoji
                se = (
                    sankey_df
                    .groupby(['Sentiment', 'Emoji'])
                    .size()
                    .reset_index(name='Count')
                )

                sources = []
                targets = []
                values = []

                # F → S
                for _, row in fs.iterrows():
                    if row['Festival'] in label_to_idx and row['Sentiment'] in label_to_idx:
                        sources.append(label_to_idx[row['Festival']])
                        targets.append(label_to_idx[row['Sentiment']])
                        values.append(row['Count'])

                # S → E
                for _, row in se.iterrows():
                    if row['Sentiment'] in label_to_idx and row['Emoji'] in label_to_idx:
                        sources.append(label_to_idx[row['Sentiment']])
                        targets.append(label_to_idx[row['Emoji']])
                        values.append(row['Count'])

                if len(sources) > 0:
                    fig_sankey = go.Figure(
                        go.Sankey(
                            node=dict(
                                label=labels,
                                pad=15,
                                thickness=20,
                                color="#4B5563"
                            ),
                            link=dict(
                                source=sources,
                                target=targets,
                                value=values,
                                color="rgba(139,92,246,0.5)"
                            )
                        )
                    )
                    fig_sankey.update_layout(
                        font=dict(color='white'),
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    st.plotly_chart(fig_sankey, use_container_width=True)
                else:
                    st.info("Not enough data to draw Sankey.")
            else:
                st.info("Need 'Festival', 'Sentiment', and 'Emoji' columns for Sankey diagram.")

        # 7B. Emoji Co-occurrence Matrix (Correlation Heatmap)
        with flow_col2:
            st.markdown("#### 🧩 Emoji Co-occurrence Matrix (Heatmap)")
            if 'Emoji' in df_filt.columns:
                # For simplicity, treat each row as one emoji (if multiple emojis per tweet, you can expand).
                # Build co-occurrence on top N emojis.
                top_emojis = (
                    df_filt['Emoji']
                    .value_counts()
                    .nlargest(top_n)
                    .index
                    .tolist()
                )

                # Build a tweet-emoji occurrence matrix
                # 1 if tweet uses that emoji (here exactly one, but generic structure).
                mat_df = pd.DataFrame(0, index=df_filt.index, columns=top_emojis)
                for e in top_emojis:
                    mat_df[e] = (df_filt['Emoji'] == e).astype(int)

                # Correlation matrix
                corr_mat = mat_df.corr()

                fig_corr = px.imshow(
                    corr_mat,
                    x=top_emojis,
                    y=top_emojis,
                    color_continuous_scale="PuRd",
                    zmin=-1,
                    zmax=1
                )
                fig_corr.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig_corr, use_container_width=True)
            else:
                st.info("Need 'Emoji' column for co-occurrence heatmap.")

        st.markdown("---")

        # ---------------------------------------------------------
        # 8. ANIMATED BUBBLE & CALENDAR HEATMAP
        # ---------------------------------------------------------
        st.subheader("🗓️ Temporal Emoji Dynamics")

        time_col1, time_col2 = st.columns(2)

        # 8A. Animated Bubble Chart: Emoji popularity over time
        with time_col1:
            st.markdown("#### 🌌 Animated Bubble Chart: Emoji Popularity Over Time")
            if 'Date' in df_filt.columns and 'Emoji' in df_filt.columns:
                anim_df = df_filt.copy()
                anim_df['Date_only'] = anim_df['Date'].dt.date

                agg_anim = (
                    anim_df
                    .groupby(['Date_only', 'Emoji'])
                    .size()
                    .reset_index(name='Count')
                )

                # restrict to top_n emojis overall for clarity
                overall_top = (
                    agg_anim.groupby('Emoji')['Count']
                    .sum()
                    .sort_values(ascending=False)
                    .head(top_n)
                    .index
                    .tolist()
                )
                agg_anim = agg_anim[agg_anim['Emoji'].isin(overall_top)]

                fig_bubble = px.scatter(
                    agg_anim,
                    x='Date_only',
                    y='Emoji',
                    size='Count',
                    color='Emoji',
                    animation_frame='Date_only',
                    size_max=20
                )
                fig_bubble.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    updatemenus=[dict(bgcolor="#111827")]
                )
                st.plotly_chart(fig_bubble, use_container_width=True)
            else:
                st.info("Need 'Date' and 'Emoji' for animated bubble chart.")

        # 8B. Calendar Heatmap (GitHub Style-ish)
        with time_col2:
            st.markdown("#### 📅 Calendar Heatmap (GitHub Style)")
            if 'Date' in df_filt.columns:
                cal_df = df_filt.copy()
                cal_df['date'] = cal_df['Date'].dt.date
                cal_agg = (
                    cal_df
                    .groupby('date')
                    .size()
                    .reset_index(name='Tweets')
                )
                cal_agg['dow'] = pd.to_datetime(cal_agg['date']).dt.weekday  # 0=Mon
                cal_agg['week'] = pd.to_datetime(cal_agg['date']).dt.isocalendar().week

                fig_cal = px.density_heatmap(
                    cal_agg,
                    x='week',
                    y='dow',
                    z='Tweets',
                    color_continuous_scale="Greens"
                )
                fig_cal.update_yaxes(
                    tickmode='array',
                    tickvals=[0, 1, 2, 3, 4, 5, 6],
                    ticktext=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
                )
                fig_cal.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig_cal, use_container_width=True)
            else:
                st.info("Need 'Date' column for calendar heatmap.")

        st.markdown("---")

        # --- RAW DATA TABLE ---
        with st.expander("🔍 Inspect Raw Data (Live Feed)"):
            st.dataframe(df_filt, use_container_width=True)

else:
    # ---------------------------------------------------------
    # WELCOME SCREEN
    # ---------------------------------------------------------
    st.container()
    st.title("👋 Welcome to Emoji Analytics")
    st.info("Please upload your **DEV DATASET.xlsx** file using the sidebar to begin.")
    
    st.markdown("""
    ### Expected File Format:
    Your Excel file should contain at least these columns:
    * **Festival**
    * **Sentiment**
    * **Emoji**
    * **Emotion**
    * **Tweet** (Text content)
    """)
