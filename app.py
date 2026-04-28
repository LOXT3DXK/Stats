import streamlit as st

# 1. CONFIGURACIÓN
st.set_page_config(page_title="LOXT Stats Calculator", page_icon="⚽", layout="centered")

# 2. INICIALIZACIÓN
if 'pj' not in st.session_state: st.session_state.pj = 0
if 'goles' not in st.session_state: st.session_state.goles = 0
if 'asist' not in st.session_state: st.session_state.asist = 0
if 'exigencia' not in st.session_state: st.session_state.exigencia = 4.0

def reset_values():
    st.session_state.pj, st.session_state.goles, st.session_state.asist, st.session_state.exigencia = 0, 0, 0, 4.0

# 3. SIDEBAR (Con Tooltips de ayuda)
with st.sidebar:
    st.markdown("<h3 style='letter-spacing:1px;'>CONFIGURACIÓN</h3>", unsafe_allow_html=True)
    modo_oscuro = st.toggle("Modo Noche", value=True)
    st.markdown("---")
    exigencia = st.slider("Exigencia (Base 4.0)", 1.0, 10.0, key="exigencia", step=0.5, 
                          help="Ajusta la dificultad. Un valor mayor a 4.0 reducirá tu TPP base.")
    periodo = st.radio("Cálculo para:", ["Mensual", "Temporada (Anual)"], 
                       help="Mensual incluye penalización por inactividad. Temporada es puramente acumulativo.")
    st.markdown("---")
    pj = st.number_input("Partidos Jugados (PJ)", min_value=0, step=1, key="pj")
    goles = st.number_input("Goles", min_value=0, step=1, key="goles")
    asist = st.number_input("Asistencias", min_value=0, step=1, key="asist")
    st.markdown("---")
    if st.button("♻️ Limpiar Todo", on_click=reset_values, use_container_width=True): st.rerun()

