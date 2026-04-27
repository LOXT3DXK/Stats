import streamlit as st

# 1. CONFIGURACIÓN
st.set_page_config(page_title="LOXT Stats Calculator", page_icon="⚽", layout="centered")

# 2. INICIALIZACIÓN DE ESTADO (Para el botón de Reset)
if 'reset' not in st.session_state:
    st.session_state.reset = False

def reset_values():
    st.session_state.pj = 0
    st.session_state.goles = 0
    st.session_state.asist = 0
    st.session_state.exigencia = 4.0

# 3. SIDEBAR
with st.sidebar:
    st.markdown("<h3 style='font-size:1.2rem;'>DATA ENTRY</h3>", unsafe_allow_html=True)
    modo_oscuro = st.toggle("Modo Noche", value=True)
    st.markdown("---")
    
    exigencia = st.slider("Exigencia (Dificultad)", 1.0, 10.0, 4.0, step=0.5, key="exigencia")
    periodo = st.radio("Cálculo para:", ["Mensual", "Temporada (Anual)"])
    
    st.markdown("---")
    pj = st.number_input("Partidos Jugados (PJ)", min_value=0, step=1, key="pj")
    goles = st.number_input("Goles", min_value=0, step=1, key="goles")
    asist = st.number_input("Asistencias", min_value=0, step=1, key="asist")
    
    st.markdown("---")
    if st.button("♻️ Limpiar Todo", on_click=reset_values, use_container_width=True):
        st.rerun()

# 4. ESTILOS CSS
if modo_oscuro:
    bg, side, txt, card, met = ("linear-gradient(135deg, #001a33 0%, #004d40 100%)", "#001a33", "#ffffff", "rgba(0,0,0,0.4)", "rgba(255,255,255,0.08)")
else:
    bg, side, txt, card, met = ("linear-gradient(135deg, #fff9c4 0%, #ffecb3 50%, #ffccbc 100%)", "#fff9c4", "#2c3e50", "rgba(255,255,255,0.6)", "rgba(0,0,0,0.05)")

st.markdown(f"""
    <style>
    .stApp {{ background: {bg}; background-attachment: fixed; }}
    section[data-testid="stSidebar"] {{ background-color: {side} !important; }}
    .stApp, p, span, label, h1, h3, div[data-testid="stMetricLabel"] > div {{ color: {txt} !important; }}
    div[data-testid="stMetric"] {{ background-color: {met} !important; border-radius: 12px; text-align: center; padding: 15px; border: 1px solid rgba(0,0,0,0.05); }}
    div[data-testid="stMetricValue"] > div {{ color: {txt} !important; font-weight: 800; font-size: 1.8rem; display: flex; justify-content: center; }}
    .nota-card {{ background: {card}; border-radius: 15px; padding: 20px; text-align: center; margin-top: 15px; border: 1px solid rgba(0,0,0,0.1); backdrop-filter: blur(5px); }}
    .nota-valor {{ font-size: 4rem !important; font-weight: 900; margin: 0; line-height: 1; }}
    .proximo-nivel {{ font-size: 0.85rem; font-style: italic; opacity: 0.8; margin-top: 10px; }}
    </style>
    """, unsafe_allow_html=True)

# 5. LÓGICA DE CÁLCULO
g_a_total = goles + asist
if pj > 0:
    ga_rate = g_a_total / pj
    meta_pro = exigencia / 4 
    tpp_base = (ga_rate * 7) / meta_pro
    tpp_final = min(tpp_base, 10.0)
    bonus = min(pj / 16, 1.0) if periodo == "Mensual" else ((pj * 2) / 48 if pj <= 48 else 2.0 + ((pj - 48) // 4) * 0.1)
    nota_final = round(min(tpp_final + bonus, 10.0), 1)
else:
    ga_rate = tpp_base = bonus = nota_final = 0.0

# 6. STATUS Y FEEDBACK DE NIVEL
niveles = [
    (10.0, "LEYENDA", "#9d4edd"),
    (8.0, "TOP", "#ffffff" if modo_oscuro else "#2c3e50"),
    (6.0, "IDEAL", "#4db6ac"),
    (5.0, "APROBADO", "#81c784"),
    (1.0, "REPROBADO", "#e57373"),
    (0.0, "RENDIMIENTO NULO", "#ff5252")
]

status, color, next_info = "SIN DATOS", "#78909c", ""
if pj > 0:
    for i, (limite, nombre, col) in enumerate(niveles):
        if nota_final >= limite:
            status, color = nombre, col
            if i > 0: # Si no es LEYENDA, calcular cuánto falta para el nivel superior
                falta = round(niveles[i-1][0] - nota_final, 1)
                next_info = f"Estás a {falta} pts del nivel {niveles[i-1][1]}"
            break

# 7. INTERFAZ PRINCIPAL
st.markdown("<h1 style='text-align:center; letter-spacing: 2px;'>LOXT STATS CALCULATOR</h1>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
c1.metric("G/A RATE", f"{ga_rate:.2f}")
c2.metric("TPP (BASE)", f"{tpp_base:.2f}")
c3.metric("BONUS", f"{bonus:.2f}")

st.markdown(f"""
    <div class='nota-card'>
        <p style='font-weight:bold; margin:0; font-size:0.8rem; opacity: 0.7;'>VALORACIÓN FINAL</p>
        <p class='nota-valor' style='color:{color};'>{nota_final}</p>
        <div style="width: 100%; background-color: rgba(0,0,0,0.1); border-radius: 20px; margin: 15px 0;">
            <div style="width: {nota_final*10}%; background-color: {color}; height: 14px; border-radius: 20px; transition: 0.8s;"></div>
        </div>
        <p style='font-weight:900; color:{color}; font-size:1.4rem; letter-spacing:3px; margin:0;'>{status}</p>
        <p class='proximo-nivel'>{next_info}</p>
    </div>
    """, unsafe_allow_html=True)

# 8. FUNCIÓN DE COPIADO (Formateado de texto)
if pj > 0:
    resumen = f"⚽ LOXT Stats: {pj} PJ | {nota_final} Valoración | Status: {status}"
    st.text_input("Copia tu resultado:", value=resumen, help="Haz clic para seleccionar y copiar")
