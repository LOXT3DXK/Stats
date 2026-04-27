import streamlit as st

# 1. CONFIGURACIÓN DE PÁGINA (Imprescindible para el diseño)
st.set_page_config(
    page_title="LOXT Stats Analyzer", 
    page_icon="⚽",
    layout="centered"
)

# 2. EL MOTOR DE DISEÑO (CSS Personalizado - Neón y Fondo)
st.markdown("""
    <style>
    /* Fondo Dinámico con Líneas de Gradiente (Cyberpunk/EDM vibe) */
    .stApp {
        background-color: #0d0d12;
        background-image: 
            linear-gradient(110deg, #0d0d12 40%, rgba(79, 139, 249, 0.05) 41%, #0d0d12 45%),
            linear-gradient(-110deg, #0d0d12 60%, rgba(255, 0, 255, 0.03) 61%, #0d0d12 65%);
        background-size: 100px 100px;
    }

    /* Títulos principales Neón */
    h1, h2, h3 {
        color: #4f8bf9;
        text-shadow: 
            0 0 5px #4f8bf9,
            0 0 10px #4f8bf9,
            0 0 20px #0000ff;
    }

    /* Cuadros de Métricas con Borde Neón Azul */
    .stMetric {
        background-color: rgba(30, 33, 48, 0.8) !important;
        border: 2px solid #4f8bf9 !important;
        box-shadow: 
            0 0 5px #4f8bf9,
            0 0 15px rgba(0, 0, 255, 0.3) inset;
        border-radius: 15px !important;
        padding: 20px !important;
        transition: transform 0.3s ease;
    }
    
    .stMetric:hover {
        transform: scale(1.03); /* Efecto hover */
    }

    /* Estilo para el Efecto de Brillo de la Nota 10 */
    @keyframes glow {
        from {
            text-shadow: 
                0 0 10px #fff, 
                0 0 20px #fff, 
                0 0 30px #f0f, 
                0 0 40px #f0f;
        }
        to {
            text-shadow: 
                0 0 20px #fff, 
                0 0 30px #ff00de, 
                0 0 40px #ff00de, 
                0 0 50px #ff00de, 
                0 0 60px #ff00de;
        }
    }

    .super-nota-10 {
        font-size: 72px !important;
        font-weight: bold !important;
        color: #fff !important;
        text-align: center;
        animation: glow 1.5s ease-in-out infinite alternate;
        padding: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. INTERFAZ DE USUARIO
st.title("⚽ LOXT Stats Analyzer")
st.write("Calculadora de Calificación de Alto Rendimiento con 'Ley de Producción'")
st.markdown("---")

# Panel Lateral de Datos
st.sidebar.header("Panel de Control")
modo = st.sidebar.radio("Selecciona el Periodo:", ["Mensual", "Temporada"])

pj = st.sidebar.number_input("Partidos Jugados (PJ)", min_value=0, value=0, step=1)
goles = st.sidebar.number_input("Goles", min_value=0, value=0, step=1)
asist = st.sidebar.number_input("Asistencias", min_value=0, value=0, step=1)

# 4. LÓGICA DE CÁLCULO (Tu 'Ley de Hierro' protegida)
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
    ga_rate = tpp = bono = nota_final = 0.0
    tipo_bono = "BR M" if modo == "Mensual" else "BR T"
    comentario_extra = "🚫 Sin producción de G/A: Nota 0" if pj > 0 else ""

# 5. RESULTADOS CON EFECTOS ESPECIALES
col1, col2, col3 = st.columns(3)

# Las cajas stMetric ya traen el borde neón del CSS
col1.metric("G/A Rate", round(ga_rate, 2))
col2.metric("Nota TPP", round(min(tpp, 10.0), 1))
col3.metric(f"Bono {modo}", round(bono, 2))

st.markdown("---")
st.subheader(f"Resultado Final: {tipo_bono}")

# EFECTO DE LA NOTA FINAL
if nota_final == 10.0:
    # --- EFECTO NOTA 10 (Glow + Estrellas) ---
    st.markdown('<p class="super-nota-10">10.0</p>', unsafe_allow_html=True)
    st.balloons() # Globos (que parecen burbujas de celebración)
    st.success("🏆 ¡NIVEL LEYENDA ALCANZADO! Tu rendimiento es impecable.")
    st.info("⭐ ⭐ ⭐ ⭐ ⭐ ⭐ ⭐ ⭐ ⭐ ⭐ ⭐") # Estrellas visuales
elif nota_final == 0 and pj > 0:
    st.error(f"💀 Nota: {round(nota_final, 1)} - {comentario_extra}")
else:
    st.warning(f"🏆 Tu Calificación es: **{round(nota_final, 1)}**")

# Feedback adicional según rendimiento
if nota_final >= 9.0 and nota_final < 10.0:
    st.success("🔥 ¡Nivel Élite! Estás muy cerca de la perfección.")
elif nota_final >= 7.0 and nota_final < 9.0:
    st.info("📈 Rendimiento Sobresaliente. Sigue así.")
