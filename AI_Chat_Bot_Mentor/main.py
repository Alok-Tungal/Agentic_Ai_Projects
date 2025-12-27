import streamlit as st
from langchain_google_genai import GoogleGenerativeAI,ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os  

# 1. Load environment variables once
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("gemini")

if not GOOGLE_API_KEY:
    st.error("Google API Key not found. Please set it in environment variables.")
    st.stop()


# Regular model
# st.title("Simple Gemini Model a regular model")

# prompt=st.text_area("type any query")

# if st.button("Give answer"):
#     rmodel=GoogleGenerativeAI(model="gemini-2.5-flash-lite",temperature=0.1)

#     response=rmodel.invoke(prompt)
#     st.write(response)


# Chat model

st.set_page_config(page_title="Chat Bot", page_icon="🤖")

st.title('🤖 Chat Bot using Gemini-2.5')

if "conv" not in st.session_state:
    st.session_state['conv']=[]
    st.session_state['memory']=[]
    st.session_state['memory'].append(("system","act like a 5 year old child"))

for y in st.session_state['conv']:
    with st.chat_message(y['role']):
        st.write(y['content'])


prompt=st.chat_input("type your quries")

if prompt:
    st.session_state['conv'].append({"role":"user","content":prompt})
    st.session_state['memory'].append(('user',prompt))

    with st.chat_message('user'):
        st.write(prompt)

    # model=ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=1.0)
    # messages = [("system", system_prompt), ("human", resume_text)]
    response=model.invoke(st.session_state['memory'])

    with st.chat_message('ai'):
        st.write(response.content)

    st.session_state['conv'].append({"role":"ai","content":response.content})
    st.session_state['memory'].append(("ai",response.content))
