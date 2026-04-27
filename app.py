import streamlit as st

# 1. CONFIGURACIÓN
st.set_page_config(page_title="LOXT Performance Hub", page_icon="⚽", layout="centered")

# 2. CSS: Ondas difuminadas, Colores Dinámicos y Layout
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');

    /* Fondo con Ondas Difuminadas (Azul a Verde) */
    .stApp {
        background: linear-gradient(135deg, #001a33 0%, #004d40 100%);
        background-attachment: fixed;
        overflow: hidden;
    }
    
    .stApp::before {
        content: "";
        position: absolute;
        top: -50%; left: -50%; width: 200%; height: 200%;
        background: radial-gradient(circle at center, rgba(0,255,150,0.05) 0%, transparent 50%);
        filter: blur(80px);
        animation: waves 20s infinite alternate;
        z-index: -1;
    }

    @keyframes waves {
        from { transform: translate(-10%, -10%) rotate(0deg); }
        to { transform: translate(10%, 10%) rotate(5deg); }
    }

    /* Sidebar Compacta */
    [data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(10px);
    }
    [data-testid="stSidebar"] .block-container { padding-top: 1.5rem !important; }
    div.stNumberInput, div.stRadio, div.stSlider { margin-bottom: -15px !important; }

    /* Cuadros de Métricas */
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }

    /* Textos Principales en Blanco */
    div[data-testid="stMetricValue"] > div {
        color: #ffffff !important;
        font-weight: 900 !important;
        font-size: 1.8rem !important;
    }
    
    div[data-testid="stMetricLabel"] > div {
        color: rgba(255,255,255,0.8) !important;
        font-size: 0.8rem !important;
        letter-spacing: 1px;
    }

    /* Contenedor de Valoración Final */
    .nota-card {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        margin-top: 20px;
        backdrop-filter: blur(5px);
    }

    .nota-valor {
        font-size: 4rem !important;
        font-weight: 900 !important;
        margin: 5px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR (Data Entry)
with st.sidebar:
    st.markdown("<h3 style='color:white; font-size:1.1rem;'>DATA ENTRY</h3>", unsafe_allow_html=True)
    exigencia = st.slider("Nivel de Exigencia", 1.0, 10.0, 4.0, step=0.5)
    modo = st.radio("Periodo:", ["Mensual", "Temporada"])
    st.markdown("---")
    pj = st.number_input("Partidos (PJ)", min_value=0, step=1)
    goles = st.number_input("Goles", min_value=0, step=1)
    asist = st.number_input("Asistencias", min_value=0, step=1)

# 4. LÓGICA DE CÁLCULO
g_a_total = goles + asist
if pj > 0 and g_a_total > 0:
    ga_rate = g_a_total / pj
    tpp = (ga_rate * 10) / (exigencia * 1.75 / 4) 
    bono = min(pj / 16, 1.0) if modo == "Mensual" else ((pj * 2) / 48 if pj <= 48 else 2.0 + ((pj - 48) // 4) * 0.1)
    nota_
