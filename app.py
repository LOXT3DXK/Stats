import streamlit as st

# 1. CONFIGURACIÓN
st.set_page_config(page_title="LOXT Street Stats", page_icon="⚽", layout="centered")

# 2. CSS: Estilo Callejero / Dorsal de Fútbol
st.markdown("""
    <style>
    /* Importar fuentes: Oswald para títulos y Stardos Stencil para el look callejero */
    @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@700&family=Stardos+Stencil:wght@700&family=Bebas+Neue&display=swap');

    /* Fondo principal: Azul Profundo Gradual */
    .stApp {
        background: linear-gradient(180deg, #001220 0%, #000000 100%) !important;
    }

    /* Barra Lateral: Más limpia, estilo "Vestuario" */
    [data-testid="stSidebar"] {
        background-color: #001a33 !important;
        background-image: radial-gradient(#00264d 1px, transparent 1px) !important;
        background-size: 20px 20px !important; /* Textura de puntos sutil */
        border-right: 2px solid #0059b3;
    }

    /* Títulos */
    h1, h3 {
        font-family: 'Bebas Neue', sans-serif !important;
        color: #ffffff !important;
        letter-spacing: 2px;
    }

    /* Cuadros de Métricas: Estilo Placa de Metal */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 2px solid #ffffff !important;
        border-radius: 0px !important; /* Cuadrados, más agresivos */
        padding: 15px !important;
        box-shadow: 5px 5px 0px #0059b3; /* Sombra sólida bloque */
    }

    /* Números: ESTILO DORSAL/CALLEJERO (Sin puntos en el centro) */
    div[data-testid="stMetricValue"] > div {
        font-family: 'Bebas Neue', sans-serif !important;
        font-size: 3rem !important;
        color: #ffffff !important;
        letter-spacing: 1px;
    }

    /* Etiquetas de métricas */
    div[data-testid="stMetricLabel"] > div {
        color: #ffffff !important;
        font-family: 'Oswald', sans-serif !important;
        text-transform: uppercase;
        opacity: 0.8;
    }

    /* Nota Final: Gigante estilo Graffiti/Dorsal */
    .street-score {
        font-family: 'Stardos Stencil', cursive !important;
        font-size: 6rem !important;
        color: #ffffff !important;
        text-shadow: 3px 3px 0px #0059b3, 6px 6px 0px #000;
        margin: 0px;
    }

    /* Inputs de la Sidebar */
    .stNumberInput label, .stRadio label {
        color: white !important;
        font-family: 'Oswald', sans-serif !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR (Data Entry Simplificado)
with st.sidebar:
    st.markdown("<h3>CONFIGURACIÓN</h3>", unsafe_allow_html=True)
    modo = st.radio("MODO DE JUEGO:", ["Mensual", "Temporada"])
    st.markdown("<br>", unsafe_allow_html=True)
    pj = st.number_input("PARTIDOS JUGADOS", min_value=0, step=1)
    goles = st.number_input("GOLES", min_value=0, step=1)
    asist = st.number_input("ASISTENCIAS", min_value=0, step=1)

# 4. LÓGICA (Ley de Hierro)
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
st.markdown("<p style='color:grey; font-family:Oswald;'>CALCULADORA DE RENDIMIENTO CALLEJERO</p>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
col1.metric("G/A RATE", f"{ga_rate:.2f}")
col2.metric("BASE TPP", f"{min(tpp, 10.0):.1f}")
col3.metric(f"BONO {modo[0]}", f"{bono:.2f}")

st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

# Área de la Nota Final
st.markdown("<center>", unsafe_allow_html=True)
st.markdown(f"<p style='color:white; font-family:Bebas Neue; letter-spacing:4px; font-size:1.2rem;'>RATING FINAL</p>", unsafe_allow_html=True)
st.markdown(f'<div class="street-score">{nota_final:.1f}</div>', unsafe_allow_html=True)

if pj > 0:
    if nota_final >= 9.0: status = "MVP / LEYENDA"
    elif nota_final >= 7.0: status = "TITULAR PRO"
    elif nota_final >= 5.0: status = "EN RACHA"
    else: status = "BAJO NIVEL"
    st.markdown(f"<h2 style='color:white; font-family:Bebas Neue;'>{status}</h2>", unsafe_allow_html=True)
st.markdown("</center>", unsafe_allow_html=True)
