import streamlit as st
import json

# Configuración de página
st.set_page_config(page_title="Corrector Matemáticas II", layout="centered")

# Cargar datos
def load_data():
    with open('ejercicios.json', 'r', encoding='utf-8') as f:
        return json.load(f)

data = load_data()
asignatura = "Matemáticas II"

st.title("📚 Asistente de Corrección CiUG")
st.markdown("---")

# Selección de Bloque y Ejercicio
bloques = list(data['asignaturas'][asignatura].keys())
bloque_sel = st.sidebar.selectbox("Selecciona Bloque", bloques)

ejercicios = data['asignaturas'][asignatura][bloque_sel]
titulos_ejercicios = [f"{ej['id']} - {ej['titulo']}" for ej in ejercicios]
ej_sel_index = st.sidebar.selectbox("Selecciona Ejercicio", range(len(titulos_ejercicios)), format_func=lambda x: titulos_ejercicios[x])

ejercicio_actual = ejercicios[ej_sel_index]

# Mostrar contenido del ejercicio
st.subheader(f"{ejercicio_actual['id']}: {ejercicio_actual['titulo']}")
st.info("**ENUNCIADO:**\n\n" + ejercicio_actual['enunciado'])

with st.expander("Ver Rúbrica y Tips"):
    st.write("**Rúbrica Oficial:**", ejercicio_actual['rubrica'])
    st.write("**Consejo Pedagógico:**", ejercicio_actual['tip'])

st.markdown("---")

# Generador de Prompt
st.subheader("🤖 Generador de Prompt para IA")
st.write("Haz clic en el botón de la esquina superior derecha del cuadro gris para copiar el texto. Luego pégalo en ChatGPT/Gemini junto a la foto de tu ejercicio.")

prompt_final = f"""Actúa como un corrector experto de las pruebas ABAU de la CiUG (Galicia). 
Mi examen de Matemáticas II consiste en el siguiente ejercicio:

ENUNCIADO:
{ejercicio_actual['enunciado']}

CRITERIOS DE CORRECCIÓN (RÚBRICA):
{ejercicio_actual['rubrica']}

CONSEJO ADICIONAL:
{ejercicio_actual['tip']}

INSTRUCCIONES PARA TI:
1. Analiza la imagen de mi ejercicio resuelto.
2. Compara mi resolución con el enunciado y la rúbrica.
3. Proporciona una NOTA estimada sobre 2.5 puntos.
4. Indica fallos específicos de cálculo o de rigor matemático.
5. Dime qué debería mejorar para obtener la máxima puntuación.

Responde de forma clara y motivadora."""

# Componente de código (permite copiar fácilmente)
st.code(prompt_final, language="text")

st.markdown("---")
st.caption("Herramienta de apoyo al estudio - Sin conexión directa con IA para evitar costes.")