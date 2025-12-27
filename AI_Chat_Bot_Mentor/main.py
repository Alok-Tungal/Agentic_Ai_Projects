# import streamlit as st
# from langchain_google_genai import GoogleGenerativeAI,ChatGoogleGenerativeAI
# from dotenv import load_dotenv
# import os  

# # 1. Load environment variables once
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("gemini")
 
# if not GOOGLE_API_KEY:
#     st.error("Google API Key not found. Please set it in environment variables.")
#     st.stop()


# # Regular model
# # st.title("Simple Gemini Model a regular model")

# # prompt=st.text_area("type any query")

# # if st.button("Give answer"):
# #     rmodel=GoogleGenerativeAI(model="gemini-2.5-flash-lite",temperature=0.1)

# #     response=rmodel.invoke(prompt)
# #     st.write(response)


# # Chat model

# st.set_page_config(page_title="Chat Bot", page_icon="🤖")

# st.title('🤖 Chat Bot using Gemini-2.5')

# if "conv" not in st.session_state:
#     st.session_state['conv']=[]
#     st.session_state['memory']=[]
#     st.session_state['memory'].append(("system","act like a 5 year old child"))

# for y in st.session_state['conv']:
#     with st.chat_message(y['role']):
#         st.write(y['content'])


# prompt=st.chat_input("type your quries")

# if prompt:
#     st.session_state['conv'].append({"role":"user","content":prompt})
#     st.session_state['memory'].append(('user',prompt))

#     with st.chat_message('user'):
#         st.write(prompt)

    
#     model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=1.0)
#     # messages = [("system", system_prompt), ("human", resume_text)]
#     response=model.invoke(st.session_state['memory'])

#     with st.chat_message('ai'):
#         st.write(response.content)

#     st.session_state['conv'].append({"role":"ai","content":response.content})
#     st.session_state['memory'].append(("ai",response.content))


import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# --- 1. CONFIGURATION (Must be first) ---
st.set_page_config(
    page_title="AI Mentor",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. SETUP & SECURITY ---
load_dotenv()

# Strictly get key from environment. No UI input.
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("gemini")

if not GOOGLE_API_KEY:
    st.error("❌ **Configuration Error:** Google API Key not found in environment variables.")
    st.info("Please set `GOOGLE_API_KEY` in your `.env` file or system environment.")
    st.stop()

# --- 3. MODERN UI STYLING (CSS) ---
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background-color: #0E1117;
        color: #F0F2F6;
    }
    
    /* Remove standard Streamlit header/footer for cleaner look */
    #MainMenu, footer, header {visiblity: hidden; height: 0px;}

    /* Custom Header */
    .header-container {
        padding: 2rem 0;
        text-align: center;
        background: linear-gradient(to right, #4b6cb7, #182848);
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .header-container h1 {
        color: white;
        margin: 0;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        letter-spacing: 1px;
    }
    .header-container p {
        color: #cfd8dc;
        font-size: 1.1em;
        margin-top: 10px;
    }

    /* Chat Bubbles */
    .stChatMessage {
        background-color: transparent;
    }
    
    /* User Message (Blue Gradient) */
    div[data-testid="stChatMessage"]:nth-child(odd) div[data-testid="stChatMessageContent"] {
        background: linear-gradient(135deg, #007AFF 0%, #00C6FF 100%);
        color: white;
        border-radius: 20px 20px 5px 20px;
        padding: 12px 18px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }

    /* AI Message (Dark Glass) */
    div[data-testid="stChatMessage"]:nth-child(even) div[data-testid="stChatMessageContent"] {
        background-color: #262730;
        border: 1px solid #3E404D;
        color: #E6E6E6;
        border-radius: 20px 20px 20px 5px;
        padding: 12px 18px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    /* Input Field */
    .stChatInput textarea {
        border-radius: 25px !important;
        border: 1px solid #4B4B4B !important;
        background-color: #1E1E1E !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. RENDER CUSTOM HEADER ---
st.markdown("""
<div class="header-container">
    <h1>🤖 AI Mentor Chatbot</h1>
    <p>Real-time assistance for your coding journey</p>
</div>
""", unsafe_allow_html=True)

# --- 5. INITIALIZE CHAT STATE ---
if "conv" not in st.session_state:
    st.session_state['conv'] = []
    st.session_state['memory'] = []
    # System prompt
    st.session_state['memory'].append(("system", "You are an expert AI Mentor. Be concise, helpful, and friendly."))

# --- 6. DISPLAY CHAT HISTORY ---
# We use a container to hold the chat
for msg in st.session_state['conv']:
    with st.chat_message(msg['role']):
        st.write(msg['content'])

# --- 7. HANDLE INPUT & STREAMING RESPONSE ---
prompt = st.chat_input("Type your query here...")

if prompt:
    # 1. Display User Message
    with st.chat_message("user"):
        st.write(prompt)
    
    # 2. Append to History
    st.session_state['conv'].append({"role": "user", "content": prompt})
    st.session_state['memory'].append(("user", prompt))
    
    # 3. Generate & Stream Response
    with st.chat_message("ai"):
        try:
            # Using 1.5-flash for speed and stability
            llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash", 
                temperature=0.7,
                google_api_key=GOOGLE_API_KEY,
                streaming=True  # ENABLE STREAMING FOR REAL-TIME FEEL
            )
            
            # Stream the response content
            response_container = st.empty()
            full_response = ""
            
            # We use stream() instead of invoke() for real-time typing effect
            for chunk in llm.stream(st.session_state['memory']):
                full_response += chunk.content
                response_container.write(full_response + "▌") # Typing cursor effect
            
            response_container.write(full_response) # Final write without cursor
            
            # 4. Save to History
            st.session_state['conv'].append({"role": "ai", "content": full_response})
            st.session_state['memory'].append(("ai", full_response))

        except Exception as e:
            st.error(f"An error occurred: {e}")
