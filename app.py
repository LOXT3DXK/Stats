import streamlit as st

# 1. CONFIGURACIÓN
st.set_page_config(page_title="LOXT Performance Hub", page_icon="⚽", layout="centered")

# 2. CSS: Ondas, Colores y Layout
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');

    .stApp {
        background: linear-gradient(135deg, #001a33 0%, #004d40 100%);
        background-attachment: fixed;
    }
    
    /* Efecto de ondas difuminadas */
    .stApp::before {
        content: "";
        position: absolute;
        top: -50%; left: -50%; width: 200%; height: 200%;
        background: radial-gradient(circle at center, rgba(0,255,150,0.03) 0%, transparent 60%);
        filter: blur(60px);
        animation: waves 15s infinite alternate;
        z-index: -1;
    }

    @keyframes waves {
        from { transform: translate(-5%, -5%) rotate(0deg); }
        to { transform: translate(5%, 5%) rotate(3deg); }
    }

    /* Sidebar Compacta */
    [data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.4) !important;
        backdrop-filter: blur(10px);
        width: 250px !important;
    }
    [data-testid="stSidebar"] .block-container { padding-top: 1rem !important; }
    div.stNumberInput, div.stRadio, div.stSlider { margin-bottom: -15px !important; }

    /* Cuadros de Métricas */
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        padding: 12px !important;
    }

    div[data-testid="stMetricValue"] > div {
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 1.7rem !important;
    }

    /* Tarjeta de Valoración */
    .nota-card {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        margin-top: 15px;
    }

    .nota-valor {
        font-size: 3.8rem !important;
        font-weight: 900 !important;
        margin: 5px 0;
        line-height: 1;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR (Data Entry)
with st.sidebar:
    st.markdown("<h3 style='color:white; font-size:1rem; margin-bottom:10px;'>DATA ENTRY</h3>", unsafe_allow_html=True)
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
    nota_final = min(tpp + bono, 10.0)
else:
    ga_rate = tpp = bono = nota_final = 0.0

# 5. DETERMINAR STATUS Y COLORES
if pj > 0:
    if nota_final >= 10.0:
        status, color = "LEYENDA", "#9d4edd" # Morado Leyenda
    elif nota_final >= 8.0:
        status, color = "TOP", "#ffffff" # Blanco
    elif nota_final >= 6.0:
        status, color = "IDEAL", "#4db6ac" # Verde Azulado
    elif nota_final >= 5.0:
        status, color = "APROBADO", "#81c784" # Verde
    elif nota_final >= 1.0:
        status, color = "REPROBADO", "#e57373" # Rojo claro
    else:
        status, color = "RENDIMIENTO NULO", "#ff5252" # Rojo
else:
    status, color = "SIN DATOS", "#546e7a"

# 6. INTERFAZ PRINCIPAL
st.markdown("<h1 style='color:white; text-align:center;'>LOXT PERFORMANCE HUB</h1>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
c1.metric("G/A RATE", f"{ga_rate:.2f}")
c2.metric("TPP (NOTA BASE)", f"{min(tpp, 10.0):.1f}")
c3.metric("BONO", f"{bono:.2f}")

# Tarjeta de Nota Final
st.markdown(f"""
    <div class='nota-card'>
        <p style='color:rgba(255,255,255,0.6); font-weight:bold; margin:0; font-size:0.8rem;'>VALORACIÓN FINAL</p>
        <p class='nota-valor' style='color:{color};'>{nota_final:.1f}</p>
    </div>
    <div style="width: 100%; background-color: rgba(255,255,255,0.1); border-radius: 10px; margin-top: 10px;">
        <div style="width: {nota_final*10}%; background-color: {color}; height: 12px; border-radius: 10px; transition: 0.5s;"></div>
    </div>
    <p style='margin-top:15px; font-weight:900; color:{color}; font-size:1.2rem; text-align:center;'>
        STATUS: {status}
    </p>
    """, unsafe_allow_html=True)
