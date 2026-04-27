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

# 2. LÓGICA DE CÁLCULO
ga_rate = (goles + asist) / pj
# La nota base TPP sigue siendo sobre 7,0
tpp = (ga_rate * 10) / 7

if modo == "Mensual":
    bono = pj / 16
    tipo_bono = "BR M"
else:
    # Lógica de Temporada
    if pj <= 48:
        bono = (pj * 2) / 48
    else:
        bono = 2.0 + ((pj - 48) // 4) * 0.1
    tipo_bono = "BR T"

# CÁLCULO FINAL CON TOPE
# Sumamos TPP + Bono y limitamos el resultado entre 0 y 10
nota_final = min(max(tpp + bono, 0.0), 10.0)

# 3. INTERFAZ DE RESULTADOS
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("G/A Rate", round(ga_rate, 2))
with col2:
    # Mostramos la nota TPP también topada a 10 para que sea coherente
    st.metric("Nota TPP (Base)", round(min(tpp, 10.0), 1))
with col3:
    st.metric(f"Bono ({modo})", round(bono, 2))

st.markdown("---")
st.subheader(f"Resultado Final: {tipo_bono}")

# Estilo visual para la nota
if nota_final >= 9.0:
    st.title(f"🔥 {round(nota_final, 1)}")
    st.success("¡Nivel Leyenda!")
elif nota_final >= 7.0:
    st.title(f"⭐ {round(nota_final, 1)}")
    st.info("Rendimiento Sobresaliente.")
else:
    st.title(f"📈 {round(nota_final, 1)}")
    st.warning("Rendimiento en desarrollo.")
