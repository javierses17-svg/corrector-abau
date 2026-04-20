import streamlit as st
import json

st.set_page_config(page_title="Asistente ABAU 2026", layout="wide")

# Estilos para limpiar la interfaz y centrar la atención en el enunciado
st.markdown("""
    <style>
    .stExpander { border: 2px solid #e6e9ef; border-radius: 10px; background-color: #ffffff; }
    .stMarkdown h3 { color: #2e4053; }
    </style>
    """, unsafe_allow_html=True)

# Función de carga
def load_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

# Sidebar: Selección de materia
st.sidebar.title("🎒 Mi Mochila ABAU")
asignatura_file = st.sidebar.selectbox("¿Qué vas a estudiar hoy?", ["Matematicas.json", "Lengua.json", "Filosofia.json", "Galego.json", "Biologia.json", "Quimica.json", "ingles.json"])

try:
    data = load_data(asignatura_file)
    asignatura_nombre = list(data['asignaturas'].keys())[0]
    
    # Selectores de Bloque y Ejercicio
    bloques = list(data['asignaturas'][asignatura_nombre].keys())
    bloque_sel = st.sidebar.selectbox("Bloque", bloques)
    ejercicios = data['asignaturas'][asignatura_nombre][bloque_sel]
    titulos_ejercicios = [f"{ej['id']} - {ej['titulo']}" for ej in ejercicios]
    ej_sel_index = st.sidebar.selectbox("Ejercicio", range(len(titulos_ejercicios)), format_func=lambda x: titulos_ejercicios[x])
    
    ejercicio_actual = ejercicios[ej_sel_index]
    normativa = "\n".join([f"- {r}" for r in data.get('normativa_2026', data.get('reglas_2026', []))])

    # --- PANTALLA PRINCIPAL: SOLO ENUNCIADO ---
    st.title(f"📝 {asignatura_nombre}")
    st.subheader(f"{ejercicio_actual['id']}: {ejercicio_actual['titulo']}")
    
    # Espacio para el enunciado (Protagonista absoluto)
    st.markdown("---")
    st.markdown(f"#### ENUNCIADO")
    st.write(ejercicio_actual['enunciado'])
    st.markdown("---")

    # --- ZONA OCULTA: SOLO SE ABRE AL TERMINAR ---
    with st.expander("✅ HE TERMINADO EL EJERCICIO (Revelar Criterios y Prompt)"):
        st.warning("Usa esta sección solo para corregir tu trabajo ya realizado.")
        
        col_rub, col_tip = st.columns(2)
        
        with col_rub:
            st.markdown("### ⚖️ Rúbrica de Corrección")
            st.write(ejercicio_actual['rubrica'])
            st.markdown("**Normativa 2026:**")
            st.caption(normativa)
            
        with col_tip:
            st.markdown("### 💡 Tip Pedagógico")
            st.info(ejercicio_actual['tip'])

        st.divider()
        
        # Generación del Prompt
        st.markdown("### 🤖 Prompt para tu IA")
        st.write("Haz clic en el icono de copiar (esquina superior derecha del cuadro gris) y pégalo en ChatGPT/Gemini junto a la foto de tu hoja.")
        
        prompt_final = f"""Actúa como un corrector oficial de la CiUG (Galicia) para la ABAU 2026.
Corrige el ejercicio de la imagen basándote en:

ASIGNATURA: {asignatura_nombre}
EJERCICIO: {ejercicio_actual['enunciado']}

RÚBRICA DETALLADA:
{ejercicio_actual['rubrica']}

NORMATIVA GENERAL (Rigor, Ortografía, Formato):
{normativa}

INSTRUCCIONES DE CORRECCIÓN:
1. Analiza el ejercicio resuelto por el alumno en la imagen.
2. Evalúa con máximo rigor ortográfico (-0.15 tildes, -0.25 faltas).
3. Da una nota estimada razonada.
4. Indica fallos específicos y cómo evitarlos en el examen real."""

        st.code(prompt_final, language="text")

except FileNotFoundError:
    st.error(f"Archivo {asignatura_file} no encontrado. Revisa tu repositorio.")