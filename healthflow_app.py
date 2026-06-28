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
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
*{font-family:'Inter',sans-serif!important;}
.stApp{background:#f5f5f5;}
#MainMenu,footer,header{visibility:hidden;}
[data-testid="collapsedControl"]{display:none;}
.hero{background:linear-gradient(135deg,#0D9488 0%,#0a7a70 60%,#0D2137 100%);
      padding:2.5rem 2rem;margin-bottom:1.5rem;border-radius:0 0 16px 16px;}
.hero-title{font-size:26px;font-weight:700;color:white;margin-bottom:6px;}
.hero-sub{font-size:14px;color:rgba(255,255,255,0.85);margin-bottom:16px;}
.pill{display:inline-flex;align-items:center;gap:6px;
      background:rgba(255,255,255,0.15);border:1px solid rgba(255,255,255,0.25);
      color:white;padding:5px 14px;border-radius:20px;font-size:13px;font-weight:500;margin-right:8px;}
.hcard{background:white;border-radius:12px;padding:20px;border:1px solid #E2E8F0;
       box-shadow:0 1px 3px rgba(0,0,0,0.05);margin-bottom:12px;position:relative;}
.hcard-name{font-size:15px;font-weight:600;color:#0D2137;margin-bottom:4px;padding-right:24px;}
.hcard-loc{font-size:12px;color:#64748B;margin-bottom:12px;}
.tdot{width:14px;height:14px;border-radius:50%;position:absolute;top:20px;right:20px;}
.sbadge{display:block;padding:5px 12px;border-radius:6px;font-size:12px;
        font-weight:600;text-align:center;margin-bottom:12px;}
.s-red{background:#FEE2E2;color:#DC2626;}
.s-amber{background:#FEF9C3;color:#B45309;}
.s-green{background:#DCFCE7;color:#15803D;}
.stat-row{display:flex;justify-content:space-between;font-size:12px;margin-bottom:5px;}
.stat-lbl{color:#64748B;}.stat-val{font-weight:600;color:#0D2137;}
.cap-bg{height:6px;background:#E2E8F0;border-radius:10px;overflow:hidden;margin:6px 0 10px;}
.cap-fill{height:100%;border-radius:10px;}
.card-ft{display:flex;justify-content:space-between;font-size:11px;color:#94A3B8;
         border-top:1px solid #F1F5F9;padding-top:8px;margin-top:4px;}
.sec-title{font-size:17px;font-weight:600;color:#0D2137;margin:1.5rem 0 1rem;}
.uvc-box{background:linear-gradient(135deg,#0D9488,#0a7a70);border-radius:12px;
         padding:24px;color:white;margin-bottom:1.5rem;}
.uvc-stats{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px;}
.uvc-stat{background:rgba(0,0,0,0.2);border-radius:8px;padding:14px;}
.uvc-stat-lbl{font-size:12px;opacity:0.8;margin-bottom:4px;}
.uvc-stat-val{font-size:20px;font-weight:700;}
.updates-box{background:#FFFBEB;border:1px solid #FDE68A;border-radius:12px;
             padding:20px 24px;margin-bottom:1.5rem;}
.upd-badge{background:#F59E0B;color:white;font-size:11px;font-weight:600;
           padding:3px 8px;border-radius:4px;}
.call999-bar{background:#DC2626;padding:20px 2rem;display:flex;
             align-items:center;justify-content:space-between;
             margin-bottom:1.5rem;border-radius:12px;}
.call999-num{font-size:28px;font-weight:700;color:white;}
.step-card{background:white;border:1px solid #E2E8F0;border-radius:12px;
           padding:20px;text-align:center;}
.step-icon{width:48px;height:48px;border-radius:50%;display:flex;
           align-items:center;justify-content:center;font-size:20px;margin:0 auto 12px;}
.step-title{font-size:15px;font-weight:700;color:#0D2137;margin-bottom:6px;}
.step-desc{font-size:12px;color:#64748B;line-height:1.4;}
.crit-box{background:#FFF1F2;border:1px solid #FECDD3;border-radius:12px;
          padding:24px;margin-bottom:1.5rem;}
.crit-badge{background:#DC2626;color:white;font-size:11px;font-weight:700;
            padding:4px 10px;border-radius:4px;}
.crit-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:16px;}
.crit-item{background:white;border:1px solid #FECDD3;border-radius:8px;
           padding:12px;display:flex;gap:10px;}
.crit-num{color:#DC2626;font-weight:700;font-size:13px;flex-shrink:0;}
.crit-name{font-size:13px;font-weight:600;color:#0D2137;}
.crit-sub{font-size:11px;color:#64748B;}
.ins-card{background:white;border-radius:10px;padding:14px 16px;
          border:1.5px solid #E2E8F0;margin-bottom:8px;}
.rec-card{background:white;border-radius:14px;padding:24px;
          border:1px solid #E2E8F0;box-shadow:0 2px 8px rgba(0,0,0,0.06);margin-top:16px;}
.footer-bar{background:#0D2137;padding:2rem;margin-top:2rem;border-radius:12px;}
.footer-title{font-size:14px;font-weight:600;color:white;margin-bottom:10px;}
.footer-item{font-size:13px;color:#94A3B8;margin-bottom:4px;}
.footer-bottom{text-align:center;font-size:12px;color:#64748B;
               margin-top:1.5rem;padding-top:1rem;border-top:1px solid #1e3a5f;}
.stSelectbox label,.stTextInput label{font-weight:600;color:#374151;font-size:0.88rem;}
.streamlit-expanderHeader{padding-left:12px!important;font-size:14px!important;font-weight:600!important;} summary svg{display:none!important;} [aria-label="arrow"]{display:none!important;}
details summary{padding:10px 14px!important;} [data-testid="stCheckbox"] label span:first-child{display:none!important;}
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

# ── Google Maps links ─────────────────────────────────────────────────────────
MAPS = {
    "Mater Misericordiae University Hospital": "https://maps.google.com/?q=Mater+Misericordiae+University+Hospital+Dublin",
    "St. James's Hospital": "https://maps.google.com/?q=St+James%27s+Hospital+Dublin",
    "St. Vincent's University Hospital": "https://maps.google.com/?q=St+Vincent%27s+University+Hospital+Dublin",
    "Beaumont Hospital": "https://maps.google.com/?q=Beaumont+Hospital+Dublin",
    "Tallaght University Hospital": "https://maps.google.com/?q=Tallaght+University+Hospital+Dublin",
    "Connolly Hospital Blanchardstown": "https://maps.google.com/?q=Connolly+Hospital+Blanchardstown+Dublin",
    "Naas General Hospital": "https://maps.google.com/?q=Naas+General+Hospital+Kildare",
    "CHI at Temple Street": "https://maps.google.com/?q=Children%27s+Health+Ireland+Temple+Street+Dublin",
    "CHI at Crumlin": "https://maps.google.com/?q=Children%27s+Health+Ireland+Crumlin+Dublin",
    "CHI at Tallaght": "https://maps.google.com/?q=Children%27s+Health+Ireland+Tallaght+Dublin",
    "Cork University Hospital": "https://maps.google.com/?q=Cork+University+Hospital",
    "Mercy University Hospital": "https://maps.google.com/?q=Mercy+University+Hospital+Cork",
    "University Hospital Kerry": "https://maps.google.com/?q=University+Hospital+Kerry+Tralee",
    "University Hospital Limerick": "https://maps.google.com/?q=University+Hospital+Limerick",
    "Galway University Hospitals": "https://maps.google.com/?q=Galway+University+Hospital",
    "Mayo University Hospital": "https://maps.google.com/?q=Mayo+University+Hospital+Castlebar",
    "Sligo University Hospital": "https://maps.google.com/?q=Sligo+University+Hospital",
    "Letterkenny University Hospital": "https://maps.google.com/?q=Letterkenny+University+Hospital+Donegal",
    "UH Waterford": "https://maps.google.com/?q=University+Hospital+Waterford",
    "Wexford General Hospital": "https://maps.google.com/?q=Wexford+General+Hospital",
    "St Luke's General Hospital Kilkenny": "https://maps.google.com/?q=St+Luke%27s+General+Hospital+Kilkenny",
    "Tipperary University Hospital": "https://maps.google.com/?q=Tipperary+University+Hospital+Clonmel",
    "Our Lady of Lourdes Hospital": "https://maps.google.com/?q=Our+Lady+of+Lourdes+Hospital+Drogheda",
    "Our Lady's Hospital Navan": "https://maps.google.com/?q=Our+Lady%27s+Hospital+Navan+Meath",
    "Cavan General Hospital": "https://maps.google.com/?q=Cavan+General+Hospital",
    "Midland Regional Hospital Portlaoise": "https://maps.google.com/?q=Midland+Regional+Hospital+Portlaoise",
    "Midland Regional Hospital Tullamore": "https://maps.google.com/?q=Midland+Regional+Hospital+Tullamore",
    "Midland Regional Hospital Mullingar": "https://maps.google.com/?q=Midland+Regional+Hospital+Mullingar",
    "Portiuncula University Hospital": "https://maps.google.com/?q=Portiuncula+University+Hospital+Ballinasloe",
}




# ── Google Maps links ─────────────────────────────────────────────────────────
GOOGLE_MAPS = {
    "Mater Misericordiae University Hospital": "https://maps.google.com/?q=Mater+Misericordiae+University+Hospital+Dublin",
    "St. James's Hospital":                   "https://maps.google.com/?q=St+James+Hospital+Dublin",
    "St. Vincent's University Hospital":      "https://maps.google.com/?q=St+Vincents+University+Hospital+Dublin",
    "Beaumont Hospital":                       "https://maps.google.com/?q=Beaumont+Hospital+Dublin",
    "Tallaght University Hospital":            "https://maps.google.com/?q=Tallaght+University+Hospital+Dublin",
    "Connolly Hospital Blanchardstown":        "https://maps.google.com/?q=Connolly+Hospital+Blanchardstown+Dublin",
    "Naas General Hospital":                   "https://maps.google.com/?q=Naas+General+Hospital+Kildare",
    "CHI at Temple Street":                    "https://maps.google.com/?q=Childrens+Health+Ireland+Temple+Street+Dublin",
    "CHI at Crumlin":                          "https://maps.google.com/?q=Childrens+Health+Ireland+Crumlin+Dublin",
    "CHI at Tallaght":                         "https://maps.google.com/?q=Childrens+Health+Ireland+Tallaght+Dublin",
    "Cork University Hospital":                "https://maps.google.com/?q=Cork+University+Hospital",
    "Mercy University Hospital":               "https://maps.google.com/?q=Mercy+University+Hospital+Cork",
    "University Hospital Kerry":               "https://maps.google.com/?q=University+Hospital+Kerry+Tralee",
    "University Hospital Limerick":            "https://maps.google.com/?q=University+Hospital+Limerick",
    "Galway University Hospitals":             "https://maps.google.com/?q=Galway+University+Hospital",
    "Mayo University Hospital":                "https://maps.google.com/?q=Mayo+University+Hospital+Castlebar",
    "Sligo University Hospital":               "https://maps.google.com/?q=Sligo+University+Hospital",
    "Letterkenny University Hospital":         "https://maps.google.com/?q=Letterkenny+University+Hospital+Donegal",
    "UH Waterford":                            "https://maps.google.com/?q=University+Hospital+Waterford",
    "Wexford General Hospital":                "https://maps.google.com/?q=Wexford+General+Hospital",
    "St Luke's General Hospital Kilkenny":     "https://maps.google.com/?q=St+Lukes+General+Hospital+Kilkenny",
    "Tipperary University Hospital":           "https://maps.google.com/?q=Tipperary+University+Hospital+Clonmel",
    "Our Lady of Lourdes Hospital":            "https://maps.google.com/?q=Our+Lady+of+Lourdes+Hospital+Drogheda",
    "Our Lady's Hospital Navan":               "https://maps.google.com/?q=Our+Ladys+Hospital+Navan",
    "Cavan General Hospital":                  "https://maps.google.com/?q=Cavan+General+Hospital",
    "Midland Regional Hospital Portlaoise":    "https://maps.google.com/?q=Midland+Regional+Hospital+Portlaoise",
    "Midland Regional Hospital Tullamore":     "https://maps.google.com/?q=Midland+Regional+Hospital+Tullamore",
    "Midland Regional Hospital Mullingar":     "https://maps.google.com/?q=Midland+Regional+Hospital+Mullingar",
    "Portiuncula University Hospital":         "https://maps.google.com/?q=Portiuncula+University+Hospital+Ballinasloe",
}

# ── Age-based hospital filtering & guidance ───────────────────────────────────
CHILDRENS_HOSPITALS = [
    "CHI at Temple Street",
    "CHI at Crumlin",
    "CHI at Tallaght",
]

def get_hospitals_for_age(county, age_group):
    base = HOSPITAL_MAP.get(county, [])
    if "Under 5" in age_group:
        chi = [h for h in CHILDRENS_HOSPITALS]
        local_backup = [h for h in base if h not in chi]
        hospitals = chi + local_backup
        note = ("⚠️ For children under 5, Children's Health Ireland (CHI) hospitals are "
                "specifically equipped for paediatric emergencies. If CHI is not nearby, "
                "proceed to your local ED and request paediatric support.")
        icon = ""
    elif "5–15" in age_group:
        chi = [h for h in CHILDRENS_HOSPITALS]
        local_backup = [h for h in base if h not in chi]
        hospitals = chi + local_backup
        note = ("🧒 For children aged 5–15, CHI hospitals have dedicated paediatric teams. "
                "Your local ED can also treat children but CHI is preferred for serious cases.")
        icon = ""
    elif "65+" in age_group:
        hospitals = base
        note = ("👴 As a senior patient, you may be eligible for priority assessment under "
                "HSE older persons services. Ask about the Frailty Intervention Therapy Team (FITT) at your local ED.")
        icon = ""
    else:
        hospitals = base
        note = None
        icon = ""
    if not hospitals:
        hospitals = base
    return hospitals, note, icon

INSURANCE_MAP = {
    "None / Public":     {"clinics":[],"benefit":"Public HSE pathway. A&E visits are free with a valid GP referral letter.","colour":"#6b7280"},
    "Laya Healthcare":   {"clinics":["Laya Health & Wellbeing Clinic – Dublin 2","Laya Clinic Cork"],"benefit":"Free GP visits and minor injury care at Laya clinics. No excess for minor injuries.","colour":"#0D9488"},
    "VHI Healthcare":    {"clinics":["VHI Swiftcare – Dublin","VHI Swiftcare – Cork","VHI Swiftcare – Limerick"],"benefit":"VHI Swiftcare clinics offer same-day appointments. €75 excess applies.","colour":"#7c3aed"},
    "Irish Life Health": {"clinics":["Affidea Urgent Care – Dublin","Affidea Urgent Care – Cork"],"benefit":"Access to Affidea network. Minor injury unit visits typically covered.","colour":"#0891b2"},
    "Aviva Health":      {"clinics":["Beacon Hospital – Dublin","Mater Private – Dublin"],"benefit":"Private hospital access with reduced excess. GP referral may be required.","colour":"#d97706"},
    "Bupa Ireland":      {"clinics":["Mater Private – Dublin","Blackrock Clinic – Dublin"],"benefit":"Private network access. Contact Bupa to confirm cover before attending.","colour":"#e11d48"},
}

CM = {"Green":"#16A34A","Amber":"#D97706","Red":"#DC2626"}

def rag_meta(status):
    if status == "Red":   return "#DC2626","s-red","Very Busy","tdot-red"
    if status == "Amber": return "#D97706","s-amber","Busy","tdot-amber"
    return "#16A34A","s-green","Normal","tdot-green"

def get_pathway(occ, insurance, urgency_type):
    if urgency_type == "life":
        return "Call 999 / A&E","#DC2626","Call 999 immediately or go directly to your nearest A&E. Do not drive yourself."
    elif urgency_type == "moderate":
        ins = INSURANCE_MAP.get(insurance,{})
        if insurance != "None / Public" and ins.get("clinics") and occ >= 7:
            return f"Private Clinic — {insurance}","#0D9488",f"Your hospital is under pressure. Based on your cover, consider {ins['clinics'][0]}."
        elif occ >= 9:
            return "A&E","#DC2626","Your condition requires A&E. Consider an alternative hospital if one is less busy."
        return "Minor Injury Unit / Urgent Virtual Care","#D97706","A Minor Injury Unit or UVC video consultation is recommended for same-day care."
    else:
        return "GP / Out-of-Hours / Pharmacy","#16A34A","A GP appointment, out-of-hours service, or pharmacist can help with your condition."

# ── Rule engine ───────────────────────────────────────────────────────────────
def apply_rule(current, predicted):
    if current=="Red"   and predicted=="Red":   return "URGENT REDIRECT","Trigger concierge alerts — surface nearest MIU and GP","#DC2626"
    if current=="Amber" and predicted=="Red":   return "EARLY WARNING",  "Notify concierge users now before status worsens","#D97706"
    if current=="Red"   and predicted in ["Amber","Green"]: return "IMPROVING","Send concierge notifications that wait is dropping","#16A34A"
    if current=="Amber" and predicted=="Amber": return "MONITOR",        "Flag for next 30-minute refresh cycle","#D97706"
    if current=="Green":                        return "NO ACTION",      "Operating within normal capacity","#16A34A"
    return "MONITOR","Insufficient data","#94A3B8"

# ── Load data ─────────────────────────────────────────────────────────────────
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

# Latest snapshot per hospital from synthetic
latest_syn = synthetic.sort_values("date").groupby("Hospital").last().reset_index()

def get_hosp_data(hospital_name):
    """Get best available data for a hospital — master first, synthetic fallback."""
    row = master[master["Hospital"].str.lower().str.contains(hospital_name.lower().split()[0], na=False)]
    if not row.empty:
        r = row.iloc[0]
        occ    = r["Occupancy_Rate_pct"] if pd.notna(r["Occupancy_Rate_pct"]) else 5.0
        status = r["Traffic_Light_Status"]
        troll  = r["Daily_Total"] if pd.notna(r["Daily_Total"]) else 0
        bis    = r["Behavioural_Impact_Score"]
        return occ, status, int(troll), bis
    # fallback to synthetic
    row2 = latest_syn[latest_syn["Hospital"].str.lower().str.contains(hospital_name.lower().split()[0], na=False)]
    if not row2.empty:
        r2     = row2.iloc[0]
        occ    = r2["occupancy_rate_pct"]
        status = r2["traffic_light_status"]
        troll  = int(r2["total_trolleys"]) if pd.notna(r2["total_trolleys"]) else 0
        bis    = r2.get("behavioural_impact_score", 0) if "behavioural_impact_score" in r2 else 0
        return occ, status, troll, bis
    return 5.0, "Green", 0, 0

# ── Landing page — shown on first visit before anything else ─────────────────
if "onboarded" not in st.session_state:
    st.session_state.onboarded = False

if not st.session_state.onboarded:
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0D9488 0%,#0a7a70 60%,#0D2137 100%);
                padding:3rem 2rem 2rem 2rem;border-radius:0 0 20px 20px;margin-bottom:2rem">
        <div style="text-align:center;color:white">
            <div style="background:rgba(255,255,255,0.2);width:60px;height:60px;border-radius:16px;
                        display:flex;align-items:center;justify-content:center;
                        font-size:28px;margin:0 auto 16px auto">🏥</div>
            <div style="font-size:28px;font-weight:700;margin-bottom:8px">Welcome to HealthFlow</div>
            <div style="font-size:15px;opacity:0.88">
                Find the right care, right now — across Ireland's HSE hospitals
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;font-size:18px;font-weight:700;color:#0D2137;margin-bottom:6px">
        Tell us about yourself to get started
    </div>
    <div style="text-align:center;font-size:13px;color:#64748B;margin-bottom:28px">
        We'll personalise your experience based on your location and age
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        county_land = st.selectbox(
            "📍 Which county are you in?",
            list(HOSPITAL_MAP.keys()),
            index=0
        )

        age_groups = [
            "Under 5 — Infant / Toddler",
            "5–15 — Child",
            "16–25 — Young Adult",
            "26–64 — Adult",
            "65+ — Senior",
        ]
        age_land = st.selectbox(
            "👤 What is the patient's age group?",
            age_groups,
            index=2
        )

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        if st.button("🏥  Find My Care  →", type="primary", use_container_width=True):
            st.session_state.onboarded      = True
            st.session_state.landing_county = county_land
            st.session_state.landing_age    = age_land
            st.session_state.page_override  = "🏥 My Hospitals"
            st.rerun()

    st.markdown("""
    <div style="text-align:center;margin-top:24px">
        <span style="font-size:12px;color:#94A3B8">
            🔒 No personal data is stored &nbsp;|&nbsp; 🇮🇪 HSE Ireland &nbsp;|&nbsp;
            📞 Emergency? Call 999
        </span>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Sidebar nav ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:8px 0 16px 0">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px">
            <div style="background:#0D9488;color:white;width:34px;height:34px;border-radius:9px;
                        display:flex;align-items:center;justify-content:center;font-weight:700">H</div>
            <div>
                <div style="font-weight:700;color:white;font-size:1rem">HealthFlow</div>
                <div style="font-size:0.7rem;color:#94A3B8">Emergency Department Monitor</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    # Handle page override from buttons
    if st.session_state.get("page_override"):
        default_page = st.session_state.pop("page_override")
    else:
        default_page = "🏥 My Hospitals"

    nav_options = ["🏥 My Hospitals","🗺️ All ED Status","💊 Patient Advice","📊 Analytics","🔍 EDA","📈 Predictive","🧠 Prescriptive","📞 Contact"]
    page = st.radio("", nav_options,
                    index=nav_options.index(default_page),
                    label_visibility="collapsed")
    st.divider()
    st.markdown("""
    <div style="background:#DC2626;border-radius:8px;padding:12px;text-align:center;margin-top:8px">
        <div style="color:rgba(255,255,255,0.8);font-size:11px">Emergency</div>
        <div style="color:white;font-size:22px;font-weight:700">📞 Call 999</div>
    </div>
    """, unsafe_allow_html=True)

# ── Summary counts from synthetic (most complete) ─────────────────────────────
red_c   = int((latest_syn["traffic_light_status"]=="Red").sum())
amb_c   = int((latest_syn["traffic_light_status"]=="Amber").sum())
grn_c   = int((latest_syn["traffic_light_status"]=="Green").sum())

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 0 — MY HOSPITALS
# ══════════════════════════════════════════════════════════════════════════════
if page == "🏥 My Hospitals":
    sel_county = st.session_state.get("landing_county", list(HOSPITAL_MAP.keys())[0])
    sel_age    = st.session_state.get("landing_age", "26–64 — Adult")
    age_hospitals, age_note, age_icon = get_hospitals_for_age(sel_county, sel_age)

    st.markdown(f"""
    <div class="hero">
        <div class="hero-title">Your Hospitals in {sel_county}</div>
        <div class="hero-sub">Showing hospitals relevant for <strong>{sel_age}</strong> patients in {sel_county}</div>
        <div>
            <span class="pill">🟢 Normal: {grn_c}</span>
            <span class="pill">🟡 Busy: {amb_c}</span>
            <span class="pill">🔴 Very Busy: {red_c}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if age_note:
        st.info(age_note)

    st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)
    st.markdown("<div style='margin-bottom:8px'></div>", unsafe_allow_html=True)
    show_change = st.toggle("📍 Change location or age group")
    if show_change:
        col1, col2 = st.columns(2)
        with col1:
            new_county = st.selectbox("County", list(HOSPITAL_MAP.keys()),
                                       index=list(HOSPITAL_MAP.keys()).index(sel_county), key="mh_county")
        with col2:
            age_opts = ["Under 5 — Infant / Toddler","5–15 — Child",
                        "16–25 — Young Adult","26–64 — Adult","65+ — Senior"]
            new_age = st.selectbox("Age group", age_opts,
                                    index=age_opts.index(sel_age) if sel_age in age_opts else 3, key="mh_age")
        if st.button("Update", type="primary"):
            st.session_state.landing_county = new_county
            st.session_state.landing_age    = new_age
            st.rerun()

    sel_county = st.session_state.get("landing_county", sel_county)
    sel_age    = st.session_state.get("landing_age", sel_age)
    age_hospitals, age_note, age_icon = get_hospitals_for_age(sel_county, sel_age)

    st.markdown(f"<div style='color:#64748B;font-size:0.85rem;margin-bottom:12px'>Showing <strong>{len(age_hospitals)}</strong> hospitals for your selection</div>", unsafe_allow_html=True)

    cols = st.columns(2)
    for i, hosp in enumerate(age_hospitals):
        occ, status, troll, bis = get_hosp_data(hosp)
        rc, sc, rl, _ = rag_meta(status)
        dot_col = {"Red":"#DC2626","Amber":"#D97706","Green":"#16A34A"}.get(status,"#94A3B8")
        cap_pct = min(int(occ*10), 100)
        cap_col = "#DC2626" if occ>=8 else "#D97706" if occ>=4 else "#16A34A"
        is_chi  = "CHI" in hosp
        badge_html = "<span style=\"background:#eff6ff;color:#1d4ed8;font-size:10px;font-weight:600;padding:2px 7px;border-radius:4px;margin-left:6px\">Children's</span>" if is_chi else "<span style=\"background:#EFF6FF;color:#2563EB;font-size:10px;font-weight:600;padding:2px 7px;border-radius:4px;margin-left:6px\">Public</span>"
        maps_url = MAPS.get(hosp, f"https://maps.google.com/?q={hosp.replace(' ','+')}+Ireland")
        with cols[i % 2]:
            st.markdown(f"""
            <div class="hcard">
                <div class="tdot" style="background:{dot_col}"></div>
                <div class="hcard-name">{hosp}</div>
                <div class="hcard-loc">📍 {sel_county} {badge_html}</div>
                <span class="sbadge {sc}">{rl}</span>
                <div class="stat-row"><span class="stat-lbl">Occupancy Rate</span><span class="stat-val">{occ:.1f}%</span></div>
                <div class="stat-row"><span class="stat-lbl">Daily Trolleys</span><span class="stat-val">{troll}</span></div>
                <div class="stat-row"><span class="stat-lbl">BIS</span><span class="stat-val">{bis:.1f}</span></div>
                <div style="display:flex;justify-content:space-between;font-size:11px;color:#64748B;margin-top:4px">
                    <span>Capacity</span><span>{cap_pct}%</span>
                </div>
                <div class="cap-bg"><div class="cap-fill" style="width:{cap_pct}%;background:{cap_col}"></div></div>
                <div class="card-ft">
                    <span>🕐 Live data</span>
                    <a href="{maps_url}" target="_blank"
                       style="color:#0D9488;font-weight:600;text-decoration:none;font-size:12px">
                        📍 Get directions →
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    if st.button("💊 Get personalised care recommendation →", type="primary", use_container_width=True):
        st.session_state.page_override = "💊 Patient Advice"
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — ALL ED STATUS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🗺️ All ED Status":
    # Pull county and age from landing page selections
    sel_county = st.session_state.get("landing_county", list(HOSPITAL_MAP.keys())[0])
    sel_age    = st.session_state.get("landing_age", "26–64 — Adult")
    age_hospitals, age_note, age_icon = get_hospitals_for_age(sel_county, sel_age)

    st.markdown(f"""
    <div class="hero">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px">
            <div>
                <div class="hero-title">{age_icon} Hospitals for {sel_county}</div>
                <div class="hero-sub">Showing hospitals relevant to your location and age group: <strong style="color:white">{sel_age}</strong></div>
                <div>
                    <span class="pill">🟢 Normal: {grn_c}</span>
                    <span class="pill">🟡 Busy: {amb_c}</span>
                    <span class="pill">🔴 Very Busy: {red_c}</span>
                </div>
            </div>
            <div style="background:rgba(255,255,255,0.15);border-radius:20px;
                        padding:7px 14px;font-size:12px;color:white;align-self:flex-start">
                🕐 Updated live
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Age-specific guidance note
    if age_note:
        st.info(age_note)

    # Allow patient to change county or age without going back
    col1, col2, col3 = st.columns([2, 1.5, 1.5])
    with col1:
        search = st.text_input("", placeholder="🔍  Search hospitals...", label_visibility="collapsed")
    with col2:
        new_county = st.selectbox("", list(HOSPITAL_MAP.keys()),
                                   index=list(HOSPITAL_MAP.keys()).index(sel_county),
                                   label_visibility="collapsed", key="ed_county")
        if new_county != sel_county:
            st.session_state.landing_county = new_county
            st.rerun()
    with col3:
        if st.button("⚙️ Get recommendation", use_container_width=True):
            st.session_state["page_override"] = "💊 Patient Advice"
            st.rerun()

    # Filter hospitals by age and county
    age_hospitals_filtered, _, _ = get_hospitals_for_age(sel_county, sel_age)
    flat = [(sel_county, h) for h in age_hospitals_filtered]

    # Also add CHI for under 16 if not already in Dublin
    if ("Under 5" in sel_age or "5–15" in sel_age) and sel_county != "Dublin":
        flat = [(sel_county, h) for h in age_hospitals_filtered if h not in CHILDRENS_HOSPITALS]
        flat = [("Dublin (CHI)", h) for h in CHILDRENS_HOSPITALS] + flat

    if search:
        flat = [(c,h) for c,h in flat if search.lower() in h.lower() or search.lower() in c.lower()]

    st.markdown(f"<div style='color:#64748B;font-size:0.85rem;margin-bottom:12px'>Showing <strong>{len(flat)}</strong> hospitals for <strong>{sel_county}</strong> · Age: <strong>{sel_age}</strong> &nbsp;|&nbsp; <a href='#' style='color:#0D9488'>Change</a></div>", unsafe_allow_html=True)

    cols = st.columns(2)
    for i,(county,hosp) in enumerate(flat):
        occ,status,troll,bis = get_hosp_data(hosp)
        rc,sc,rl,_ = rag_meta(status)
        dot_col = {"Red":"#DC2626","Amber":"#D97706","Green":"#16A34A"}.get(status,"#94A3B8")
        cap_pct = min(int(occ*10),100)
        cap_col = "#DC2626" if occ>=8 else "#D97706" if occ>=4 else "#16A34A"
        with cols[i%2]:
            st.markdown(f"""
            <div class="hcard">
                <div class="tdot" style="background:{dot_col}"></div>
                <div class="hcard-name">{hosp}</div>
                <div class="hcard-loc">📍 {county} &nbsp;
                    <span style="background:#EFF6FF;color:#2563EB;font-size:10px;font-weight:600;
                                 padding:2px 7px;border-radius:4px;border:1px solid #BFDBFE">Public</span>
                </div>
                <span class="sbadge {sc}">{rl}</span>
                <div class="stat-row"><span class="stat-lbl">Occupancy Rate</span><span class="stat-val">{occ:.1f}%</span></div>
                <div class="stat-row"><span class="stat-lbl">Daily Trolleys</span><span class="stat-val">{troll}</span></div>
                <div class="stat-row"><span class="stat-lbl">Behavioural Impact Score</span><span class="stat-val">{bis:.1f}</span></div>
                <div style="display:flex;justify-content:space-between;font-size:11px;color:#64748B;margin-top:4px">
                    <span>Capacity</span><span>{cap_pct}%</span>
                </div>
                <div class="cap-bg"><div class="cap-fill" style="width:{cap_pct}%;background:{cap_col}"></div></div>
                <div class="card-ft">
                    <span>🕐 Live data</span><span>Tap for details</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — PATIENT ADVICE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "💊 Patient Advice":
    st.markdown("""
    <div class="hero">
        <div class="hero-title">Patient Advice &amp; Emergency Guidelines</div>
        <div class="hero-sub">Important information to help you decide when and where to seek medical care</div>
    </div>""", unsafe_allow_html=True)

    # Important update
    st.markdown("""
    <div class="updates-box">
        <div style="display:flex;align-items:flex-start;gap:14px">
            <div style="background:#FEF3C7;border-radius:10px;padding:10px;font-size:1.3rem;flex-shrink:0">📈</div>
            <div>
                <span class="upd-badge">Important Updates</span>
                <span style="font-size:11px;color:#6b7280;margin-left:8px">Updated June 2025</span>
                <div style="background:white;border-radius:10px;padding:14px;font-size:13px;
                            color:#374151;line-height:1.7;margin-top:10px">
                    Over the next <strong>1–4 weeks</strong> we expect ED attendances to go up by
                    <strong style="color:#F59E0B">15–20%</strong> based on seasonal triggers and previous data.
                    We would <strong>strongly advise people to only come to the ED if very necessary</strong>
                    and if advised by their GP.
                </div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    # UVC box
    st.markdown("""
    <div class="uvc-box">
        <div style="font-size:16px;font-weight:700;margin-bottom:6px">📹 Urgent Virtual Care (UVC) Success</div>
        <div style="font-size:13px;opacity:0.9;line-height:1.6">
            Our Urgent Virtual Care service has successfully managed over <strong>8,450 cases</strong>
            in the past month without requiring ED visits, helping reduce waiting times for critical emergencies.
        </div>
        <div class="uvc-stats">
            <div class="uvc-stat"><div class="uvc-stat-lbl">Cases Managed</div><div class="uvc-stat-val">8,450+</div></div>
            <div class="uvc-stat"><div class="uvc-stat-lbl">Avg Wait Reduction</div><div class="uvc-stat-val">2.3 hrs</div></div>
        </div>
    </div>""", unsafe_allow_html=True)

    # Get recommendation
    st.markdown('<div class="sec-title">Get Your Personalised Recommendation</div>', unsafe_allow_html=True)

    with st.expander("📍 Step 1 — Your location & insurance", expanded=True):
        col1,col2 = st.columns(2)
        with col1:
            default_county = st.session_state.get("landing_county", list(HOSPITAL_MAP.keys())[0])
            county_idx = list(HOSPITAL_MAP.keys()).index(default_county) if default_county in HOSPITAL_MAP else 0
            county_pa = st.selectbox("County / City", list(HOSPITAL_MAP.keys()), index=county_idx, key="pa_c")
            sel_hosp  = st.selectbox("Nearest hospital", HOSPITAL_MAP[county_pa], key="pa_h")
            age_groups = ["Under 5 — Infant / Toddler","5–15 — Child","16–25 — Young Adult","26–64 — Adult","65+ — Senior"]
            default_age = st.session_state.get("landing_age", "26–64 — Adult")
            age_idx = age_groups.index(default_age) if default_age in age_groups else 2
            patient_age = st.selectbox("Patient age group", age_groups, index=age_idx, key="pa_age")
        with col2:
            insurance = st.selectbox("Health insurance", list(INSURANCE_MAP.keys()), key="pa_i")
            ins_info  = INSURANCE_MAP[insurance]
            clinics_html = f"<div style='font-size:12px;color:#0D9488;margin-top:6px'>✅ {' · '.join(ins_info['clinics'])}</div>" if ins_info["clinics"] else ""
            st.markdown(f"""
            <div class="ins-card">
                <div style="font-weight:600;color:{ins_info['colour']};margin-bottom:4px">{insurance}</div>
                <div style="font-size:12px;color:#6b7280">{ins_info['benefit']}</div>
                {clinics_html}
            </div>""", unsafe_allow_html=True)

    st.markdown('<div style="color:#0D9488;font-size:11px;font-weight:700;letter-spacing:0.06em;margin:16px 0 4px 0">STEP 2 OF 2</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:18px;font-weight:700;color:#0D2137;margin-bottom:6px">Why are you considering attending A&E?</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:13px;color:#64748B;margin-bottom:14px">Select the option that best describes your situation. We\'ll show you the most appropriate care pathway.</div>', unsafe_allow_html=True)

    URGENCY_OPTIONS = [
        ("❤️","Chest pain or breathing difficulty","Tightness, pressure, shortness of breath","life"),
        ("⚠️","Stroke symptoms","Face drooping, arm weakness, speech difficulty","life"),
        ("⚠️","Severe injury or uncontrolled bleeding","Major trauma, deep wound, broken bones","life"),
        ("⚠️","Collapsed, unconscious, or seizure","Loss of consciousness, fitting","life"),
        ("🤒","Moderate illness – needs same-day care","Infection, fever, moderate pain","moderate"),
        ("💊","Minor – can wait or self-manage","Cold, rash, prescription renewal, UTI","minor"),
    ]

    sel_urg = st.radio("", [f"{ic}  {ti}" for ic,ti,_,_ in URGENCY_OPTIONS], label_visibility="collapsed")
    urgency_type = "minor"
    for ic,ti,sub,ut in URGENCY_OPTIONS:
        if ti in sel_urg:
            urgency_type = ut
            st.caption(f"_{sub}_")
            break

    occ,status,troll,bis = get_hosp_data(sel_hosp)
    rc,sc,rl,_ = rag_meta(status)
    pathway,path_c,path_desc = get_pathway(occ, insurance, urgency_type)

    st.markdown(f"""
    <div class="rec-card" style="border-left:5px solid {path_c}">
        <div style="color:{path_c};font-size:11px;font-weight:700;margin-bottom:6px;letter-spacing:0.05em">
            RECOMMENDED CARE PATHWAY
        </div>
        <div style="font-size:20px;font-weight:700;color:{path_c}">🏥 {pathway}</div>
        <div style="font-size:13px;color:#374151;margin-top:10px;line-height:1.7">{path_desc}</div>
        <div style="margin-top:14px;padding-top:12px;border-top:1px solid #F1F5F9;
                    font-size:12px;color:#94A3B8">
            📍 {sel_hosp} &nbsp;|&nbsp;
            Status: <strong style="color:{rc}">{rl}</strong> &nbsp;|&nbsp;
            Occupancy: <strong>{occ:.1f}%</strong> &nbsp;|&nbsp;
            BIS: <strong>{bis:.1f}</strong>
        </div>
    </div>""", unsafe_allow_html=True)

    if urgency_type=="life":
        st.error("🚨 Call 999 immediately. Do not drive yourself to hospital.")
    elif status=="Red":
        st.warning(f"⚠️ {sel_hosp} is very busy. Consider an alternative if your condition allows.")

    # Critical symptoms
    st.markdown("""
    <div class="crit-box">
        <span class="crit-badge">🚨 Critical Symptoms Requiring Immediate 999</span>
        <div class="crit-grid">
            <div class="crit-item"><span class="crit-num">1</span><div><div class="crit-name">Chest Pain / Heart Attack</div><div class="crit-sub">Crushing chest pain, left arm pain, sweating</div></div></div>
            <div class="crit-item"><span class="crit-num">2</span><div><div class="crit-name">Stroke Symptoms</div><div class="crit-sub">FAST — Face, Arms, Speech, Time</div></div></div>
            <div class="crit-item"><span class="crit-num">3</span><div><div class="crit-name">Severe Breathing Difficulty</div><div class="crit-sub">Unable to speak in full sentences</div></div></div>
            <div class="crit-item"><span class="crit-num">4</span><div><div class="crit-name">Loss of Consciousness</div><div class="crit-sub">Collapsed, unresponsive, or seizure</div></div></div>
        </div>
    </div>""", unsafe_allow_html=True)

    # Concierge
    st.markdown('<div class="sec-title">🔔 Concierge Notification</div>', unsafe_allow_html=True)
    col1,col2 = st.columns([3,1])
    with col1:
        email = st.text_input("", placeholder="Your email address", label_visibility="collapsed")
    with col2:
        if st.button("Notify me", type="primary", use_container_width=True):
            st.success(f"✅ You'll be notified at {email} when {sel_hosp} wait times improve.") if email else st.warning("Please enter your email.")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📊 Analytics":
    st.markdown('<div style="padding:1.5rem 0">', unsafe_allow_html=True)
    st.title("📊 Live ED Analytics")

    rn = int((latest_syn["traffic_light_status"]=="Red").sum())
    an = int((latest_syn["traffic_light_status"]=="Amber").sum())
    gn = int((latest_syn["traffic_light_status"]=="Green").sum())
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("🔴 Very Busy", rn)
    c2.metric("🟡 Busy", an)
    c3.metric("🟢 Normal", gn)
    c4.metric("🏥 Total Hospitals", latest_syn["Hospital"].nunique())
    st.divider()

    chart_df = latest_syn.dropna(subset=["occupancy_rate_pct"]).sort_values("occupancy_rate_pct", ascending=True)
    colors   = chart_df["traffic_light_status"].map(CM).fillna("#64748B")
    fig = go.Figure(go.Bar(
        x=chart_df["occupancy_rate_pct"], y=chart_df["Hospital"],
        orientation="h", marker_color=list(colors),
        text=chart_df["occupancy_rate_pct"].apply(lambda x: f"{x:.1f}%"),
        textposition="outside"))
    fig.update_layout(plot_bgcolor="white",paper_bgcolor="white",height=520,
                      xaxis_title="Occupancy Rate (%)",margin=dict(l=0,r=60,t=20,b=20))
    fig.add_vline(x=8, line_dash="dash", line_color="#DC2626", annotation_text="Red threshold")
    fig.add_vline(x=4, line_dash="dash", line_color="#D97706", annotation_text="Amber threshold")
    st.plotly_chart(fig, use_container_width=True)

    col1,col2 = st.columns(2)
    with col1:
        tl = latest_syn["traffic_light_status"].value_counts().reset_index()
        tl.columns = ["Status","Count"]
        fig2 = px.pie(tl, names="Status", values="Count", color="Status",
                      color_discrete_map=CM, title="Traffic Light Distribution")
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig2, use_container_width=True)
    with col2:
        wt = synthetic["wait_tier"].value_counts().reset_index()
        wt.columns = ["Tier","Count"]
        fig3 = px.bar(wt, x="Tier", y="Count", color="Tier",
                      color_discrete_map={"No breach":"#16A34A","Low breach":"#D97706",
                                          "Moderate breach":"#EA580C","High breach":"#DC2626"},
                      title="Wait Tier Breakdown")
        fig3.update_layout(plot_bgcolor="white",paper_bgcolor="rgba(0,0,0,0)",showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — EDA
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🔍 EDA":
    st.title("🔍 EDA & Insights")
    c1,c2,c3 = st.columns(3)
    c1.metric("Total Rows",   f"{len(synthetic):,}")
    c2.metric("Hospitals",    synthetic["Hospital"].nunique())
    c3.metric("Date Range",   f"{synthetic['date'].min().strftime('%b %Y')} – {synthetic['date'].max().strftime('%b %Y')}")
    st.divider()

    col1,col2 = st.columns([2,1])
    with col1:
        sel_hosps = st.multiselect("Select hospitals", sorted(synthetic["Hospital"].unique()),
                                    default=["Cork University Hospital","University Hospital Limerick","Beaumont Hospital"])
    with col2:
        sel_metric = st.selectbox("Metric", ["occupancy_rate_pct","total_trolleys","trolley_load"])

    filt = synthetic[synthetic["Hospital"].isin(sel_hosps)].copy()
    monthly = filt.groupby(["Hospital","year","month"])[sel_metric].mean().reset_index()
    monthly["date"] = pd.to_datetime(monthly[["year","month"]].assign(day=1))
    fig = px.line(monthly, x="date", y=sel_metric, color="Hospital",
                  title=f"Monthly Average {sel_metric.replace('_',' ').title()} Over Time",
                  color_discrete_sequence=["#0D9488","#0891b2","#7c3aed","#d97706","#e11d48"])
    fig.update_layout(plot_bgcolor="white",paper_bgcolor="rgba(0,0,0,0)",height=380)
    st.plotly_chart(fig, use_container_width=True)

    col1,col2 = st.columns(2)
    with col1:
        seasonal = synthetic.groupby("month")["occupancy_rate_pct"].mean().reset_index()
        fig2 = px.bar(seasonal, x="month", y="occupancy_rate_pct",
                      title="Average Occupancy by Month (Seasonal Pattern)",
                      color="occupancy_rate_pct", color_continuous_scale=["#16A34A","#D97706","#DC2626"])
        fig2.update_layout(plot_bgcolor="white",paper_bgcolor="rgba(0,0,0,0)",height=340)
        st.plotly_chart(fig2, use_container_width=True)
    with col2:
        flu = synthetic.groupby("is_flu_season")["occupancy_rate_pct"].mean().reset_index()
        flu["is_flu_season"] = flu["is_flu_season"].map({True:"Flu Season",False:"Normal Period"})
        fig3 = px.bar(flu, x="is_flu_season", y="occupancy_rate_pct",
                      color="is_flu_season",
                      color_discrete_sequence=["#0D9488","#DC2626"],
                      title="Avg Occupancy: Flu Season vs Normal",
                      labels={"is_flu_season":"","occupancy_rate_pct":"Avg Occupancy (%)"})
        fig3.update_layout(plot_bgcolor="white",paper_bgcolor="rgba(0,0,0,0)",showlegend=False,height=340)
        st.plotly_chart(fig3, use_container_width=True)

    with st.expander("📋 Raw Synthetic Data"):
        st.dataframe(synthetic, use_container_width=True, height=400)
        csv = synthetic.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download CSV", csv, "synthetic_dataset.csv", "text/csv")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — PREDICTIVE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📈 Predictive":
    st.title("📈 Predictive Analytics — SARIMAX")
    st.info("SARIMAX model trained on Jan 2022 – Dec 2023 synthetic data. Forecasts occupancy 4 hours ahead.")

    try:
        from statsmodels.tsa.statespace.sarimax import SARIMAX

        col1,col2 = st.columns(2)
        with col1:
            county_fc = st.selectbox("County", list(HOSPITAL_MAP.keys()), key="fc_c")
        with col2:
            sel_fc = st.selectbox("Hospital", HOSPITAL_MAP[county_fc], key="fc_h")

        occ_fc,status_fc,_,bis_fc = get_hosp_data(sel_fc)
        st.info(f"**{sel_fc}** | Occupancy: **{occ_fc:.1f}%** | Status: **{status_fc}** | BIS: **{bis_fc:.1f}**")

        # Get synthetic time series for this hospital
        syn_h = synthetic[synthetic["Hospital"].str.lower().str.contains(sel_fc.lower().split()[0], na=False)].copy()
        syn_h = syn_h.sort_values("date")

        if len(syn_h) >= 30:
            monthly = syn_h.groupby(["year","month"])["occupancy_rate_pct"].mean().reset_index()
            monthly["date"] = pd.to_datetime(monthly[["year","month"]].assign(day=1))
            monthly = monthly.sort_values("date")
            series   = monthly["occupancy_rate_pct"].values
            hist_idx = monthly["date"].tolist()
            fore_idx = [hist_idx[-1]+pd.DateOffset(months=i) for i in range(1,7)]
            st.success(f"✅ Training on {len(monthly)} monthly observations for {sel_fc}.")
        else:
            st.info("ℹ️ Insufficient hospital-level data — using national aggregate.")
            monthly = synthetic.groupby(["year","month"])["occupancy_rate_pct"].mean().reset_index()
            monthly["date"] = pd.to_datetime(monthly[["year","month"]].assign(day=1))
            monthly = monthly.sort_values("date")
            series   = monthly["occupancy_rate_pct"].values
            hist_idx = monthly["date"].tolist()
            fore_idx = [hist_idx[-1]+pd.DateOffset(months=i) for i in range(1,7)]

        n = len(series)
        exog = np.zeros((n,1))
        with st.spinner("Fitting SARIMAX(1,0,1)(1,0,1,12)..."):
            res = SARIMAX(series, exog=exog, order=(1,0,1), seasonal_order=(1,0,1,12),
                          enforce_stationarity=False, enforce_invertibility=False).fit(disp=False)

        fc   = res.get_forecast(steps=6, exog=np.zeros((6,1)))
        fc_m = fc.predicted_mean
        ci   = fc.conf_int()

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hist_idx, y=series, mode="lines", name="Historical",
                                  line=dict(color="#0D9488",width=2)))
        fig.add_trace(go.Scatter(x=fore_idx, y=fc_m, mode="lines+markers", name="SARIMAX Forecast",
                                  line=dict(color="#D97706",width=2.5,dash="dot")))
        fig.add_trace(go.Scatter(x=list(fore_idx)+list(fore_idx)[::-1],
                                  y=list(ci.iloc[:,1])+list(ci.iloc[:,0])[::-1],
                                  fill="toself",fillcolor="rgba(217,119,6,0.15)",
                                  line=dict(color="rgba(0,0,0,0)"),name="95% CI"))
        fig.add_hline(y=8, line_dash="dash", line_color="#DC2626", annotation_text="Red (8%)")
        fig.add_hline(y=4, line_dash="dash", line_color="#D97706", annotation_text="Amber (4%)")
        fig.update_layout(title=f"Occupancy Forecast — {sel_fc}",
                          xaxis_title="Month", yaxis_title="Occupancy (%)",
                          plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)", height=440,
                          legend=dict(orientation="h",yanchor="bottom",y=1.02))
        st.plotly_chart(fig, use_container_width=True)

        fore_tbl = pd.DataFrame({
            "Month":    [d.strftime("%b %Y") for d in fore_idx],
            "Forecast": fc_m.round(2).values,
            "Lower CI": ci.iloc[:,0].round(2).values,
            "Upper CI": ci.iloc[:,1].round(2).values,
            "Status":   ["Red" if v>=8 else "Amber" if v>=4 else "Green" for v in fc_m.values]
        })
        st.dataframe(fore_tbl, use_container_width=True, hide_index=True)

        c1,c2,c3 = st.columns(3)
        resid = res.resid
        c1.metric("MAE",  f"{np.mean(np.abs(resid)):.3f}")
        c2.metric("RMSE", f"{np.sqrt(np.mean(resid**2)):.3f}")
        c3.metric("MAPE", f"{np.mean(np.abs(resid/(series+1e-5)))*100:.2f}%")

        # Seasonal pattern
        st.divider()
        seasonal = synthetic.groupby("month")["occupancy_rate_pct"].mean().reset_index()
        fig2 = px.bar(seasonal, x="month", y="occupancy_rate_pct",
                      title="Seasonal Demand Pattern — All Hospitals",
                      color="occupancy_rate_pct",
                      color_continuous_scale=["#16A34A","#D97706","#DC2626"])
        fig2.update_layout(plot_bgcolor="white",paper_bgcolor="rgba(0,0,0,0)",height=320)
        st.plotly_chart(fig2, use_container_width=True)

        with st.expander("Model Summary"):
            st.text(res.summary().as_text())

    except Exception as e:
        st.error(f"Error fitting SARIMAX: {e}")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 6 — PRESCRIPTIVE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🧠 Prescriptive":
    st.title("🧠 Prescriptive Analytics — Rule Engine")

    results = []
    for _,row in latest_syn.iterrows():
        cur  = row["traffic_light_status"]
        occ  = row["occupancy_rate_pct"]
        pred = "Red" if occ>=8 else "Amber" if occ>=4 else "Green"
        action, detail, colour = apply_rule(cur, pred)
        results.append({
            "Hospital":       row["Hospital"],
            "Current Status": cur,
            "Predicted":      pred,
            "System Action":  action,
            "Action Detail":  detail,
            "Occupancy %":    round(occ,1),
        })
    pdf = pd.DataFrame(results)

    u = (pdf["System Action"]=="URGENT REDIRECT").sum()
    w = (pdf["System Action"]=="EARLY WARNING").sum()
    o = pdf["System Action"].isin(["MONITOR","NO ACTION","IMPROVING"]).sum()
    c1,c2,c3 = st.columns(3)
    c1.metric("🚨 Urgent Redirect", int(u))
    c2.metric("⚠️ Early Warning",   int(w))
    c3.metric("✅ Monitor / OK",    int(o))
    st.divider()

    # Decision matrix
    st.markdown('<div class="sec-title">Decision Matrix</div>', unsafe_allow_html=True)
    st.dataframe(pd.DataFrame({
        "Current Status":  ["🔴 Red","🟡 Amber","🔴 Red","🟡 Amber","🟢 Green"],
        "Predicted (4hr)": ["🔴 Red","🔴 Red","🟢 Green","🟡 Amber","Any"],
        "System Action":   ["URGENT REDIRECT","EARLY WARNING","IMPROVING","MONITOR","NO ACTION"],
        "Detail":          ["Concierge alert + MIU surface","Notify users before it worsens",
                            "Notify users wait is dropping","Flag for 30-min refresh","Operating normally"],
    }), use_container_width=True, hide_index=True)

    st.divider()
    st.markdown('<div class="sec-title">All Hospitals — Rule Engine Output</div>', unsafe_allow_html=True)

    def colour_action(val):
        if val=="URGENT REDIRECT": return "background-color:#FEE2E2;color:#DC2626;font-weight:600"
        if val=="EARLY WARNING":   return "background-color:#FEF3C7;color:#D97706;font-weight:600"
        if val=="IMPROVING":       return "background-color:#DCFCE7;color:#16A34A"
        return ""
    def colour_status(val):
        if val=="Red":   return "color:#DC2626;font-weight:600"
        if val=="Amber": return "color:#D97706;font-weight:600"
        if val=="Green": return "color:#16A34A;font-weight:600"
        return ""

    styled = pdf.style.map(colour_action, subset=["System Action"]).map(colour_status, subset=["Current Status","Predicted"])
    st.dataframe(styled, use_container_width=True, height=500)

    fig = px.pie(pdf["System Action"].value_counts().reset_index(),
                 names="System Action", values="count",
                 color_discrete_sequence=["#DC2626","#D97706","#16A34A","#0D9488","#94A3B8"],
                 title="System Action Distribution")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 7 — CONTACT
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📞 Contact":
    st.markdown("""
    <div class="call999-bar">
        <div style="display:flex;align-items:center;gap:16px">
            <span style="font-size:24px;color:white">📞</span>
            <div>
                <div style="font-size:12px;color:rgba(255,255,255,0.8)">Emergency Services</div>
                <div class="call999-num">Call 999</div>
            </div>
        </div>
        <div style="font-size:13px;color:rgba(255,255,255,0.85);max-width:400px;line-height:1.5">
            Do not delay if you experience any life-threatening symptoms. Time is critical.
        </div>
    </div>""", unsafe_allow_html=True)

    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown("""<div style="background:#EFF6FF;border:1px solid #BFDBFE;border-radius:12px;padding:20px">
            <div style="font-size:15px;font-weight:600;color:#0D2137;margin-bottom:8px">GP Services</div>
            <div style="font-size:13px;color:#64748B;margin-bottom:8px">For non-emergency medical advice, contact your GP during office hours.</div>
            <div style="font-size:12px;color:#2563EB;font-weight:500">Mon–Fri: 9:00 AM – 5:00 PM</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div style="background:#F0FDF4;border:1px solid #BBF7D0;border-radius:12px;padding:20px">
            <div style="font-size:15px;font-weight:600;color:#0D2137;margin-bottom:8px">Out of Hours</div>
            <div style="font-size:13px;color:#64748B;margin-bottom:8px">ShanDoc provides out-of-hours GP services when your practice is closed.</div>
            <div style="font-size:12px;color:#16A34A;font-weight:500">📞 1850 777 911</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div style="background:#FAF5FF;border:1px solid #E9D5FF;border-radius:12px;padding:20px">
            <div style="font-size:15px;font-weight:600;color:#0D2137;margin-bottom:8px">Minor Injury Units</div>
            <div style="font-size:13px;color:#64748B;margin-bottom:8px">For minor injuries like sprains, cuts, and minor burns without appointment.</div>
            <div style="font-size:12px;color:#7C3AED;font-weight:500">Check local unit opening hours</div>
        </div>""", unsafe_allow_html=True)

    st.divider()
    cc1,cc2,cc3 = st.columns(3)
    for col,s in zip([cc1,cc2,cc3],[
        {"i":"📞","n":"Samaritans","d":"24/7 emotional support for anyone in distress","c":"116 123 (Free)"},
        {"i":"💜","n":"Pieta House","d":"Free therapy for those in suicidal distress or self-harm","c":"1800 247 247"},
        {"i":"💬","n":"Text 50808","d":"24/7 anonymous text support service","c":"Text HELLO to 50808"},
    ]):
        with col:
            st.markdown(f"""<div style="background:white;border:1px solid #E2E8F0;border-radius:12px;
                                        padding:20px;text-align:center">
                <div style="font-size:24px;margin-bottom:8px">{s["i"]}</div>
                <div style="font-size:15px;font-weight:600;color:#0D2137;margin-bottom:6px">{s["n"]}</div>
                <div style="font-size:12px;color:#64748B;margin-bottom:8px;line-height:1.4">{s["d"]}</div>
                <div style="color:#DC2626;font-size:13px;font-weight:500">{s["c"]}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="footer-bar">
        <div style="display:grid;grid-template-columns:2fr 1fr 1fr;gap:2rem">
            <div>
                <div class="footer-title">HSE HealthFlow</div>
                <p style="font-size:13px;color:#94A3B8;line-height:1.5">
                    Providing real-time emergency department information to help you make
                    informed decisions about your healthcare.
                </p>
            </div>
            <div>
                <div class="footer-title">Quick Links</div>
                <div class="footer-item">Find Your Nearest ED</div>
                <div class="footer-item">GP Services</div>
                <div class="footer-item">Health Information</div>
            </div>
            <div>
                <div class="footer-title">Emergency Contacts</div>
                <div style="font-size:13px;color:#94A3B8;line-height:1.8">
                    <strong style="color:white">Emergency:</strong> 999<br>
                    <strong style="color:white">ShanDoc:</strong> 1850 777 911<br>
                    <strong style="color:white">HSE Live:</strong> 1850 24 1850
                </div>
            </div>
        </div>
        <div class="footer-bottom">© 2026 HealthFlow — Group 2 · UCC · IS6611</div>
    </div>""", unsafe_allow_html=True)
