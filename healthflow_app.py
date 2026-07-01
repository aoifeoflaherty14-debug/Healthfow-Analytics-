import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="HealthFlow | Live ED Status",
    page_icon="https://img.icons8.com/color/48/hospital.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
*{font-family:'Inter',sans-serif!important;box-sizing:border-box;}
.stApp{background:#f5f5f5;}
#MainMenu,footer,header{visibility:hidden;}
[data-testid="collapsedControl"]{display:none;}

/* Mobile-first responsive */
.block-container{padding:0 1rem 2rem 1rem!important;max-width:100%!important;}

/* Hero */
.hero{background:linear-gradient(135deg,#0D9488 0%,#0a7a70 60%,#0D2137 100%);
      padding:2rem 1.5rem;margin-bottom:1.5rem;}
.hero-title{font-size:22px;font-weight:700;color:white;margin-bottom:6px;line-height:1.3;}
.hero-sub{font-size:13px;color:rgba(255,255,255,0.85);margin-bottom:14px;line-height:1.5;}
.pill{display:inline-flex;align-items:center;gap:5px;
      background:rgba(255,255,255,0.15);border:1px solid rgba(255,255,255,0.25);
      color:white;padding:4px 10px;border-radius:20px;font-size:12px;font-weight:500;
      margin-right:6px;margin-bottom:6px;}

/* Nav */
.nav-bar{background:white;padding:12px 1rem;border-bottom:1px solid #E2E8F0;
         display:flex;align-items:center;gap:8px;overflow-x:auto;
         position:sticky;top:0;z-index:999;flex-wrap:wrap;}
.nav-logo{font-size:15px;font-weight:700;color:#0D2137;white-space:nowrap;margin-right:12px;}
.nav-logo span{color:#0D9488;}

/* Hospital card */
.hcard{background:white;border-radius:12px;padding:16px;border:1px solid #E2E8F0;
       box-shadow:0 1px 3px rgba(0,0,0,0.05);margin-bottom:12px;position:relative;
       width:100%;}
.hcard-name{font-size:14px;font-weight:700;color:#0D2137;margin-bottom:3px;padding-right:20px;line-height:1.3;}
.hcard-loc{font-size:11px;color:#64748B;margin-bottom:10px;}
.tdot{width:12px;height:12px;border-radius:50%;position:absolute;top:16px;right:16px;flex-shrink:0;}
.sbadge{display:block;padding:5px 10px;border-radius:6px;font-size:12px;
        font-weight:600;text-align:center;margin-bottom:10px;}
.s-red{background:#FEE2E2;color:#DC2626;}
.s-amber{background:#FEF9C3;color:#B45309;}
.s-green{background:#DCFCE7;color:#15803D;}
.stat-row{display:flex;justify-content:space-between;font-size:12px;margin-bottom:4px;}
.stat-lbl{color:#64748B;}.stat-val{font-weight:600;color:#0D2137;}
.cap-bg{height:5px;background:#E2E8F0;border-radius:10px;overflow:hidden;margin:6px 0 8px;}
.cap-fill{height:100%;border-radius:10px;}
.maps-btn{display:block;margin-top:10px;background:#0D9488;color:white;
          text-align:center;padding:8px 12px;border-radius:8px;
          font-size:12px;font-weight:600;text-decoration:none;width:100%;}

/* Section */
.sec-title{font-size:16px;font-weight:700;color:#0D2137;margin:1.2rem 0 0.8rem;}

/* Advice cards */
.advice-card{background:white;border-radius:12px;padding:16px;
             border:1px solid #E2E8F0;margin-bottom:12px;}
.rec-card{background:white;border-radius:12px;padding:18px;
          border:1px solid #E2E8F0;box-shadow:0 2px 6px rgba(0,0,0,0.06);margin-top:14px;}
.ins-card{background:white;border-radius:10px;padding:12px 14px;
          border:1.5px solid #E2E8F0;margin-bottom:8px;}
.update-card{background:#FFFBEB;border:1px solid #FDE68A;border-radius:12px;
             padding:16px;margin-bottom:12px;}
.uvc-card{background:linear-gradient(135deg,#0D9488,#0f766e);
          border-radius:12px;padding:16px;margin-bottom:12px;color:white;}
.important-badge{background:#F59E0B;color:white;font-size:10px;font-weight:700;
                 padding:2px 7px;border-radius:4px;display:inline-block;margin-bottom:8px;}
.crit-box{background:#FFF1F2;border:1px solid #FECDD3;border-radius:12px;padding:16px;margin-bottom:12px;}
.crit-badge{background:#DC2626;color:white;font-size:10px;font-weight:700;
            padding:3px 8px;border-radius:4px;}
.crit-item{background:white;border:1px solid #FECDD3;border-radius:8px;
           padding:10px;margin-top:8px;display:flex;gap:10px;}
.crit-num{color:#DC2626;font-weight:700;font-size:12px;flex-shrink:0;}
.crit-name{font-size:12px;font-weight:600;color:#0D2137;}
.crit-sub{font-size:11px;color:#64748B;}

/* Resources */
.resource-card{background:white;border-radius:12px;padding:16px;
               border:1px solid #E2E8F0;margin-bottom:12px;}
.resource-title{font-size:14px;font-weight:700;color:#0D2137;margin-bottom:6px;}
.resource-desc{font-size:12px;color:#64748B;line-height:1.5;margin-bottom:8px;}
.resource-link{color:#0D9488;font-size:12px;font-weight:600;text-decoration:none;}

/* Contact */
.contact-card{background:white;border-radius:12px;padding:16px;
              border:1px solid #E2E8F0;margin-bottom:12px;text-align:center;}
.contact-num{font-size:20px;font-weight:700;color:#DC2626;}
.call999-bar{background:#DC2626;padding:16px;border-radius:12px;
             margin-bottom:16px;text-align:center;}

/* Footer */
.footer{background:#0D2137;padding:1.5rem;margin-top:2rem;border-radius:12px;
        font-size:12px;color:#94A3B8;text-align:center;line-height:1.8;}

/* Streamlit overrides */
.stSelectbox label,.stTextInput label{font-weight:600;color:#374151;font-size:13px!important;}
.stRadio label{font-size:13px!important;}
div[data-testid="stRadio"] > label{font-weight:600;color:#374151;}
.stButton button{border-radius:8px!important;font-weight:600!important;font-size:13px!important;}
details summary{list-style:none!important;}
details summary::-webkit-details-marker{display:none!important;}

@media(max-width:768px){
    .hero-title{font-size:18px;}
    .hero{padding:1.5rem 1rem;}
    .hcard-name{font-size:13px;}
    .nav-logo{font-size:13px;}
}
</style>
""", unsafe_allow_html=True)

# ── Hospital map ──────────────────────────────────────────────────────────────
HOSPITAL_MAP = {
    "Dublin":      ["Mater Misericordiae University Hospital","St. James's Hospital",
                    "St. Vincent's University Hospital","Beaumont Hospital",
                    "Tallaght University Hospital","Connolly Hospital Blanchardstown",
                    "Naas General Hospital","CHI at Temple Street","CHI at Crumlin","CHI at Tallaght"],
    "Cork":        ["Cork University Hospital","Mercy University Hospital"],
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

GOOGLE_MAPS = {
    "Mater Misericordiae University Hospital": "https://maps.google.com/?q=Mater+Misericordiae+University+Hospital+Dublin",
    "St. James's Hospital":                    "https://maps.google.com/?q=St+James+Hospital+Dublin",
    "St. Vincent's University Hospital":       "https://maps.google.com/?q=St+Vincents+University+Hospital+Dublin",
    "Beaumont Hospital":                        "https://maps.google.com/?q=Beaumont+Hospital+Dublin",
    "Tallaght University Hospital":             "https://maps.google.com/?q=Tallaght+University+Hospital+Dublin",
    "Connolly Hospital Blanchardstown":         "https://maps.google.com/?q=Connolly+Hospital+Blanchardstown",
    "Naas General Hospital":                    "https://maps.google.com/?q=Naas+General+Hospital+Kildare",
    "CHI at Temple Street":                     "https://maps.google.com/?q=Childrens+Health+Ireland+Temple+Street+Dublin",
    "CHI at Crumlin":                           "https://maps.google.com/?q=Childrens+Health+Ireland+Crumlin+Dublin",
    "CHI at Tallaght":                          "https://maps.google.com/?q=Childrens+Health+Ireland+Tallaght+Dublin",
    "Cork University Hospital":                 "https://maps.google.com/?q=Cork+University+Hospital",
    "Mercy University Hospital":                "https://maps.google.com/?q=Mercy+University+Hospital+Cork",
    "University Hospital Kerry":                "https://maps.google.com/?q=University+Hospital+Kerry+Tralee",
    "University Hospital Limerick":             "https://maps.google.com/?q=University+Hospital+Limerick",
    "Galway University Hospitals":              "https://maps.google.com/?q=Galway+University+Hospital",
    "Mayo University Hospital":                 "https://maps.google.com/?q=Mayo+University+Hospital+Castlebar",
    "Sligo University Hospital":                "https://maps.google.com/?q=Sligo+University+Hospital",
    "Letterkenny University Hospital":          "https://maps.google.com/?q=Letterkenny+University+Hospital+Donegal",
    "UH Waterford":                             "https://maps.google.com/?q=University+Hospital+Waterford",
    "Wexford General Hospital":                 "https://maps.google.com/?q=Wexford+General+Hospital",
    "St Luke's General Hospital Kilkenny":      "https://maps.google.com/?q=St+Lukes+General+Hospital+Kilkenny",
    "Tipperary University Hospital":            "https://maps.google.com/?q=Tipperary+University+Hospital+Clonmel",
    "Our Lady of Lourdes Hospital":             "https://maps.google.com/?q=Our+Lady+of+Lourdes+Hospital+Drogheda",
    "Our Lady's Hospital Navan":                "https://maps.google.com/?q=Our+Ladys+Hospital+Navan",
    "Cavan General Hospital":                   "https://maps.google.com/?q=Cavan+General+Hospital",
    "Midland Regional Hospital Portlaoise":     "https://maps.google.com/?q=Midland+Regional+Hospital+Portlaoise",
    "Midland Regional Hospital Tullamore":      "https://maps.google.com/?q=Midland+Regional+Hospital+Tullamore",
    "Midland Regional Hospital Mullingar":      "https://maps.google.com/?q=Midland+Regional+Hospital+Mullingar",
    "Portiuncula University Hospital":          "https://maps.google.com/?q=Portiuncula+University+Hospital+Ballinasloe",
}

CM = {"Green":"#16A34A","Amber":"#D97706","Red":"#DC2626"}

def rag_meta(status):
    if status == "Red":   return "#DC2626","s-red","Very Busy"
    if status == "Amber": return "#D97706","s-amber","Busy"
    return "#16A34A","s-green","Normal"

def get_hospitals_for_age(county, age):
    all_hosps = HOSPITAL_MAP.get(county, [])
    if "Under 5" in age or "5–15" in age:
        chi = [h for h in all_hosps if "CHI" in h]
        others = [h for h in all_hosps if "CHI" not in h]
        note = "Children's Health Ireland (CHI) hospitals are specifically equipped for paediatric emergencies. CHI hospitals are listed first."
        return chi + others, note
    elif "65+" in age:
        note = "All hospitals listed. Ask about the FITT (Frailty Intervention Therapy Team) service when you arrive."
        return all_hosps, note
    return all_hosps, None

def get_pathway(occ, urgency_type):
    if urgency_type == "life":
        return "Call 999 / A&E", "#DC2626", "Call 999 immediately or go directly to your nearest A&E. Do not drive yourself."
    elif urgency_type == "moderate":
        if occ >= 9:
            return "A&E", "#DC2626", "Your condition requires A&E. Consider an alternative hospital if one is less busy."
        return "Minor Injury Unit / Urgent Virtual Care", "#D97706", "A Minor Injury Unit or Urgent Virtual Care (UVC) video consultation is recommended for same-day care."
    return "GP / Out-of-Hours / Pharmacy", "#16A34A", "A GP appointment, out-of-hours service, or pharmacist can help with your condition."

@st.cache_data
def load_master():
    df = pd.read_csv("master_table.csv", encoding="latin-1")
    df.columns = df.columns.str.strip()
    df["Hospital"] = df["Hospital"].str.replace("\x92","'").str.replace("\x93",'"').str.replace("\x94",'"')
    df = df.dropna(subset=["Hospital"])
    df["Occupancy_Rate_pct"] = pd.to_numeric(df["Occupancy_Rate_pct"], errors="coerce")
    df["Traffic_Light_Status"] = df.apply(
        lambda r: r["Traffic_Light_Status"] if r["Traffic_Light_Status"] not in ["Unknown",""]
        else ("Red" if r["Occupancy_Rate_pct"]>=8 else ("Amber" if r["Occupancy_Rate_pct"]>=4 else "Green"))
        if pd.notna(r["Occupancy_Rate_pct"]) else "Green", axis=1)
    df["Behavioural_Impact_Score"] = pd.to_numeric(df["Behavioural_Impact_Score"], errors="coerce").fillna(0)
    for col in ["Daily_ED_Trolleys","Daily_Ward_Trolleys","Daily_Total"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    return df

@st.cache_data
def load_synthetic():
    df = pd.read_csv("synthetic_dataset.csv", encoding="latin-1")
    df["date"] = pd.to_datetime(df["date"], format="mixed")
    df["occupancy_rate_pct"] = pd.to_numeric(df["occupancy_rate_pct"], errors="coerce").fillna(0)
    return df

master    = load_master()
synthetic = load_synthetic()
latest_syn = synthetic.sort_values("date").groupby("Hospital").last().reset_index()

def get_hosp_data(hospital_name):
    row = master[master["Hospital"].str.lower().str.contains(hospital_name.lower().split()[0], na=False)]
    if not row.empty:
        r = row.iloc[0]
        occ    = r["Occupancy_Rate_pct"] if pd.notna(r["Occupancy_Rate_pct"]) else 5.0
        status = r["Traffic_Light_Status"]
        troll  = int(r["Daily_Total"]) if pd.notna(r["Daily_Total"]) else 0
        bis    = r["Behavioural_Impact_Score"]
        return occ, status, troll, bis
    row2 = latest_syn[latest_syn["Hospital"].str.lower().str.contains(hospital_name.lower().split()[0], na=False)]
    if not row2.empty:
        r2     = row2.iloc[0]
        occ    = r2["occupancy_rate_pct"]
        status = r2["traffic_light_status"]
        troll  = int(r2["total_trolleys"]) if pd.notna(r2.get("total_trolleys", 0)) else 0
        bis    = float(r2.get("behavioural_impact_score", 0))
        return occ, status, troll, bis
    return 5.0, "Green", 0, 0.0

red_c = int((latest_syn["traffic_light_status"]=="Red").sum())
amb_c = int((latest_syn["traffic_light_status"]=="Amber").sum())
grn_c = int((latest_syn["traffic_light_status"]=="Green").sum())

# ── Session state ─────────────────────────────────────────────────────────────
if "onboarded" not in st.session_state:
    st.session_state.onboarded = False
if "page" not in st.session_state:
    st.session_state.page = "ED Status"
if "show_change" not in st.session_state:
    st.session_state.show_change = False

# ── Landing page ──────────────────────────────────────────────────────────────
if not st.session_state.onboarded:
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0D9488 0%,#0a7a70 60%,#0D2137 100%);
                padding:3rem 1.5rem 2rem 1.5rem;text-align:center;">
        <div style="background:rgba(255,255,255,0.2);width:56px;height:56px;border-radius:14px;
                    display:flex;align-items:center;justify-content:center;
                    font-size:26px;margin:0 auto 14px auto">H</div>
        <div style="font-size:24px;font-weight:700;color:white;margin-bottom:8px">Welcome to HealthFlow</div>
        <div style="font-size:13px;color:rgba(255,255,255,0.88);line-height:1.6">
            Find the right care, right now — across Ireland's HSE hospitals
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;font-size:17px;font-weight:700;color:#0D2137;margin:1.5rem 0 4px 0">
        Tell us about yourself to get started
    </div>
    <div style="text-align:center;font-size:13px;color:#64748B;margin-bottom:1.2rem">
        We will personalise your experience based on your location and age
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([0.5, 3, 0.5])
    with col2:
        county_land = st.selectbox("Which county are you in?", list(HOSPITAL_MAP.keys()))
        age_opts = ["Under 5 — Infant / Toddler","5–15 — Child",
                    "16–25 — Young Adult","26–64 — Adult","65+ — Senior"]
        age_land = st.selectbox("What is the patient's age group?", age_opts, index=3)
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        if st.button("Find My Care", type="primary", use_container_width=True):
            st.session_state.onboarded      = True
            st.session_state.landing_county = county_land
            st.session_state.landing_age    = age_land
            st.session_state.page           = "ED Status"
            st.rerun()

    st.markdown("""
    <div style="text-align:center;margin-top:1.5rem;font-size:11px;color:#94A3B8">
        No personal data is stored &nbsp;|&nbsp; HSE Ireland &nbsp;|&nbsp; Emergency? Call 999
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Top nav ───────────────────────────────────────────────────────────────────
pages = ["ED Status", "Patient Advice", "Resources", "Contact"]

col_logo, col_n1, col_n2, col_n3, col_n4, col_999 = st.columns([2,1,1.2,1,1,1.5])
with col_logo:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:8px;padding:4px 0">
        <div style="background:#0D9488;color:white;width:30px;height:30px;border-radius:8px;
                    display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px;flex-shrink:0">H</div>
        <div style="font-weight:700;color:#0D2137;font-size:14px;line-height:1.1">
            Health<span style="color:#0D9488">Flow</span>
        </div>
    </div>""", unsafe_allow_html=True)
with col_n1:
    if st.button("ED Status",      use_container_width=True): st.session_state.page="ED Status";      st.rerun()
with col_n2:
    if st.button("Patient Advice", use_container_width=True): st.session_state.page="Patient Advice"; st.rerun()
with col_n3:
    if st.button("Resources",      use_container_width=True): st.session_state.page="Resources";      st.rerun()
with col_n4:
    if st.button("Contact",        use_container_width=True): st.session_state.page="Contact";        st.rerun()
with col_999:
    st.markdown("""
    <div style="text-align:right;padding-top:2px">
        <a href="tel:999" style="background:#DC2626;color:white;padding:6px 14px;
           border-radius:20px;font-weight:700;font-size:13px;text-decoration:none">Call 999</a>
    </div>""", unsafe_allow_html=True)

st.markdown("<hr style='margin:4px 0 8px 0;border:none;border-top:1px solid #E2E8F0'>", unsafe_allow_html=True)

page = st.session_state.page
sel_county = st.session_state.get("landing_county", list(HOSPITAL_MAP.keys())[0])
sel_age    = st.session_state.get("landing_age", "26–64 — Adult")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — ED STATUS
# ══════════════════════════════════════════════════════════════════════════════
if page == "ED Status":
    age_hospitals, age_note = get_hospitals_for_age(sel_county, sel_age)

    st.markdown(f"""
    <div class="hero">
        <div class="hero-title">Your Hospitals in {sel_county}</div>
        <div class="hero-sub">Showing hospitals for <strong>{sel_age}</strong> patients</div>
        <div>
            <span class="pill">Normal: {grn_c}</span>
            <span class="pill">Busy: {amb_c}</span>
            <span class="pill">Very Busy: {red_c}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if age_note:
        st.info(age_note)

    # Change button
    if st.button("Change Location or Age Group", use_container_width=False):
        st.session_state.show_change = not st.session_state.show_change
    if st.session_state.show_change:
        col1, col2 = st.columns(2)
        with col1:
            new_county = st.selectbox("County", list(HOSPITAL_MAP.keys()),
                                       index=list(HOSPITAL_MAP.keys()).index(sel_county), key="mh_county")
        with col2:
            age_opt_list = ["Under 5 — Infant / Toddler","5–15 — Child",
                            "16–25 — Young Adult","26–64 — Adult","65+ — Senior"]
            new_age = st.selectbox("Age group", age_opt_list,
                                    index=age_opt_list.index(sel_age) if sel_age in age_opt_list else 3,
                                    key="mh_age")
        if st.button("Update", type="primary", key="mh_update"):
            st.session_state.landing_county = new_county
            st.session_state.landing_age    = new_age
            st.session_state.show_change    = False
            st.rerun()

    # Refresh after update
    sel_county = st.session_state.get("landing_county", sel_county)
    sel_age    = st.session_state.get("landing_age", sel_age)
    age_hospitals, age_note = get_hospitals_for_age(sel_county, sel_age)

    # Search
    search = st.text_input("", placeholder="Search hospitals...", label_visibility="collapsed")
    if search:
        age_hospitals = [h for h in age_hospitals if search.lower() in h.lower()]

    st.markdown(f"<div style='color:#64748B;font-size:12px;margin-bottom:10px'>Showing <strong>{len(age_hospitals)}</strong> hospitals</div>", unsafe_allow_html=True)

    cols = st.columns(2)
    for i, hosp in enumerate(age_hospitals):
        occ, status, troll, bis = get_hosp_data(hosp)
        rc, sc, rl = rag_meta(status)
        dot_col = {"Red":"#DC2626","Amber":"#D97706","Green":"#16A34A"}.get(status,"#94A3B8")
        cap_pct = min(int(occ*10), 100)
        cap_col = "#DC2626" if occ>=8 else "#D97706" if occ>=4 else "#16A34A"
        is_chi  = "CHI" in hosp
        badge   = "Children's" if is_chi else "Public"
        maps_url = GOOGLE_MAPS.get(hosp, f"https://maps.google.com/?q={hosp.replace(' ','+')}+Ireland")
        with cols[i % 2]:
            st.markdown(f"""
            <div class="hcard">
                <div class="tdot" style="background:{dot_col}"></div>
                <div class="hcard-name">{hosp}</div>
                <div class="hcard-loc">{sel_county} &nbsp;
                    <span style="background:#EFF6FF;color:#2563EB;font-size:10px;font-weight:600;
                                 padding:2px 6px;border-radius:4px">{badge}</span>
                </div>
                <span class="sbadge {sc}">{rl}</span>
                <div class="stat-row"><span class="stat-lbl">Occupancy</span><span class="stat-val">{occ:.1f}%</span></div>
                <div class="stat-row"><span class="stat-lbl">Daily Trolleys</span><span class="stat-val">{troll}</span></div>
                <div class="stat-row"><span class="stat-lbl">BIS</span><span class="stat-val">{bis:.1f}</span></div>
                <div class="cap-bg"><div class="cap-fill" style="width:{cap_pct}%;background:{cap_col}"></div></div>
                <a href="{maps_url}" target="_blank" class="maps-btn">Get Directions</a>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    if st.button("Get personalised care recommendation", type="primary", use_container_width=True):
        st.session_state.page = "Patient Advice"
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — PATIENT ADVICE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Patient Advice":
    st.markdown("""
    <div class="hero">
        <div class="hero-title">Patient Advice & Emergency Guidelines</div>
        <div class="hero-sub">Important information to help you decide when and where to seek medical care</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="update-card">
        <span class="important-badge">Important Update</span>
        <span style="font-size:11px;color:#6b7280;margin-left:8px">June 2025</span>
        <div style="background:white;border-radius:8px;padding:12px;font-size:13px;
                    color:#374151;line-height:1.7;margin-top:8px">
            Over the next <strong>1–4 weeks</strong> we expect ED attendances to increase by
            <strong style="color:#F59E0B">15–20%</strong> based on seasonal trends.
            We strongly advise people to <strong>only attend A&E if very necessary</strong>
            and if advised by their GP.
        </div>
    </div>
    <div class="uvc-card">
        <div style="font-size:14px;font-weight:700;margin-bottom:6px">Urgent Virtual Care Success</div>
        <div style="font-size:12px;opacity:0.9;line-height:1.6">
            Our Urgent Virtual Care service has managed over <strong>8,450 cases</strong>
            this month without ED visits, reducing wait times for critical cases.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-title">Get Your Personalised Recommendation</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        county_idx = list(HOSPITAL_MAP.keys()).index(sel_county) if sel_county in HOSPITAL_MAP else 0
        county_pa  = st.selectbox("County / City", list(HOSPITAL_MAP.keys()), index=county_idx, key="pa_c")
        sel_hosp   = st.selectbox("Nearest hospital", HOSPITAL_MAP[county_pa], key="pa_h")
        age_opt_list = ["Under 5 — Infant / Toddler","5–15 — Child",
                        "16–25 — Young Adult","26–64 — Adult","65+ — Senior"]
        age_idx    = age_opt_list.index(sel_age) if sel_age in age_opt_list else 3
        patient_age = st.selectbox("Patient age group", age_opt_list, index=age_idx, key="pa_age")
    with col2:
        st.markdown("""
        <div class="ins-card">
            <div style="font-weight:600;color:#0D9488;margin-bottom:4px">Public HSE Patient</div>
            <div style="font-size:12px;color:#6b7280">
                A&E visits are free with a valid GP referral letter. No insurance required.
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div style="color:#0D9488;font-size:11px;font-weight:700;letter-spacing:0.06em;margin:14px 0 4px 0">STEP 2 OF 2</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:16px;font-weight:700;color:#0D2137;margin-bottom:6px">Why are you considering attending A&E?</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:13px;color:#64748B;margin-bottom:12px">Select the option that best describes your situation.</div>', unsafe_allow_html=True)

    URGENCY_OPTIONS = [
        ("Chest pain or breathing difficulty",     "Tightness, pressure, shortness of breath",      "life"),
        ("Stroke symptoms",                        "Face drooping, arm weakness, speech difficulty", "life"),
        ("Severe injury or uncontrolled bleeding", "Major trauma, deep wound, broken bones",         "life"),
        ("Collapsed, unconscious, or seizure",     "Loss of consciousness, fitting",                 "life"),
        ("Moderate illness – needs same-day care", "Infection, fever, moderate pain",                "moderate"),
        ("Minor – can wait or self-manage",        "Cold, rash, prescription renewal, UTI",          "minor"),
    ]

    sel_urg = st.radio("", [ti for ti,_,_ in URGENCY_OPTIONS], label_visibility="collapsed")
    urgency_type = "minor"
    for ti, sub, ut in URGENCY_OPTIONS:
        if ti == sel_urg:
            urgency_type = ut
            st.caption(f"_{sub}_")
            break

    occ, status, troll, bis = get_hosp_data(sel_hosp)
    rc, sc, rl = rag_meta(status)
    pathway, path_c, path_desc = get_pathway(occ, urgency_type)

    st.markdown(f"""
    <div class="rec-card" style="border-left:5px solid {path_c}">
        <div style="color:{path_c};font-size:11px;font-weight:700;margin-bottom:6px;letter-spacing:0.05em">
            RECOMMENDED CARE PATHWAY
        </div>
        <div style="font-size:18px;font-weight:700;color:{path_c}">{pathway}</div>
        <div style="font-size:13px;color:#374151;margin-top:10px;line-height:1.7">{path_desc}</div>
        <div style="margin-top:12px;padding-top:10px;border-top:1px solid #F1F5F9;font-size:11px;color:#94A3B8">
            {sel_hosp} &nbsp;|&nbsp;
            Status: <strong style="color:{rc}">{rl}</strong> &nbsp;|&nbsp;
            Occupancy: <strong>{occ:.1f}%</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if urgency_type == "life":
        st.error("Call 999 immediately. Do not drive yourself to hospital.")
    elif status == "Red":
        st.warning(f"{sel_hosp} is very busy. Consider an alternative if your condition allows.")
        alt = [h for h in HOSPITAL_MAP.get(county_pa,[]) if h != sel_hosp]
        for h in alt[:2]:
            o2,s2,_,_ = get_hosp_data(h)
            _,_,rl2 = rag_meta(s2)
            st.markdown(f"- **{h}** — {rl2}")

    st.markdown("""
    <div class="crit-box">
        <span class="crit-badge">Critical Symptoms — Call 999 Immediately</span>
        <div class="crit-item"><span class="crit-num">1</span><div><div class="crit-name">Chest Pain</div><div class="crit-sub">Crushing chest pain, left arm pain, sweating</div></div></div>
        <div class="crit-item"><span class="crit-num">2</span><div><div class="crit-name">Stroke</div><div class="crit-sub">FAST — Face, Arms, Speech, Time to call 999</div></div></div>
        <div class="crit-item"><span class="crit-num">3</span><div><div class="crit-name">Severe Breathing Difficulty</div><div class="crit-sub">Unable to speak in full sentences</div></div></div>
        <div class="crit-item"><span class="crit-num">4</span><div><div class="crit-name">Loss of Consciousness</div><div class="crit-sub">Collapsed, unresponsive, or seizure</div></div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-title">Concierge Notification</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:13px;color:#64748B;margin-bottom:10px">Register to be notified when wait times drop at your preferred hospital.</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([3,1])
    with col1:
        email = st.text_input("", placeholder="Your email address", label_visibility="collapsed")
    with col2:
        if st.button("Notify me", type="primary", use_container_width=True):
            if email:
                st.success(f"You will be notified at {email} when wait times improve at {sel_hosp}.")
            else:
                st.warning("Please enter your email.")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — RESOURCES
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Resources":
    st.markdown("""
    <div class="hero">
        <div class="hero-title">Healthcare Resources</div>
        <div class="hero-sub">Useful information and links to help you navigate the Irish healthcare system</div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec-title">Care Pathway Options</div>', unsafe_allow_html=True)
    pathways = [
        ("Pharmacy","For minor self-limiting conditions — UTIs, cold sores, hay fever, contraception. No appointment needed.","https://www.hse.ie/eng/health/az/p/pharmacy-services/"),
        ("GP / Family Doctor","For non-emergency conditions requiring diagnosis or prescription. Contact your GP during office hours.","https://www.hse.ie/eng/services/list/3/primarycare/"),
        ("GP Out-of-Hours","When your GP is closed. ShanDoc: 1850 777 911. Available evenings, weekends, and bank holidays.","https://www.hse.ie/eng/services/list/3/primarycare/outofhours.html"),
        ("Minor Injury Unit","For sprains, minor fractures, cuts, and burns that are not life-threatening. No GP referral needed.","https://www.hse.ie/eng/services/list/3/acutehospitals/"),
        ("Urgent Virtual Care (UVC)","Video consultation with a doctor or nurse. Available 24/7. Suitable for moderate non-emergency conditions.","https://www.hse.ie/eng/"),
        ("A&E / Emergency Department","For life-threatening emergencies only. If in doubt, call 999 first.","https://www.hse.ie/eng/services/list/3/acutehospitals/"),
    ]
    for title, desc, link in pathways:
        st.markdown(f"""
        <div class="resource-card">
            <div class="resource-title">{title}</div>
            <div class="resource-desc">{desc}</div>
            <a href="{link}" target="_blank" class="resource-link">Learn more on HSE.ie</a>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="sec-title">Mental Health Support</div>', unsafe_allow_html=True)
    supports = [
        ("Samaritans","24/7 emotional support for anyone in distress","116 123 (Free)","tel:116123"),
        ("Pieta House","Free therapy for those experiencing suicidal distress or self-harm","1800 247 247","tel:1800247247"),
        ("Text 50808","24/7 anonymous text-based mental health support","Text HELLO to 50808","sms:50808"),
        ("HSE Mental Health","Information and services for mental health in Ireland","hse.ie","https://www.hse.ie/eng/services/list/4/mental-health-services/"),
    ]
    for title, desc, contact, link in supports:
        st.markdown(f"""
        <div class="resource-card">
            <div class="resource-title">{title}</div>
            <div class="resource-desc">{desc}</div>
            <a href="{link}" class="resource-link">{contact}</a>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — CONTACT
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Contact":
    st.markdown("""
    <div class="hero">
        <div class="hero-title">Contact & Emergency Numbers</div>
        <div class="hero-sub">Important contacts for healthcare services across Ireland</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="call999-bar">
        <div style="font-size:13px;color:rgba(255,255,255,0.85);margin-bottom:4px">Life-threatening emergency</div>
        <div style="font-size:28px;font-weight:700;color:white">Call 999</div>
        <div style="font-size:12px;color:rgba(255,255,255,0.75);margin-top:4px">Do not delay if you experience life-threatening symptoms</div>
    </div>
    """, unsafe_allow_html=True)

    contacts = [
        ("GP Services",        "Contact your GP during office hours for non-emergency medical advice.", "Mon–Fri: 9:00 AM – 5:00 PM", None),
        ("ShanDoc Out-of-Hours","GP out-of-hours service when your practice is closed.",                "1850 777 911",               "tel:1850777911"),
        ("HSE Live",           "Health information and signposting to services.",                       "1850 24 1850",               "tel:1850241850"),
        ("Minor Injury Units", "For minor injuries without appointment. Check local opening hours.",    "hse.ie",                     "https://www.hse.ie"),
        ("Samaritans",         "24/7 emotional support.",                                               "116 123",                    "tel:116123"),
        ("Pieta House",        "Support for suicidal distress and self-harm.",                          "1800 247 247",               "tel:1800247247"),
    ]

    for title, desc, contact, link in contacts:
        link_html = f'<a href="{link}" style="display:block;margin-top:8px;background:#0D9488;color:white;text-align:center;padding:8px;border-radius:8px;font-size:13px;font-weight:600;text-decoration:none">{contact}</a>' if link else f'<div style="margin-top:6px;font-size:12px;color:#64748B">{contact}</div>'
        st.markdown(f"""
        <div class="contact-card" style="text-align:left">
            <div class="resource-title">{title}</div>
            <div class="resource-desc">{desc}</div>
            {link_html}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
        HealthFlow &nbsp;|&nbsp; Group 2 &nbsp;|&nbsp; UCC IS6611 &nbsp;|&nbsp; 2026<br>
        This platform is for informational purposes only and does not replace professional medical advice.
    </div>
    """, unsafe_allow_html=True)
