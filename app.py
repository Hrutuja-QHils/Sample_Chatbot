import streamlit as st
import os
from langflow_api import run_flow, FLOW_ID, TWEAKS
import logging
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.title("Marathi Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

async def get_response(prompt):
    response = await asyncio.to_thread(
        run_flow,
        message=prompt,
        endpoint=FLOW_ID,
        output_type="chat",
        input_type="chat",
        tweaks=TWEAKS
    )
    
    assistant_response = "I'm sorry, I couldn't generate a response."
    
    if isinstance(response, dict) and 'outputs' in response:
        outputs = response['outputs']
        if outputs and isinstance(outputs[0], dict) and 'outputs' in outputs[0]:
            inner_outputs = outputs[0]['outputs']
            if inner_outputs and isinstance(inner_outputs[0], dict) and 'results' in inner_outputs[0]:
                results = inner_outputs[0]['results']
                if 'message' in results and 'text' in results['message']:
                    assistant_response = results['message']['text']
    
    return assistant_response

if "waiting_for_response" not in st.session_state:
    st.session_state.waiting_for_response = False

if not st.session_state.waiting_for_response:
    prompt = st.chat_input("What is your question?")
    if prompt:
        st.session_state.waiting_for_response = True
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.spinner("Please wait, generating response..."):
            assistant_response = asyncio.run(get_response(prompt))
        
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        st.session_state.waiting_for_response = False
        st.experimental_rerun()
else:
    st.info("Please wait for the current response before asking another question.")
