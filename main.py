import streamlit as st
import PyPDF2
import requests
import os

# Función para extraer texto de un PDF
def extract_pdf_text(pdf_file):
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error al procesar el PDF: {str(e)}"

# Función para interactuar con Ollama
def query_ollama(prompt, context, model="llama3"):
    try:
        # Endpoint local de Ollama (por defecto usa localhost en el puerto 11434)
        url = "http://localhost:11434/api/chat"
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": f"Eres un asistente basado en el siguiente contexto: {context}"},
                {"role": "user", "content": prompt}
            ]
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Verifica errores en la solicitud
        data = response.json()
        return data.get("choices", [{}])[0].get("content", "Sin respuesta.")
    except requests.exceptions.RequestException as e:
        return f"Error al comunicarse con Ollama: {str(e)}"

# Aplicación principal
def main():
    st.title("🤖 ChatBot AI con Ollama")
    st.write("Sube un archivo PDF lleno de información y haz preguntas al respecto.")

    # Carga de archivos PDF
    uploaded_file = st.file_uploader("Sube tu archivo PDF aquí", type="pdf")

    if uploaded_file:
        # Procesar el archivo PDF
        st.write(f"📄 Procesando archivo: {uploaded_file.name}")
        pdf_text = extract_pdf_text(uploaded_file)

        if "Error" in pdf_text:
            st.error(pdf_text)
        else:
            st.success("✅ PDF cargado y procesado correctamente.")

            # Campo de texto para preguntas del usuario
            user_question = st.text_input("Escribe tu pregunta:")
            if st.button("Consultar"):
                if user_question.strip():
                    with st.spinner("Pensando..."):
                        response = query_ollama(user_question, pdf_text)
                    st.text_area("Respuesta del ChatBot:", response, height=200)
                else:
                    st.warning("Por favor, escribe una pregunta.")

if __name__ == "__main__":
    main()
