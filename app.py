import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="HealthFlow Live ED Status", page_icon="🏥", layout="wide", initial_sidebar_state="expanded")

if 'selected_hospital' not in st.session_state: st.session_state.selected_hospital = None

@st.cache_data
def load_master():
    try:
        df = pd.read_csv('data/master_dataset.csv', encoding='latin-1')
        df.columns = df.columns.str.strip()
        if 'hospital' in df.columns and 'Hospital' not in df.columns:
            df = df.rename(columns={'hospital':'Hospital'})
        for col in ['occupancy_rate_pct','trolley_load','hospital_beds','waiting_over_24hrs','daily_total']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        if 'traffic_light_status' not in df.columns and 'occupancy_rate_pct' in df.columns:
            df['traffic_light_status'] = df['occupancy_rate_pct'].apply(
                lambda x: 'Red' if x >= 8 else ('Amber' if x >= 4 else 'Green'))
        return df
    except Exception as e:
        return pd.DataFrame()

@st.cache_data
def load_synthetic():
    try:
        return pd.read_csv('data/synthetic_dataset_only.csv', encoding='latin-1')
    except:
        return pd.DataFrame()

master    = load_master()
synthetic = load_synthetic()

NAVY="#0D2137"; TEAL="#0D9488"; RED="#DC2626"; AMBER="#D97706"; GREEN="#16A34A"

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif!important;}
[data-testid="stAppViewContainer"]{background:#f5f5f5;padding:0!important;}
[data-testid="stMain"]{padding:0!important;}
.block-container{padding:0!important;max-width:100%!important;}
[data-testid="stSidebar"]{background:#0D2137;min-width:220px!important;}
[data-testid="stSidebar"] *{color:white!important;}
[data-testid="stHeader"]{display:none;}
#MainMenu,footer{display:none;}
.hero{background:linear-gradient(135deg,#0D9488 0%,#0a7a70 60%,#0D2137 100%);padding:2.5rem;margin-bottom:0;}
.hero-title{font-size:28px;font-weight:700;color:white;margin-bottom:6px;}
.hero-sub{font-size:14px;color:rgba(255,255,255,0.85);margin-bottom:16px;}
.hero-pills{display:flex;gap:10px;flex-wrap:wrap;}
.pill{display:inline-flex;align-items:center;gap:6px;background:rgba(255,255,255,0.15);border:1px solid rgba(255,255,255,0.25);color:white;padding:5px 12px;border-radius:20px;font-size:13px;font-weight:500;}
.dot{width:8px;height:8px;border-radius:50%;display:inline-block;}
.updated{background:rgba(255,255,255,0.15);border:1px solid rgba(255,255,255,0.3);color:white;padding:6px 14px;border-radius:20px;font-size:12px;}
.hcard{background:white;border-radius:12px;padding:20px;border:1px solid #E2E8F0;box-shadow:0 1px 3px rgba(0,0,0,0.05);margin-bottom:4px;}
.hcard-header{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:8px;}
.hcard-name{font-size:15px;font-weight:600;color:#0D2137;flex:1;margin-right:8px;}
.tdot{width:14px;height:14px;border-radius:50%;flex-shrink:0;margin-top:3px;}
.hloc{font-size:12px;color:#64748B;margin-bottom:12px;}
.pbadge{background:#EFF6FF;color:#2563EB;font-size:10px;font-weight:600;padding:2px 7px;border-radius:4px;border:1px solid #BFDBFE;}
.sbadge{display:block;padding:6px 14px;border-radius:6px;font-size:13px;font-weight:500;text-align:center;margin-bottom:14px;}
.s-red{background:#FEE2E2;color:#DC2626;}
.s-amber{background:#FEF9C3;color:#B45309;}
.s-green{background:#DCFCE7;color:#15803D;}
.stat-row{display:flex;justify-content:space-between;font-size:13px;margin-bottom:5px;}
.stat-lbl{color:#64748B;}
.stat-val{font-weight:600;color:#0D2137;}
.cap-hdr{display:flex;justify-content:space-between;font-size:12px;color:#64748B;margin-bottom:4px;}
.cap-bg{height:6px;background:#E2E8F0;border-radius:10px;overflow:hidden;margin-bottom:10px;}
.cap-fill{height:100%;border-radius:10px;}
.card-ft{display:flex;justify-content:space-between;font-size:12px;color:#94A3B8;border-top:1px solid #F1F5F9;padding-top:8px;margin-top:4px;}
.card-cta{font-size:11px;color:#94A3B8;text-align:center;margin-top:6px;}
.uvc-box{background:linear-gradient(135deg,#0D9488,#0a7a70);border-radius:12px;padding:24px;color:white;margin-bottom:1.5rem;}
.uvc-stats{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px;}
.uvc-stat{background:rgba(0,0,0,0.2);border-radius:8px;padding:14px;}
.uvc-stat-lbl{font-size:12px;opacity:0.8;margin-bottom:4px;}
.uvc-stat-val{font-size:20px;font-weight:700;}
.updates-box{background:#FFFBEB;border:1px solid #FDE68A;border-radius:12px;padding:20px 24px;margin-bottom:1.5rem;}
.upd-badge{background:#F59E0B;color:white;font-size:11px;font-weight:600;padding:3px 8px;border-radius:4px;}
.step-card{background:white;border:1px solid #E2E8F0;border-radius:12px;padding:20px;text-align:center;}
.step-icon{width:48px;height:48px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:20px;margin:0 auto 12px;}
.step-lbl{font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px;}
.step-title{font-size:15px;font-weight:700;color:#0D2137;margin-bottom:6px;}
.step-desc{font-size:12px;color:#64748B;line-height:1.4;}
.pharm-box{background:#F0FDF4;border:1px solid #BBF7D0;border-radius:12px;padding:24px;margin-bottom:1.5rem;}
.hse-badge{background:#0D9488;color:white;font-size:11px;font-weight:600;padding:3px 8px;border-radius:4px;}
.cond-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px;}
.cond-card{background:white;border:1px solid #E2E8F0;border-radius:10px;padding:14px;}
.cond-name{font-size:13px;font-weight:600;color:#0D2137;margin-bottom:4px;}
.cond-desc{font-size:11px;color:#64748B;line-height:1.4;}
.crit-box{background:#FFF1F2;border:1px solid #FECDD3;border-radius:12px;padding:24px;margin-bottom:1.5rem;}
.crit-badge{background:#DC2626;color:white;font-size:11px;font-weight:700;padding:4px 10px;border-radius:4px;}
.crit-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:16px;}
.crit-item{background:white;border:1px solid #FECDD3;border-radius:8px;padding:12px;display:flex;gap:10px;}
.crit-num{color:#DC2626;font-weight:700;font-size:13px;flex-shrink:0;}
.crit-name{font-size:13px;font-weight:600;color:#0D2137;}
.crit-sub{font-size:11px;color:#64748B;}
.res-card{background:white;border:1px solid #E2E8F0;border-radius:12px;padding:20px;margin-bottom:12px;}
.sec-title{font-size:17px;font-weight:600;color:#0D2137;display:flex;align-items:center;gap:8px;margin:1.5rem 0 1rem;}
.mh-card{background:white;border:1px solid #E2E8F0;border-radius:12px;padding:20px;text-align:center;}
.mh-icon{width:48px;height:48px;background:#FFF1F2;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:20px;margin:0 auto 12px;}
.mh-name{font-size:15px;font-weight:600;color:#0D2137;margin-bottom:6px;}
.mh-desc{font-size:12px;color:#64748B;margin-bottom:10px;line-height:1.4;}
.mh-phone{color:#DC2626;font-size:13px;font-weight:500;}
.call999-bar{background:#DC2626;padding:20px 2rem;display:flex;align-items:center;justify-content:space-between;margin-bottom:1.5rem;}
.call999-num{font-size:28px;font-weight:700;color:white;}
.call999-lbl{font-size:12px;color:rgba(255,255,255,0.8);}
.call999-msg{font-size:13px;color:rgba(255,255,255,0.9);max-width:400px;}
.contact-card{background:white;border:1px solid #E2E8F0;border-radius:12px;padding:20px;}
.contact-title{font-size:15px;font-weight:600;color:#0D2137;margin-bottom:8px;}
.contact-desc{font-size:13px;color:#64748B;margin-bottom:8px;line-height:1.5;}
.contact-detail{font-size:13px;color:#0D9488;font-weight:500;}
.footer-bar{background:#0D2137;padding:2rem;margin-top:2rem;}
.footer-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:2rem;}
.footer-title{font-size:14px;font-weight:600;color:white;margin-bottom:12px;}
.footer-item{font-size:13px;color:#94A3B8;margin-bottom:6px;}
.footer-bottom{text-align:center;color:#64748B;font-size:12px;margin-top:1.5rem;padding-top:1rem;border-top:1px solid rgba(255,255,255,0.1);}
div[data-testid="metric-container"]{background:white;padding:12px 16px;border-radius:10px;border:1px solid #E2E8F0;}
.notify-btn{width:100%;padding:12px;background:#FEF9C3;border:1px solid #FDE68A;border-radius:10px;color:#92400E;font-size:14px;font-weight:500;text-align:center;margin-top:12px;}
.pad{padding:1.5rem 2rem;}
</style>""", unsafe_allow_html=True)

def sc(s): return {'Red':'#DC2626','Amber':'#D97706','Green':'#16A34A'}.get(s,'#64748B')
def sl(s): return {'Red':'Very Busy','Amber':'Busy','Green':'Normal'}.get(s,'Unknown')

def get_hospitals():
    if master.empty: return []
    out = []
    for _, r in master.iterrows():
        occ  = float(r.get('occupancy_rate_pct',0) or 0)
        st_  = r.get('traffic_light_status','Green')
        load = float(r.get('trolley_load',0) or 0)
        beds = int(r.get('hospital_beds',300) or 300)
        reg  = str(r.get('region','')).title()
        wt   = '8–12 hrs' if occ>=8 else '4–6 hrs' if occ>=6 else '2–4 hrs' if occ>=4 else '1–2 hrs'
        pts  = int(load * np.random.uniform(1.5,2.5)) if load>0 else 0
        tr   = np.random.choice(['Up','Stable','Down'],p=[0.4,0.35,0.25])
        out.append({'name':r.get('Hospital',''),'loc':reg,'type':'Public','status':st_,
                    'occ':occ,'load':load,'beds':beds,'wt':wt,'pts':pts,
                    'tr':tr,'upd':f"{np.random.choice([5,10,15,20])} mins ago"})
    return out

with st.sidebar:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:1.5rem;">
      <div style="width:36px;height:36px;background:#0D9488;border-radius:8px;display:flex;align-items:center;justify-content:center;color:white;font-weight:700;font-size:14px;">HF</div>
      <div><div style="font-size:14px;font-weight:600;">HealthFlow</div><div style="font-size:11px;color:#94A3B8;">ED Monitor</div></div>
    </div>""", unsafe_allow_html=True)
    page = st.radio("", ["ED Status","Patient Advice","Resources","Contact","📊 Analytics","📈 Predictive","🧠 Prescriptive","🔍 EDA"], label_visibility="collapsed")

# ─── ED STATUS ───────────────────────────────────────────────
if page == "ED Status":
    hospitals = get_hospitals()
    rn = sum(1 for h in hospitals if h['status']=='Red')
    an = sum(1 for h in hospitals if h['status']=='Amber')
    gn = sum(1 for h in hospitals if h['status']=='Green')

    st.markdown(f"""
    <div class="hero">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;">
        <div>
          <div class="hero-title">Live Emergency Department Status</div>
          <div class="hero-sub">Real-time capacity and wait time information across Ireland</div>
          <div class="hero-pills">
            <div class="pill"><span class="dot" style="background:#4ADE80"></span>Normal: {gn}</div>
            <div class="pill"><span class="dot" style="background:#FCD34D"></span>Busy: {an}</div>
            <div class="pill"><span class="dot" style="background:#F87171"></span>Very Busy: {rn}</div>
          </div>
        </div>
        <div class="updated">🕐 Updated live</div>
      </div>
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns([4,2])
    with c1:
        search = st.text_input("","", placeholder="🔍  Search hospitals, locations...", label_visibility="collapsed")
    with c2:
        county = st.selectbox("",["All Counties","Eastern","Country","Paediatric"], label_visibility="collapsed")

    filtered = [h for h in hospitals
                if (not search or search.lower() in h['name'].lower())
                and (county=="All Counties" or h['loc'].lower()==county.lower())]

    st.markdown(f'<div style="padding:8px 0 4px;font-size:13px;color:#64748B;">Showing <strong>{len(filtered)}</strong> of <strong>{len(hospitals)}</strong> hospitals</div>', unsafe_allow_html=True)

    n_cols = 3
    for i in range(0, len(filtered), n_cols):
        row = filtered[i:i+n_cols]
        cols = st.columns(n_cols)
        for j, h in enumerate(row):
            with cols[j]:
                bw  = min(int(h['occ']*6),100)
                trc = {'Up':'↗ Up','Down':'↘ Down','Stable':'— Stable'}[h['tr']]
                tcolor = {'Up':'#16A34A','Down':'#DC2626','Stable':'#64748B'}[h['tr']]
                st.markdown(f"""
                <div class="hcard">
                  <div class="hcard-header">
                    <div class="hcard-name">{h['name']}</div>
                    <div class="tdot" style="background:{sc(h['status'])}"></div>
                  </div>
                  <div class="hloc">📍 {h['loc']} &nbsp;<span class="pbadge">{h['type']}</span></div>
                  <div class="sbadge s-{h['status'].lower()}">{sl(h['status'])}</div>
                  <div class="stat-row"><span class="stat-lbl">🕐 Wait Time</span><span class="stat-val">{h['wt']}</span></div>
                  <div class="stat-row"><span class="stat-lbl">👤 Waiting</span><span class="stat-val">{h['pts']} patients</span></div>
                  <div style="margin-top:10px;">
                    <div class="cap-hdr"><span>Capacity</span><span style="font-weight:600;color:{sc(h['status'])}">{h['occ']:.0f}%</span></div>
                    <div class="cap-bg"><div class="cap-fill" style="width:{bw}%;background:{sc(h['status'])}"></div></div>
                  </div>
                  <div class="card-ft">
                    <span>{h['upd']}</span>
                    <span style="color:{tcolor};font-weight:500;">{trc}</span>
                  </div>
                  <div class="card-cta">Click for details &amp; notifications</div>
                </div>""", unsafe_allow_html=True)
                if st.button("View", key=f"v_{i}_{j}", use_container_width=True):
                    st.session_state.selected_hospital = h

    if st.session_state.selected_hospital:
        h = st.session_state.selected_hospital
        st.markdown("---")
        col1, col2 = st.columns([3,1])
        with col1:
            bw = min(int(h['occ']*6),100)
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
              <div class="tdot" style="background:{sc(h['status'])};width:18px;height:18px;"></div>
              <span style="font-size:20px;font-weight:700;color:#0D2137;">{h['name']}</span>
            </div>
            <div class="hloc">📍 {h['loc']} &nbsp;<span class="pbadge">{h['type']}</span></div>
            <div class="sbadge s-{h['status'].lower()}" style="display:inline-block;width:auto;padding:6px 16px;">{sl(h['status'])}</div>
            """, unsafe_allow_html=True)
            ca, cb = st.columns(2)
            ca.metric("⏱ Wait Time", h['wt'])
            cb.metric("👤 Patients Waiting", h['pts'])
            st.markdown(f"""
            <div class="cap-hdr" style="margin-top:12px;"><span>Capacity</span><span style="font-weight:600;color:{sc(h['status'])}">{h['occ']:.0f}%</span></div>
            <div class="cap-bg"><div class="cap-fill" style="width:{bw}%;background:{sc(h['status'])}"></div></div>
            <div style="font-size:12px;color:#94A3B8;margin-top:6px;">Last updated: {h['upd']}</div>
            """, unsafe_allow_html=True)
            if h['status'] in ['Red','Amber']:
                st.markdown('<div class="notify-btn">🔔 Notify me when wait time decreases</div>', unsafe_allow_html=True)
        with col2:
            if st.button("✕ Close", use_container_width=True):
                st.session_state.selected_hospital = None
                st.rerun()

# ─── PATIENT ADVICE ──────────────────────────────────────────
elif page == "Patient Advice":
    st.markdown("""
    <div class="hero">
      <div class="hero-title">Patient Advice &amp; Emergency Guidelines</div>
      <div class="hero-sub">Important information to help you decide when and where to seek medical care</div>
    </div>""", unsafe_allow_html=True)
    st.markdown('<div class="pad">', unsafe_allow_html=True)
    st.markdown("""
    <div class="updates-box">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
        <span class="upd-badge">Important Updates</span>
        <span style="font-size:12px;color:#64748B;">Updated February 22, 2026</span>
      </div>
      <p style="font-size:14px;color:#374151;line-height:1.6;margin:0;">
        Over the next <strong>1–4 weeks</strong> we expect ED attendances to go up by
        <strong style="color:#DC2626;">15–20%</strong> based on seasonal triggers and previous data.
        We would <strong>strongly advise people to only come to the ED if very necessary</strong> and are advised by their GP.
      </p>
    </div>
    <div class="uvc-box">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:10px;">
        <div style="width:40px;height:40px;background:rgba(255,255,255,0.15);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:18px;">📹</div>
        <div>
          <div style="font-size:16px;font-weight:600;">Urgent Virtual Care (UVC) Success</div>
          <div style="font-size:13px;opacity:0.85;">Successfully managed over <strong>8,450 cases</strong> in the past month without requiring ED visits.</div>
        </div>
      </div>
      <div class="uvc-stats">
        <div class="uvc-stat"><div class="uvc-stat-lbl">✓ Cases Resolved</div><div class="uvc-stat-val">8,450+</div></div>
        <div class="uvc-stat"><div class="uvc-stat-lbl">✓ Avg Wait Time</div><div class="uvc-stat-val">12 mins</div></div>
      </div>
    </div>""", unsafe_allow_html=True)

    col1,col2,col3 = st.columns(3)
    for col, title, body in zip([col1,col2,col3],
        ["Alternative Options","Minor Injuries","Virtual Care"],
        ["Contact your GP first","Visit an Injury Unit","Try UVC Service"]):
        with col:
            st.markdown(f'<div style="background:#FFFBEB;border:1px solid #FDE68A;border-radius:8px;padding:14px;"><div style="font-size:11px;font-weight:600;color:#D97706;margin-bottom:4px;">{title}</div><div style="font-size:14px;color:#0D2137;font-weight:500;">{body}</div></div>', unsafe_allow_html=True)

    st.markdown("<br><h3>Where Should I Go?</h3><p style='font-size:13px;color:#64748B;'>A quick guide to choosing the right care for your situation</p>", unsafe_allow_html=True)

    c1,ca,c2,cb,c3 = st.columns([3,0.3,3,0.3,3])
    with c1:
        st.markdown('<div class="step-card"><div class="step-icon" style="background:#F0FDF4;">💊</div><div class="step-lbl" style="color:#0D9488;">STEP 1 — TRY FIRST</div><div class="step-title">Your Pharmacist</div><div class="step-desc">For UTIs, cold sores, hay fever, shingles, minor skin conditions — no appointment needed.</div></div>', unsafe_allow_html=True)
    with ca:
        st.markdown('<div style="text-align:center;padding-top:80px;font-size:20px;color:#CBD5E1;">→</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="step-card"><div class="step-icon" style="background:#EFF6FF;">✓</div><div class="step-lbl" style="color:#2563EB;">STEP 2 — IF NEEDED</div><div class="step-title">Your GP</div><div class="step-desc">For illness requiring diagnosis, ongoing conditions, referrals, or anything your pharmacist cannot manage.</div></div>', unsafe_allow_html=True)
    with cb:
        st.markdown('<div style="text-align:center;padding-top:80px;font-size:20px;color:#CBD5E1;">→</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="step-card"><div class="step-icon" style="background:#FFF1F2;">📞</div><div class="step-lbl" style="color:#DC2626;">STEP 3 — EMERGENCY ONLY</div><div class="step-title">ED / Call 999</div><div class="step-desc">Life-threatening symptoms, major trauma, or when advised by a clinician.</div></div>', unsafe_allow_html=True)

    st.markdown("""<br>
    <div class="pharm-box">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
        <div style="width:40px;height:40px;background:#0D9488;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:18px;color:white;">💊</div>
        <div><div style="font-size:16px;font-weight:600;color:#0D2137;">Pharmacy First — Skip the GP Queue &nbsp;<span class="hse-badge">HSE Scheme</span></div></div>
      </div>
      <p style="font-size:13px;color:#374151;line-height:1.6;margin-bottom:12px;">Under the HSE's expanded pharmacy services, pharmacists across Ireland can now <strong>assess, advise, and in some cases prescribe</strong> for a range of common conditions without a GP appointment first.</p>
      <div style="background:white;border:1px solid #BBF7D0;border-radius:8px;padding:12px;font-size:12px;color:#374151;margin-bottom:16px;">ℹ Walk into any participating pharmacy. No appointment necessary. GMS/medical card holders may be entitled to free treatment.</div>
      <div class="cond-grid">
        <div class="cond-card"><div class="cond-name">Urinary Tract Infection (UTI)</div><div class="cond-desc">Uncomplicated UTIs in women aged 16–64 can be assessed and treated with antibiotics directly by your pharmacist.</div></div>
        <div class="cond-card"><div class="cond-name">Cold Sores (Herpes Labialis)</div><div class="cond-desc">Antiviral creams and oral antivirals available without a prescription.</div></div>
        <div class="cond-card"><div class="cond-name">Hay Fever &amp; Allergies</div><div class="cond-desc">Antihistamines, nasal sprays, and eye drops can be recommended or prescribed by your pharmacist.</div></div>
        <div class="cond-card"><div class="cond-name">Indigestion &amp; Heartburn</div><div class="cond-desc">Antacids, H2 blockers, and lifestyle advice available without a prescription.</div></div>
      </div>
    </div>
    <div class="crit-box">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
        <div style="width:40px;height:40px;background:#DC2626;border-radius:8px;display:flex;align-items:center;justify-content:center;color:white;font-size:18px;">📞</div>
        <div>
          <div style="font-size:17px;font-weight:700;color:#0D2137;">10 Critical Symptoms Requiring Immediate Review</div>
          <div style="margin-top:4px;"><span class="crit-badge">CALL 999 IMMEDIATELY</span></div>
        </div>
      </div>
      <div class="crit-grid">
        <div class="crit-item"><span class="crit-num">1.</span><div><div class="crit-name">Chest pain or tightness</div><div class="crit-sub">Especially crushing, radiating, with sweating or nausea</div></div></div>
        <div class="crit-item"><span class="crit-num">2.</span><div><div class="crit-name">Sudden shortness of breath</div><div class="crit-sub">Possible respiratory failure or cardiac issues</div></div></div>
        <div class="crit-item"><span class="crit-num">3.</span><div><div class="crit-name">Sudden weakness or paralysis</div><div class="crit-sub">Especially one-sided — possible stroke</div></div></div>
        <div class="crit-item"><span class="crit-num">4.</span><div><div class="crit-name">Altered consciousness</div><div class="crit-sub">Confusion, collapse, fainting or unresponsiveness</div></div></div>
        <div class="crit-item"><span class="crit-num">5.</span><div><div class="crit-name">Severe allergic reaction</div><div class="crit-sub">Facial/lip swelling, wheezing, difficulty breathing</div></div></div>
        <div class="crit-item"><span class="crit-num">6.</span><div><div class="crit-name">Uncontrolled bleeding</div><div class="crit-sub">External or suspected internal bleeding</div></div></div>
        <div class="crit-item"><span class="crit-num">7.</span><div><div class="crit-name">Severe abdominal pain</div><div class="crit-sub">Sudden, severe with rigidity or vomiting</div></div></div>
        <div class="crit-item"><span class="crit-num">8.</span><div><div class="crit-name">High fever with signs of infection</div><div class="crit-sub">Over 39°C with confusion or rash</div></div></div>
        <div class="crit-item"><span class="crit-num">9.</span><div><div class="crit-name">Seizures</div><div class="crit-sub">First seizure or lasting more than 5 minutes</div></div></div>
        <div class="crit-item"><span class="crit-num">10.</span><div><div class="crit-name">Suspected overdose or poisoning</div><div class="crit-sub">Any accidental or intentional ingestion of harmful substances</div></div></div>
      </div>
    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─── RESOURCES ───────────────────────────────────────────────
elif page == "Resources":
    st.markdown("""
    <div class="hero">
      <div class="hero-title">Healthcare Resources</div>
      <div class="hero-sub">Access alternative healthcare services and helpful resources to get the care you need</div>
    </div>""", unsafe_allow_html=True)
    st.markdown('<div class="pad">', unsafe_allow_html=True)
    st.markdown("""
    <div class="uvc-box">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
        <div style="width:40px;height:40px;background:rgba(255,255,255,0.15);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:18px;">📹</div>
        <div>
          <span style="font-size:16px;font-weight:600;">Urgent Virtual Care (UVC)</span>
          <span style="background:#0D9488;border:1px solid rgba(255,255,255,0.3);color:white;font-size:11px;padding:2px 8px;border-radius:4px;margin-left:8px;">Recommended</span>
          <div style="font-size:13px;opacity:0.85;margin-top:2px;">Get immediate medical assessment via video call. Over 8,450 cases resolved without ED visits.</div>
        </div>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px;">
        <div style="background:rgba(0,0,0,0.2);border-radius:8px;padding:14px;"><div style="font-size:11px;opacity:0.8;margin-bottom:4px;">🕐 Available</div><div style="font-size:15px;font-weight:600;">8am – 8pm Daily</div></div>
        <div style="background:rgba(0,0,0,0.2);border-radius:8px;padding:14px;"><div style="font-size:11px;opacity:0.8;margin-bottom:4px;">⚡ Response Time</div><div style="font-size:15px;font-weight:600;">Usually within 1 hour</div></div>
      </div>
      <div style="background:rgba(0,0,0,0.15);border-radius:8px;padding:12px;font-size:12px;"><strong>GP Referral Required:</strong> UVC is available only when referred by your GP.</div>
    </div>
    <div class="sec-title">🩺 Primary Care Services</div>""", unsafe_allow_html=True)

    c1,c2 = st.columns(2)
    with c1:
        st.markdown("""<div class="res-card">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
            <div style="width:36px;height:36px;background:#EFF6FF;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:16px;">🩺</div>
            <span style="font-size:15px;font-weight:600;color:#0D2137;">GP Services</span>
          </div>
          <p style="font-size:13px;color:#374151;line-height:1.5;margin-bottom:12px;">Your GP is your first point of contact for non-emergency medical issues. <span style="color:#2563EB;">They can assess, treat, and refer you if needed.</span></p>
          <div style="font-size:12px;color:#64748B;margin-bottom:4px;">🕐 Mon–Fri: 9am – 5pm (typical)</div>
          <div style="font-size:12px;color:#64748B;margin-bottom:12px;">📍 Find your nearest GP practice</div>
          <div style="border:1px solid #E2E8F0;border-radius:8px;padding:10px;text-align:center;font-size:13px;color:#64748B;">🔗 Find a GP</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="res-card">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
            <div style="width:36px;height:36px;background:#FEF3C7;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:16px;">🕐</div>
            <span style="font-size:15px;font-weight:600;color:#0D2137;">Out-of-Hours GP</span>
          </div>
          <p style="font-size:13px;color:#374151;line-height:1.5;margin-bottom:12px;">When your GP surgery is closed, out-of-hours services provide urgent medical care. <em>Note: GP services are also under capacity pressure.</em></p>
          <div style="font-size:12px;font-weight:500;margin-bottom:3px;">ShanDoc (Shannon Region)</div><div style="font-size:13px;color:#0D9488;margin-bottom:8px;">📞 1850 777 911</div>
          <div style="font-size:12px;font-weight:500;margin-bottom:3px;">CareDoc (Dublin)</div><div style="font-size:13px;color:#0D9488;margin-bottom:8px;">📞 01 209 4021</div>
          <div style="font-size:12px;font-weight:500;margin-bottom:3px;">NowDoc (Dublin)</div><div style="font-size:13px;color:#0D9488;">📞 1850 592 0900</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec-title">🏥 Injury &amp; Pharmacy Services</div>', unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        st.markdown("""<div class="res-card">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
            <div style="width:36px;height:36px;background:#F0FDF4;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:16px;">🏥</div>
            <span style="font-size:15px;font-weight:600;color:#0D2137;">Minor Injury Units</span>
          </div>
          <p style="font-size:13px;color:#374151;line-height:1.5;margin-bottom:12px;">Treatment for minor injuries like sprains, cuts, burns, and fractures without ED wait times.</p>
          <div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px;">
            <span style="background:#FEF3C7;color:#92400E;font-size:11px;padding:3px 8px;border-radius:4px;">Sprains &amp; Strains</span>
            <span style="background:#FEF3C7;color:#92400E;font-size:11px;padding:3px 8px;border-radius:4px;">Minor Burns</span>
            <span style="background:#FEF3C7;color:#92400E;font-size:11px;padding:3px 8px;border-radius:4px;">Cuts</span>
          </div>
          <div style="border:1px solid #E2E8F0;border-radius:8px;padding:10px;text-align:center;font-size:13px;color:#64748B;">📍 Find Nearest Unit</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="res-card">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
            <div style="width:36px;height:36px;background:#F0FDF4;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:16px;">💊</div>
            <span style="font-size:15px;font-weight:600;color:#0D2137;">Pharmacy Services</span>
          </div>
          <p style="font-size:13px;color:#374151;line-height:1.5;margin-bottom:12px;">Pharmacists can provide advice and treatment for minor ailments without a prescription.</p>
          <div style="font-size:12px;color:#64748B;font-weight:500;margin-bottom:8px;">Can help with:</div>
          <div style="font-size:12px;color:#374151;line-height:1.8;">• Coughs, colds &amp; flu<br>• Minor skin conditions<br>• Indigestion &amp; heartburn<br>• Emergency contraception</div>
          <div style="border:1px solid #E2E8F0;border-radius:8px;padding:10px;text-align:center;font-size:13px;color:#64748B;margin-top:12px;">📍 Find a Pharmacy</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec-title">🧠 Mental Health Support</div>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:13px;color:#64748B;margin-bottom:1rem;">Community mental health services and CAMHS are under significant capacity pressure. Crisis pathways below are always available.</p>', unsafe_allow_html=True)

    cc1,cc2,cc3 = st.columns(3)
    for col, s in zip([cc1,cc2,cc3],[
        {"i":"📞","n":"Samaritans","d":"24/7 emotional support for anyone in distress","c":"116 123 (Free)"},
        {"i":"💜","n":"Pieta House","d":"Free therapy for those in suicidal distress or self-harm","c":"1800 247 247"},
        {"i":"💬","n":"Text 50808","d":"24/7 anonymous text support service","c":"Text HELLO to 50808"},
    ]):
        with col:
            st.markdown(f'<div class="mh-card"><div class="mh-icon">{s["i"]}</div><div class="mh-name">{s["n"]}</div><div class="mh-desc">{s["d"]}</div><div class="mh-phone">{s["c"]}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─── CONTACT ────────────────────────────────────────────────
elif page == "Contact":
    st.markdown("""
    <div class="call999-bar">
      <div style="display:flex;align-items:center;gap:16px;">
        <span style="font-size:24px;color:white;">📞</span>
        <div><div class="call999-lbl">Emergency Services</div><div class="call999-num">Call 999</div></div>
      </div>
      <div class="call999-msg">Do not delay if you experience any life-threatening symptoms. Time is critical in emergency situations.</div>
    </div>""", unsafe_allow_html=True)
    st.markdown('<div class="pad">', unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown('<div class="contact-card" style="background:#EFF6FF;border-color:#BFDBFE;"><div class="contact-title">GP Services</div><div class="contact-desc">For non-emergency medical advice, contact your GP during office hours.</div><div class="contact-detail">Mon–Fri: 9:00 AM – 5:00 PM</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="contact-card" style="background:#F0FDF4;border-color:#BBF7D0;"><div class="contact-title">Out of Hours</div><div class="contact-desc">ShanDoc provides out-of-hours GP services when your practice is closed.</div><div class="contact-detail">📞 1850 777 911</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="contact-card" style="background:#FAF5FF;border-color:#E9D5FF;"><div class="contact-title">Minor Injury Units</div><div class="contact-desc">For minor injuries like sprains, cuts, and minor burns without appointment.</div><div class="contact-detail" style="color:#7C3AED;">Check local unit opening hours</div></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="footer-bar">
      <div class="footer-grid">
        <div><div class="footer-title">HSE Emergency Services</div><p style="font-size:13px;color:#94A3B8;line-height:1.5;">Providing real-time emergency department information to help you make informed decisions about your healthcare.</p></div>
        <div><div class="footer-title">Quick Links</div><div class="footer-item">Find Your Nearest ED</div><div class="footer-item">GP Services</div><div class="footer-item">Health Information</div><div class="footer-item">Contact HSE</div></div>
        <div><div class="footer-title">Emergency Contacts</div><div style="font-size:13px;color:#94A3B8;line-height:1.8;"><strong style="color:white;">Emergency:</strong> 999<br><strong style="color:white;">ShanDoc:</strong> 1850 777 911<br><strong style="color:white;">HSE Live:</strong> 1850 24 1850</div></div>
      </div>
      <div class="footer-bottom">© 2026 HealthFlow — Group 2 · UCC · IS6611</div>
    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─── ANALYTICS ──────────────────────────────────────────────
elif page == "📊 Analytics":
    st.markdown('<div class="pad">', unsafe_allow_html=True)
    st.title("📊 Live ED Analytics")
    if not master.empty:
        rn=(master['traffic_light_status']=='Red').sum(); an=(master['traffic_light_status']=='Amber').sum(); gn=(master['traffic_light_status']=='Green').sum()
        c1,c2,c3,c4=st.columns(4)
        c1.metric("🔴 Very Busy",rn); c2.metric("🟡 Busy",an); c3.metric("🟢 Normal",gn); c4.metric("🏥 Total",len(master))
        st.markdown("---")
        chart_df=master.dropna(subset=['occupancy_rate_pct']).sort_values('occupancy_rate_pct',ascending=True)
        cm={'Red':'#DC2626','Amber':'#D97706','Green':'#16A34A'}
        colors=chart_df['traffic_light_status'].map(cm).fillna('#64748B')
        fig=go.Figure(go.Bar(x=chart_df['occupancy_rate_pct'],y=chart_df['Hospital'],orientation='h',marker_color=list(colors),text=chart_df['occupancy_rate_pct'].apply(lambda x:f"{x:.1f}%"),textposition='outside'))
        fig.update_layout(plot_bgcolor='white',paper_bgcolor='white',height=500,xaxis_title='Occupancy Rate (%)',margin=dict(l=0,r=60,t=20,b=20))
        fig.add_vline(x=8,line_dash="dash",line_color="#DC2626"); fig.add_vline(x=4,line_dash="dash",line_color="#D97706")
        st.plotly_chart(fig,use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "📈 Predictive":
    st.markdown('<div class="pad">', unsafe_allow_html=True)
    st.title("📈 Predictive Analytics — SARIMAX")
    st.info("SARIMAX(1,1,1)(1,1,1,12) — trained Jan 2022 – Dec 2023, tested Oct–Dec 2023.")
    if not synthetic.empty:
        syn=synthetic.copy(); syn['date']=pd.to_datetime(syn['date'])
        monthly=syn.groupby(['Hospital','year','month'])['trolley_load'].mean().reset_index()
        monthly['date']=pd.to_datetime(monthly[['year','month']].assign(day=1))
        top5=syn.groupby('Hospital')['trolley_load'].mean().nlargest(5).index
        fig=px.line(monthly[monthly['Hospital'].isin(top5)],x='date',y='trolley_load',color='Hospital',title="Monthly Avg Trolley Load — Top 5 Hospitals")
        fig.update_layout(plot_bgcolor='white',paper_bgcolor='white',height=400)
        st.plotly_chart(fig,use_container_width=True)
        seasonal=syn.groupby('month')['occupancy_rate_pct'].mean().reset_index()
        fig2=px.bar(seasonal,x='month',y='occupancy_rate_pct',title="Average Occupancy by Month — Seasonal Pattern",color='occupancy_rate_pct',color_continuous_scale=['#16A34A','#D97706','#DC2626'])
        fig2.update_layout(plot_bgcolor='white',paper_bgcolor='white',height=350)
        st.plotly_chart(fig2,use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "🧠 Prescriptive":
    from utils.prescriptive_engine import run_prescriptive
    st.markdown('<div class="pad">', unsafe_allow_html=True)
    st.title("🧠 Prescriptive Analytics — Rule Engine")
    if not master.empty:
        pdf=run_prescriptive(master)
        u=(pdf['System Action']=='URGENT REDIRECT').sum(); w=(pdf['System Action']=='EARLY WARNING').sum(); o=pdf['System Action'].isin(['MONITOR','NO ACTION','IMPROVING']).sum()
        c1,c2,c3=st.columns(3); c1.metric("🚨 Urgent Redirect",u); c2.metric("⚠️ Early Warning",w); c3.metric("✅ Monitor/OK",o)
        def ca(v):
            if v=='URGENT REDIRECT': return 'background-color:#FEE2E2;color:#DC2626;font-weight:600'
            if v=='EARLY WARNING': return 'background-color:#FEF3C7;color:#D97706;font-weight:600'
            if v=='IMPROVING': return 'background-color:#DCFCE7;color:#16A34A'
            return ''
        def cs(v):
            if v=='Red': return 'color:#DC2626;font-weight:600'
            if v=='Amber': return 'color:#D97706;font-weight:600'
            if v=='Green': return 'color:#16A34A;font-weight:600'
            return ''
        st.dataframe(pdf.style.applymap(ca,subset=['System Action']).applymap(cs,subset=['Current Status','Predicted']),use_container_width=True,height=500)
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "🔍 EDA":
    st.markdown('<div class="pad">', unsafe_allow_html=True)
    st.title("🔍 EDA & Insights")
    if not synthetic.empty:
        c1,c2,c3=st.columns(3)
        c1.metric("Total Rows",f"{len(synthetic):,}"); c2.metric("Hospitals",synthetic['Hospital'].nunique()); c3.metric("Columns",len(synthetic.columns))
        st.markdown("---")
        wt=synthetic['wait_tier'].value_counts().reset_index()
        fig=px.bar(wt,x='wait_tier',y='count',color='wait_tier',color_discrete_map={'No breach':'#16A34A','Low breach':'#D97706','Moderate breach':'#EA580C','High breach':'#DC2626'})
        fig.update_layout(plot_bgcolor='white',paper_bgcolor='white',height=350,showlegend=False)
        st.plotly_chart(fig,use_container_width=True)
        st.dataframe(synthetic,use_container_width=True,height=400)
        csv=synthetic.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV",csv,"synthetic.csv","text/csv")
    st.markdown('</div>', unsafe_allow_html=True)
