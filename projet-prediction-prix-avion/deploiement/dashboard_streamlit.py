#  ── Imports ──

import joblib
import numpy as np
import pandas as pd
import streamlit as st
from pathlib import Path
import requests

# ── Configuration ──
st.set_page_config(
    page_title="Flight Price Finder",
    page_icon="✈️",
    layout="wide",
)

# ── Thèmes ──
THEMES = {
    "Ciel":   dict(bg="#f3f7fc", card="#ffffff", card2="#eef3fa", text="#18263b", muted="#64748b",
                   accent="#2563eb", accent2="#1d4ed8", soft="rgba(37,99,235,.10)",
                   line="rgba(37,99,235,.28)", border="rgba(15,23,42,.10)", shadow="rgba(37,99,235,.28)"),
    "Menthe": dict(bg="#f2f9f6", card="#ffffff", card2="#e9f5f0", text="#14312b", muted="#5f7a73",
                   accent="#0d8a73", accent2="#0a7461", soft="rgba(13,138,115,.10)",
                   line="rgba(13,138,115,.30)", border="rgba(20,49,43,.10)", shadow="rgba(13,138,115,.28)"),
    "Sable":  dict(bg="#fbf6f0", card="#ffffff", card2="#f6ede2", text="#33261c", muted="#8a7466",
                   accent="#d4501f", accent2="#bf4119", soft="rgba(212,80,31,.10)",
                   line="rgba(212,80,31,.30)", border="rgba(51,38,28,.12)", shadow="rgba(212,80,31,.28)"),
}
THEME_NAME = "Sable"
t = THEMES[THEME_NAME]

st.markdown(f"""
<style>
:root {{
  --bg:{t['bg']}; --card:{t['card']}; --card2:{t['card2']};
  --text:{t['text']}; --muted:{t['muted']};
  --accent:{t['accent']}; --accent2:{t['accent2']};
  --soft:{t['soft']}; --line:{t['line']};
  --border:{t['border']}; --shadow:{t['shadow']};
}}
</style>
""", unsafe_allow_html=True)

# ── CSS (utilise les variables ci-dessus) ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=Inter:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: var(--bg); color: var(--text); }
header[data-testid="stHeader"] { background: transparent; }

/* hero */
.hero { text-align: center; padding: 2.5rem 0 1.5rem; }
.hero-badge { display: inline-block; background: var(--soft); border: 1px solid var(--line);
  color: var(--accent); font-size: .75rem; font-weight: 600; padding: 4px 14px; border-radius: 999px;
  margin-bottom: 1rem; letter-spacing: .8px; text-transform: uppercase; }
.hero-title { font-family: 'Syne', sans-serif; font-size: 2.8rem; font-weight: 800;
  letter-spacing: -1px; color: var(--text); margin: 0 0 .4rem; }
.hero-sub { color: var(--muted); font-size: 1rem; font-weight: 300; }

/* carte formulaire (conteneur Streamlit key="form_card") */
.st-key-form_card { background: var(--card); border: 1px solid var(--border); border-radius: 20px;
  padding: 1.8rem 2rem 1.5rem; box-shadow: 0 8px 30px rgba(15,23,42,.06); }
.form-section-label, .result-label, .detail-title { font-size: .7rem; font-weight: 600;
  letter-spacing: 1.2px; text-transform: uppercase; color: var(--accent); }
.form-section-label { margin-bottom: .6rem; }
.result-label { margin-bottom: .5rem; }
.detail-title { margin-bottom: 1rem; }

/* widgets */
div[data-testid="stSelectbox"] label p, div[data-testid="stSlider"] label p,
div[data-testid="stNumberInput"] label p, div[data-testid="stSegmentedControl"] label p {
  color: var(--muted) !important; font-size: .8rem !important; font-weight: 500 !important; }
div[data-baseweb="select"] > div, div[data-baseweb="input"] {
  background: var(--card2) !important; border: 1px solid var(--border) !important; border-radius: 10px !important; }
div[data-baseweb="select"] *, div[data-baseweb="input"] input { color: var(--text) !important; }
div[data-baseweb="input"] input { background: transparent !important; }
div[data-testid="stNumberInput"] button { background: transparent !important; color: var(--muted) !important; }

/* bouton */
.stButton > button { width: 100%; background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
  color: #fff !important; border: none !important; border-radius: 12px !important;
  padding: .9rem 1.5rem !important; font-family: 'Syne', sans-serif !important; font-size: 1rem !important;
  font-weight: 700 !important; transition: all .2s ease !important; box-shadow: 0 4px 18px var(--shadow) !important; }
.stButton > button:hover { transform: translateY(-1px); box-shadow: 0 8px 24px var(--shadow) !important; }

