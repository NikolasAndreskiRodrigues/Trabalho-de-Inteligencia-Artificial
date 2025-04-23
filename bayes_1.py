# iMPORTAR AS BIBLIOTECAS
import streamlit as st
import fitz
from groq import Groq
import os

# Caminho dinâmico da imagem
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(CURRENT_DIR, "logo.png")   

# Configurar chave da Groq
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# função para extrair os arquivos     
def extract_files(uploader):
    text = ""
    local_pdf_path = "base_de_dados.pdf" 

    if os.path.exists(local_pdf_path):
        with fitz.open(local_pdf_path) as doc:
            for page in doc:
                text += page.get_text("text")

    for pdf in uploader:
        with fitz.open(stream=pdf.read(), filetype="pdf") as doc: 
            for page in doc:
                text += page.get_text("text") 
    return text

# Motor de inferência para o sistema inteligente
def chat_with_groq(prompt, context):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Você é um assistente de Sistemas de viagem que responde com base em documentos fornecidos sobre quais são os melhores lugares e ponto pra visitar."},
            {"role": "user", "content": f"{context}\n\nPergunta: {prompt}"}
        ]
    )
    return response.choices[0].message.content    
    
# CRIAR A INTERFACE
def main():
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(LOGO_PATH, width=200)
    with col2:
        st.title("Sistema Inteligente de Viagem")
    # Incluir uma imagem de acordo ao sistema escolhido
    with st.sidebar:
        st.header("UPLoader Files")
        uploader = st.file_uploader("Adicione arquivos", type="pdf", accept_multiple_files=True)
    if uploader:
        text = extract_files(uploader)
        st.session_state["document-text"] = text
        user_input = st.text_input("Digite a sua pergunta")
        st.write("Resposta do Agente:")
        st.write(chat_with_groq(user_input, text))


if __name__ == "__main__":
    main()

#Rodar script -> streamlit run .\bayes_1.py