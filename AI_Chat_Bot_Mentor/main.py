import streamlit as st
from langchain_google_genai import GoogleGenerativeAI,ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os 

# 1. Load environment variables once
load_dotenv()
os.environ['GOOGLE_API_KEY'] = os.getenv('gemini')


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

    model=ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

    response=model.invoke(st.session_state['memory'])

    with st.chat_message('ai'):
        st.write(response.content)

    st.session_state['conv'].append({"role":"ai","content":response.content})
    st.session_state['memory'].append(("ai",response.content))
