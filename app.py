import streamlit as st

# Configuración de la página
st.set_page_config(page_title="LOXT Stats Analyzer", page_icon="⚽")

st.title("⚽ LOXT: Sistema de Calificación")
st.markdown("---")

# 1. ENTRADA DE DATOS
st.sidebar.header("Panel de Control")
modo = st.sidebar.radio("Selecciona el Periodo:", ["Mensual", "Temporada"])

# Permitimos que PJ empiece en 0 para que la app pueda marcar 0 total al inicio
pj = st.sidebar.number_input("Partidos Jugados (PJ)", min_value=0, value=0, step=1)
goles = st.sidebar.number_input("Goles", min_value=0, value=0, step=1)
asist = st.sidebar.number_input("Asistencias", min_value=0, value=0, step=1)

# 2. LÓGICA DE CÁLCULO
# Evitamos división por cero
if pj > 0:
    ga_rate = (goles + asist) / pj
    tpp = (ga_rate * 10) / 7
    
    if modo == "Mensual":
        bono = pj / 16
        tipo_bono = "BR M"
    else:
        if pj <= 48:
            bono = (pj * 2) / 48
        else:
            bono = 2.0 + ((pj - 48) // 4) * 0.1
        tipo_bono = "BR T"
    
    # CÁLCULO FINAL CON TOPE ESTRICTO DE 10
    nota_final = tpp + bono
    if nota_final > 10.0:
        nota_final = 10.0
else:
    ga_rate = 0.0
    tpp = 0.0
    bono = 0.0
    nota_final = 0.0
    tipo_bono = "BR M" if modo == "Mensual" else "BR T"

# 3. INTERFAZ DE RESULTADOS
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("G/A Rate", round(ga_rate, 2))
with col2:
    st.metric("Nota TPP (Base)", round(min(tpp, 10.0), 1))
with col3:
    st.metric(f"Bono ({modo})", round(bono, 2))

st.markdown("---")
st.subheader(f"Resultado Final: {tipo_bono}")

# Mostrar nota con formato limpio
st.title(f"⭐ {round(nota_final, 1)}")

if nota_final >= 9.0:
    st.success("¡Rendimiento de Élite Mundial!")
elif nota_final >= 7.0:
    st.info("Rendimiento Sobresaliente.")
elif pj > 0:
    st.warning("Rendimiento en desarrollo.")
else:
    st.write("Ingresa datos para calcular tu nota.")
