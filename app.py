import streamlit as st

# 1. CONFIGURACIÓN DE PÁGINA (Compacta y Centrada)
st.set_page_config(
    page_title="LOXT Stats", 
    page_icon="⚽",
    layout="centered"
)

# 2. CSS AVANZADO: Estilo Claro, Futurista y Compacto
st.markdown("""
    <style>
    /* Importar fuente sans-serif limpia y moderna */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

    /* Fondo Principal: Degradado Azul Claro Futurista */
    .stApp {
        background: linear-gradient(135deg, #e0f7fa 0%, #81d4fa 100%) !important;
        color: #003366 !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Barra Lateral: Clara y Simple (Estilo Clínico) */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #b3e5fc;
    }
    
    /* Compactar la Sidebar */
    [data-testid="stSidebar"] .block-container {
        padding-top: 1rem !important;
    }

    /* Títulos Principales */
    h1 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 800 !important;
        font-size: 1.8rem !important;
        color: #003366 !important;
        margin-bottom: 0.5rem !important;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Cuadros de Métricas: Futuristas Claros */
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.7) !important;
        border: 1px solid #81d4fa !important;
        border-radius: 8px !important;
        padding: 10px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }

    /* Números de Métricas: Blancos sobre el fondo del cuadro */
    div[data-testid="stMetricValue"] > div {
        font-family: 'Inter', sans-serif !important;
        font-weight: 800 !important;
        font-size: 2rem !important;
        color: #003366 !important; /* Azul oscuro para contraste sobre blanco */
    }

    /* Etiquetas de métricas */
    div[data-testid="stMetricLabel"] > div {
        color: #005662 !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        text-transform: uppercase;
        font-size: 0.8rem !important;
    }

    /* Nota Final y Progreso */
    .nota-container {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 8px 15px rgba(0,0,0,0.1);
        text-align: center;
        margin-top: 10px;
    }

    .nota-final {
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        color: #0277bd !important;
        line-height: 1;
        margin: 0;
    }

    /* Ajustar espacios generales para evitar scroll */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }
    
    div.stNumberInput, div.stRadio {
        margin-bottom: -10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR (Data Entry Simple y Claro)
with st.sidebar:
    st.markdown("<h2 style='color:#003366; text-align:center;'>INPUTS</h2>", unsafe_allow_html=True)
    modo = st.radio("Periodo:", ["Mensual", "Temporada"])
    st.markdown("---", unsafe_allow_html=True)
    pj = st.number_input("Partidos (PJ)", min_value=0, step=1)
    goles = st.number_input("Goles", min_value=0, step=1)
    asist = st.number_input("Asistencias", min_value=0, step=1)

# 4. LÓGICA DE CÁLCULO
g_a_total = goles + asist

if pj > 0 and g_a_total > 0:
    ga_rate = g_a_total / pj
    tpp = (ga_rate * 10) / 7
    
    if modo == "Mensual":
        bono = min(pj / 16, 1.0)
        tipo_bono = "BR M"
    else:
        if pj <= 48:
            bono = (pj * 2) / 48
        else:
            bono = 2.0 + ((pj - 48) // 4) * 0.1
        tipo_bono = "BR T"
    
    nota_final = min(tpp + bono, 10.0)
else:
    ga_rate = tpp = bono = nota_final = 0.0
    tipo_bono = "BR M" if modo == "Mensual" else "BR T"

# 5. MAIN INTERFACE (Compacta)
st.title("LOXT PERFORMANCE HUB")

# Fila de Métricas (Más pequeñas)
col1, col2, col3 = st.columns(3)
col1.metric("G/A RATE", f"{ga_rate:.2f}")
col2.metric("TPP BASE", f"{min(tpp, 10.0):.1f}")
col3.metric(f"BONO {modo[0]}", f"{bono:.2f}")

# Fila de Nota Final y Barra de Progreso
st.markdown("<div class='nota-container'>", unsafe_allow_html=True)
st.markdown(f"<p style='color:#005662; font-weight:600; margin:0;'>VALORACIÓN FINAL ({tipo_bono})</p>", unsafe_allow_html=True)
st.markdown(f'<p class="nota-final">{nota_final:.1f}</p>', unsafe_allow_html=True)

# BARRA DE PROGRESO (Original, escalada a 10.0)
progress_value = int(nota_final * 10) # Streamlit progress usa 0-100
st.progress(progress_value)

if pj > 0:
    if nota_final >= 9.0: status, color = "LEYENDA/MVP", "#0277bd"
    elif nota_final >= 7.0: status, color = "TITULAR PRO", "#00838f"
    elif nota_final >= 5.0: status, color = "COMPETITIVO", "#00695c"
    else: status, color = "INSUFICIENTE", "#c62828"
    st.markdown(f"<p style='color:{color}; font-weight:800; margin-top:5px;'>{status}</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
