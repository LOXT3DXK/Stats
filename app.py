import streamlit as st

# 1. CONFIGURACIÓN
st.set_page_config(page_title="LOXT Performance", page_icon="⚽", layout="centered")

# 2. CSS: Estética Pro y Compactación de Sidebar
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');

    .stApp {
        background: linear-gradient(180deg, #4da3ff 0%, #00264d 50%, #000814 100%) !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Sidebar sin scroll y compacta */
    [data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.2) !important;
        width: 250px !important;
    }
    [data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 0rem !important;
    }
    div.stNumberInput, div.stRadio, div.stSlider {
        margin-bottom: -15px !important;
    }

    /* Zona Principal */
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 8px !important;
        padding: 10px !important; 
    }

    div[data-testid="stMetricValue"] > div {
        font-size: 1.6rem !important;
        font-weight: 800 !important;
    }

    .nota-card {
        background: rgba(0, 0, 0, 0.2);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        margin-top: 10px;
    }

    .nota-valor {
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        margin: 5px 0;
    }

    h1 {
        font-size: 1.5rem !important;
        margin-bottom: 1rem !important;
        text-align: center;
    }

    .stProgress > div > div > div > div {
        background-color: #ffffff !important;
        height: 8px !important;
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
    # Ajuste proporcional a la exigencia (Meta de G/A para alcanzar el 7.0 base)
    tpp = (ga_rate * 10) / (exigencia * 1.75 / 4) 
    
    if modo == "Mensual":
        bono = min(pj / 16, 1.0)
    else:
        bono = (pj * 2) / 48 if pj <= 48 else 2.0 + ((pj - 48) // 4) * 0.1
    
    nota_final = min(tpp + bono, 10.0)
else:
    ga_rate = bono = nota_final = 0.0

# 5. INTERFAZ PRINCIPAL
st.title("LOXT PERFORMANCE HUB")

col1, col2, col3 = st.columns(3)
col1.metric("G/A RATE", f"{ga_rate:.2f}")
col2.metric("META G/A", f"{exigencia}")
col3.metric(f"BONO", f"{bono:.2f}")

# Contenedor de la Nota Final
st.markdown("<div class='nota-card'>", unsafe_allow_html=True)
st.markdown(f"<p style='color:#b3d9ff; font-weight:bold; margin:0; font-size:0.8rem;'>VALORACIÓN FINAL</p>", unsafe_allow_html=True)
st.markdown(f'<p class="nota-valor">{nota_final:.1f}</p>', unsafe_allow_html=True)

st.progress(int(nota_final * 10))

# 6. ESCALA DE RENDIMIENTO (Corrección de SyntaxError)
if pj > 0:
    if nota_final >= 10.0:
        status = "LEYENDA"
        color = "#ffffff"
    elif nota_final >= 8.0:
        status = "TOP"
        color = "#81d4fa"
    elif nota_final >= 6.0:
        status = "INCREÍBLE RENDIMIENTO"
        color = "#4db6ac"
    elif nota_final >= 5.0:
        status = "APROBADO"
        color = "#aed581"
    elif nota_final >= 1.0:
        status = "REPROBADO"
        color = "#ff8a65"
    else:
        status = "RENDIMIENTO NULO"
        color = "#ff5252"
    
    st.markdown(f"<p style='margin-top:15px; font-weight:900; color:{color}; font-size:1.2rem;'>STATUS: {status}</p>", unsafe_allow_html=True)
else:
    st.markdown("<p style='margin-top:15px; color:grey;'>Esperando datos de partidos...</p>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
