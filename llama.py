import streamlit as st
import os
from logs import write_log_entry

import openai
from google.auth import default, transport

project_id = os.environ['GOOGLE_CLOUD_PROJECT']
region = os.environ['GOOGLE_CLOUD_REGION']

def get_llama_response(models, prompt, output_area):
    """Streams response from Llama model using OpenAI-compatible SDK."""
    credentials, _ = default()
    auth_request = transport.requests.Request()
    credentials.refresh(auth_request)

    client = openai.OpenAI(
        base_url=f"https://{region}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{region}/endpoints/openapi/chat/completions?",
        api_key=credentials.token,
    )

    system_msg = {
        "role": "system",
        "content": (
            "You are the ROI Generative AI Chatbot. You provide clear, accurate, "
            "and professional responses. Use step-by-step reasoning if prompted."
        )
    }
    welcome_msg = {"role": "assistant", "content": "Hi! I'm the ROI Chatbot. How can I help you?"}
    user_msg = {"role": "user", "content": prompt}
    messages = [system_msg, welcome_msg, user_msg]

    stream = client.chat.completions.create(

"""
TODO: Pass paramters for model, messages, stream, temperature and max_tokens here
"""
    )

    response = ""
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            write_log_entry(models['Llama'], prompt, content)
            response += content
            output_area.markdown(response, unsafe_allow_html=True)
