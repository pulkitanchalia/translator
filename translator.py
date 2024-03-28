from io import StringIO
import streamlit as st
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)
from langchain.document_loaders import *

def translator(open_api_key, json_text, source_language, target_language):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        temperature=0.7,
        openai_api_key=open_api_key
    )
    system_template = """You are a language translator. Your task is to translate JSON file content from {source_language} to {target_language} in JSON format only.
            Keep in mind to produce the most accurate translation possible while maintaining the original meaning of the content.
            keep the keys in JSON as it is and only translate the values of the keys."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Please translate the following JSON file content from {source_language} to {target_language}: '{json_text}'."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(json_text=json_text, source_language=source_language, target_language=target_language)
    return result  # returns string

st.title("SendPro 360 Translation Utility")

# Initialize state variables
source_language = ""
target_language = ""
string_data = ""
translated_text = ""

with st.form("form1", clear_on_submit=True):
    # Get the source language from the user
    uploaded_file = st.file_uploader("Upload a source JSON file", type=["json"])

    if uploaded_file is not None:
        translated_text = ""
        bytes_data = uploaded_file.getvalue()

        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

        # To read file as string:
        string_data = stringio.read()

    source_language = st.selectbox("Source Language", [ "en-US", "en-GB", "en-AU", "en-CA", "en-IN", "es-ES", "es-MX", "fr-CA", "fr-FR", "it-IT", "ja-JP", "da-DK", "de-DE"])

    target_language = st.selectbox("Target Language", ["da-DK", "de-DE", "en-AU", "en-CA", "en-GB", "en-IN", "en-US", "es-ES", "es-MX", "fr-CA", "fr-FR", "it-IT", "ja-JP"])

    open_api_key = st.text_input("Enter OpenAI API Key", type="password")
    # Create a button to trigger the translation
    if st.form_submit_button("Translate"):
        if not open_api_key:
            st.info("Please add your OpenAI API key to continue.")
        if string_data and source_language and target_language and open_api_key:
            with st.spinner('Translation is taking place...'):
                translated_text = translator(open_api_key, string_data, source_language, target_language)
                # remove the quotes from the translated text
                translated_text = translated_text.replace("'", "")
        else:
            translated_text = ""

    # Display the translated text to the user
    if translated_text:
        st.json(translated_text) 