# 4. LÓGICA DE CÁLCULO
g_a_total = goles + asist
if pj > 0:
    ga_rate = g_a_total / pj
    
    # TPP con Auditoría
    tpp_bruto = (ga_rate * 10) / 7
    ajuste_exigencia = 4 / exigencia 
    tpp_final = round(tpp_bruto * ajuste_exigencia, 1)
    
    # Explicación TPP para el Tooltip
    tpp_help = f"Fórmula: ({ga_rate:.2f} Rate * 10) / 7 = {tpp_bruto:.2f}. Ajustado por exigencia: {tpp_final}"
    
    # Bonus con Auditoría
    if periodo == "Mensual":
        if pj == 1: bonus, b_help = -0.50, "Penalización: Solo 1 PJ en el mes."
        elif pj == 2: bonus, b_help = -0.25, "Penalización: Solo 2 PJ en el mes."
        elif pj == 3: bonus, b_help = -0.10, "Penalización: Solo 3 PJ en el mes."
        elif pj == 4: bonus, b_help = 0.0, "Punto de equilibrio: 4 PJ no suma ni resta."
        else: 
            bonus = round((pj / 16), 2)
            b_help = f"Bonificación por actividad: {pj}/16 = {bonus}"
    else:
        val_bonus = ((pj * 2) / 48 if pj <= 48 else 2.0 + ((pj - 48) // 4) * 0.1)
        bonus = round(val_bonus, 2)
        b_help = f"Bono de temporada acumulado: {bonus}"
    
    nota_final = round(tpp_final + bonus, 1)
    nota_final = max(0.0, min(nota_final, 10.0))
else:
    ga_rate = tpp_final = bonus = nota_final = 0.0
    tpp_help = b_help = "Ingresa datos para ver el cálculo."

# 5. RANGOS
niveles = [(10.0, "LEYENDA", "#9d4edd"), (8.0, "TOP", "#ffffff" if modo_oscuro else "#2c3e50"), (6.0, "IDEAL", "#4db6ac"), (5.0, "APROBADO", "#81c784"), (1.0, "REPROBADO", "#e57373"), (0.0, "RENDIMIENTO NULO", "#ff5252")]
status, color, next_info = "SIN DATOS", "#78909c", ""
if pj > 0:
    for i, (lim, nom, col) in enumerate(niveles):
        if nota_final >= lim:
            status, color = nom, col
            if i > 0:
                falta = round(niveles[i-1][0] - nota_final, 1)
                next_info = f"Estás a {falta} pts del nivel {niveles[i-1][1]}"
            break

# 6. ESTILOS
if modo_oscuro:
    bg, side, txt, card = ("linear-gradient(135deg, #001a33 0%, #004d40 100%)", "#001a33", "#ffffff", "rgba(0,0,0,0.5)")
else:
    bg, side, txt, card = ("linear-gradient(135deg, #fff9c4 0%, #ffecb3 50%, #ffccbc 100%)", "#fff9c4", "#2c3e50", "rgba(255,255,255,0.7)")

st.markdown(f"""
    <style>
    .stApp {{ background: {bg}; background-attachment: fixed; transition: background 0.8s ease; }}
    section[data-testid='stSidebar'] {{ background-color: {side} !important; }}
    .stApp, p, span, label, h1, h3, div[data-testid='stMetricLabel'] > div {{ color: {txt} !important; }}
    .nota-card {{ 
        background: {card}; border-radius: 20px; padding: 30px; text-align: center; margin-top: 20px; 
        border: 1px solid {color}44; box-shadow: 0 10px 30px -10px {color}66; backdrop-filter: blur(10px);
    }}
    .nota-valor {{ font-size: 5rem !important; font-weight: 900; margin: 0; color: {color} !important; text-shadow: 0 0 15px {color}44; }}
    .progress-container {{ background: rgba(0,0,0,0.1); border-radius: 20px; margin: 20px 0; height: 16px; overflow: hidden; }}
    .progress-bar {{ background: {color}; height: 100%; border-radius: 20px; transition: width 0.8s ease-in-out; }}
    </style>
    """, unsafe_allow_html=True)

# 7. INTERFAZ PRINCIPAL
st.markdown("<h1 style='text-align:center; letter-spacing: 3px; font-weight:900;'>LOXT CALCULATOR</h1>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1: st.metric("G/A RATE", f"{ga_rate:.2f}", help="Promedio de contribuciones (Goles + Asistencias) por partido.")
with c2: st.metric("TPP BASE", f"{tpp_final}", help=tpp_help)
with c3: st.metric("BONUS", f"{bonus}", help=b_help)

st.markdown(f"""
    <div class='nota-card'>
        <p style='font-weight:bold; margin:0; font-size:0.9rem; opacity: 0.6; letter-spacing: 2px;'>VALORACIÓN FINAL</p>
        <p class='nota-valor'>{nota_final}</p>
        <div class='progress-container'>
            <div class='progress-bar' style='width: {nota_final*10}%'></div>
        </div>
        <p style='font-weight:900; color:{color}; font-size:1.6rem; letter-spacing:5px; margin:0;'>{status}</p>
        <p style='font-size: 0.85rem; font-style: italic; opacity: 0.7; margin-top: 10px;'>{next_info}</p>
    </div>
    """, unsafe_allow_html=True)

# 8. COPIADO
if pj > 0:
    st.markdown("<br><p style='font-size:0.8rem; font-weight:bold; opacity:0.7; letter-spacing:1px;'>COPIA TU REPORTE:</p>", unsafe_allow_html=True)
    card_text = f"⚽ REGISTRO LOXT [{periodo.upper()}]\n---------------------------\nSTATS: {pj} PJ | {goles} G | {asist} A\nRITMO: {ga_rate:.2f} G/A por partido\nBONUS: {bonus}\n---------------------------\nNOTA FINAL: {nota_final}\nSTATUS: {status}"
    st.code(card_text, language=None)
