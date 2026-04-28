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

# 3. SIDEBAR
with st.sidebar:
    st.markdown("<h3 style='letter-spacing:1px;'>CONFIGURACIÓN</h3>", unsafe_allow_html=True)
    modo_oscuro = st.toggle("Modo Noche", value=True)
    st.markdown("---")
    exigencia = st.slider("Exigencia (Base 4.0)", 1.0, 10.0, key="exigencia", step=0.5, 
                          help="Ajusta la dificultad. Un valor mayor a 4.0 reducirá tu TPP base.")
    periodo = st.radio("Cálculo para:", ["Mensual", "Temporada (Anual)"])
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
    tpp_bruto = (ga_rate * 10) / 7
    tpp_final = round(tpp_bruto * (4 / exigencia), 1)
    
    if periodo == "Mensual":
        if pj == 1: bonus = -0.50
        elif pj == 2: bonus = -0.25
        elif pj == 3: bonus = -0.10
        elif pj == 4: bonus = 0.0
        else: bonus = round((pj / 16), 2)
    else:
        val_bonus = ((pj * 2) / 48 if pj <= 48 else 2.0 + ((pj - 48) // 4) * 0.1)
        bonus = round(val_bonus, 2)
    
    nota_final = round(tpp_final + bonus, 1)
    nota_final = max(0.0, min(nota_final, 10.0))
else:
    ga_rate = tpp_final = bonus = nota_final = 0.0

# 5. RANGOS Y COLORES
niveles = [(10.0, "LEYENDA", "#9d4edd"), (8.0, "TOP", "#ffffff" if modo_oscuro else "#005a9c"), (6.0, "IDEAL", "#4db6ac"), (5.0, "APROBADO", "#81c784"), (1.0, "REPROBADO", "#e57373"), (0.0, "RENDIMIENTO NULO", "#ff5252")]
status, color, next_info = "SIN DATOS", "#78909c", ""
if pj > 0:
    for i, (lim, nom, col) in enumerate(niveles):
        if nota_final >= lim:
            status, color = nom, col
            if i > 0:
                falta = round(niveles[i-1][0] - nota_final, 1)
                next_info = f"Estás a {falta} pts del nivel {niveles[i-1][1]}"
            break

# 6. ESTILOS CSS (MODO CLARO AZUL PASTEL)
if modo_oscuro:
    bg, side, txt, card = ("linear-gradient(135deg, #001a33 0%, #004d40 100%)", "#001a33", "#ffffff", "rgba(0,0,0,0.4)")
else:
    # Paleta Azul Cielo / Pastel
    bg, side, txt, card = ("linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%)", "#e3f2fd", "#01579b", "rgba(255,255,255,0.6)")

st.markdown(f"""
    <style>
    .stApp {{ background: {bg}; background-attachment: fixed; transition: background 0.5s ease; }}
    section[data-testid='stSidebar'] {{ background-color: {side} !important; border-right: 1px solid rgba(0,0,0,0.1); }}
    .stApp, p, span, label, h1, h3, div[data-testid='stMetricLabel'] > div {{ color: {txt} !important; }}
    
    .nota-card {{ 
        background: {card}; 
        border-radius: 20px; 
        padding: 30px; 
        text-align: center; 
        margin-top: 20px; 
        border: 2px solid {color}22; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        backdrop-filter: blur(10px);
    }}
    .nota-valor {{ font-size: 5rem !important; font-weight: 900; margin: 0; line-height: 1; color: {color} !important; }}
    
    .progress-container {{ background: rgba(0,0,0,0.05); border-radius: 20px; margin: 20px 0; height: 16px; overflow: hidden; }}
    .progress-bar {{ background: {color}; height: 100%; border-radius: 20px; transition: width 0.8s ease-in-out; }}
    </style>
    """, unsafe_allow_html=True)

# 7. INTERFAZ PRINCIPAL
st.markdown("<h1 style='text-align:center; letter-spacing: 3px; font-weight:900;'>LOXT CALCULATOR</h1>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1: st.metric("G/A RATE", f"{ga_rate:.2f}")
with c2: st.metric("TPP BASE", f"{tpp_final}")
with c3: st.metric("BONUS", f"{bonus}")

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
