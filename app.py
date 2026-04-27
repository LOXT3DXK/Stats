import streamlit as st

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="LOXT Stats Pro", 
    page_icon="⚽",
    layout="centered"
)

# 2. CSS: Estilo Deep Blue Futurista y Compacto
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');

    /* Fondo Degradado Azul Oscuro */
    .stApp {
        background: linear-gradient(180deg, #001a33 0%, #000814 100%) !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Barra Lateral unificada */
    [data-testid="stSidebar"] {
        background-color: rgba(0, 26, 51, 0.95) !important;
        border-right: 1px solid #003366;
    }

    /* Títulos */
    h1 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 900 !important;
        font-size: 1.6rem !important;
        color: #ffffff !important;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 1rem !important;
    }

    /* Cuadros de Métricas Futuristas */
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid #004080 !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }

    div[data-testid="stMetricValue"] > div {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
        color: #ffffff !important;
    }

    /* Contenedor de Nota Final */
    .nota-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 15px;
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        margin-top: 10px;
    }

    .nota-valor {
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        color: #ffffff !important;
        line-height: 1;
        margin: 5px 0;
    }

    /* Compactación */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 1rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR (Data Entry con Exigencia)
with st.sidebar:
    st.markdown("<h2 style='color:white; font-size:1.2rem;'>CONFIGURACIÓN</h2>", unsafe_allow_html=True)
    
    # NUEVA OPCIÓN: Nivel de Exigencia
    exigencia = st.slider("Exigencia (G/A para el 7.0):", 1.0, 10.0, 4.0, step=0.5)
    
    st.markdown("---")
    modo = st.radio("Periodo:", ["Mensual", "Temporada"])
    pj = st.number_input("Partidos (PJ)", min_value=0, step=1)
    goles = st.number_input("Goles", min_value=0, step=1)
    asist = st.number_input("Asistencias", min_value=0, step=1)

# 4. LÓGICA DE CÁLCULO DINÁMICA
g_a_total = goles + asist

if pj > 0 and g_a_total > 0:
    ga_rate = g_a_total / pj
    
    # El TPP ahora es relativo a la exigencia elegida
    # Antes: (ga_rate * 10) / 7 -> Asumía que 0.7 era el 1.0 de nota base (aprox 4.9 de 7)
    # Ahora: Ajustamos para que alcanzar la 'exigencia' promedio por partido dé un 7.0 base
    tpp = (ga_rate * 7) / (exigencia / pj if pj > 0 else 1) # Simplificado para que escale con la meta
    tpp = (ga_rate * 10) / (exigencia * 1.75 / 4) # Ajuste proporcional a tu regla original de 4 G/A
    
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

# Métricas
c1, c2, c3 = st.columns(3)
c1.metric("G/A RATE", f"{ga_rate:.2f}")
c2.metric("META G/A", f"{exigencia}")
c3.metric(f"BONO {modo[0]}", f"{bono:.2f}")

# Tarjeta de Nota Final
st.markdown("<div class='nota-card'>", unsafe_allow_html=True)
st.markdown(f"<p style='color:#81d4fa; font-weight:bold; margin:0; letter-spacing:2px;'>VALORACIÓN FINAL</p>", unsafe_allow_html=True)
st.markdown(f'<p class="nota-valor">{nota_final:.1f}</p>', unsafe_allow_html=True)

# Barra de Progreso
st.progress(int(nota_final * 10))

# Status
if pj > 0:
    if nota_final >= 9.0: status = "NIVEL LEYENDA"
    elif nota_final >= exigencia + 2: status = "ÉLITE PRO"
    elif nota_final >= 5.0: status = "COMPETITIVO"
    else: status = "BAJO RENDIMIENTO"
    st.markdown(f"<p style='margin-top:10px; font-weight:bold; letter-spacing:1px;'>SITUACIÓN: {status}</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
