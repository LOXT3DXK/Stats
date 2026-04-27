import streamlit as st

# 1. CONFIGURACIÓN
st.set_page_config(page_title="LOXT Pro Analyzer", page_icon="⚽", layout="centered")

# 2. CSS AVANZADO: Estilo Deep Blue & Cyber-Gothic
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@700&family=JetBrains+Mono:wght@400;700&display=swap');

    /* Fondo principal: Degradado Azul Profundo con toque Aqua */
    .stApp {
        background: radial-gradient(circle at top, #001a33 0%, #00050a 100%) !important;
    }

    /* Barra Lateral: Diseño Cyber-Gothic */
    [data-testid="stSidebar"] {
        background-color: #000814 !important;
        background-image: 
            linear-gradient(30deg, #001a33 12%, transparent 12.5%, transparent 87%, #001a33 87.5%, #001a33),
            linear-gradient(150deg, #001a33 12%, transparent 12.5%, transparent 87%, #001a33 87.5%, #001a33),
            linear-gradient(30deg, #001a33 12%, transparent 12.5%, transparent 87%, #001a33 87.5%, #001a33),
            linear-gradient(150deg, #001a33 12%, transparent 12.5%, transparent 87%, #001a33 87.5%, #001a33),
            linear-gradient(60deg, #00264d 25%, transparent 25.5%, transparent 75%, #00264d 75%, #00264d),
            linear-gradient(60deg, #00264d 25%, transparent 25.5%, transparent 75%, #00264d 75%, #00264d) !important;
        background-size: 40px 70px !important;
        border-right: 1px solid #004080;
    }

    /* Títulos */
    h1, h3 {
        font-family: 'Oswald', sans-serif !important;
        color: #ffffff !important;
        text-transform: uppercase;
        letter-spacing: 3px;
    }

    /* Cuadros de Métricas: Glassmorphism con textura */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-left: 4px solid #0059b3 !important; /* Barra lateral decorativa */
        border-radius: 4px !important;
        padding: 15px !important;
        box-shadow: 10px 10px 20px rgba(0,0,0,0.5);
        backdrop-filter: blur(5px);
    }

    /* Números en Blanco Puro */
    div[data-testid="stMetricValue"] > div {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 1.8rem !important;
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* Etiquetas de métricas */
    div[data-testid="stMetricLabel"] > div {
        color: #80b3ff !important;
        font-family: 'Oswald', sans-serif !important;
        text-transform: uppercase;
    }

    /* Nota Final Gigante */
    .big-score {
        font-family: 'Oswald', sans-serif !important;
        font-size: 5rem !important;
        color: #ffffff !important;
        line-height: 1;
        margin: 10px 0;
        text-shadow: 4px 4px 0px #003366;
    }

    /* Línea divisoria técnica */
    hr {
        border: 0;
        height: 2px;
        background-image: linear-gradient(to right, transparent, #0059b3, transparent);
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR (Data Entry)
with st.sidebar:
    st.markdown("<h3>SYSTEM ACCESS</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:#80b3ff; font-size:0.7rem;'>LOXT v3.0 // ANALYZER</p>", unsafe_allow_html=True)
    modo = st.radio("PERIOD_SELECTOR:", ["Mensual", "Temporada"])
    st.markdown("---")
    pj = st.number_input("TOTAL_PJ", min_value=0, step=1)
    goles = st.number_input("GOALS_COUNT", min_value=0, step=1)
    asist = st.number_input("ASSISTS_COUNT", min_value=0, step=1)

# 4. LÓGICA
g_a_total = goles + asist
if pj > 0 and g_a_total > 0:
    ga_rate = g_a_total / pj
    tpp = (ga_rate * 10) / 7
    if modo == "Mensual":
        bono = min(pj / 16, 1.0)
    else:
        bono = (pj * 2) / 48 if pj <= 48 else 2.0 + ((pj - 48) // 4) * 0.1
    nota_final = min(tpp + bono, 10.0)
else:
    ga_rate = tpp = bono = nota_final = 0.0

# 5. MAIN INTERFACE
st.title("LOXT PERFORMANCE HUB")

col1, col2, col3 = st.columns(3)
col1.metric("G/A RATE", f"{ga_rate:.2f}")
col2.metric("BASE TPP", f"{min(tpp, 10.0):.1f}")
col3.metric(f"BONUS ({modo[0]})", f"{bono:.2f}")

st.markdown("<hr>", unsafe_allow_html=True)

# Área de la Nota Final
st.markdown("<center>", unsafe_allow_html=True)
st.markdown(f"<p style='color:#80b3ff; letter-spacing:5px; margin:0;'>OVERALL RATING</p>", unsafe_allow_html=True)
st.markdown(f'<div class="big-score">{nota_final:.1f}</div>', unsafe_allow_html=True)

if pj > 0:
    if nota_final >= 9.0: status, color = "ELITE_CLASS", "#ffffff"
    elif nota_final >= 7.0: status, color = "PRO_PERFORMANCE", "#80b3ff"
    elif nota_final >= 5.0: status, color = "CORE_LEVEL", "#4d94ff"
    else: status, color = "LOW_EFFICIENCY", "#ff4d4d"
    st.markdown(f"<p style='color:{color}; font-family:JetBrains Mono; font-weight:bold;'>[ STATUS: {status} ]</p>", unsafe_allow_html=True)
st.markdown("</center>", unsafe_allow_html=True)
