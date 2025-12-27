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

# --- 1. PAGE CONFIGURATION (MUST BE FIRST) ---
st.set_page_config(
    page_title="AI Mentor Pro",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

# --- 2. PROFESSIONAL STYLING (CSS) ---
# We inject this immediately so the UI looks good while loading
st.markdown("""
<style>
    /* 1. Main Background and Font */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }

    /* 2. Hide Default Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 3. Custom Header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    .main-header p {
        color: #e0e0e0;
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }

    /* 4. Chat Message Styling */
    /* AI Message (Left) */
    .stChatMessage[data-testid="stChatMessage"]:nth-of-type(even) {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 10px;
    }
    
    /* User Message (Right - Visual trick using CSS is hard in Streamlit, 
       so we stick to a clean highlighted look) */
    .stChatMessage[data-testid="stChatMessage"]:nth-of-type(odd) {
        background-color: #1e1e1e;
        border: 1px solid #667eea;
        border-radius: 10px;
        padding: 10px;
    }

    /* 5. Input Box Styling */
    .stChatInput textarea {
        background-color: #1e293b !important;
        color: white !important;
        border: 1px solid #475569 !important;
    }
    
    /* 6. Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid #1e293b;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. UI HEADER ---
st.markdown("""
<div class="main-header">
    <h1>🎓 AI Mentor Chatbot</h1>
    <p>Your intelligent companion for coding and wisdom</p>
</div>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR SETTINGS ---
with st.sidebar:
    st.header("⚙️ Settings")
    
    # API Key Input (if not in env)
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        api_key = st.text_input("Enter Google API Key", type="password")
    
    st.divider()
    
    # Model Controls
    temperature = st.slider("Creativity Level", 0.0, 1.0, 0.7)
    model_name = st.selectbox("Select Model", ["gemini-1.5-flash", "gemini-1.5-pro"])
    
    st.divider()
    
    # Clear Chat Button
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state['conv'] = []
        st.session_state['memory'] = []
        st.rerun()

    st.markdown("---")
    st.caption("Developed by Alok Mahadev Tungal")

# --- 5. INITIALIZE STATE ---
if "conv" not in st.session_state:
    st.session_state['conv'] = []
    st.session_state['memory'] = []
    # System Prompt
    system_prompt = "You are an expert AI Mentor. Answer questions clearly, provide code examples where helpful, and be encouraging."
    st.session_state['memory'].append(("system", system_prompt))

# --- 6. MAIN CHAT INTERFACE ---

# If no API key, stop here
if not api_key:
    st.warning("⚠️ Please enter your Google API Key in the sidebar to continue.")
    st.stop()

# Display Chat History
for msg in st.session_state['conv']:
    # Choose avatar based on role
    icon = "👤" if msg['role'] == 'user' else "🤖"
    with st.chat_message(msg['role'], avatar=icon):
        st.write(msg['content'])

# Chat Input
prompt = st.chat_input("Ask me anything about coding or life...")

if prompt:
    # 1. Show User Message
    st.chat_message("user", avatar="👤").write(prompt)
    
    # 2. Add to History
    st.session_state['conv'].append({"role": "user", "content": prompt})
    st.session_state['memory'].append(("user", prompt))
    
    # 3. Generate Response
    try:
        llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            google_api_key=api_key
        )
        
        with st.chat_message("ai", avatar="🤖"):
            response_placeholder = st.empty()
            response = llm.invoke(st.session_state['memory'])
            response_placeholder.write(response.content)
            
        # 4. Add AI Response to History
        st.session_state['conv'].append({"role": "ai", "content": response.content})
        st.session_state['memory'].append(("ai", response.content))
        
    except Exception as e:
        st.error(f"Error: {e}")
