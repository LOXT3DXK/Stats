import streamlit as st

# Configuración de la página
st.set_page_config(page_title="LOXT Stats Analyzer", page_icon="⚽")

st.title("⚽ LOXT: Sistema de Calificación")
st.markdown("---")

# 1. ENTRADA DE DATOS
st.sidebar.header("Panel de Control")
modo = st.sidebar.radio("Selecciona el Periodo:", ["Mensual", "Temporada"])

pj = st.sidebar.number_input("Partidos Jugados (PJ)", min_value=0, value=0, step=1)
goles = st.sidebar.number_input("Goles", min_value=0, value=0, step=1)
asist = st.sidebar.number_input("Asistencias", min_value=0, value=0, step=1)

# 2. LÓGICA DE CÁLCULO
g_a_total = goles + asist

# REGLA DE ORO: Si no hay G/A, la nota es 0 automáticamente
if pj > 0 and g_a_total > 0:
    ga_rate = g_a_total / pj
    tpp = (ga_rate * 10) / 7
    
    # Cálculo del Bono con límites estrictos
    if modo == "Mensual":
        # Bono mensual máximo de 1.0
        bono = min(pj / 16, 1.0)
        tipo_bono = "BR M"
    else:
        # Lógica de Temporada / Anual
        if pj <= 48:
            # Bono base hasta 2.0
            bono = (pj * 2) / 48
        else:
            # 2.0 base + 0.1 por cada 4 partidos extra
            extra = ((pj - 48) // 4) * 0.1
            bono = 2.0 + extra
        tipo_bono = "BR T"
    
    # Nota final topada en 10.0
    nota_final = min(tpp + bono, 10.0)
    comentario_extra = ""

else:
    # Si PJ es 0 o G+A es 0, todo es cero absoluto
    ga_rate = 0.0
    tpp = 0.0
    bono = 0.0
    nota_final = 0.0
    tipo_bono = "BR M" if modo == "Mensual" else "BR T"
    comentario_extra = "🚫 Sin producción de G/A: Nota 0" if pj > 0 else ""

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

# Mostrar nota con estilo profesional
if nota_final == 0 and pj > 0:
    st.title(f"💀 {round(nota_final, 1)}")
    st.error(comentario_extra)
else:
    st.title(f"⭐ {round(nota_final, 1)}")

# Feedback visual de rendimiento
if nota_final >= 9.0:
    st.success("¡Rendimiento de Élite Mundial!")
elif nota_final >= 7.0:
    st.info("Rendimiento Sobresaliente.")
elif nota_final >= 5.0:
    st.info("Rendimiento Aceptable.")
elif pj > 0:
    st.error("Rendimiento insuficiente (Reprobado).")
