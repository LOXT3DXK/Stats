import streamlit as st

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="LOXT Stats Analyzer", 
    page_icon="⚽",
    layout="centered"
)

# 2. CSS: Degradado, Espaciado y Sidebar Compacta
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');

    /* Fondo: Degradado de Azul Claro a Oscuro */
    .stApp {
        background: linear-gradient(180deg, #4da3ff 0%, #00264d 50%, #000814 100%) !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Sidebar: Más pequeña y sin scroll interno */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        width: 260px !important;
    }
    
    [data-testid="stSidebar"] .block-container {
        padding-top: 2rem !important;
        padding-bottom: 0rem !important;
    }

    /* Ajuste de espaciado para que no estén tan juntos */
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        padding: 20px !important; /* Más aire interno */
        margin-bottom: 15px !important;
    }

    /* Números de métricas grandes y claros */
    div[data-testid="stMetricValue"] > div {
        font-family: 'Inter', sans-serif !important;
        font-weight: 900 !important;
        font-size: 2.2rem !important;
        color: #ffffff !important;
    }

    /* Tarjeta de Nota Final */
    .nota-card {
        background: rgba(0, 0, 0, 0.2);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        margin-top: 25px;
    }

    .nota-valor {
        font-size: 4.5rem !important;
        font-weight: 900 !important;
        color: #ffffff !important;
        margin: 10px 0;
        text-shadow: 0px 4px 10px rgba(0,0,0,0.3);
    }

    /* Títulos con más espacio */
    h1 {
        font-size: 2rem !important;
        letter-spacing: 2px;
        margin-bottom: 2rem !important;
    }

    /* Personalización de la barra de progreso */
    .stProgress > div > div > div > div {
        background-color: #4da3ff !important;
        height: 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR (Data Entry Compacto)
with st.sidebar:
    st.markdown("<h3 style='color:white; margin-bottom:20px;'>DATA ENTRY</h3>", unsafe_allow_html=True)
    
    # Texto simplificado por petición del usuario
    exigencia = st.slider("Nivel de Exigencia", 1.0, 10.0, 4.0, step=0.5)
    
    st.divider()
    
    modo = st.radio("Periodo:", ["Mensual", "Temporada"])
    pj = st.number_input("Partidos (PJ)", min_value=0, step=1, key="pj")
    goles = st.number_input("Goles", min_value=0, step=1, key="goles")
    asist = st.number_input("Asistencias", min_value=0, step=1, key="asist")

# 4. LÓGICA DE CÁLCULO
g_a_total = goles + asist

if pj > 0 and g_a_total > 0:
    ga_rate = g_a_total / pj
    
    # Ajuste proporcional basado en la meta de exigencia elegida
    # Si ga_rate es igual a (exigencia/pj), la nota base es 7.0
    objetivo_por_partido = exigencia / pj if pj > 0 else 1
    tpp = (ga_rate * 7) / objetivo_por_partido
    
    if modo == "Mensual":
        bono = min(pj / 16, 1.0)
        tipo_bono = "BR M"
    else:
        bono = (pj * 2) / 48 if pj <= 48 else 2.0 + ((pj - 48) // 4) * 0.1
        tipo_bono = "BR T"
    
    nota_final = min(tpp + bono, 10.0)
else:
    ga_rate = tpp = bono = nota_final = 0.0
    tipo_bono = "BR M" if modo == "Mensual" else "BR T"

# 5. INTERFAZ PRINCIPAL
st.title("LOXT PERFORMANCE HUB")

# Cuadros de métricas con más separación
col1, col2, col3 = st.columns(3)
col1.metric("G/A RATE", f"{ga_rate:.2f}")
col2.metric("META ACTUAL", f"{exigencia}")
col3.metric(f"BONO {modo[0]}", f"{bono:.2f}")

# Contenedor de la Nota Final
st.markdown("<div class='nota-card'>", unsafe_allow_html=True)
st.markdown(f"<p style='color:#b3d9ff; font-weight:bold; margin:0; letter-spacing:3px;'>VALORACIÓN DEL RENDIMIENTO</p>", unsafe_allow_html=True)
st.markdown(f'<p class="nota-valor">{nota_final:.1f}</p>', unsafe_allow_html=True)

# Barra de progreso más gruesa
st.progress(int(nota_final * 10))

# Status final
if pj > 0:
    if nota_final >= 9.0: status = "NIVEL ELITE MUNDIAL"
    elif nota_final >= 7.0: status = "RENDIMIENTO PRO"
    elif nota_final >= 5.0: status = "NIVEL COMPETITIVO"
    else: status = "BAJO RENDIMIENTO"
    st.markdown(f"<p style='margin-top:15px; font-weight:700; font-size:1.1rem;'>ESTADO: {status}</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
