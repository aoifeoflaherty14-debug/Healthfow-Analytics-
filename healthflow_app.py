import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="HealthFlow | HSE Analytics Platform",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f5f0e8; }
    .stApp { background-color: #f5f0e8; }
    h1, h2, h3 { color: #1a2744; font-family: Georgia, serif; }
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 5px solid #1a2744;
    }
    .red-card   { border-left-color: #c0392b !important; }
    .amber-card { border-left-color: #e67e22 !important; }
    .green-card { border-left-color: #27ae60 !important; }
    .section-header {
        background: #1a2744;
        color: white;
        padding: 10px 18px;
        border-radius: 8px;
        font-family: Georgia, serif;
        font-size: 1.1rem;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_excel("HF_Master_AE.xlsx")
    df["snapshot_date"] = pd.to_datetime(df["snapshot_date"])
    return df

df = load_data()

COLOUR_MAP = {"Green": "#27ae60", "Amber": "#e67e22", "Red": "#c0392b"}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/HSE_logo.svg/320px-HSE_logo.svg.png", width=120)
    st.markdown("## 🏥 HealthFlow")
    st.markdown("*HSE Urgent Care Analytics*")
    st.divider()
    page = st.radio("Navigate", [
        "📊 Live Dashboard",
        "🔍 Exploratory Analysis",
        "⚙️ Rule Engine",
        "📈 SARIMAX Forecast"
    ])
    st.divider()
    region_filter = st.multiselect("Filter by Region", options=df["region"].unique().tolist(), default=df["region"].unique().tolist())
    st.caption(f"Data snapshot: {df['snapshot_date'].iloc[0].strftime('%d %b %Y')}")

filtered_df = df[df["region"].isin(region_filter)]

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — LIVE DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if page == "📊 Live Dashboard":
    st.markdown("# 📊 Live ED Status Dashboard")
    st.markdown("Real-time traffic light status across HSE hospitals")

    # KPI row
    col1, col2, col3, col4 = st.columns(4)
    red_count   = len(filtered_df[filtered_df["traffic_light_status"] == "Red"])
    amber_count = len(filtered_df[filtered_df["traffic_light_status"] == "Amber"])
    green_count = len(filtered_df[filtered_df["traffic_light_status"] == "Green"])
    total_trolleys = int(filtered_df["total_trolleys"].sum())

    with col1:
        st.markdown(f'<div class="metric-card red-card"><h3 style="color:#c0392b;margin:0">🔴 {red_count}</h3><p style="margin:0;color:#666">Critical Hospitals</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card amber-card"><h3 style="color:#e67e22;margin:0">🟡 {amber_count}</h3><p style="margin:0;color:#666">Elevated Pressure</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card green-card"><h3 style="color:#27ae60;margin:0">🟢 {green_count}</h3><p style="margin:0;color:#666">Operating Normally</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><h3 style="color:#1a2744;margin:0">🛏️ {total_trolleys}</h3><p style="margin:0;color:#666">Total Trolleys</p></div>', unsafe_allow_html=True)

    st.divider()

    # Hospital cards
    st.markdown('<div class="section-header">🏥 Hospital Status Cards</div>', unsafe_allow_html=True)
    sort_order = {"Red": 0, "Amber": 1, "Green": 2}
    display_df = filtered_df.copy()
    display_df["_sort"] = display_df["traffic_light_status"].map(sort_order)
    display_df = display_df.sort_values("_sort")

    cols = st.columns(3)
    for i, (_, row) in enumerate(display_df.iterrows()):
        status = row["traffic_light_status"]
        colour = COLOUR_MAP[status]
        emoji  = {"Red": "🔴", "Amber": "🟡", "Green": "🟢"}[status]
        with cols[i % 3]:
            st.markdown(f"""
            <div style="background:white;border-radius:10px;padding:14px;margin-bottom:12px;
                        border-left:5px solid {colour};box-shadow:0 2px 6px rgba(0,0,0,0.07)">
                <strong style="color:#1a2744">{row['Hospital']}</strong><br>
                <span style="font-size:0.85rem;color:#666">{row['region'].title()} · {row['hospital_model']}</span><br><br>
                <span style="font-size:1.1rem">{emoji} <strong style="color:{colour}">{status}</strong></span><br>
                <span style="font-size:0.8rem;color:#555">
                    Occupancy: <strong>{row['occupancy_rate_pct']}%</strong> &nbsp;|&nbsp;
                    Trolleys: <strong>{int(row['total_trolleys'])}</strong><br>
                    Wait Tier: <strong>{row['wait_tier']}</strong> &nbsp;|&nbsp;
                    Avoidable: <strong>{row['avoidable_rate_pct']}%</strong>
                </span>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # Occupancy chart
    st.markdown('<div class="section-header">📊 Occupancy Rate by Hospital</div>', unsafe_allow_html=True)
    occ_df = filtered_df.sort_values("occupancy_rate_pct", ascending=False)
    fig = px.bar(occ_df, x="Hospital", y="occupancy_rate_pct",
                 color="traffic_light_status",
                 color_discrete_map=COLOUR_MAP,
                 labels={"occupancy_rate_pct": "Occupancy Rate (%)", "Hospital": ""},
                 title="Occupancy Rate by Hospital")
    fig.update_layout(xaxis_tickangle=-45, plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
                      legend_title="Status", height=420)
    fig.add_hline(y=7, line_dash="dash", line_color="#e67e22", annotation_text="Amber threshold")
    fig.add_hline(y=9, line_dash="dash", line_color="#c0392b", annotation_text="Red threshold")
    st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — EXPLORATORY ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🔍 Exploratory Analysis":
    st.markdown("# 🔍 Exploratory Data Analysis")
    st.markdown("Key dimensions of HSE urgent care demand across 27 hospitals")

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Initial EDA", "📈 Advanced EDA", "🗺️ Regional Analysis", "📋 Raw Data"])

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            # Traffic light distribution
            tl_counts = filtered_df["traffic_light_status"].value_counts().reset_index()
            tl_counts.columns = ["Status", "Count"]
            fig_pie = px.pie(tl_counts, names="Status", values="Count",
                             color="Status", color_discrete_map=COLOUR_MAP,
                             title="Traffic Light Status Distribution")
            fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            # Wait tier breakdown
            wt_counts = filtered_df["wait_tier"].value_counts().reset_index()
            wt_counts.columns = ["Wait Tier", "Count"]
            wt_order = ["No breach", "Low breach", "Moderate breach", "High breach"]
            wt_counts["Wait Tier"] = pd.Categorical(wt_counts["Wait Tier"], categories=wt_order, ordered=True)
            wt_counts = wt_counts.sort_values("Wait Tier")
            fig_wt = px.bar(wt_counts, x="Wait Tier", y="Count",
                            color="Wait Tier",
                            color_discrete_sequence=["#27ae60","#f1c40f","#e67e22","#c0392b"],
                            title="Wait Tier Breakdown (Patients >24hrs)")
            fig_wt.update_layout(plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)", showlegend=False)
            st.plotly_chart(fig_wt, use_container_width=True)

        # Trolley load vs beds scatter
        fig_scatter = px.scatter(filtered_df, x="hospital_beds", y="trolley_load",
                                 color="traffic_light_status",
                                 color_discrete_map=COLOUR_MAP,
                                 hover_name="Hospital",
                                 size="occupancy_rate_pct",
                                 labels={"hospital_beds": "Hospital Beds", "trolley_load": "Trolley Load"},
                                 title="Trolley Load vs Hospital Beds")
        fig_scatter.update_layout(plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_scatter, use_container_width=True)

    with tab2:
        # Top 10 by monthly attendances
        top10 = filtered_df.nlargest(10, "est_monthly_attendances")
        fig_top = px.bar(top10, x="est_monthly_attendances", y="Hospital",
                         orientation="h",
                         color="traffic_light_status",
                         color_discrete_map=COLOUR_MAP,
                         labels={"est_monthly_attendances": "Avg Monthly Attendances", "Hospital": ""},
                         title="Top 10 Hospitals by Average Monthly ED Attendances")
        fig_top.update_layout(plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
                               yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig_top, use_container_width=True)

        # Avoidable rate by hospital
        avoid_df = filtered_df.sort_values("avoidable_rate_pct", ascending=False)
        fig_avoid = px.bar(avoid_df, x="Hospital", y="avoidable_rate_pct",
                           color="hospital_model",
                           labels={"avoidable_rate_pct": "Avoidable Attendance Rate (%)", "Hospital": ""},
                           title="Avoidable ED Attendance Rate by Hospital")
        fig_avoid.update_layout(xaxis_tickangle=-45, plot_bgcolor="white",
                                 paper_bgcolor="rgba(0,0,0,0)", height=420)
        st.plotly_chart(fig_avoid, use_container_width=True)

        # Behavioural Impact Score
        fig_bis = px.bar(filtered_df.sort_values("behavioural_impact_score", ascending=False),
                         x="Hospital", y="behavioural_impact_score",
                         color="traffic_light_status",
                         color_discrete_map=COLOUR_MAP,
                         labels={"behavioural_impact_score": "Behavioural Impact Score", "Hospital": ""},
                         title="Behavioural Impact Score by Hospital")
        fig_bis.update_layout(xaxis_tickangle=-45, plot_bgcolor="white",
                               paper_bgcolor="rgba(0,0,0,0)", height=420)
        st.plotly_chart(fig_bis, use_container_width=True)

    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            reg_occ = filtered_df.groupby("region")["occupancy_rate_pct"].mean().reset_index()
            fig_reg = px.bar(reg_occ, x="region", y="occupancy_rate_pct",
                             color="region",
                             labels={"occupancy_rate_pct": "Avg Occupancy Rate (%)", "region": "Region"},
                             title="Average Occupancy Rate by Region")
            fig_reg.update_layout(plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)", showlegend=False)
            st.plotly_chart(fig_reg, use_container_width=True)

        with col2:
            reg_tl = filtered_df.groupby(["region","traffic_light_status"]).size().reset_index(name="count")
            fig_reg_tl = px.bar(reg_tl, x="region", y="count",
                                color="traffic_light_status",
                                color_discrete_map=COLOUR_MAP,
                                barmode="group",
                                labels={"count": "Number of Hospitals", "region": "Region"},
                                title="Traffic Light Distribution by Region")
            fig_reg_tl.update_layout(plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_reg_tl, use_container_width=True)

    with tab4:
        st.dataframe(filtered_df.drop(columns=["_sort"], errors="ignore"), use_container_width=True)
        st.caption(f"{len(filtered_df)} hospitals shown")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — RULE ENGINE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "⚙️ Rule Engine":
    st.markdown("# ⚙️ Prescriptive Rule Engine")
    st.markdown("Compares current and predicted RAG status to trigger appropriate system responses")

    # Rule engine logic
    def get_system_action(current, predicted):
        if current == "Red" and predicted == "Red":
            return "🚨 Urgent Redirection", "#c0392b"
        elif current == "Amber" and predicted == "Red":
            return "🔔 Notify Concierge Users", "#e67e22"
        elif current == "Amber" and predicted == "Green":
            return "👁️ Monitor — No Alert", "#f39c12"
        elif current == "Green":
            return "✅ No Action Required", "#27ae60"
        else:
            return "👁️ Monitor — No Alert", "#3498db"

    def get_care_pathway(avoidable_rate, occupancy, bis):
        if occupancy >= 9 or bis >= 6:
            return "A&E / 999", "#c0392b", "Critical condition requiring emergency care"
        elif occupancy >= 7 or bis >= 5:
            return "Minor Injury Unit", "#e67e22", "Moderate condition requiring diagnosis or prescription"
        elif avoidable_rate >= 23:
            return "GP / Out-of-Hours or Urgent Virtual Care", "#f39c12", "Non-emergency condition manageable by GP or UVC"
        else:
            return "Pharmacy", "#27ae60", "Minor self-limiting condition — no GP visit required"

    # Summary rule table
    st.markdown('<div class="section-header">📋 Rule Engine Decision Matrix</div>', unsafe_allow_html=True)
    rules_data = {
        "Current Status": ["🔴 Red", "🟡 Amber", "🟡 Amber", "🟢 Green"],
        "Predicted Status": ["🔴 Red", "🔴 Red", "🟢 Green", "Any"],
        "System Action": ["Urgent Patient Redirection", "Notify Concierge Users", "Monitor — No Alert", "No Action Required"],
        "Severity": ["Critical", "High", "Low", "None"]
    }
    st.dataframe(pd.DataFrame(rules_data), use_container_width=True, hide_index=True)

    st.divider()

    # Interactive simulator
    st.markdown('<div class="section-header">🔬 Live Rule Engine Simulator</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        selected_hospital = st.selectbox("Select Hospital", filtered_df["Hospital"].tolist())
        hosp_row = filtered_df[filtered_df["Hospital"] == selected_hospital].iloc[0]
        current_status = hosp_row["traffic_light_status"]
        st.info(f"**Current Status:** {current_status} | **Occupancy:** {hosp_row['occupancy_rate_pct']}% | **BIS:** {hosp_row['behavioural_impact_score']}")

    with col2:
        predicted_status = st.selectbox("Predicted Status (4hr forecast)", ["Green", "Amber", "Red"],
                                         index=["Green","Amber","Red"].index(current_status))

    action, action_colour = get_system_action(current_status, predicted_status)
    pathway, pathway_colour, pathway_desc = get_care_pathway(
        hosp_row["avoidable_rate_pct"],
        hosp_row["occupancy_rate_pct"],
        hosp_row["behavioural_impact_score"]
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="background:white;border-radius:10px;padding:20px;border-left:6px solid {action_colour};box-shadow:0 2px 8px rgba(0,0,0,0.08)">
            <h4 style="color:#1a2744;margin:0 0 8px 0">System Action</h4>
            <h2 style="color:{action_colour};margin:0">{action}</h2>
            <p style="color:#666;margin:8px 0 0 0;font-size:0.85rem">
                Current: <strong>{current_status}</strong> → Predicted: <strong>{predicted_status}</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="background:white;border-radius:10px;padding:20px;border-left:6px solid {pathway_colour};box-shadow:0 2px 8px rgba(0,0,0,0.08)">
            <h4 style="color:#1a2744;margin:0 0 8px 0">Recommended Care Pathway</h4>
            <h2 style="color:{pathway_colour};margin:0">🏥 {pathway}</h2>
            <p style="color:#666;margin:8px 0 0 0;font-size:0.85rem">{pathway_desc}</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Full hospital rule engine output
    st.markdown('<div class="section-header">🏥 Rule Engine Output — All Hospitals</div>', unsafe_allow_html=True)
    engine_rows = []
    for _, row in filtered_df.iterrows():
        # Simulate a predicted status slightly worse for high occupancy
        occ = row["occupancy_rate_pct"]
        if occ >= 9:
            pred = "Red"
        elif occ >= 6:
            pred = "Amber"
        else:
            pred = "Green"
        action_text, _ = get_system_action(row["traffic_light_status"], pred)
        pathway_text, _, _ = get_care_pathway(row["avoidable_rate_pct"], occ, row["behavioural_impact_score"])
        engine_rows.append({
            "Hospital": row["Hospital"],
            "Current": row["traffic_light_status"],
            "Predicted (4hr)": pred,
            "System Action": action_text,
            "Care Pathway": pathway_text,
            "Occupancy %": row["occupancy_rate_pct"],
            "BIS": row["behavioural_impact_score"],
            "Avoidable %": row["avoidable_rate_pct"]
        })

    engine_df = pd.DataFrame(engine_rows)
    st.dataframe(engine_df, use_container_width=True, hide_index=True)

    # Care pathway distribution chart
    pathway_counts = engine_df["Care Pathway"].value_counts().reset_index()
    pathway_counts.columns = ["Pathway", "Count"]
    fig_pw = px.pie(pathway_counts, names="Pathway", values="Count",
                    title="Recommended Care Pathway Distribution",
                    color_discrete_sequence=["#c0392b","#e67e22","#f39c12","#27ae60"])
    fig_pw.update_layout(paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_pw, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — SARIMAX FORECAST
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📈 SARIMAX Forecast":
    st.markdown("# 📈 SARIMAX Occupancy Forecast")
    st.markdown("Simulated four-hour ahead occupancy forecasts with seasonal and exogenous components")

    try:
        from statsmodels.tsa.statespace.sarimax import SARIMAX

        selected_hospital = st.selectbox("Select Hospital", filtered_df["Hospital"].tolist())
        hosp_row = filtered_df[filtered_df["Hospital"] == selected_hospital].iloc[0]

        st.info(f"**{selected_hospital}** | Current Occupancy: **{hosp_row['occupancy_rate_pct']}%** | Status: **{hosp_row['traffic_light_status']}**")

        # Generate synthetic time series based on real hospital characteristics
        np.random.seed(42)
        n_points = 29 * 6  # 29 months × 6 four-hour intervals per day (simplified)
        base_occ = hosp_row["occupancy_rate_pct"]
        seasonal_amp = hosp_row["behavioural_impact_score"] * 0.3

        # Build realistic occupancy series
        t = np.arange(n_points)
        daily_cycle    = seasonal_amp * np.sin(2 * np.pi * t / 6)
        weekly_cycle   = (seasonal_amp * 0.5) * np.sin(2 * np.pi * t / 42)
        monthly_trend  = 0.003 * t
        noise          = np.random.normal(0, 0.4, n_points)
        occupancy_series = base_occ + daily_cycle + weekly_cycle + monthly_trend + noise
        occupancy_series = np.clip(occupancy_series, 0, 20)

        # Exogenous: bank holiday flag (random sparse)
        exog_train = np.random.choice([0, 1], size=n_points, p=[0.97, 0.03]).reshape(-1, 1)

        # Fit SARIMAX
        with st.spinner("Fitting SARIMAX model..."):
            model = SARIMAX(occupancy_series,
                            exog=exog_train,
                            order=(1, 0, 1),
                            seasonal_order=(1, 0, 1, 6),
                            enforce_stationarity=False,
                            enforce_invertibility=False)
            result = model.fit(disp=False)

        # Forecast 12 steps ahead (= 48 hours)
        n_forecast = 12
        exog_forecast = np.zeros((n_forecast, 1))
        forecast = result.get_forecast(steps=n_forecast, exog=exog_forecast)
        forecast_mean = forecast.predicted_mean
        conf_int = forecast.conf_int()

        # Build datetime index
        base_dt = datetime(2024, 6, 3, 8, 0)
        hist_index = [base_dt + timedelta(hours=4*i) for i in range(n_points)]
        fore_index = [hist_index[-1] + timedelta(hours=4*i) for i in range(1, n_forecast+1)]

        # RAG thresholds
        def occ_to_rag(val):
            if val >= 9:   return "Red"
            elif val >= 7: return "Amber"
            else:          return "Green"

        fig = go.Figure()

        # Historical
        fig.add_trace(go.Scatter(
            x=hist_index[-48:], y=occupancy_series[-48:],
            mode="lines", name="Historical Occupancy",
            line=dict(color="#1a2744", width=2)
        ))

        # Forecast
        fig.add_trace(go.Scatter(
            x=fore_index, y=forecast_mean,
            mode="lines+markers", name="SARIMAX Forecast",
            line=dict(color="#e67e22", width=2.5, dash="dot"),
            marker=dict(size=6)
        ))

        # Confidence interval
        fig.add_trace(go.Scatter(
            x=fore_index + fore_index[::-1],
            y=list(conf_int.iloc[:, 1]) + list(conf_int.iloc[:, 0])[::-1],
            fill="toself", fillcolor="rgba(230,126,34,0.15)",
            line=dict(color="rgba(255,255,255,0)"),
            name="95% Confidence Interval"
        ))

        # Threshold lines
        fig.add_hline(y=7, line_dash="dash", line_color="#e67e22",
                      annotation_text="Amber threshold (7%)", annotation_position="left")
        fig.add_hline(y=9, line_dash="dash", line_color="#c0392b",
                      annotation_text="Red threshold (9%)", annotation_position="left")

        fig.update_layout(
            title=f"4-Hour Occupancy Forecast — {selected_hospital}",
            xaxis_title="Date / Time",
            yaxis_title="Occupancy Rate (%)",
            plot_bgcolor="white",
            paper_bgcolor="rgba(0,0,0,0)",
            height=480,
            legend=dict(orientation="h", yanchor="bottom", y=1.02)
        )
        st.plotly_chart(fig, use_container_width=True)

        # Forecast table with RAG
        st.markdown('<div class="section-header">📋 48-Hour Forecast Breakdown</div>', unsafe_allow_html=True)
        fore_df = pd.DataFrame({
            "Timestamp": [dt.strftime("%d %b %H:%M") for dt in fore_index],
            "Forecast Occupancy (%)": forecast_mean.round(2).values,
            "Lower CI": conf_int.iloc[:, 0].round(2).values,
            "Upper CI": conf_int.iloc[:, 1].round(2).values,
            "Predicted Status": [occ_to_rag(v) for v in forecast_mean.values]
        })
        st.dataframe(fore_df, use_container_width=True, hide_index=True)

        # Model summary
        with st.expander("📊 SARIMAX Model Summary"):
            st.text(result.summary().as_text())

        # Model metrics
        col1, col2, col3 = st.columns(3)
        residuals = result.resid
        mae  = np.mean(np.abs(residuals))
        rmse = np.sqrt(np.mean(residuals**2))
        mape = np.mean(np.abs(residuals / (occupancy_series + 1e-5))) * 100
        with col1:
            st.metric("MAE",  f"{mae:.3f}")
        with col2:
            st.metric("RMSE", f"{rmse:.3f}")
        with col3:
            st.metric("MAPE", f"{mape:.2f}%")

    except Exception as e:
        st.error(f"SARIMAX fitting error: {e}")
        st.info("Install statsmodels: `pip install statsmodels`")
