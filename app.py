import streamlit as st
from langflow_api import run_flow, FLOW_ID, TWEAKS
import os
from streamlit.web import cli as stcli
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Starting Streamlit app")
st.write("Streamlit app is running")
st.title("Langflow Chatbot")
port = int(os.environ.get("PORT", 8501))
st.write(f"Using port: {port}")



def main():
    st.write("Streamlit is running")
    # Rest of your app code...

# Rest of your Streamlit app code...
    if "messages" not in st.session_state:
    st.session_state.messages = []
    
    for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    
    if prompt := st.chat_input("What is your question?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    response = run_flow(
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
                if 'result' in results:
                    assistant_response = results['result']
    
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

if __name__ == '__main__':
    if st._is_running_with_streamlit:
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