/* résultat */
.result-card { background: var(--card); border: 1px solid var(--line); border-radius: 20px;
  padding: 2rem; box-shadow: 0 8px 30px rgba(15,23,42,.06); }
.price-inr { font-family: 'Syne', sans-serif; font-size: 3rem; font-weight: 800; color: var(--text); line-height: 1; margin: 0; }
.price-eur { font-size: 1.3rem; color: var(--accent); margin-top: .25rem; }
.price-note { font-size: .75rem; color: var(--muted); margin-top: .5rem; }
.divider { border: none; border-top: 1px solid var(--border); margin: 1.5rem 0; }

.pill { display: inline-block; padding: 5px 12px; border-radius: 999px; background: var(--card2);
  border: 1px solid var(--border); font-size: .78rem; color: var(--muted); margin: 3px 4px 3px 0; }
.pill-highlight { background: var(--soft); border-color: var(--line); color: var(--accent); }

.conf-high, .conf-medium, .conf-low { padding: 6px 14px; border-radius: 999px; font-size: .8rem; font-weight: 500; display: inline-block; }
.conf-high   { background: rgba(16,185,129,.12); border: 1px solid rgba(16,185,129,.35); color: #047857; }
.conf-medium { background: rgba(245,158,11,.12); border: 1px solid rgba(245,158,11,.35); color: #b45309; }
.conf-low    { background: rgba(239,68,68,.10);  border: 1px solid rgba(239,68,68,.30);  color: #b91c1c; }

.detail-card { background: var(--card2); border: 1px solid var(--border); border-radius: 16px; padding: 1.5rem; height: 100%; }
.detail-row { display: flex; justify-content: space-between; padding: .45rem 0;
  border-bottom: 1px solid var(--border); font-size: .85rem; }
.detail-row:last-child { border-bottom: none; }
.detail-key { color: var(--muted); }
.detail-value { color: var(--text); font-weight: 500; }
</style>
""", unsafe_allow_html=True)

# -------------------------------- Chargement modèle -------------------

@st.cache_resource
def load_model():
    model_path = Path(__file__).parent.parent / "artifacts" / "flight_price_model.joblib"
    if not model_path.exists():
        st.error("Modèle introuvable — vérifie le chemin vers `artifacts/flight_price_model.joblib`.")
        st.stop()
    return joblib.load(model_path)

# ------------------Taux de change ----------------

@st.cache_data(ttl=3600)
def get_eur_rate():
    try:
        r = requests.get("https://api.exchangerate-api.com/v4/latest/INR", timeout=5)
        return r.json()["rates"]["EUR"]
    except Exception:
        return 0.011

model = load_model()

# ----------------------- Constantes -------------------------------
AIRLINES   = ['Vistara', 'Air_India', 'Indigo', 'GO_FIRST', 'AirAsia', 'SpiceJet']
CITIES     = ['Delhi', 'Mumbai', 'Bangalore', 'Kolkata', 'Hyderabad', 'Chennai']
TIME_BANDS = ['Morning', 'Afternoon', 'Evening', 'Night', 'Early_Morning', 'Late_Night']
STOPS_MAP  = {"zero": 0, "one": 1, "two_or_more": 2}
CLASS_MAP  = {"Economy": 0, "Business": 1}

AIRLINE_FLAGS = {
    'Vistara': '🟣', 'Air_India': '🔴', 'Indigo': '🔵',
    'GO_FIRST': '🟠', 'AirAsia': '🔴', 'SpiceJet': '🟡'
}

# ----------------------- Fonctions helpers ---------------------------

def make_row(airline, source_city, dest_city, dep_time, arr_time, duration, days_left, stops, cls):
    # Valeur par défaut si None
    cls = cls or "Economy"
    stops = stops or "zero"
    
    return pd.DataFrame([{
        "airline": airline,
        "source_city": source_city,
        "destination_city": dest_city,
        "departure_time": dep_time,
        "arrival_time": arr_time,
        "duration": float(duration),
        "days_left": int(days_left),
        "stops_num": int(STOPS_MAP[stops]),
        "class_num": int(CLASS_MAP[cls]),
    }])

def fmt_inr(x):
    return f"₹ {float(x):,.0f}"

def get_price_range(model, X_input):
    rf   = model.named_steps["model"]
    prep = model.named_steps["preprocessor"]
    X_t  = prep.transform(X_input)
    preds = np.array([t.predict(X_t) for t in rf.estimators_]).flatten()
    lo, hi = np.percentile(preds, [10, 90])
    return max(0.0, float(lo)), max(0.0, float(hi))

# ---------------------------- Hero ----------------------------------

st.markdown("""
<div class="hero">
  <div class="hero-badge">Machine learning · Vols intérieurs en Inde</div>
  <div class="hero-title">Estimateur de prix de vols</div>
  <div class="hero-sub">Un modèle entraîné sur 300 000 vols réels, déployé avec Docker</div>
</div>
""", unsafe_allow_html=True)

# ------------------------------ Formulaire --------------------------------

with st.container(key="form_card") :

    st.markdown('<div class="form-section-label">Trajet</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1.2, 1.2, 1], vertical_alignment="bottom")
    with c1:
        source_city = st.selectbox("Ville de départ", CITIES, index=0)
    with c2:
        dest_options = [c for c in CITIES if c != source_city]
        destination_city = st.selectbox("Ville d'arrivée", dest_options, index=0)
    with c3:
        class_label = st.segmented_control(
                            "Classe",
                            options=["Economy", "Business"],
                            default="Economy",
                            selection_mode="single"  
                            )
    if class_label is None:
        class_label = "Economy"
        
    st.markdown('<div style="height:1px;background:var(--border);margin:1.2rem 0"></div>', unsafe_allow_html=True)
    st.markdown('<div class="form-section-label">Vol</div>', unsafe_allow_html=True)

    c4, c5, c6, c7 = st.columns([1, 1, 1, 1], vertical_alignment="bottom")
    with c4:
        airline = st.selectbox("Compagnie", AIRLINES, index=0)
    with c5:
        stops_label = st.selectbox("Escales", ["zero", "one", "two_or_more"], index=0,
                                format_func=lambda x: {"zero":"Sans escale","one":"1 escale","two_or_more":"2+ escales"}[x])
    with c6:
        days_left = st.slider("Jours avant le vol", 1, 60, 15)
    with c7:
        duration = st.number_input("Durée (heures)", min_value=0.5, max_value=60.0, value=2.5, step=0.5)

    c8, c9 = st.columns(2, vertical_alignment="bottom")
    with c8:
        departure_time = st.selectbox("Créneau départ", TIME_BANDS, index=0)
    with c9:
        arrival_time = st.selectbox("Créneau arrivée", TIME_BANDS, index=2)

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)
    run = st.button("✈  Estimer le prix", use_container_width=True)



# ---------------------------------------Résultats -------------------------------------

if run:
    if source_city == destination_city:
        st.warning("Départ et arrivée identiques — choisissez deux villes différentes.")
    else:
        X_input = make_row(airline, source_city, destination_city,
                           departure_time, arrival_time, duration,
                           days_left, stops_label, class_label)

        with st.spinner("Calcul en cours…"):
            try:
                pred = max(0.0, float(model.predict(X_input)[0]))
                rate = get_eur_rate()
                pred_eur = pred * rate
                lo, hi = get_price_range(model, X_input)
                lo_eur, hi_eur = lo * rate, hi * rate
            except Exception as e:
                st.error(f"Erreur lors de la prédiction : {e}")
                st.stop()

        left, right = st.columns([1.3, 0.9], gap="large")

        with left:
            st.markdown(f"""
            <div class="result-card">
              <div class="result-label">Prix estimé</div>
              <div class="price-inr">{fmt_inr(pred)}</div>
              <div class="price-eur">≈ {pred_eur:,.0f} €</div>
              <div class="price-note">Taux de change en temps réel · Roupies indiennes</div>
              <hr class="divider">
              <div style="margin-bottom:.1rem">
                  <div class="range-label">Fourchette indicative</div>
                  <div class="range-inr">{fmt_inr(lo)} – {fmt_inr(hi)}</div>
                  <div class="range-eur">≈ {lo_eur:,.0f} – {hi_eur:,.0f} €</div>
              </div>
              <div>
                <span class="pill pill-highlight">{source_city} → {destination_city}</span>
                <span class="pill">{AIRLINE_FLAGS.get(airline,'')} {airline}</span>
                <span class="pill">{'Sans escale' if stops_label=='zero' else stops_label}</span>
                <span class="pill">{class_label}</span>
                <span class="pill">⏱ {duration}h</span>
                <span class="pill">J-{days_left}</span>
                <span class="pill">↑ {departure_time}</span>
                <span class="pill">↓ {arrival_time}</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

        with right:
            rows = {
                "Compagnie": f"{AIRLINE_FLAGS.get(airline,'')} {airline}",
                "Trajet": f"{source_city} → {destination_city}",
                "Classe": class_label,
                "Escales": stops_label,
                "Durée": f"{duration} h",
                "Jours avant vol": f"J-{days_left}",
                "Départ": departure_time,
                "Arrivée": arrival_time,
            }
            rows_html = "".join([
                f'<div class="detail-row"><span class="detail-key">{k}</span><span class="detail-value">{v}</span></div>'
                for k, v in rows.items()
            ])
            st.markdown(f"""
            <div class="detail-card">
              <div class="detail-title">Paramètres envoyés au modèle</div>
              {rows_html}
            </div>
            """, unsafe_allow_html=True)