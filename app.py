import streamlit as st
import os
from langflow_api import run_flow, FLOW_ID, TWEAKS
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    st.title("Langflow Chatbot")
    
    port = int(os.environ.get("PORT", 10000))
    st.write(f"Using port: {port}")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is your question?"):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.spinner("Generating response..."):
            response = run_flow(
                message=prompt,
                endpoint=FLOW_ID,
                output_type="chat",
                input_type="chat",
                tweaks=TWEAKS
            )

        if "error" in response:
            st.error(f"Error: {response['error']}")
            logger.error(f"Error in response: {response['error']}")
        else:
            assistant_response = "I'm sorry, I couldn't generate a response."
            if isinstance(response, dict) and 'outputs' in response:
                outputs = response['outputs']
                if outputs and isinstance(outputs[0], dict) and 'outputs' in outputs[0]:
                    inner_outputs = outputs[0]['outputs']
                    if inner_outputs and isinstance(inner_outputs[0], dict) and 'results' in inner_outputs[0]:
                        results = inner_outputs[0]['results']
                        if 'result' in results:
                            assistant_response = results['result']
            else:
                st.warning(f"Unexpected response format: {response}")
                logger.warning(f"Unexpected response format: {response}")

            with st.chat_message("assistant"):
                st.markdown(assistant_response)
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})

if __name__ == "__main__":
    main()
