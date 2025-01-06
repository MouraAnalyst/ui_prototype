import openai
import streamlit as st

# Título de la aplicación
st.title("ChatGPT-like clone")

# Configuración de la clave API
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Estado inicial de la sesión
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# Mostrar mensajes anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del usuario
if prompt := st.chat_input("What is up?"):
    # Agregar el mensaje del usuario al estado
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Llamar a la API de OpenAI
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=st.session_state.messages, stream=True
            )

            for chunk in response:
                chunk_message = chunk["choices"][0]["delta"].get("content", "")
                full_response += chunk_message
                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

        except Exception as e:
            st.error(f"Error: {e}")

        # Agregar la respuesta del asistente al estado
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )
