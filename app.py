import streamlit as st

# 1. CONFIGURACIÓN DE PÁGINA (Compacta)
st.set_page_config(
    page_title="LOXT Stats", 
    page_icon="⚽",
    layout="centered"
)

# 2. DISEÑO UNIFICADO AZUL-VERDE (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@600&display=swap');

    /* Fondo Degradado Unificado (App y Sidebar) */
    .stApp, [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #002b36 0%, #004d40 100%) !important;
    }
    
    /* Hacer que la barra lateral sea transparente para que se vea el degradado */
    [data-testid="stSidebar"] > div:first-child {
        background: transparent !important;
    }

    /* Reducir espacios y compactar */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }

    h1 {
        font-family: 'Oswald', sans-serif !important;
        font-size: 1.8rem !important;
        margin-bottom: 0.5rem !important;
        color: #ffffff;
        text-align: center;
    }

    /* Cuadros de métricas más pequeños y con borde sutil */
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.07) !important;
        border: 1.5px solid #26a69a !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }

    div[data-testid="stMetricValue"] > div {
        font-family: 'Oswald', sans-serif !important;
        font-size: 1.6rem !important;
        color: #4db6ac !important;
    }

    /* Nota final compacta */
    .nota-display {
        font-family: 'Oswald', sans-serif !important;
        font-size: 3.5rem !important;
        color: #ffffff;
        margin: 0px !important;
        line-height: 1 !important;
    }

    /* Estilo para los inputs de la barra lateral */
    .stNumberInput, .stRadio {
        color: white !important;
        font-size: 0.8rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. INTERFAZ COMPACTA
st.title("⚽ LOXT PERFORMANCE")

# Data Entry en Sidebar (Mismo tono que el fondo)
with st.sidebar:
    st.markdown("<h3 style='color:white; font-family:Oswald;'>DATA ENTRY</h3>", unsafe_allow_html=True)
    modo = st.radio("Periodo:", ["Mensual", "Temporada"])
    pj = st.number_input("PJ", min_value=0, value=0, step=1)
    goles = st.number_input("Goles", min_value=0, value=0, step=1)
    asist = st.number_input("Asist", min_value=0, value=0, step=1)

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

# 5. RESULTADOS EN UNA SOLA FILA
c1, c2, c3 = st.columns(3)
c1.metric("G/A RATE", round(ga_rate, 2))
c2.metric("TPP BASE", round(min(tpp, 10.0), 1))
c3.metric(f"BONO {modo[:1]}", round(bono, 2))

# Visualización central de la Nota
st.markdown("<hr style='margin:10px 0;'>", unsafe_allow_html=True)
st.markdown(f"<center><p style='font-family:Oswald; font-size:1rem; margin:0;'>VALORACIÓN FINAL ({tipo_bono})</p>", unsafe_allow_html=True)

if nota_final == 0 and pj > 0:
    st.markdown(f'<p class="nota-display" style="color:#ff5252;">{round(nota_final, 1)}</p>', unsafe_allow_html=True)
    st.caption("Requiere producción para calificar")
else:
    color_nota = "#4db6ac" if nota_final >= 7 else "#ffffff"
    st.markdown(f'<p class="nota-display" style="color:{color_nota};">{round(nota_final, 1)}</p>', unsafe_allow_html=True)

# Estado de rendimiento en texto pequeño
if pj > 0:
    if nota_final >= 9.0: status = "ÉLITE"
    elif nota_final >= 7.0: status = "SOBRESALIENTE"
    elif nota_final >= 5.0: status = "COMPETITIVO"
    else: status = "INSUFICIENTE"
    st.markdown(f"<center><b>ESTADO: {status}</b></center>", unsafe_allow_html=True)
