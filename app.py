import streamlit as st

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="LOXT Stats - Pro Edition", 
    page_icon="⚽",
    layout="centered"
)

# 2. DISEÑO SPORT-PRO (CSS)
st.markdown("""
    <style>
    /* Importar una fuente más deportiva (tipo roboto/inter) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@900&family=Oswald:wght@700&display=swap');

    /* Fondo con Degradado de Azules */
    .stApp {
        background: linear-gradient(180deg, #001f3f 0%, #000814 100%);
        color: white;
    }

    /* Títulos con Fuente Deportiva */
    h1, h2, h3 {
        font-family: 'Oswald', sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #ffffff;
    }

    /* Cuadros con Bordes Sólidos (Sin Neón) */
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 2px solid #4f8bf9 !important;
        border-radius: 5px !important;
        padding: 15px !important;
    }

    /* Fuente para las Métricas */
    div[data-testid="stMetricValue"] > div {
        font-family: 'Oswald', sans-serif !important;
        font-size: 2.5rem !important;
    }

    /* Efecto Brillo para el 10 (Sobrio) */
    .nota-maxima {
        font-family: 'Oswald', sans-serif !important;
        font-size: 80px !important;
        color: #ffffff;
        text-align: center;
        border-bottom: 5px solid #4f8bf9;
        display: inline-block;
        padding: 0 20px;
        margin-top: 20px;
    }

    /* Quitar bordes rojos/amarillos de alertas por defecto para uniformidad */
    .stAlert {
        border-radius: 5px !important;
        background-color: rgba(0, 0, 0, 0.3) !important;
        border: 1px solid #4f8bf9 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. INTERFAZ
st.title("⚽ LOXT: Performance Analyzer")
st.markdown("---")

# Panel Lateral
st.sidebar.header("Data Entry")
modo = st.sidebar.radio("Periodo:", ["Mensual", "Temporada"])

pj = st.sidebar.number_input("Partidos Jugados (PJ)", min_value=0, value=0, step=1)
goles = st.sidebar.number_input("Goles", min_value=0, value=0, step=1)
asist = st.sidebar.number_input("Asistencias", min_value=0, value=0, step=1)

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

# 5. VISUALIZACIÓN DE RESULTADOS
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("G/A RATE", round(ga_rate, 2))
with col2:
    st.metric("TPP BASE", round(min(tpp, 10.0), 1))
with col3:
    st.metric(f"BONO {modo[:1]}", round(bono, 2))

st.markdown("<br>", unsafe_allow_html=True)
st.write(f"SISTEMA DE CALIFICACIÓN: {tipo_bono}")

# Mostrar Nota Final con el nuevo estilo
st.markdown("<center>", unsafe_allow_html=True)
if nota_final == 10.0:
    st.markdown(f'<div class="nota-maxima">10.0</div>', unsafe_allow_html=True)
    st.info("RENDIMIENTO PERFECTO: LÍMITE DE ESCALA ALCANZADO.")
elif nota_final == 0 and pj > 0:
    st.error(f"VALORACIÓN: {round(nota_final, 1)} | REQUIERE PRODUCCIÓN DE G/A")
else:
    st.markdown(f'<div class="nota-maxima">{round(nota_final, 1)}</div>', unsafe_allow_html=True)
st.markdown("</center>", unsafe_allow_html=True)

# Mensajes de rendimiento cortos y directos
if nota_final >= 9.0:
    st.write("📈 **ESTADO:** ÉLITE")
elif nota_final >= 7.0:
    st.write("📈 **ESTADO:** SOBRESALIENTE")
elif nota_final >= 5.0:
    st.write("📈 **ESTADO:** COMPETITIVO")
elif pj > 0:
    st.write("📉 **ESTADO:** INSUFICIENTE")
