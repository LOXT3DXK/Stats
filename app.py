import streamlit as st

# Configuración de la página
st.set_page_config(page_title="LOXT Stats Analyzer", page_icon="⚽")

st.title("⚽ LOXT: Sistema de Calificación")
st.markdown("---")

# 1. ENTRADA DE DATOS
st.sidebar.header("Panel de Control")
modo = st.sidebar.radio("Selecciona el Periodo:", ["Mensual", "Temporada"])

pj = st.sidebar.number_input("Partidos Jugados (PJ)", min_value=1, value=1, step=1)
goles = st.sidebar.number_input("Goles", min_value=0, value=0, step=1)
asist = st.sidebar.number_input("Asistencias", min_value=0, value=0, step=1)

# 2. LÓGICA DE CÁLCULO (Según tu cuaderno)
ga_rate = (goles + asist) / pj
tpp = min((ga_rate * 10) / 7, 10.0)

if modo == "Mensual":
    bono = min(pj / 16, 1.0)
    nota_final = tpp + bono
    tipo_bono = "BR M"
else:
    # Lógica de Temporada (A: <48, B: >48)
    if pj <= 48:
        bono = (pj * 2) / 48
    else:
        # 2.0 base + 0.1 por cada 4 PJ adicionales
        bono = 2.0 + ((pj - 48) // 4) * 0.1
    nota_final = tpp + bono
    tipo_bono = "BR T"

# 3. INTERFAZ DE RESULTADOS
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("G/A Rate", round(ga_rate, 2))
with col2:
    st.metric("Nota TPP (Base)", round(tpp, 1))
with col3:
    st.metric(f"Bono ({modo})", round(bono, 2))

st.markdown("---")
st.subheader(f"Resultado Final: {tipo_bono}")
st.title(f"⭐ {round(nota_final, 1)}")

# 4. FEEDBACK VISUAL (Opcional)
if nota_final >= 9.0:
    st.success("¡Rendimiento de Élite Mundial!")
elif nota_final >= 7.0:
    st.info("Rendimiento Sobresaliente.")
else:
    st.warning("Rendimiento en desarrollo.")