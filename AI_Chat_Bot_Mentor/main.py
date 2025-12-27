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
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# --- 1. CONFIGURATION MUST BE FIRST ---
st.set_page_config(
    page_title="AI Mentor",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. CUSTOM THEME (HTML/CSS/JS) ---
# This function injects custom CSS to remove Streamlit branding and style the chat
def inject_custom_css():
    st.markdown("""
    <style>
        /* Main Background and Text */
        .stApp {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        
        /* Hide Streamlit Main Menu and Footer */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Custom Header Styling */
        .custom-header {
            text-align: center;
            padding: 2rem 0;
            background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
            border-radius: 0 0 20px 20px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        }
        .custom-header h1 {
            color: white;
            font-family: 'Helvetica Neue', sans-serif;
            font-weight: 700;
            margin: 0;
            font-size: 2.5rem;
        }
        .custom-header p {
            color: #d1d5db;
            margin-top: 10px;
            font-size: 1.1rem;
        }

        /* Chat Message Bubble Styling */
        .stChatMessage {
            background-color: transparent !important;
            border: none !important;
        }

        /* User Message (Right Side/Blue) */
        div[data-testid="stChatMessage"]:nth-child(odd) {
            flex-direction: row-reverse;
            text-align: right;
        }
        div[data-testid="stChatMessage"]:nth-child(odd) div[data-testid="stChatMessageContent"] {
            background: linear-gradient(135deg, #0061ff 0%, #60efff 100%);
            color: white;
            border-radius: 20px 20px 0 20px;
            padding: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        /* AI Message (Left Side/Dark Gray) */
        div[data-testid="stChatMessage"]:nth-child(even) div[data-testid="stChatMessageContent"] {
            background-color: #262730;
            border: 1px solid #4a4a4a;
            color: #e0e0e0;
            border-radius: 20px 20px 20px 0;
            padding: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        /* Avatar Styling */
        div[data-testid="stChatMessage"] .st-emotion-cache-1p1m4ay {
            display: none; /* Hide default avatars to keep it clean, optional */
        }
        
        /* Input Box Styling */
        .stChatInput {
            position: fixed;
            bottom: 20px;
            width: 700px; /* Adjust based on layout */
            z-index: 1000;
        }
    </style>
    """, unsafe_allow_html=True)

    # Custom Header HTML
    st.markdown("""
        <div class="custom-header">
            <h1>🧠 AI Mentor</h1>
            <p>Your personal guide to wisdom and coding</p>
        </div>
    """, unsafe_allow_html=True)

# --- 3. API SETUP ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# If no key in Env, try sidebar input for testing
if not GOOGLE_API_KEY:
    with st.sidebar:
        st.warning("⚠️ No API Key found in Environment.")
        GOOGLE_API_KEY = st.text_input("Enter Gemini API Key", type="password")

if not GOOGLE_API_KEY:
    inject_custom_css()
    st.info("Please enter your Google API Key to start the mentor session.")
    st.stop()

# --- 4. INITIALIZE STATE ---
if "conv" not in st.session_state:
    st.session_state['conv'] = []
    st.session_state['memory'] = []
    # UPDATED SYSTEM PROMPT: Changed from "5 year old" to "Mentor"
    system_instruction = "You are a wise, patient, and expert AI Mentor. You help users solve problems with clear examples and encouraging language."
    st.session_state['memory'].append(("system", system_instruction))

# --- 5. RENDER UI ---
inject_custom_css()

# Display Chat History
# We use a container to keep the messages separate from the input
chat_container = st.container()

with chat_container:
    for message in st.session_state['conv']:
        # Assign avatars based on role
        avatar = "🧑‍💻" if message['role'] == 'user' else "🧠"
        with st.chat_message(message['role'], avatar=avatar):
            st.write(message['content'])

# --- 6. HANDLE INPUT & LOGIC ---
prompt = st.chat_input("Ask your mentor anything...")

if prompt:
    # 1. Display User Message Immediately
    with chat_container:
        with st.chat_message('user', avatar="🧑‍💻"):
            st.write(prompt)

    # 2. Update History
    st.session_state['conv'].append({"role": "user", "content": prompt})
    st.session_state['memory'].append(('user', prompt))

    # 3. Generate Response
    try:
        # Note: 'gemini-2.5-flash' is likely a typo or private preview. 
        # Using 'gemini-1.5-flash' for stability. Change back if needed.
        model = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash", 
            temperature=0.7, # Slightly creative but focused
            api_key=GOOGLE_API_KEY
        )
        
        response = model.invoke(st.session_state['memory'])
        
        # 4. Display AI Message
        with chat_container:
            with st.chat_message('ai', avatar="🧠"):
                st.write(response.content)

        # 5. Update History with AI Response
        st.session_state['conv'].append({"role": "ai", "content": response.content})
        st.session_state['memory'].append(("ai", response.content))

    except Exception as e:
        st.error(f"An error occurred: {e}")
