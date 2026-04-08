import streamlit as st
import json

# Configuración estética
st.set_page_config(page_title="Corrector CiUG 2026", layout="wide")

# Estilo personalizado NotebookLM
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stSelectbox label, .stButton button { font-weight: bold; }
    .reportview-container .main .block-container { padding-top: 2rem; }
    </style>
    """, unsafe_allow_html=True)

def load_data():
    with open('matematicas.json', 'r', encoding='utf-8') as f:
        return json.load(f)

data = load_data()
asignatura = "Matemáticas II"

# Sidebar organizada
st.sidebar.title("🛠️ Panel de Control")
bloques = list(data['asignaturas'][asignatura].keys())
bloque_sel = st.sidebar.selectbox("Selecciona Bloque", bloques)

ejercicios = data['asignaturas'][asignatura][bloque_sel]
titulos_ejercicios = [f"{ej['id']} - {ej['titulo']}" for ej in ejercicios]
ej_sel_index = st.sidebar.selectbox("Ejercicio", range(len(titulos_ejercicios)), format_func=lambda x: titulos_ejercicios[x])

ejercicio_actual = ejercicios[ej_sel_index]
reglas_2026 = "\n".join([f"- {r}" for r in data['reglas_2026']])

# Cuerpo principal
col1, col2 = st.columns([1, 1])

with col1:
    st.title("📄 Enunciado")
    st.markdown(f"### {ejercicio_actual['id']} - {ejercicio_actual['titulo']}")
    # Renderizado de fórmulas
    st.write(ejercicio_actual['enunciado'])
    
    st.divider()
    st.subheader("💡 Ayuda Pedagógica")
    st.info(ejercicio_actual['tip'])

with col2:
    st.title("⚖️ Rúbrica CiUG")
    with st.expander("Ver criterios de puntuación", expanded=True):
        st.write(ejercicio_actual['rubrica'])
    
    with st.expander("⚠️ Novedades Tutoría 2026"):
        st.write(reglas_2026)

st.divider()

# Generador de Prompt Elegante
st.subheader("🤖 Copiar Prompt para Corrección")
prompt_final = f"""Actúa como un corrector oficial de la CiUG (Galicia) para la ABAU 2026.
Corrige el ejercicio de la imagen basándote en:

EJERCICIO:
{ejercicio_actual['enunciado']}

RÚBRICA DETALLADA:
{ejercicio_actual['rubrica']}

REGLAS DE ORO 2026 (Obligatorio aplicar):
{reglas_2026}

INSTRUCCIONES DE RESPUESTA:
1. Evalúa el rigor en la notación (puntos vs vectores).
2. Estima la nota sobre el total indicado.
3. Sé directo pero motivador. Indica fallos de cálculo paso a paso.
4. Si falta el esbozo gráfico (en análisis) o justificación de teoremas, penaliza según la rúbrica."""

st.code(prompt_final, language="text")
st.caption("Copia este texto y pégalo en tu IA junto a la foto de tu libreta.")