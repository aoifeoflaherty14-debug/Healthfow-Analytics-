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
*{font-family:'Book Antiqua','Palatino Linotype',Palatino,serif!important;box-sizing:border-box;}
.stApp{background:#f5f5f5;}
#MainMenu,footer,header{visibility:hidden;}
[data-testid="collapsedControl"]{display:none;}

/* Mobile-first responsive */
.block-container{padding:0 1rem 2rem 1rem!important;max-width:100%!important;}

/* Hero */
.hero{background:linear-gradient(135deg,#0D9488 0%,#0a7a70 60%,#0D2137 100%);
      padding:2rem 1.5rem;margin-bottom:1.5rem;}
.hero-title{font-size:28px;font-weight:700;color:white;margin-bottom:8px;line-height:1.3;}
.hero-sub{font-size:16px;color:rgba(255,255,255,0.88);margin-bottom:16px;line-height:1.6;}
.pill{display:inline-flex;align-items:center;gap:6px;
      background:rgba(255,255,255,0.15);border:1px solid rgba(255,255,255,0.25);
      color:white;padding:6px 14px;border-radius:20px;font-size:15px;font-weight:500;
      margin-right:8px;margin-bottom:8px;}

/* Nav */
.nav-bar{background:white;padding:12px 1rem;border-bottom:1px solid #E2E8F0;
         display:flex;align-items:center;gap:8px;overflow-x:auto;
         position:sticky;top:0;z-index:999;flex-wrap:wrap;}
.nav-logo{font-size:17px;font-weight:700;color:#0D2137;white-space:nowrap;margin-right:12px;}
.nav-logo span{color:#0D9488;}

/* Hospital card */
.hcard{background:white;border-radius:12px;padding:20px;border:1px solid #E2E8F0;
       box-shadow:0 1px 3px rgba(0,0,0,0.05);margin-bottom:14px;position:relative;
       width:100%;}
.hcard-name{font-size:17px;font-weight:700;color:#0D2137;margin-bottom:4px;padding-right:24px;line-height:1.3;}
.hcard-loc{font-size:14px;color:#64748B;margin-bottom:12px;}
.tdot{width:14px;height:14px;border-radius:50%;position:absolute;top:20px;right:20px;flex-shrink:0;}
.sbadge{display:block;padding:8px 12px;border-radius:6px;font-size:15px;
        font-weight:700;text-align:center;margin-bottom:12px;}
.s-red{background:#FEE2E2;color:#DC2626;}
.s-amber{background:#FEF9C3;color:#B45309;}
.s-green{background:#DCFCE7;color:#15803D;}
.stat-row{display:flex;justify-content:space-between;font-size:15px;margin-bottom:6px;}
.stat-lbl{color:#64748B;}.stat-val{font-weight:700;color:#0D2137;}
.cap-bg{height:7px;background:#E2E8F0;border-radius:10px;overflow:hidden;margin:8px 0 10px;}
.cap-fill{height:100%;border-radius:10px;}
.maps-btn{display:block;margin-top:12px;background:#0D9488;color:white;
          text-align:center;padding:12px 16px;border-radius:8px;
          font-size:15px;font-weight:700;text-decoration:none;width:100%;}

/* Section */
.sec-title{font-size:20px;font-weight:700;color:#0D2137;margin:1.4rem 0 1rem;}

/* Advice cards */
.advice-card{background:white;border-radius:12px;padding:18px;
             border:1px solid #E2E8F0;margin-bottom:14px;}
.rec-card{background:white;border-radius:12px;padding:22px;
          border:1px solid #E2E8F0;box-shadow:0 2px 6px rgba(0,0,0,0.06);margin-top:16px;}
.ins-card{background:white;border-radius:10px;padding:16px 18px;
          border:1.5px solid #E2E8F0;margin-bottom:10px;}
.update-card{background:#FFFBEB;border:1px solid #FDE68A;border-radius:12px;
             padding:18px;margin-bottom:14px;}
.uvc-card{background:linear-gradient(135deg,#0D9488,#0f766e);
          border-radius:12px;padding:18px;margin-bottom:14px;color:white;}
.important-badge{background:#F59E0B;color:white;font-size:13px;font-weight:700;
                 padding:4px 10px;border-radius:4px;display:inline-block;margin-bottom:10px;}
.crit-box{background:#FFF1F2;border:1px solid #FECDD3;border-radius:12px;padding:18px;margin-bottom:14px;}
.crit-badge{background:#DC2626;color:white;font-size:13px;font-weight:700;
            padding:4px 10px;border-radius:4px;}
.crit-item{background:white;border:1px solid #FECDD3;border-radius:8px;
           padding:12px;margin-top:10px;display:flex;gap:12px;}
.crit-num{color:#DC2626;font-weight:700;font-size:15px;flex-shrink:0;}
.crit-name{font-size:15px;font-weight:600;color:#0D2137;}
.crit-sub{font-size:13px;color:#64748B;}

/* Resources */
.resource-card{background:white;border-radius:12px;padding:18px;
               border:1px solid #E2E8F0;margin-bottom:14px;}
.resource-title{font-size:17px;font-weight:700;color:#0D2137;margin-bottom:8px;}
.resource-desc{font-size:15px;color:#64748B;line-height:1.6;margin-bottom:10px;}
.resource-link{color:#0D9488;font-size:15px;font-weight:600;text-decoration:none;}

/* Contact */
.contact-card{background:white;border-radius:12px;padding:18px;
              border:1px solid #E2E8F0;margin-bottom:14px;text-align:center;}
.contact-num{font-size:24px;font-weight:700;color:#DC2626;}
.call999-bar{background:#DC2626;padding:18px;border-radius:12px;
             margin-bottom:18px;text-align:center;}

/* Survey */
.survey-card{background:white;border-radius:14px;padding:24px;border:1px solid #E2E8F0;
             box-shadow:0 2px 8px rgba(0,0,0,0.06);margin-top:20px;}
.survey-title{font-size:20px;font-weight:700;color:#0D2137;margin-bottom:6px;}
.survey-sub{font-size:15px;color:#64748B;margin-bottom:18px;}
.survey-thanks{background:#F0FDF4;border:1px solid #BBF7D0;border-radius:12px;
               padding:20px;text-align:center;margin-top:16px;}
/* Footer */
.footer{background:#0D2137;padding:1.5rem;margin-top:2rem;border-radius:12px;
        font-size:14px;color:#94A3B8;text-align:center;line-height:1.8;}

/* Streamlit overrides */
.stSelectbox label,.stTextInput label{font-weight:600;color:#374151;font-size:16px!important;}
.stRadio label{font-size:16px!important;}
div[data-testid="stRadio"] > label{font-weight:600;color:#374151;}
.stButton button{border-radius:8px!important;font-weight:700!important;font-size:18px!important;padding:12px 22px!important;}
details summary{list-style:none!important;}
details summary::-webkit-details-marker{display:none!important;}
p, div, span, li{font-size:15px;line-height:1.7;}

@media(max-width:768px){
    .hero-title{font-size:22px;}
    .hero{padding:1.5rem 1rem;}
    .hcard-name{font-size:16px;}
    .nav-logo{font-size:15px;}
    .stat-row{font-size:14px;}
    .sbadge{font-size:14px;}
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

def rag_meta(occ_or_status):
    """Accept either occupancy float or status string."""
    try:
        occ = float(occ_or_status)
        if occ >= 8:   return "#DC2626","s-red","Very Busy"
        if occ >= 4:   return "#D97706","s-amber","Busy"
        return "#16A34A","s-green","Normal"
    except (TypeError, ValueError):
        # Fallback if a status string is passed
        if occ_or_status == "Red":   return "#DC2626","s-red","Very Busy"
        if occ_or_status == "Amber": return "#D97706","s-amber","Busy"
        return "#16A34A","s-green","Normal"

def get_hospitals_for_age(county, age):
    all_hosps = HOSPITAL_MAP.get(county, [])
    if "Under 5" in age or "5" in age and "15" in age:
        chi    = [h for h in all_hosps if "CHI" in h]
        others = [h for h in all_hosps if "CHI" not in h]
        note   = "Children's Health Ireland (CHI) hospitals are specifically equipped for paediatric emergencies. CHI hospitals are listed first."
        return chi + others, note
    elif "65+" in age:
        adult_hosps = [h for h in all_hosps if "CHI" not in h]
        note = "All adult hospitals listed. Ask about the FITT (Frailty Intervention Therapy Team) service when you arrive."
        return adult_hosps, note
    else:
        # Adults and young adults — never show CHI hospitals
        adult_hosps = [h for h in all_hosps if "CHI" not in h]
        return adult_hosps, None

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

@st.cache_data
def load_gp():
    try:
        df = pd.read_csv(
            "https://raw.githubusercontent.com/125109486-dev/Health-Flow-Datasets-Code/refs/heads/main/gp_out_of_hours.csv",
            encoding="latin-1", header=1
        )
        df = df[["Name","Address","Opening Hours","Day"]].dropna(subset=["Name"])
        df.columns = ["name","address","hours","days"]
        return df
    except Exception:
        return pd.DataFrame()

@st.cache_data
def load_miu():
    try:
        df = pd.read_csv(
            "https://raw.githubusercontent.com/125109486-dev/Health-Flow-Datasets-Code/refs/heads/main/minor_injury_units.csv",
            encoding="latin-1"
        )
        df.columns = [c.replace("\ufeff","").replace("ï»¿","").strip() for c in df.columns]
        df = df[["County","Name","Address","Hours","Days","Ages"]].dropna(subset=["Name"])
        df.columns = ["county","name","address","hours","days","ages"]
        return df
    except Exception:
        return pd.DataFrame()


master    = load_master()
synthetic = load_synthetic()
latest_syn = synthetic.sort_values("date").groupby("Hospital").last().reset_index()
gp_df  = load_gp()
miu_df = load_miu()

def occ_to_status(occ):
    """Derive RAG status from occupancy rate."""
    try:
        occ = float(occ)
    except (TypeError, ValueError):
        return "Green"
    if occ >= 8:   return "Red"
    elif occ >= 4: return "Amber"
    return "Green"

def get_hosp_data(hospital_name):
    row = master[master["Hospital"].str.lower().str.contains(hospital_name.lower().split()[0], na=False)]
    if not row.empty:
        r   = row.iloc[0]
        occ = float(r["Occupancy_Rate_pct"]) if pd.notna(r["Occupancy_Rate_pct"]) else 5.0
        troll = int(r["Daily_Total"]) if pd.notna(r["Daily_Total"]) else 0
        bis   = r["Behavioural_Impact_Score"]
        # Derive status from occupancy — don't trust stale Traffic_Light_Status field
        status = occ_to_status(occ)
        return occ, status, troll, bis
    row2 = latest_syn[latest_syn["Hospital"].str.lower().str.contains(hospital_name.lower().split()[0], na=False)]
    if not row2.empty:
        r2    = row2.iloc[0]
        occ   = float(r2["occupancy_rate_pct"]) if pd.notna(r2["occupancy_rate_pct"]) else 5.0
        troll = int(r2["total_trolleys"]) if pd.notna(r2.get("total_trolleys", 0)) else 0
        bis   = float(r2.get("behavioural_impact_score", 0))
        status = occ_to_status(occ)
        return occ, status, troll, bis
    return 5.0, "Green", 0, 0.0

latest_syn["derived_status"] = latest_syn["occupancy_rate_pct"].apply(occ_to_status)
red_c = int((latest_syn["derived_status"]=="Red").sum())
amb_c = int((latest_syn["derived_status"]=="Amber").sum())
grn_c = int((latest_syn["derived_status"]=="Green").sum())

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
    <div style="text-align:center;font-size:24px;font-weight:700;color:#0D2137;margin:1.5rem 0 4px 0">
        Tell us about yourself to get started
    </div>
    <div style="text-align:center;font-size:18px;color:#64748B;margin-bottom:1.2rem">
        We will personalise your experience based on your location and age
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([0.5, 3, 0.5])
    with col2:
        st.markdown("<div style='font-size:20px;font-weight:600;color:#0D2137;margin-bottom:6px'>Which county are you in?</div>", unsafe_allow_html=True)
        county_land = st.selectbox("", list(HOSPITAL_MAP.keys()), label_visibility="collapsed")
        age_opts = ["Under 5 — Infant / Toddler","5–15 — Child",
                    "16–25 — Young Adult","26–64 — Adult","65+ — Senior"]
        st.markdown("<div style='font-size:20px;font-weight:600;color:#0D2137;margin-bottom:6px'>What is the patient's age group?</div>", unsafe_allow_html=True)
        age_land = st.selectbox("", age_opts, index=3, label_visibility="collapsed")
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
    pass
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
            <span class="pill">🟢 Normal: {grn_c}</span>
            <span class="pill">🟡 Busy: {amb_c}</span>
            <span class="pill">🔴 Very Busy: {red_c}</span>
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
        rc, sc, rl = rag_meta(occ)
        dot_col = {"Red":"#DC2626","Amber":"#D97706","Green":"#16A34A"}.get(status,"#94A3B8")
        cap_pct = min(int(occ*10), 100)
        cap_col = {"Red":"#DC2626","Amber":"#D97706","Green":"#16A34A"}.get(status,"#16A34A")
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

    # Important Update
    st.markdown("""
    <div class="update-card">
        <span class="important-badge">Important Updates</span>
        <span style="font-size:13px;color:#6b7280;margin-left:8px">Updated February 22, 2026</span>
        <div style="background:white;border-radius:8px;padding:14px;font-size:15px;
                    color:#374151;line-height:1.7;margin-top:10px">
            Over the next <strong>1–4 weeks</strong> we expect ED attendances to go up by
            <strong style="color:#F59E0B">15–20%</strong> based on seasonal triggers and previous data.
            Therefore, we would <strong>strongly advise people to only come to the ED if very necessary</strong>
            and are advised by their GP.
        </div>
    </div>""", unsafe_allow_html=True)

    # UVC Card
    st.markdown("""
    <div class="uvc-card">
        <div style="font-size:16px;font-weight:700;margin-bottom:10px">Urgent Virtual Care (UVC) Success</div>
        <div style="font-size:14px;opacity:0.9;line-height:1.6;margin-bottom:14px">
            Our Urgent Virtual Care service has successfully managed over <strong>8,450 cases</strong>
            in the past month without requiring ED visits, helping reduce waiting times for critical emergencies.
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:16px">
            <div style="background:rgba(0,0,0,0.2);border-radius:8px;padding:14px">
                <div style="font-size:12px;opacity:0.8;margin-bottom:4px">Cases Resolved</div>
                <div style="font-size:22px;font-weight:700">8,450+</div>
            </div>
            <div style="background:rgba(0,0,0,0.2);border-radius:8px;padding:14px">
                <div style="font-size:12px;opacity:0.8;margin-bottom:4px">Avg Wait Time</div>
                <div style="font-size:22px;font-weight:700">12 mins</div>
            </div>
        </div>
        <div style="font-size:13px;font-weight:600;opacity:0.9;margin-bottom:8px">Alternative Options</div>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px">
            <div style="background:rgba(255,255,255,0.15);border-radius:8px;padding:10px;text-align:center">
                <div style="font-size:11px;opacity:0.8;margin-bottom:4px">Contact your GP first</div>
                <div style="font-size:13px;font-weight:600">GP Services</div>
            </div>
            <div style="background:rgba(255,255,255,0.15);border-radius:8px;padding:10px;text-align:center">
                <div style="font-size:11px;opacity:0.8;margin-bottom:4px">Minor Injuries</div>
                <div style="font-size:13px;font-weight:600">Visit an Injury Unit</div>
            </div>
            <div style="background:rgba(255,255,255,0.15);border-radius:8px;padding:10px;text-align:center">
                <div style="font-size:11px;opacity:0.8;margin-bottom:4px">Virtual Care</div>
                <div style="font-size:13px;font-weight:600">Try UVC Service</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    # Personalised recommendation
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
            <div style="font-size:14px;color:#6b7280">
                A&E visits are free with a valid GP referral letter. No insurance required.
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div style="color:#0D9488;font-size:12px;font-weight:700;letter-spacing:0.06em;margin:16px 0 6px 0">STEP 2 OF 2</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:18px;font-weight:700;color:#0D2137;margin-bottom:6px">Why are you considering attending A&E?</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:15px;color:#64748B;margin-bottom:14px">Select the option that best describes your situation. We will show you the most appropriate care pathway.</div>', unsafe_allow_html=True)

    URGENCY_OPTIONS = [
        ("Chest Pain or Breathing Difficulty",     "Tightness, pressure, shortness of breath",        "life",     "#FFF1F2","#DC2626"),
        ("Stroke Symptoms",                        "Face drooping, arm weakness, speech difficulty",   "life",     "#FFF1F2","#DC2626"),
        ("Severe Injury or Uncontrolled Bleeding", "Major trauma, deep wound, broken bones",           "life",     "#FFF1F2","#DC2626"),
        ("Collapsed, unconscious, or seizure",     "Loss of consciousness, fitting",                   "life",     "#FFF1F2","#DC2626"),
        ("Severe Allergic Reaction",               "Swelling of face, lips or throat, wheezing",       "life",     "#FFF1F2","#DC2626"),
        ("Minor Injury",                           "Sprain, small cut, minor burn, possible fracture", "moderate", "#FFFBEB","#D97706"),
        ("Stomach / Abdominal Pain",               "Cramps, nausea, vomiting, indigestion",            "moderate", "#FFFBEB","#D97706"),
        ("Moderate Illness",                       "Skin infection, fever, moderate pain",             "moderate", "#FFFBEB","#D97706"),
        ("Minor — can wait or self-manage",        "Cold sore, rash, UTI",                             "minor",    "#F0FDF4","#16A34A"),
        ("Child Illness / High Fever",             "Unwell child, persistent high temperature",        "life",     "#FFF1F2","#DC2626"),
        ("Not Sure / Something Else",              "Something else / Not listed above",                "minor",    "#F8FAFC","#64748B"),
    ]

    if "sel_urgency" not in st.session_state:
        st.session_state.sel_urgency = URGENCY_OPTIONS[0][0]

    urg_cols = st.columns(2)
    for idx, (ti, sub, ut, bg, bc) in enumerate(URGENCY_OPTIONS):
        is_sel      = (st.session_state.sel_urgency == ti)
        dot         = "🔴" if ut == "life" else ("🟡" if ut == "moderate" else "🟢")
        card_bg     = bg if is_sel else "white"
        card_border = bc if is_sel else "#E2E8F0"
        card_weight = "700" if is_sel else "500"
        with urg_cols[idx % 2]:
            if st.button(
                dot + "  " + ti + "\n" + sub,
                key="urg_" + str(idx),
                use_container_width=True,
                type="primary" if is_sel else "secondary"
            ):
                st.session_state.sel_urgency = ti
                st.rerun()

    sel_urg = st.session_state.sel_urgency
    urgency_type = "minor"
    sel_bc  = "#0D9488"
    sel_sub = ""
    for ti, sub, ut, bg, bc in URGENCY_OPTIONS:
        if ti == sel_urg:
            urgency_type = ut
            sel_bc  = bc
            sel_sub = sub
            break

    st.markdown(
        "<div style='background:white;border-left:4px solid " + sel_bc + ";"
        "border-radius:8px;padding:12px 16px;margin:8px 0 16px 0;border:1px solid #E2E8F0'>"
        "<strong style='color:" + sel_bc + ";font-size:15px'>" + sel_urg + "</strong><br>"
        "<span style='font-size:13px;color:#64748B'>" + sel_sub + "</span></div>",
        unsafe_allow_html=True
    )

    occ, status, troll, bis = get_hosp_data(sel_hosp)
    rc, sc, rl = rag_meta(occ)
    pathway, path_c, path_desc = get_pathway(occ, urgency_type)

    st.markdown(f"""
    <div class="rec-card" style="border-left:5px solid {path_c}">
        <div style="color:{path_c};font-size:12px;font-weight:700;margin-bottom:6px;letter-spacing:0.05em">
            RECOMMENDED CARE PATHWAY
        </div>
        <div style="font-size:20px;font-weight:700;color:{path_c}">{pathway}</div>
        <div style="font-size:15px;color:#374151;margin-top:10px;line-height:1.7">{path_desc}</div>
        <div style="margin-top:14px;padding-top:12px;border-top:1px solid #F1F5F9;font-size:13px;color:#94A3B8">
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

    symptoms = [
        (1,  "Chest pain or chest tightness",            "Especially if crushing, radiating, or associated with sweating or nausea"),
        (2,  "Sudden shortness of breath",               "Could indicate respiratory failure, pulmonary embolism, or cardiac issues"),
        (3,  "Sudden weakness, numbness, or paralysis",  "Especially one-sided — possible stroke"),
        (4,  "Altered level of consciousness",           "Confusion, collapse, fainting, or unresponsiveness"),
        (5,  "Severe allergic reaction",                 "Facial/lip/tongue swelling, wheezing, difficulty breathing"),
        (6,  "Uncontrolled bleeding",                    "External or suspected internal bleeding"),
        (7,  "Severe abdominal pain",                    "Especially with rigidity, fever, or vomiting"),
        (8,  "High fever with signs of infection",       "Fever + confusion, rapid heart rate, low blood pressure (possible sepsis)"),
        (9,  "Persistent seizures or first-time seizure","Especially if lasting more than 5 minutes"),
        (10, "Severe headache of sudden onset",          "Sudden, intense headache unlike any experienced before"),
    ]
    symptoms_html = ""
    for num, title, desc in symptoms:
        symptoms_html += (
            "<div style='background:white;border:1px solid #FECDD3;border-radius:10px;"
            "padding:16px;display:flex;gap:14px;align-items:flex-start'>"
            "<div style='background:#FFF1F2;min-width:36px;height:36px;border-radius:8px;"
            "display:flex;align-items:center;justify-content:center;"
            "font-size:15px;font-weight:700;color:#DC2626'>" + str(num) + "</div>"
            "<div><div style='font-size:15px;font-weight:600;color:#0D2137;margin-bottom:4px'>" + title + "</div>"
            "<div style='font-size:13px;color:#64748B;line-height:1.5'>" + desc + "</div></div>"
            "</div>"
        )
    st.markdown(
        "<div style='background:#FFF1F2;border-radius:12px;padding:20px;margin-bottom:16px'>"
        "<div style='display:flex;align-items:center;gap:14px;margin-bottom:16px'>"
        "<div style='background:#DC2626;width:48px;height:48px;border-radius:12px;"
        "display:flex;align-items:center;justify-content:center;color:white;font-size:20px;flex-shrink:0'>!</div>"
        "<div><div style='font-size:17px;font-weight:700;color:#0D2137;margin-bottom:6px'>"
        "10 Critical Symptoms Requiring Immediate Review</div>"
        "<a href='tel:999' style='background:#DC2626;color:white;padding:6px 14px;"
        "border-radius:6px;font-size:12px;font-weight:700;text-decoration:none;margin-right:10px'>"
        "CALL 999 IMMEDIATELY</a>"
        "<span style='font-size:12px;color:#64748B'>Call emergency services right away</span>"
        "</div></div>"
        "<div style='display:grid;grid-template-columns:1fr 1fr;gap:10px'>"
        + symptoms_html +
        "</div></div>",
        unsafe_allow_html=True
    )


    st.divider()
    col_sv1, col_sv2 = st.columns(2)
    with col_sv1:
        if st.button("Leave Feedback on this Recommendation", use_container_width=True):
            st.session_state.page = "Survey"
            st.rerun()
    with col_sv2:
        pass

    st.markdown('<div class="sec-title">Concierge Notification</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:15px;color:#64748B;margin-bottom:10px">Register to be notified when wait times drop at your preferred hospital.</div>', unsafe_allow_html=True)
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

    # Where Should I Go
    st.markdown('<div class="sec-title">Where Should I Go?</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:15px;color:#64748B;margin-bottom:16px">A quick guide to choosing the right care for your situation</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background:white;border-radius:12px;padding:24px;border:1px solid #E2E8F0;text-align:center;height:100%">
            <div style="width:56px;height:56px;background:#DCFCE7;border-radius:50%;
                        display:flex;align-items:center;justify-content:center;
                        margin:0 auto 14px auto;font-size:24px">1</div>
            <div style="color:#16A34A;font-size:11px;font-weight:700;letter-spacing:0.08em;margin-bottom:8px">STEP 1 — TRY FIRST</div>
            <div style="font-size:17px;font-weight:700;color:#0D2137;margin-bottom:10px">Your Pharmacist</div>
            <div style="font-size:14px;color:#64748B;line-height:1.6">
                For UTIs, cold sores, hay fever, shingles, minor skin conditions, and more — no appointment needed.
            </div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background:white;border-radius:12px;padding:24px;border:1px solid #E2E8F0;text-align:center;height:100%">
            <div style="width:56px;height:56px;background:#EFF6FF;border-radius:50%;
                        display:flex;align-items:center;justify-content:center;
                        margin:0 auto 14px auto;font-size:24px">2</div>
            <div style="color:#2563EB;font-size:11px;font-weight:700;letter-spacing:0.08em;margin-bottom:8px">STEP 2 — IF NEEDED</div>
            <div style="font-size:17px;font-weight:700;color:#0D2137;margin-bottom:10px">Your GP</div>
            <div style="font-size:14px;color:#64748B;line-height:1.6">
                For illness requiring diagnosis, ongoing conditions, referrals, or anything your pharmacist cannot manage.
            </div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="background:white;border-radius:12px;padding:24px;border:1px solid #E2E8F0;text-align:center;height:100%">
            <div style="width:56px;height:56px;background:#FFF1F2;border-radius:50%;
                        display:flex;align-items:center;justify-content:center;
                        margin:0 auto 14px auto;font-size:24px">3</div>
            <div style="color:#DC2626;font-size:11px;font-weight:700;letter-spacing:0.08em;margin-bottom:8px">STEP 3 — EMERGENCY ONLY</div>
            <div style="font-size:17px;font-weight:700;color:#0D2137;margin-bottom:10px">ED / Call 999</div>
            <div style="font-size:14px;color:#64748B;line-height:1.6">
                Life-threatening symptoms, major trauma, or when advised by a clinician.
            </div>
        </div>""", unsafe_allow_html=True)

    st.divider()

    # Primary Care Services
    st.markdown('<div class="sec-title">Primary Care Services</div>', unsafe_allow_html=True)

    res_county = st.session_state.get("landing_county", "")

    # Out of hours mapping
    if res_county in ["Dublin", "Kildare", "Wicklow", "Meath", "Louth"]:
        ooh_services = [("NowDoc (Dublin & Leinster)", "1850 592 0900", "tel:18505920900", "https://www.nowdoc.ie")]
    elif res_county in ["Cork", "Kerry"]:
        ooh_services = [("SouthDoc (Cork & Kerry)", "0818 355 999", "tel:0818355999", "https://www.southdoc.ie")]
    elif res_county in ["Limerick", "Tipperary", "Clare", "Galway", "Mayo", "Roscommon", "Sligo", "Leitrim"]:
        ooh_services = [("ShanDoc (Shannon & West)", "1850 777 911", "tel:1850777911", "https://www.shandoc.ie")]
    elif res_county in ["Donegal", "Cavan", "Monaghan"]:
        ooh_services = [("NorthDoc (North West)", "0818 000 003", "tel:0818000003", "https://www.northdoc.ie")]
    elif res_county in ["Waterford", "Wexford", "Kilkenny", "Carlow", "Tipperary"]:
        ooh_services = [("Caredoc (South East)", "0818 300 365", "tel:0818300365", "https://www.caredoc.ie")]
    elif res_county in ["Longford", "Westmeath", "Offaly", "Laois", "Portlaoise", "Tullamore", "Mullingar"]:
        ooh_services = [("Midlands Doc (Midlands)", "0818 123 456", "tel:0818123456", "https://www.hse.ie/eng/services/list/3/primarycare/outofhours.html")]
    else:
        ooh_services = [
            ("NowDoc (Dublin)", "1850 592 0900", "tel:18505920900", "https://www.nowdoc.ie"),
            ("SouthDoc (Cork & Kerry)", "0818 355 999", "tel:0818355999", "https://www.southdoc.ie"),
            ("ShanDoc (Shannon & West)", "1850 777 911", "tel:1850777911", "https://www.shandoc.ie"),
            ("Caredoc (South East)", "0818 300 365", "tel:0818300365", "https://www.caredoc.ie"),
        ]

    ooh_html = ""
    for name, number, tel_link, web_link in ooh_services:
        ooh_html += (
            "<div style='background:#F8FAFC;border-radius:8px;padding:14px;margin-bottom:8px'>"
            "<div style='font-size:14px;color:#64748B;margin-bottom:6px'>" + name + "</div>"
            "<a href='" + tel_link + "' style='font-size:16px;font-weight:700;color:#0D9488;text-decoration:none;display:block;margin-bottom:6px'>" + number + "</a>"
            "<a href='" + web_link + "' target='_blank' style='font-size:13px;color:#2563EB;text-decoration:none;font-weight:500'>Visit website</a>"
            "</div>"
        )
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            "<div style='background:white;border-radius:12px;padding:24px;border:1px solid #E2E8F0;height:100%'>"
            "<div style='display:flex;align-items:center;gap:12px;margin-bottom:14px'>"
            "<div style='background:#CCFBF1;width:48px;height:48px;border-radius:10px;"
            "display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0'>+</div>"
            "<div style='font-size:17px;font-weight:700;color:#0D2137'>GP Services</div></div>"
            "<div style='font-size:15px;color:#374151;line-height:1.7;margin-bottom:14px'>"
            "Your GP is your first point of contact for non-emergency medical issues. "
            "They can assess, treat, and refer you if needed.</div>"
            "<div style='font-size:14px;color:#0D9488;margin-bottom:6px'>Mon-Fri: 9am – 5pm (typical)</div>"
            "<div style='font-size:14px;color:#64748B;margin-bottom:14px'>Find your nearest GP practice</div>"
            "<a href='https://www.google.com/maps/search/GP+doctor+near+me' target='_blank'"
            " style='display:block;border:1px solid #E2E8F0;border-radius:8px;padding:10px;"
            "text-align:center;font-size:14px;font-weight:600;color:#0D2137;text-decoration:none'>"
            "Find a GP Near Me</a>"
            "</div>",
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            "<div style='background:white;border-radius:12px;padding:24px;border:1px solid #E2E8F0;height:100%'>"
            "<div style='display:flex;align-items:center;gap:12px;margin-bottom:14px'>"
            "<div style='background:#EFF6FF;width:48px;height:48px;border-radius:10px;"
            "display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0'>*</div>"
            "<div style='font-size:17px;font-weight:700;color:#0D2137'>Out-of-Hours GP</div></div>"
            "<div style='font-size:15px;color:#374151;line-height:1.7;margin-bottom:14px'>"
            "When your GP surgery is closed, out-of-hours services provide urgent medical care.</div>"
            + ooh_html +
            "<div style='font-size:14px;color:#64748B'>Available evenings, nights &amp; weekends</div>"
            "</div>",
            unsafe_allow_html=True
        )

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            "<div style='background:white;border-radius:12px;padding:24px;border:1px solid #E2E8F0;height:100%'>"
            "<div style='display:flex;align-items:center;gap:12px;margin-bottom:14px'>"
            "<div style='background:#FEF3C7;width:48px;height:48px;border-radius:10px;"
            "display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0'>!</div>"
            "<div style='font-size:17px;font-weight:700;color:#0D2137'>Minor Injury Units</div></div>"
            "<div style='font-size:15px;color:#374151;line-height:1.7;margin-bottom:14px'>"
            "Treatment for minor injuries like sprains, cuts, burns, and fractures without ED wait times.</div>"
            "<a href='https://www.google.com/maps/search/minor+injury+unit+near+me' target='_blank'"
            " style='display:block;border:1px solid #E2E8F0;border-radius:8px;padding:10px;"
            "text-align:center;font-size:14px;font-weight:600;color:#0D2137;text-decoration:none'>"
            "Find Nearest Minor Injury Unit</a>"
            "</div>",
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            "<div style='background:white;border-radius:12px;padding:24px;border:1px solid #E2E8F0;height:100%'>"
            "<div style='display:flex;align-items:center;gap:12px;margin-bottom:14px'>"
            "<div style='background:#FAF5FF;width:48px;height:48px;border-radius:10px;"
            "display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0'>P</div>"
            "<div style='font-size:17px;font-weight:700;color:#0D2137'>Pharmacy Services</div></div>"
            "<div style='font-size:15px;color:#374151;line-height:1.7;margin-bottom:14px'>"
            "Pharmacists can provide advice and treatment for minor ailments without a prescription.</div>"
            "<a href='https://www.google.com/maps/search/pharmacy+near+me' target='_blank'"
            " style='display:block;border:1px solid #E2E8F0;border-radius:8px;padding:10px;"
            "text-align:center;font-size:14px;font-weight:600;color:#0D2137;text-decoration:none'>"
            "Find Nearest Pharmacy</a>"
            "</div>",
            unsafe_allow_html=True
        )

    st.divider()

    # Pharmacy First
    st.markdown('<div class="sec-title">Pharmacy First — Skip the GP Queue</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#F0FDF4;border-radius:12px;padding:20px;margin-bottom:16px">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px">
            <span style="background:#0D9488;color:white;font-size:12px;font-weight:600;
                         padding:3px 10px;border-radius:4px">HSE Scheme</span>
        </div>
        <div style="font-size:15px;color:#374151;line-height:1.7;margin-bottom:12px">
            Under the HSE expanded pharmacy services, pharmacists across Ireland can now
            <strong>assess, advise, and in some cases prescribe</strong> for a range of common conditions
            without you needing a GP appointment first.
        </div>
        <div style="background:white;border:1px solid #BBFDD8;border-radius:8px;padding:14px;
                    font-size:14px;color:#374151;line-height:1.6">
            Walk into any participating pharmacy. No appointment necessary.
            GMS/medical card holders may be entitled to free treatment.
        </div>
    </div>""", unsafe_allow_html=True)

    pharmacy_conditions = [
        ("Urinary Tract Infection (UTI)", "Uncomplicated UTIs in women aged 16–64 can be assessed and treated with antibiotics directly by your pharmacist.", "Women only. No referral needed."),
        ("Cold Sores (Herpes Labialis)", "Antiviral creams and oral antivirals for cold sores are available from your pharmacist without a prescription.", None),
        ("Shingles", "Pharmacists can supply antiviral treatment for shingles. Early treatment (within 72 hours of rash) is most effective.", "Start treatment as early as possible."),
        ("Impetigo", "A common bacterial skin infection. Pharmacists can assess and supply appropriate antibiotic treatment.", None),
        ("Hay Fever & Allergic Rhinitis", "Antihistamines, nasal sprays, and eye drops are available directly from pharmacists for seasonal and year-round allergy symptoms.", None),
        ("Emergency Contraception", "The morning-after pill is available directly from pharmacists without a prescription, including out of hours.", None),
        ("Head Lice", "Assessment and treatment for head lice infestations, including medicated lotions and wet-combing advice.", None),
        ("Athlete's Foot & Fungal Infections", "Antifungal creams and treatments are available directly from pharmacists for skin, nail, and mouth fungal infections.", None),
        ("Minor Skin Conditions", "Eczema flares, mild acne, rashes, and insect bites can often be managed with products recommended by your pharmacist.", None),
        ("Coughs, Colds & Sore Throats", "Symptom relief and advice for common respiratory infections. Pharmacists can rule out anything that needs further care.", None),
        ("Indigestion & Heartburn", "Antacids, H2 blockers, and lifestyle advice for acid reflux and indigestion are available without a prescription.", None),
        ("Threadworms", "Mebendazole and hygiene advice for threadworm infections in adults and children over 2 years.", None),
    ]

    cols = st.columns(2)
    for i, (title, desc, note) in enumerate(pharmacy_conditions):
        note_html = (f"<div style='margin-top:8px;background:#F0FDF4;border:1px solid #BBFDD8;"
                     f"border-radius:20px;padding:4px 10px;font-size:12px;color:#16A34A;"
                     f"display:inline-block'>{note}</div>") if note else ""
        with cols[i % 2]:
            st.markdown(
                f"<div style='background:white;border:1px solid #D1FAE5;border-radius:10px;"
                f"padding:16px;margin-bottom:12px'>"
                f"<div style='font-size:15px;font-weight:600;color:#0D2137;margin-bottom:6px'>{title}</div>"
                f"<div style='font-size:13px;color:#64748B;line-height:1.5'>{desc}</div>"
                f"{note_html}</div>",
                unsafe_allow_html=True
            )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <a href="https://www.hse.ie/eng/health/az/p/pharmacy-services/" target="_blank"
           style="display:block;background:#0D9488;color:white;text-align:center;padding:14px;
                  border-radius:10px;font-size:15px;font-weight:600;text-decoration:none;margin-top:8px">
            Find a Participating Pharmacy Near You
        </a>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <a href="https://www.hse.ie/eng/" target="_blank"
           style="display:block;background:white;color:#0D9488;text-align:center;padding:14px;
                  border-radius:10px;font-size:15px;font-weight:600;text-decoration:none;
                  border:2px solid #0D9488;margin-top:8px">
            Learn More on HSE.ie
        </a>""", unsafe_allow_html=True)

    st.divider()

    # GP Out of Hours from data
    st.markdown('<div class="sec-title">GP Out-of-Hours Services Near You</div>', unsafe_allow_html=True)
    res_county = st.session_state.get("landing_county", None)
    if not res_county:
        res_county = st.selectbox(
            "Select your county to see local services",
            [""] + sorted(["Carlow","Cavan","Clare","Cork","Donegal","Dublin","Galway",
                "Kerry","Kildare","Kilkenny","Laois","Leitrim","Limerick",
                "Longford","Louth","Mayo","Meath","Monaghan","Offaly",
                "Roscommon","Sligo","Tipperary","Waterford","Westmeath","Wexford","Wicklow"]),
            key="resources_county"
        )
    else:
        st.markdown(
            f"<div style='background:#CCFBF1;border:1px solid #0D9488;border-radius:8px;"
            f"padding:12px 16px;margin-bottom:1rem;font-size:15px;color:#0D2137;'>"
            f"Showing services for <strong>{res_county}</strong></div>",
            unsafe_allow_html=True
        )

    if not gp_df.empty:
        st.markdown('<div style="font-size:14px;color:#64748B;margin-bottom:8px">Showing all GP out-of-hours services — use the geographic guide above to find yours.</div>', unsafe_allow_html=True)
        for _, row in gp_df.head(10).iterrows():
            st.markdown(
                "<div class='resource-card'><div class='resource-title'>" + str(row['name']) + "</div>"
                "<div class='resource-desc'>" + str(row['address']) + "</div>"
                "<div style='font-size:14px;color:#374151;'>" + str(row['hours']) + " · " + str(row['days']) + "</div></div>",
                unsafe_allow_html=True
            )
    else:
        st.info("GP out-of-hours data is currently unavailable.")

    # Minor Injury Units from data
    st.markdown('<div class="sec-title">Minor Injury Units Near You</div>', unsafe_allow_html=True)
    if not miu_df.empty and res_county:
        county_miu = miu_df[miu_df["county"].str.strip().str.lower() == res_county.strip().lower()]
        if len(county_miu) > 0:
            mcols = st.columns(min(len(county_miu), 2))
            for i, (_, row) in enumerate(county_miu.iterrows()):
                with mcols[i % 2]:
                    st.markdown(
                        f"<div class='resource-card'><div class='resource-title'>{row['name']}</div>"
                        f"<div class='resource-desc'>{row['address']}</div>"
                        f"<div style='font-size:14px;color:#374151;margin-bottom:3px;'>{row['hours']}</div>"
                        f"<div style='font-size:14px;color:#374151;margin-bottom:3px;'>{row['days']}</div>"
                        f"<div style='font-size:14px;color:#0D9488;font-weight:600;'>Ages: {row['ages']}</div></div>",
                        unsafe_allow_html=True
                    )
        else:
            st.markdown(
                f"<div style='background:#FEF9C3;border:1px solid #FDE68A;border-radius:8px;"
                f"padding:14px;font-size:15px;color:#374151;'>No Minor Injury Unit in <strong>{res_county}</strong>. "
                f"See <a href='https://www.hse.ie/eng/services/list/3/injuryunits/' target='_blank' "
                f"style='color:#0D9488;'>HSE Injury Units</a> for the full national list.</div>",
                unsafe_allow_html=True
            )
    else:
        st.info("Select your county above to see local Minor Injury Units.")

    st.divider()

    # Mental Health
    st.markdown('<div class="sec-title">Mental Health Support</div>', unsafe_allow_html=True)
    mh_col1, mh_col2, mh_col3 = st.columns(3)
    for col, (title, desc, contact, link) in zip(
        [mh_col1, mh_col2, mh_col3],
        [
            ("Samaritans",  "24/7 emotional support for anyone in distress",          "116 123 (Free)",      "tel:116123"),
            ("Pieta House", "Free therapy for those in suicidal distress or self-harm","1800 247 247",        "tel:1800247247"),
            ("Text 50808",  "24/7 anonymous text support service",                    "Text HELLO to 50808", "sms:50808"),
        ]
    ):
        with col:
            st.markdown(
                f"<div style='background:white;border-radius:12px;padding:20px;border:1px solid #E2E8F0;text-align:center'>"
                f"<div style='background:#FFF1F2;width:48px;height:48px;border-radius:10px;"
                f"margin:0 auto 14px auto;display:flex;align-items:center;justify-content:center;font-size:20px;color:#DC2626'>+</div>"
                f"<div style='font-size:16px;font-weight:700;color:#0D2137;margin-bottom:8px'>{title}</div>"
                f"<div style='font-size:13px;color:#64748B;line-height:1.5;margin-bottom:14px'>{desc}</div>"
                f"<a href='{link}' style='color:#DC2626;font-size:15px;font-weight:600;text-decoration:none'>{contact}</a>"
                f"</div>",
                unsafe_allow_html=True
            )

    st.divider()

    # Digital Resources
    st.markdown('<div class="sec-title">Digital Resources</div>', unsafe_allow_html=True)
    dr_col1, dr_col2, dr_col3 = st.columns(3)
    digital = [
        ("HSE Health App",       "Access health information and services on the go",   "Download", "https://www.hse.ie/eng/", "#0D9488"),
    ]
    for col, (title, desc, cta, link, colour) in zip([dr_col1, dr_col2, dr_col3], digital):
        with col:
            st.markdown(
                f"<div style='background:white;border-radius:12px;padding:20px;border:1px solid #E2E8F0;text-align:center'>"
                f"<div style='background:#F0FDF4;width:56px;height:56px;border-radius:12px;"
                f"margin:0 auto 14px auto;display:flex;align-items:center;justify-content:center;"
                f"font-size:22px;color:{colour}'>D</div>"
                f"<div style='font-size:16px;font-weight:700;color:#0D2137;margin-bottom:8px'>{title}</div>"
                f"<div style='font-size:13px;color:#64748B;line-height:1.5;margin-bottom:14px'>{desc}</div>"
                f"<a href='{link}' target='_blank' style='background:{colour};color:white;padding:8px 20px;"
                f"border-radius:20px;font-size:13px;font-weight:600;text-decoration:none'>{cta}</a>"
                f"</div>",
                unsafe_allow_html=True
            )

    st.divider()

    # HSE Information Services
    st.markdown('<div class="sec-title">HSE Information Services</div>', unsafe_allow_html=True)
    hi_col1, hi_col2 = st.columns(2)
    with hi_col1:
        st.markdown("""
        <div style="background:white;border-radius:12px;padding:20px;border:1px solid #E2E8F0">
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px">
                <div style="background:#CCFBF1;width:40px;height:40px;border-radius:8px;
                            display:flex;align-items:center;justify-content:center;color:#0D9488;font-size:18px;flex-shrink:0">T</div>
                <div style="font-size:17px;font-weight:700;color:#0D2137">HSE Live</div>
            </div>
            <div style="font-size:14px;color:#374151;margin-bottom:12px">
                Get information about health services and entitlements
            </div>
            <div style="background:#F8FAFC;border-radius:8px;padding:12px">
                <a href="tel:1850241850" style="font-size:16px;font-weight:700;color:#0D9488;text-decoration:none;display:block;margin-bottom:4px">1850 24 1850</a>
                <div style="font-size:13px;color:#64748B">Mon-Fri: 8am – 8pm</div>
            </div>
        </div>""", unsafe_allow_html=True)
    with hi_col2:
        st.markdown("""
        <div style="background:white;border-radius:12px;padding:20px;border:1px solid #E2E8F0">
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px">
                <div style="background:#CCFBF1;width:40px;height:40px;border-radius:8px;
                            display:flex;align-items:center;justify-content:center;color:#0D9488;font-size:18px;flex-shrink:0">i</div>
                <div style="font-size:17px;font-weight:700;color:#0D2137">HSE.ie</div>
            </div>
            <div style="font-size:14px;color:#374151;margin-bottom:12px">
                Comprehensive health information and service directory
            </div>
            <a href="https://www.hse.ie" target="_blank"
               style="display:block;border:1px solid #E2E8F0;border-radius:8px;padding:10px;
                      text-align:center;font-size:14px;font-weight:600;color:#0D2137;text-decoration:none">
                Visit HSE.ie
            </a>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — SURVEY
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Survey":
    st.markdown("""
    <div class="hero">
        <div class="hero-title">Patient Feedback Survey</div>
        <div class="hero-sub">Help us improve HealthFlow — this takes less than a minute</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="survey-card">
        <div class="survey-title">Your Experience Today</div>
        <div class="survey-sub">
            This survey collects information about your condition, what action you took,
            and how satisfied you were with the recommendation you received.
            All responses are anonymous and used only to improve the service.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    with st.form("care_survey", clear_on_submit=True):
        st.markdown('<div style="font-size:17px;font-weight:700;color:#0D2137;margin-bottom:16px">About your condition</div>', unsafe_allow_html=True)

        q1 = st.selectbox("What condition or symptom brought you here today?", [
            "Select...",
            "Chest pain / breathing difficulty",
            "Fever / flu-like symptoms",
            "Injury (sprain, cut, burn)",
            "UTI / infection",
            "Mental health concern",
            "Abdominal / stomach pain",
            "Skin condition / rash",
            "Cold / sore throat / cough",
            "Child illness",
            "Other",
        ])

        q_age = st.selectbox("What age group applies to the patient?", [
            "Under 5 — Infant / Toddler",
            "5–15 — Child",
            "16–25 — Young Adult",
            "26–64 — Adult",
            "65+ — Senior",
        ], index=3)

        st.markdown('<div style="font-size:17px;font-weight:700;color:#0D2137;margin:20px 0 16px 0">What you did</div>', unsafe_allow_html=True)

        q2 = st.selectbox("What action did you actually take (or plan to take)?", [
            "Select...",
            "Called 999 / went to A&E",
            "Visited a Minor Injury Unit",
            "Contacted my GP",
            "Used GP out-of-hours service",
            "Used Urgent Virtual Care (UVC)",
            "Went to a pharmacy",
            "Stayed at home / self-managed",
            "Still deciding",
        ])

        st.markdown('<div style="font-size:17px;font-weight:700;color:#0D2137;margin:20px 0 16px 0">Your satisfaction</div>', unsafe_allow_html=True)

        q3 = st.select_slider(
            "How satisfied were you with the recommendation you received?",
            options=["Very Dissatisfied", "Dissatisfied", "Neutral", "Satisfied", "Very Satisfied"],
            value="Satisfied"
        )

        q4 = st.radio(
            "Did the recommendation match what you actually needed?",
            ["Yes, it was accurate",
             "Somewhat — I needed something slightly different",
             "No, I needed different advice"],
        )

        q5 = st.radio(
            "Would you use HealthFlow again?",
            ["Definitely yes", "Probably yes", "Not sure", "Probably not", "Definitely not"],
            horizontal=True
        )

        st.markdown('<div style="font-size:17px;font-weight:700;color:#0D2137;margin:20px 0 16px 0">Any other comments?</div>', unsafe_allow_html=True)
        q6 = st.text_area("", placeholder="Tell us how we can improve HealthFlow...", height=100, label_visibility="collapsed")

        submitted = st.form_submit_button("Submit Feedback", type="primary", use_container_width=True)

        if submitted and q1 != "Select..." and q2 != "Select...":
            st.markdown("""
            <div class="survey-thanks">
                <div style="font-size:24px;font-weight:700;color:#16A34A;margin-bottom:8px">Thank you for your feedback</div>
                <div style="font-size:16px;color:#374151;line-height:1.7">
                    Your response has been recorded and will help us improve HealthFlow for everyone in Ireland.
                </div>
            </div>
            """, unsafe_allow_html=True)
        elif submitted:
            st.warning("Please answer the first two questions before submitting.")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — CONTACT
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Contact":
    st.markdown("""
    <div class="hero">
        <div class="hero-title">Contact & Emergency Numbers</div>
        <div class="hero-sub">Important contacts for healthcare services across Ireland</div>
    </div>""", unsafe_allow_html=True)

    # 10 Critical Symptoms
    st.markdown("""
    <div style="background:#FFF1F2;border-radius:12px;padding:24px;margin-bottom:20px">
        <div style="display:flex;align-items:center;gap:14px;margin-bottom:16px">
            <div style="background:#DC2626;width:52px;height:52px;border-radius:12px;
                        display:flex;align-items:center;justify-content:center;
                        font-size:22px;flex-shrink:0;color:white">📞</div>
            <div>
                <div style="font-size:17px;font-weight:700;color:#0D2137;margin-bottom:6px">
                    10 Critical Symptoms Requiring Immediate Review
                </div>
                <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap">
                    <a href="tel:999" style="background:#DC2626;color:white;padding:6px 14px;
                       border-radius:6px;font-size:12px;font-weight:700;text-decoration:none;
                       letter-spacing:0.04em">CALL 999 IMMEDIATELY</a>
                    <span style="font-size:12px;color:#64748B">If you experience any of these symptoms, call emergency services right away</span>
                </div>
            </div>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">
    """, unsafe_allow_html=True)

    symptoms = [
        (1, "Chest pain or chest tightness",           "Especially if crushing, radiating, or associated with sweating or nausea"),
        (2, "Sudden shortness of breath",              "Could indicate respiratory failure, pulmonary embolism, or cardiac issues"),
        (3, "Sudden weakness, numbness, or paralysis", "Especially one-sided — possible stroke"),
        (4, "Altered level of consciousness",          "Confusion, collapse, fainting, or unresponsiveness"),
        (5, "Severe allergic reaction",                "Facial/lip/tongue swelling, wheezing, difficulty breathing"),
        (6, "Uncontrolled bleeding",                   "External or suspected internal bleeding"),
        (7, "Severe abdominal pain",                   "Especially with rigidity, fever, or vomiting"),
        (8, "High fever with signs of infection",      "Fever + confusion, rapid heart rate, low blood pressure (possible sepsis)"),
        (9, "Persistent seizures or first-time seizure","Especially if lasting more than 5 minutes"),
        (10,"Severe headache of sudden onset",         "Sudden, intense headache unlike any experienced before"),
    ]

    contact_symp_html = ""
    for num, title, desc in symptoms:
        contact_symp_html += (
            "<div style='background:white;border:1px solid #FECDD3;border-radius:10px;"
            "padding:16px;display:flex;gap:14px;align-items:flex-start'>"
            "<div style='background:#FFF1F2;min-width:36px;height:36px;border-radius:8px;"
            "display:flex;align-items:center;justify-content:center;"
            "font-size:15px;font-weight:700;color:#DC2626'>" + str(num) + "</div>"
            "<div><div style='font-size:15px;font-weight:600;color:#0D2137;margin-bottom:4px'>" + title + "</div>"
            "<div style='font-size:13px;color:#64748B;line-height:1.5'>" + desc + "</div></div>"
            "</div>"
        )
    st.markdown(
        "<div style='display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:16px'>"
        + contact_symp_html + "</div></div></div>",
        unsafe_allow_html=True
    )


    # Call 999 banner
    st.markdown("""
    <div style="background:#DC2626;border-radius:12px;padding:20px 24px;margin-bottom:20px;
                display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px">
        <div style="display:flex;align-items:center;gap:14px">
            <div style="font-size:22px;color:white">📞</div>
            <div>
                <div style="font-size:12px;color:rgba(255,255,255,0.8)">Emergency Services</div>
                <div style="font-size:26px;font-weight:700;color:white">Call 999</div>
            </div>
        </div>
        <div style="font-size:13px;color:rgba(255,255,255,0.85);max-width:400px;line-height:1.5">
            Do not delay if you experience any of these symptoms. Time is critical in emergency situations.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # GP / Out of Hours / Minor Injury cards
    # Geo-based out of hours
    contact_county = st.session_state.get("landing_county", "")
    if contact_county in ["Dublin", "Kildare", "Wicklow", "Meath", "Louth"]:
        ooh_name, ooh_num, ooh_tel, ooh_web = "NowDoc (Dublin & Leinster)", "1850 592 0900", "tel:18505920900", "https://www.nowdoc.ie"
    elif contact_county in ["Cork", "Kerry"]:
        ooh_name, ooh_num, ooh_tel, ooh_web = "SouthDoc (Cork & Kerry)", "0818 355 999", "tel:0818355999", "https://www.southdoc.ie"
    elif contact_county in ["Limerick", "Tipperary", "Clare", "Galway", "Mayo", "Roscommon", "Sligo", "Leitrim"]:
        ooh_name, ooh_num, ooh_tel, ooh_web = "ShanDoc (Shannon & West)", "1850 777 911", "tel:1850777911", "https://www.shandoc.ie"
    elif contact_county in ["Donegal", "Cavan", "Monaghan"]:
        ooh_name, ooh_num, ooh_tel, ooh_web = "NorthDoc (North West)", "0818 000 003", "tel:0818000003", "https://www.northdoc.ie"
    elif contact_county in ["Waterford", "Wexford", "Kilkenny", "Carlow"]:
        ooh_name, ooh_num, ooh_tel, ooh_web = "Caredoc (South East)", "0818 300 365", "tel:0818300365", "https://www.caredoc.ie"
    else:
        ooh_name, ooh_num, ooh_tel, ooh_web = "Out-of-Hours GP", "1850 777 911", "tel:1850777911", "https://www.hse.ie/eng/services/list/3/primarycare/outofhours.html"

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            "<div style='background:#EFF6FF;border:1px solid #BFDBFE;border-radius:12px;padding:20px;height:100%'>"
            "<div style='font-size:15px;font-weight:700;color:#1D4ED8;margin-bottom:12px'>GP Services</div>"
            "<div style='font-size:13px;color:#1E40AF;line-height:1.6;margin-bottom:16px'>"
            "For non-emergency medical advice, contact your GP during office hours.</div>"
            "<div style='font-size:12px;color:#2563EB;font-weight:500;margin-bottom:12px'>Mon–Fri: 9:00 AM – 5:00 PM</div>"
            "<a href='https://www.google.com/maps/search/GP+doctor+near+me' target='_blank'"
            " style='display:block;background:#1D4ED8;color:white;text-align:center;"
            "padding:10px;border-radius:8px;font-size:13px;font-weight:600;text-decoration:none'>"
            "Find a GP Near Me</a>"
            "</div>",
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            "<div style='background:#F0FDFA;border:1px solid #99F6E4;border-radius:12px;padding:20px;height:100%'>"
            "<div style='font-size:15px;font-weight:700;color:#0D9488;margin-bottom:12px'>" + ooh_name + "</div>"
            "<div style='font-size:13px;color:#0F766E;line-height:1.6;margin-bottom:16px'>"
            "When your GP surgery is closed, out-of-hours services provide urgent medical care.</div>"
            "<a href='" + ooh_tel + "' style='display:block;font-size:16px;font-weight:700;"
            "color:#0D9488;text-decoration:none;margin-bottom:10px'>📞 " + ooh_num + "</a>"
            "<a href='" + ooh_web + "' target='_blank'"
            " style='display:block;background:#0D9488;color:white;text-align:center;"
            "padding:10px;border-radius:8px;font-size:13px;font-weight:600;text-decoration:none'>"
            "Visit Website</a>"
            "</div>",
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            "<div style='background:#FAF5FF;border:1px solid #E9D5FF;border-radius:12px;padding:20px;height:100%'>"
            "<div style='font-size:15px;font-weight:700;color:#7C3AED;margin-bottom:12px'>Minor Injury Units</div>"
            "<div style='font-size:13px;color:#6D28D9;line-height:1.6;margin-bottom:16px'>"
            "For minor injuries like sprains, cuts, and minor burns without appointment.</div>"
            "<a href='https://www.google.com/maps/search/minor+injury+unit+near+me' target='_blank'"
            " style='display:block;background:#7C3AED;color:white;text-align:center;"
            "padding:10px;border-radius:8px;font-size:13px;font-weight:600;text-decoration:none'>"
            "Find Nearest MIU</a>"
            "</div>",
            unsafe_allow_html=True
        )

    # Footer
    # Footer
    st.markdown(
        "<div style='background:#0D2137;border-radius:12px;padding:28px 24px;margin-top:24px'>"
        "<div style='display:grid;grid-template-columns:2fr 1fr 1fr;gap:2rem;margin-bottom:20px'>"
        "<div>"
        "<div style='font-size:15px;font-weight:700;color:white;margin-bottom:10px'>HSE Emergency Services</div>"
        "<div style='font-size:13px;color:#94A3B8;line-height:1.6'>"
        "Providing real-time emergency department information to help you make informed decisions about your healthcare."
        "</div></div>"
        "<div>"
        "<div style='font-size:15px;font-weight:700;color:white;margin-bottom:10px'>Quick Links</div>"
        "<div style='font-size:13px;color:#64748B;line-height:2'>"
        "<a href='#' style='color:#64748B;text-decoration:none;display:block'>Find Your Nearest ED</a>"
        "<a href='#' style='color:#64748B;text-decoration:none;display:block'>GP Services</a>"
        "<a href='https://www.hse.ie' style='color:#64748B;text-decoration:none;display:block'>Health Information</a>"
        "</div></div>"
        "<div>"
        "<div style='font-size:15px;font-weight:700;color:white;margin-bottom:10px'>Emergency Contacts</div>"
        "<div style='font-size:13px;color:#94A3B8;line-height:2'>"
        "<div><strong style='color:white'>Emergency:</strong> 999</div>"
        "<div><strong style='color:white'>Out of Hours (" + ooh_name + "):</strong> " + ooh_num + "</div>"
        "<div><strong style='color:white'>HSE Live:</strong> 1850 24 1850</div>"
        "</div></div></div>"
        "<div style='border-top:1px solid #1e3a5f;padding-top:16px;text-align:center;font-size:12px;color:#64748B'>"
        "HealthFlow &nbsp;|&nbsp; Group 2 &nbsp;|&nbsp; UCC IS6611 &nbsp;|&nbsp; 2026 &nbsp;|&nbsp;"
        "This platform is for informational purposes only and does not replace professional medical advice."
        "</div></div>",
        unsafe_allow_html=True
    )
