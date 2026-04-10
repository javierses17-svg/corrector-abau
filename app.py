import streamlit as st
import json

st.set_page_config(page_title="Corrector CiUG 2026", layout="wide")

# Selector de Asignatura en el Sidebar
st.sidebar.title("🎒 Mi Mochila ABAU")
asignatura_file = st.sidebar.selectbox("¿Qué asignatura vas a estudiar?", ["matematicas.json", "Lengua.json"])

# Función de carga dinámica
def load_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

try:
    data = load_data(asignatura_file)
    # Extraer el nombre de la asignatura del JSON
    asignatura_nombre = list(data['asignaturas'].keys())[0]
    
    st.sidebar.divider()
    
    # Selector de Bloque y Ejercicio
    bloques = list(data['asignaturas'][asignatura_nombre].keys())
    bloque_sel = st.sidebar.selectbox("Selecciona Bloque", bloques)

    ejercicios = data['asignaturas'][asignatura_nombre][bloque_sel]
    titulos_ejercicios = [f"{ej['id']} - {ej['titulo']}" for ej in ejercicios]
    ej_sel_index = st.sidebar.selectbox("Ejercicio", range(len(titulos_ejercicios)), format_func=lambda x: titulos_ejercicios[x])

    ejercicio_actual = ejercicios[ej_sel_index]
    normativa = "\n".join([f"- {r}" for r in data.get('normativa_2026', data.get('reglas_2026', []))])

    # Interfaz Principal
    col1, col2 = st.columns([1, 1])

    with col1:
        st.title("📄 Enunciado")
        st.markdown(f"### {ejercicio_actual['id']} - {ejercicio_actual['titulo']}")
        st.write(ejercicio_actual['enunciado'])
        st.divider()
        st.subheader("💡 Ayuda Pedagógica")
        st.info(ejercicio_actual['tip'])

    with col2:
        st.title("⚖️ Rúbrica CiUG")
        with st.expander("Ver criterios de puntuación", expanded=True):
            st.write(ejercicio_actual['rubrica'])
        with st.expander("⚠️ Normativa Aplicada"):
            st.write(normativa)

    st.divider()
    st.subheader("🤖 Copiar Prompt para Corrección")
    prompt_final = f"""Actúa como un corrector oficial de la CiUG (Galicia) para la ABAU 2026.
Corrige el ejercicio de la imagen basándote en:

ASIGNATURA: {asignatura_nombre}
EJERCICIO: {ejercicio_actual['enunciado']}

RÚBRICA DETALLADA:
{ejercicio_actual['rubrica']}

NORMATIVA GENERAL:
{normativa}

INSTRUCCIONES:
1. Analiza el contenido y la forma.
2. Evalúa la ortografía con rigor (-0.15 tildes, -0.25 faltas).
3. Estima la nota.
4. Indica mejoras en redacción o desarrollo."""

    st.code(prompt_final, language="text")

except FileNotFoundError:
    st.error(f"No se encuentra el archivo {asignatura_file} en GitHub. Asegúrate de haberlo subido.")
