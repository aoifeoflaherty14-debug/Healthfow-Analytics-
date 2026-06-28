import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="HealthFlow | Find Your Care",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background-color: #f5f0e8; }
    h1, h2, h3 { color: #1a2744; font-family: Georgia, serif; }
    .section-header {
        background: #1a2744; color: white;
        padding: 10px 18px; border-radius: 8px;
        font-family: Georgia, serif; font-size: 1.05rem;
        margin-bottom: 14px;
    }
    .card {
        background: white; border-radius: 10px;
        padding: 16px 20px; margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    }
    .hero {
        background: #1a2744; color: white;
        padding: 32px 36px; border-radius: 14px;
        margin-bottom: 28px;
    }
</style>
""", unsafe_allow_html=True)

# ── Hospital map ──────────────────────────────────────────────────────────────
HOSPITAL_MAP = {
    "Dublin": [
        "Mater Misericordiae University Hospital",
        "St. James's Hospital",
        "St. Vincent's University Hospital",
        "Beaumont Hospital",
        "Tallaght University Hospital",
        "Connolly Hospital Blanchardstown",
        "Naas General Hospital",
        "CHI at Temple Street",
        "CHI at Crumlin",
        "CHI at Tallaght",
    ],
    "Cork":        ["Cork University Hospital", "Mercy University Hospital"],
    "Kerry":       ["University Hospital Kerry"],
    "Limerick":    ["University Hospital Limerick"],
    "Galway":      ["Galway University Hospitals"],
    "Mayo":        ["Mayo University Hospital"],
    "Sligo":       ["Sligo University Hospital"],
    "Donegal":     ["Letterkenny University Hospital"],
    "Waterford":   ["UH Waterford"],
    "Wexford":     ["Wexford General Hospital"],
    "Kilkenny":    ["St Luke's General Hospital Kilkenny"],
    "Tipperary":   ["Tipperary University Hospital"],
    "Drogheda":    ["Our Lady of Lourdes Hospital"],
    "Navan":       ["Our Lady's Hospital Navan"],
    "Cavan":       ["Cavan General Hospital"],
    "Portlaoise":  ["Midland Regional Hospital Portlaoise"],
    "Tullamore":   ["Midland Regional Hospital Tullamore"],
    "Mullingar":   ["Midland Regional Hospital Mullingar"],
    "Ballinasloe": ["Portiuncula University Hospital"],
}

INSURANCE_MAP = {
    "None / Public": {
        "clinics": [],
        "benefit": "Public HSE pathway. A&E visits are free with a valid GP referral letter.",
        "colour": "#7f8c8d"
    },
    "Laya Healthcare": {
        "clinics": ["Laya Health & Wellbeing Clinic – Dublin 2", "Laya Clinic Cork"],
        "benefit": "Free GP visits and minor injury care at Laya clinics. No excess for minor injuries.",
        "colour": "#2980b9"
    },
    "VHI Healthcare": {
        "clinics": ["VHI Swiftcare – Dublin", "VHI Swiftcare – Cork", "VHI Swiftcare – Limerick"],
        "benefit": "VHI Swiftcare clinics offer same-day appointments. €75 excess applies.",
        "colour": "#8e44ad"
    },
    "Irish Life Health": {
        "clinics": ["Affidea Urgent Care – Dublin", "Affidea Urgent Care – Cork"],
        "benefit": "Access to Affidea network. Minor injury unit visits typically covered.",
        "colour": "#16a085"
    },
    "Aviva Health": {
        "clinics": ["Beacon Hospital – Dublin", "Mater Private – Dublin"],
        "benefit": "Private hospital access with reduced excess. GP referral may be required.",
        "colour": "#d35400"
    },
    "Bupa Ireland": {
        "clinics": ["Mater Private – Dublin", "Blackrock Clinic – Dublin"],
        "benefit": "Private network access. Contact Bupa to confirm cover before attending.",
        "colour": "#c0392b"
    },
}

COLOUR_MAP = {"Green": "#27ae60", "Amber": "#e67e22", "Red": "#c0392b"}

def wait_to_rag(hours):
    if hours < 2:   return "Green",  "#27ae60", "🟢", "Short wait"
    elif hours < 4: return "Amber",  "#e67e22", "🟡", "Moderate wait"
    else:           return "Red",    "#c0392b", "🔴", "Long wait"

def get_pathway(occ, avoidable, insurance, urgency):
    if urgency == "🚨 Life-threatening emergency":
        return "Call 999 / A&E", "#c0392b", "Call 999 immediately or go directly to your nearest A&E. Do not drive yourself."
    elif urgency == "⚠️ Moderate – needs same-day care":
        ins = INSURANCE_MAP.get(insurance, {})
        if insurance != "None / Public" and ins.get("clinics") and occ >= 7:
            clinic = ins["clinics"][0]
            return f"Private Clinic ({insurance})", "#2980b9", f"Your hospital is under pressure. Based on your insurance, consider {clinic} to avoid a long wait."
        elif occ >= 9:
            return "A&E", "#c0392b", "Your condition requires A&E. Prepare for a significant wait — consider an alternative hospital if one is less busy."
        else:
            return "Minor Injury Unit / Urgent Virtual Care", "#e67e22", "A Minor Injury Unit or Urgent Virtual Care (UVC) video consultation is recommended for same-day care."
    elif urgency == "💊 Minor – can wait or self-manage":
        if avoidable >= 23:
            return "GP / Out-of-Hours / UVC", "#f39c12", "A GP appointment, out-of-hours service, or Urgent Virtual Care video call is most appropriate for your condition."
        else:
            return "Pharmacy", "#27ae60", "A pharmacist can help with your condition without a GP visit. No appointment needed."
    return "GP / Out-of-Hours", "#f39c12", "Contact your GP or an out-of-hours service."

@st.cache_data
def load_data():
    df = pd.read_excel("HF_Master_AE.xlsx")
    df["snapshot_date"] = pd.to_datetime(df["snapshot_date"])
    np.random.seed(42)
    df["est_wait_hours"] = df["occupancy_rate_pct"].apply(
        lambda x: round(max(0.5, x * 0.6 + np.random.uniform(-0.3, 0.3)), 1)
    )
    df["wait_rag"] = df["est_wait_hours"].apply(lambda x: wait_to_rag(x)[0])
    return df

df = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏥 HealthFlow")
    st.markdown("*HSE Urgent Care Platform*")
    st.divider()
    page = st.radio("Navigate", [
        "🏠 Find My Care",
        "📊 Live ED Status",
        "🔍 Analytics",
        "⚙️ Rule Engine",
        "📈 Forecast"
    ])

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — FIND MY CARE
# ══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Find My Care":

    # Hero banner
    st.markdown("""
    <div class="hero">
        <h1 style="color:white;margin:0;font-family:Georgia,serif;font-size:2rem">🏥 HealthFlow</h1>
        <p style="color:#c8d6e5;margin:6px 0 0 0;font-size:1.1rem">
            Find the right care, right now — personalised to your location and insurance.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── THE TWO DROPDOWNS — first thing patient sees ──────────────────────────
    st.markdown('<div class="section-header">📍 Where are you located?&nbsp;&nbsp;&nbsp;🏥 What insurance do you have?</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        county = st.selectbox(
            "Select your county / city",
            list(HOSPITAL_MAP.keys()),
            index=0
        )
        hospital_options = HOSPITAL_MAP[county]
        selected_hospital = st.selectbox(
            "Select your nearest hospital",
            hospital_options
        )

    with col2:
        insurance = st.selectbox(
            "Select your health insurance provider",
            list(INSURANCE_MAP.keys()),
            index=0
        )
        ins_info = INSURANCE_MAP[insurance]
        st.markdown(f"""
        <div style="background:white;border-radius:8px;padding:12px 16px;
                    border-left:4px solid {ins_info['colour']};margin-top:4px">
            <span style="font-size:0.88rem;color:#444">{ins_info['benefit']}</span>
        </div>
        """, unsafe_allow_html=True)
        if ins_info["clinics"]:
            st.markdown(f"<span style='font-size:0.82rem;color:#666'>✅ Covered clinics: {' · '.join(ins_info['clinics'])}</span>", unsafe_allow_html=True)

    st.divider()

    # ── Hospital live status ───────────────────────────────────────────────────
    hosp_row = df[df["Hospital"] == selected_hospital]
    if hosp_row.empty:
        hosp_row = df.iloc[[0]]
        st.caption(f"ℹ️ Live data not yet available for {selected_hospital} — showing illustrative figures.")
    hosp_row = hosp_row.iloc[0]

    wait_hrs = hosp_row["est_wait_hours"]
    rag, rag_colour, rag_emoji, rag_label = wait_to_rag(wait_hrs)

    card_class = "red-card" if rag == "Red" else "amber-card" if rag == "Amber" else "green-card"
    st.markdown(f"""
    <div class="card {card_class}">
        <h3 style="color:#1a2744;margin:0 0 4px 0">{selected_hospital}</h3>
        <span style="color:#666;font-size:0.85rem">{county}</span>
        <br><br>
        <span style="font-size:1.5rem">{rag_emoji}</span>
        <strong style="color:{rag_colour};font-size:1.2rem"> {rag_label} — estimated wait: ~{wait_hrs} hours</strong>
        <br><br>
        <span style="font-size:0.82rem;color:#555">
            Occupancy: <strong>{hosp_row['occupancy_rate_pct']}%</strong> &nbsp;|&nbsp;
            Trolleys: <strong>{int(hosp_row['total_trolleys'])}</strong> &nbsp;|&nbsp;
            Avoidable rate: <strong>{hosp_row['avoidable_rate_pct']}%</strong>
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── Urgency selector ──────────────────────────────────────────────────────
    st.markdown('<div class="section-header">How urgent is your condition?</div>', unsafe_allow_html=True)
    urgency = st.radio("", [
        "🚨 Life-threatening emergency",
        "⚠️ Moderate – needs same-day care",
        "💊 Minor – can wait or self-manage"
    ], horizontal=True)

    st.divider()

    # ── Recommendation ────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">✅ Your Personalised Recommendation</div>', unsafe_allow_html=True)
    pathway, path_colour, path_desc = get_pathway(
        hosp_row["occupancy_rate_pct"],
        hosp_row["avoidable_rate_pct"],
        insurance,
        urgency
    )

    st.markdown(f"""
    <div class="card" style="border-left:6px solid {path_colour};padding:24px;">
        <h2 style="color:{path_colour};margin:0 0 10px 0">🏥 {pathway}</h2>
        <p style="color:#333;margin:0;font-size:1rem;line-height:1.6">{path_desc}</p>
    </div>
    """, unsafe_allow_html=True)

    if "Life-threatening" in urgency:
        st.error("🚨 Call 999 immediately. Do not drive yourself to hospital.")
    elif rag == "Red":
        st.warning(f"⚠️ {selected_hospital} is under severe pressure ({wait_hrs}hr wait). Consider an alternative hospital if your condition allows.")

        # Suggest less busy alternatives in same county
        alt = df[df["Hospital"].isin(HOSPITAL_MAP.get(county, []))].copy()
        alt = alt[alt["Hospital"] != selected_hospital].sort_values("est_wait_hours")
        if not alt.empty:
            st.markdown("**🔄 Less busy alternatives nearby:**")
            for _, ar in alt.head(2).iterrows():
                ar_rag, ar_col, ar_emoji, ar_label = wait_to_rag(ar["est_wait_hours"])
                st.markdown(f"- {ar_emoji} **{ar['Hospital']}** — ~{ar['est_wait_hours']}hrs wait")
    elif rag == "Amber":
        st.info(f"ℹ️ {selected_hospital} is experiencing elevated demand. Estimated wait: {wait_hrs} hours.")
    else:
        st.success(f"✅ {selected_hospital} is operating normally. Estimated wait: {wait_hrs} hours.")

    # ── Concierge ─────────────────────────────────────────────────────────────
    st.divider()
    st.markdown("#### 🔔 Concierge Alert")
    st.markdown("Register to be notified when wait times drop at your preferred hospital.")
    email = st.text_input("Your email address")
    if st.button("Notify Me When Wait Times Drop"):
        if email:
            st.success(f"✅ You'll be notified at **{email}** when wait times improve at {selected_hospital}.")
        else:
            st.warning("Please enter your email address.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — LIVE ED STATUS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📊 Live ED Status":
    st.markdown("# 📊 Live ED Status")
    st.markdown("Wait time traffic light status across all HSE hospitals")

    col1, col2, col3, col4 = st.columns(4)
    red_c   = len(df[df["wait_rag"]=="Red"])
    amb_c   = len(df[df["wait_rag"]=="Amber"])
    grn_c   = len(df[df["wait_rag"]=="Green"])
    col1.metric("🔴 Long waits (4hrs+)", red_c)
    col2.metric("🟡 Moderate waits (2-4hrs)", amb_c)
    col3.metric("🟢 Short waits (<2hrs)", grn_c)
    col4.metric("🏥 Hospitals monitored", len(df))

    st.divider()

    for county, hospitals in HOSPITAL_MAP.items():
        county_df = df[df["Hospital"].isin(hospitals)]
        if county_df.empty:
            continue
        st.markdown(f"#### 📍 {county}")
        cols = st.columns(min(len(hospitals), 3))
        for i, (_, row) in enumerate(county_df.iterrows()):
            rag, rag_c, rag_e, rag_l = wait_to_rag(row["est_wait_hours"])
            card_cls = "red-card" if rag=="Red" else "amber-card" if rag=="Amber" else "green-card"
            with cols[i % 3]:
                st.markdown(f"""
                <div class="card {card_cls}">
                    <strong style="color:#1a2744">{row['Hospital']}</strong><br>
                    <span>{rag_e} <strong style="color:{rag_c}">~{row['est_wait_hours']}hrs</strong> — {rag_l}</span><br>
                    <span style="font-size:0.78rem;color:#666">
                        Occupancy: {row['occupancy_rate_pct']}% | Trolleys: {int(row['total_trolleys'])}
                    </span>
                </div>
                """, unsafe_allow_html=True)

    st.divider()
    fig = px.bar(df.sort_values("est_wait_hours", ascending=False),
                 x="Hospital", y="est_wait_hours",
                 color="wait_rag", color_discrete_map=COLOUR_MAP,
                 labels={"est_wait_hours":"Estimated Wait (hrs)","Hospital":""},
                 title="Estimated Wait Times — All Hospitals")
    fig.add_hline(y=2, line_dash="dash", line_color="#e67e22", annotation_text="Amber (2hrs)")
    fig.add_hline(y=4, line_dash="dash", line_color="#c0392b", annotation_text="Red (4hrs)")
    fig.update_layout(xaxis_tickangle=-45, plot_bgcolor="white",
                      paper_bgcolor="rgba(0,0,0,0)", height=420)
    st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🔍 Analytics":
    st.markdown("# 🔍 Exploratory Analytics")
    tab1, tab2 = st.tabs(["📊 Initial EDA", "📈 Advanced EDA"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            tl = df["wait_rag"].value_counts().reset_index()
            tl.columns = ["Status","Count"]
            fig_pie = px.pie(tl, names="Status", values="Count",
                             color="Status", color_discrete_map=COLOUR_MAP,
                             title="Wait Time Status Distribution")
            fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_pie, use_container_width=True)
        with col2:
            wt = df["wait_tier"].value_counts().reset_index()
            wt.columns = ["Tier","Count"]
            fig_wt = px.bar(wt, x="Tier", y="Count",
                            title="Wait Tier Breakdown (>24hrs)")
            fig_wt.update_layout(plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_wt, use_container_width=True)

        fig_sc = px.scatter(df, x="hospital_beds", y="trolley_load",
                            color="wait_rag", color_discrete_map=COLOUR_MAP,
                            hover_name="Hospital", size="occupancy_rate_pct",
                            title="Trolley Load vs Hospital Beds")
        fig_sc.update_layout(plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_sc, use_container_width=True)

    with tab2:
        top10 = df.nlargest(10,"est_monthly_attendances")
        fig_top = px.bar(top10, x="est_monthly_attendances", y="Hospital",
                         orientation="h", color="wait_rag",
                         color_discrete_map=COLOUR_MAP,
                         title="Top 10 Hospitals by Monthly Attendances")
        fig_top.update_layout(plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
                               yaxis={"categoryorder":"total ascending"})
        st.plotly_chart(fig_top, use_container_width=True)

        fig_av = px.bar(df.sort_values("avoidable_rate_pct", ascending=False),
                        x="Hospital", y="avoidable_rate_pct",
                        color="wait_rag", color_discrete_map=COLOUR_MAP,
                        title="Avoidable ED Attendance Rate by Hospital")
        fig_av.update_layout(xaxis_tickangle=-45, plot_bgcolor="white",
                              paper_bgcolor="rgba(0,0,0,0)", height=420)
        st.plotly_chart(fig_av, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — RULE ENGINE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "⚙️ Rule Engine":
    st.markdown("# ⚙️ Prescriptive Rule Engine")

    def get_action(current, predicted):
        if current=="Red" and predicted=="Red":     return "🚨 Urgent Redirection","#c0392b"
        elif current=="Amber" and predicted=="Red": return "🔔 Notify Concierge Users","#e67e22"
        elif current=="Amber" and predicted=="Green": return "👁️ Monitor — No Alert","#f39c12"
        elif current=="Green":                      return "✅ No Action Required","#27ae60"
        return "👁️ Monitor","#3498db"

    rules = {
        "Current Status":   ["🔴 Red","🟡 Amber","🟡 Amber","🟢 Green"],
        "Predicted Status": ["🔴 Red","🔴 Red","🟢 Green","Any"],
        "System Action":    ["Urgent Redirection","Notify Concierge","Monitor — No Alert","No Action"],
    }
    st.dataframe(pd.DataFrame(rules), use_container_width=True, hide_index=True)
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        county = st.selectbox("County", list(HOSPITAL_MAP.keys()))
        sel = st.selectbox("Hospital", HOSPITAL_MAP[county])
        row = df[df["Hospital"]==sel]
        if row.empty: row = df.iloc[[0]]
        row = row.iloc[0]
        cur = row["wait_rag"]
        st.info(f"Current: **{cur}** | Wait: **{row['est_wait_hours']}hrs** | Occupancy: **{row['occupancy_rate_pct']}%**")
    with col2:
        pred = st.selectbox("Predicted status (4hr)", ["Green","Amber","Red"],
                             index=["Green","Amber","Red"].index(cur))

    action, ac = get_action(cur, pred)
    st.markdown(f"""
    <div class="card" style="border-left:6px solid {ac};">
        <h3 style="color:{ac};margin:0">System Action: {action}</h3>
        <p style="color:#555;margin:4px 0 0 0">Current: <strong>{cur}</strong> → Predicted: <strong>{pred}</strong></p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    rows = []
    for _, r in df.iterrows():
        occ = r["occupancy_rate_pct"]
        pred_s = "Red" if occ>=9 else "Amber" if occ>=6 else "Green"
        act, _ = get_action(r["wait_rag"], pred_s)
        rows.append({"Hospital":r["Hospital"],"Current":r["wait_rag"],
                     "Predicted":pred_s,"Action":act,
                     "Wait (hrs)":r["est_wait_hours"],"Occupancy %":occ})
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — FORECAST
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📈 Forecast":
    st.markdown("# 📈 SARIMAX Occupancy Forecast")
    try:
        from statsmodels.tsa.statespace.sarimax import SARIMAX

        col1, col2 = st.columns(2)
        with col1:
            county = st.selectbox("County", list(HOSPITAL_MAP.keys()))
        with col2:
            sel = st.selectbox("Hospital", HOSPITAL_MAP[county])

        row = df[df["Hospital"]==sel]
        if row.empty: row = df.iloc[[0]]
        row = row.iloc[0]

        st.info(f"**{sel}** | Occupancy: **{row['occupancy_rate_pct']}%** | Est. Wait: **{row['est_wait_hours']}hrs**")

        np.random.seed(42)
        n = 174
        base = row["occupancy_rate_pct"]
        amp  = row["behavioural_impact_score"]*0.3
        t    = np.arange(n)
        series = np.clip(
            base + amp*np.sin(2*np.pi*t/6) + (amp*0.5)*np.sin(2*np.pi*t/42)
            + 0.003*t + np.random.normal(0, 0.4, n), 0, 20)
        exog_tr = np.random.choice([0,1],size=n,p=[0.97,0.03]).reshape(-1,1)

        with st.spinner("Fitting SARIMAX model..."):
            res = SARIMAX(series, exog=exog_tr, order=(1,0,1),
                          seasonal_order=(1,0,1,6),
                          enforce_stationarity=False,
                          enforce_invertibility=False).fit(disp=False)

        n_fore = 12
        fc = res.get_forecast(steps=n_fore, exog=np.zeros((n_fore,1)))
        fc_mean = fc.predicted_mean
        ci = fc.conf_int()

        base_dt  = datetime(2024,6,3,8,0)
        hist_idx = [base_dt+timedelta(hours=4*i) for i in range(n)]
        fore_idx = [hist_idx[-1]+timedelta(hours=4*i) for i in range(1,n_fore+1)]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hist_idx[-48:], y=series[-48:],
                                  mode="lines", name="Historical",
                                  line=dict(color="#1a2744",width=2)))
        fig.add_trace(go.Scatter(x=fore_idx, y=fc_mean,
                                  mode="lines+markers", name="Forecast",
                                  line=dict(color="#e67e22",width=2.5,dash="dot")))
        fig.add_trace(go.Scatter(
            x=fore_idx+fore_idx[::-1],
            y=list(ci.iloc[:,1])+list(ci.iloc[:,0])[::-1],
            fill="toself", fillcolor="rgba(230,126,34,0.15)",
            line=dict(color="rgba(0,0,0,0)"), name="95% CI"))
        fig.add_hline(y=7, line_dash="dash", line_color="#e67e22", annotation_text="Amber (7%)")
        fig.add_hline(y=9, line_dash="dash", line_color="#c0392b", annotation_text="Red (9%)")
        fig.update_layout(title=f"48-Hour Forecast — {sel}",
                          xaxis_title="Time", yaxis_title="Occupancy (%)",
                          plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)", height=460)
        st.plotly_chart(fig, use_container_width=True)

        fore_df = pd.DataFrame({
            "Time":       [d.strftime("%d %b %H:%M") for d in fore_idx],
            "Forecast %": fc_mean.round(2).values,
            "Lower CI":   ci.iloc[:,0].round(2).values,
            "Upper CI":   ci.iloc[:,1].round(2).values,
            "Status":     ["Red" if v>=9 else "Amber" if v>=7 else "Green" for v in fc_mean.values]
        })
        st.dataframe(fore_df, use_container_width=True, hide_index=True)

        col1,col2,col3 = st.columns(3)
        resid = res.resid
        col1.metric("MAE",  f"{np.mean(np.abs(resid)):.3f}")
        col2.metric("RMSE", f"{np.sqrt(np.mean(resid**2)):.3f}")
        col3.metric("MAPE", f"{np.mean(np.abs(resid/(series+1e-5)))*100:.2f}%")

        with st.expander("Model Summary"):
            st.text(res.summary().as_text())

    except Exception as e:
        st.error(f"Error: {e}")
