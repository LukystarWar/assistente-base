import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# Carrega variáveis de ambiente
load_dotenv()

# Configuração da API Groq
client = OpenAI(
    api_key=os.getenv('GROQ_API_KEY'),
    base_url="https://api.groq.com/openai/v1"
)

def load_system_prompt():
    try:
        with open('prompt.txt', 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        return "Você é um assistente prestativo e direto."

def get_ai_response(messages):
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erro ao comunicar com a API: {str(e)}"

# Configuração da página
st.set_page_config(
    page_title="Assistante IA", 
    page_icon="🤖",
    layout="centered"
)

st.title("🎬 Framey IA")
st.caption("Converse com o Assistente usando modelos avançados de IA")

# Inicialização do histórico na sessão
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": load_system_prompt()}
    ]

# Exibe o histórico de mensagens usando st.chat_message
for message in st.session_state.messages[1:]:  # Pula a mensagem do sistema
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    else:
        with st.chat_message("assistant", avatar="🎬"):
            st.markdown(message["content"])

# Campo de entrada do usuário usando st.chat_input
if prompt := st.chat_input("Digite sua pergunta aqui..."):
    # Adiciona e exibe mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Obtém e exibe resposta da IA
    with st.chat_message("assistant", avatar="🎬"):
        with st.spinner("Pensando..."):
            response = get_ai_response(st.session_state.messages)
        st.markdown(response)
        
        # Adiciona resposta ao histórico
        st.session_state.messages.append({"role": "assistant", "content": response})

# Botão para limpar histórico
if st.sidebar.button("🗑️ Limpar Conversa"):
    st.session_state.messages = [
        {"role": "system", "content": load_system_prompt()}
    ]
    st.rerun()