# import streamlit as st
# import pandas as pd
# import pdfplumber
# import io
# import json
# import os        
# import time 
# from dotenv import load_dotenv 
# import google.generativeai as genai
# from pydantic import BaseModel, Field
# from typing import List, Optional

# # ==========================================
# # 1. ADVANCED PAGE CONFIG
# # ==========================================
# st.set_page_config(
#     page_title="Resume Intelligence AI",
#     page_icon="🧠",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # ==========================================
# # 2. ADVANCED CSS (GLASSMORPHISM THEME)
# # ==========================================
# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700&display=swap');
    
#     /* BACKGROUND & FONT */
#     .stApp {
#         background: radial-gradient(circle at top left, #1e1e2f, #0a0a12);
#         color: #e0e0e0;
#         font-family: 'Outfit', sans-serif;
#     }
    
#     /* HIDE DEFAULT STREAMLIT UI */
#     #MainMenu, footer, header {visibility: hidden;}
#     section[data-testid="stSidebar"] {display: none;}
    
#     /* HERO SECTION (TITLE) */
#     .hero-container {
#         text-align: center;
#         padding: 3rem 1rem;
#         background: rgba(255, 255, 255, 0.03);
#         border: 1px solid rgba(255, 255, 255, 0.05);
#         border-radius: 20px;
#         backdrop-filter: blur(10px);
#         margin-bottom: 2rem;
#         box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
#     }
#     .hero-title {
#         font-size: 3.5rem;
#         font-weight: 700;
#         background: linear-gradient(90deg, #00c6ff, #0072ff);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         margin-bottom: 0.5rem;
#     }
#     .hero-subtitle {
#         font-size: 1.2rem;
#         color: #a0a0b0;
#     }

#     /* UPLOAD ZONE STYLE */
#     .stFileUploader {
#         background: rgba(255, 255, 255, 0.02);
#         border: 1px dashed #4b4b60;
#         border-radius: 15px;
#         padding: 2rem;
#         transition: all 0.3s ease;
#     }
#     .stFileUploader:hover {
#         border-color: #0072ff;
#         background: rgba(0, 114, 255, 0.05);
#     }

#     /* METRIC CARDS */
#     div[data-testid="stMetric"] {
#         background: rgba(255, 255, 255, 0.05);
#         border: 1px solid rgba(255, 255, 255, 0.1);
#         border-radius: 12px;
#         padding: 15px;
#         box-shadow: 0 4px 6px rgba(0,0,0,0.1);
#         transition: transform 0.2s;
#     }
#     div[data-testid="stMetric"]:hover {
#         transform: translateY(-5px);
#         border-color: #00c6ff;
#     }
    
#     /* GLOWING BUTTON */
#     div.stButton > button {
#         background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
#         color: white;
#         font-weight: 600;
#         padding: 0.8rem 2.5rem;
#         border-radius: 30px;
#         border: none;
#         box-shadow: 0 0 15px rgba(0, 114, 255, 0.5);
#         transition: all 0.3s ease;
#         text-transform: uppercase;
#         letter-spacing: 1px;
#     }
#     div.stButton > button:hover {
#         box-shadow: 0 0 25px rgba(0, 114, 255, 0.8);
#         transform: scale(1.05);
#     }

#     /* DATAFRAME STYLING */
#     div[data-testid="stDataFrame"] {
#         background: rgba(255, 255, 255, 0.02);
#         border-radius: 10px;
#         padding: 10px;
#     }
# </style>
# """, unsafe_allow_html=True)

# # ==========================================
# # 3. SETUP & LOGIC
# # ==========================================
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("gemini")

# # Data Models
# class ContactInfo(BaseModel):
#     name: Optional[str] = Field(None)
#     email: Optional[str] = Field(None)
#     phone: Optional[str] = Field(None)
#     linkedin: Optional[str] = Field(None)

# class Project(BaseModel):
#     title: str
#     tech_stack: Optional[str] = Field(None)

# class ResumeData(BaseModel):
#     contact: ContactInfo
#     skills: List[str] = Field(default_factory=list)
#     projects: List[Project] = Field(default_factory=list)
#     education_degree: Optional[str] = Field(None)
#     years_experience: Optional[str] = Field(None)

# def extract_text(file_bytes):
#     try:
#         with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
#             return "\n".join([p.extract_text() or "" for p in pdf.pages])
#     except: return ""

# def analyze_resume(text):
#     if not GOOGLE_API_KEY: return None
#     genai.configure(api_key=GOOGLE_API_KEY)
#     model = genai.GenerativeModel('gemini-1.5-flash')
    
#     prompt = f""" 
#     Analyze resume. Return JSON.
#     Extract: Name, Email, Phone, LinkedIn, Latest Degree, Exp (Years), Top Skills, ALL Projects.
    
#     RESUME: {text[:8000]}
    
#     JSON SCHEMA:
#     {{
#         "contact": {{ "name": "...", "email": "...", "phone": "...", "linkedin": "..." }},
#         "education_degree": "...",
#         "years_experience": "...",
#         "skills": ["..."],
#         "projects": [ {{ "title": "...", "tech_stack": "..." }} ]
#     }}
#     """
#     try:
#         res = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
#         return ResumeData(**json.loads(res.text))
#     except: return None

# # ==========================================
# # 4. ADVANCED UI LAYOUT
# # ==========================================

# # --- HERO HEADER ---
# st.markdown("""
# <div class="hero-container">
#     <div class="hero-title">Resume Intelligence AI</div>
#     <div class="hero-subtitle">Upload Resumes • Extract Insights • Export Data</div>
# </div>
# """, unsafe_allow_html=True)

# # --- ERROR CHECK ---
# if not GOOGLE_API_KEY:
#     st.error("🔒 **System Locked:** API Key Missing. Please configure your `.env` file.")
#     st.stop()

# # --- MAIN INTERFACE ---
# col1, col2, col3 = st.columns([1, 2, 1])

# with col2:
#     uploaded_files = st.file_uploader("📂 Drag & Drop PDF Resumes", type=["pdf"], accept_multiple_files=True)

# # Only show the "Start" button if files are uploaded
# if uploaded_files:
#     st.markdown("<br>", unsafe_allow_html=True)
    
#     # Centered Button
#     c1, c2, c3 = st.columns([1, 1, 1])
#     with c2:
#         start_process = st.button("🚀 IGNITE ANALYSIS", use_container_width=True)

#     if start_process:
#         # --- PROCESSING UI ---
#         results = []
#         progress_bar = st.progress(0)
#         status_box = st.empty()
        
#         for i, file in enumerate(uploaded_files):
#             status_box.info(f"⚡ Analyzing: **{file.name}**")
#             text = extract_text(file.read())
#             if text:
#                 data = analyze_resume(text)
#                 if data: results.append(data)
            
#             progress_bar.progress((i + 1) / len(uploaded_files))
#             time.sleep(0.05) # UX Animation
            
#         progress_bar.empty()
#         status_box.empty()
        
#         # --- RESULTS DASHBOARD ---
#         if results:
#             st.markdown("---")
#             st.subheader("📊 Intelligence Report")
            
#             # 1. METRICS ROW
#             m1, m2, m3, m4 = st.columns(4)
#             m1.metric("Candidates", len(results))
#             m2.metric("Total Projects", sum(len(r.projects) for r in results))
#             m3.metric("Avg. Experience", f"{len(results)} Yrs" if len(results) > 0 else "N/A") # Placeholder logic
#             m4.metric("Success Rate", "100%")

#             # 2. TABBED VIEW
#             tab1, tab2 = st.tabs(["📄 Detailed Table", "💾 JSON Data"])
            
#             # Prepare Data
#             rows = []
#             for r in results:
#                 proj_str = " • ".join([f"{p.title} [{p.tech_stack}]" for p in r.projects])
#                 rows.append({
#                     "Name": r.contact.name,
#                     "Experience": r.years_experience,
#                     "Degree": r.education_degree,
#                     "Projects": proj_str,
#                     "Skills": ", ".join(r.skills[:5]) + "...",
#                     "Email": r.contact.email,
#                     "LinkedIn": r.contact.linkedin
#                 })
#             df = pd.DataFrame(rows)

#             with tab1:
#                 st.dataframe(
#                     df,
#                     column_config={
#                         "Name": st.column_config.TextColumn("Candidate", width="medium"),
#                         "Projects": st.column_config.TextColumn("Key Projects", width="large"),
#                         "LinkedIn": st.column_config.LinkColumn("Profile"),
#                     },
#                     use_container_width=True,
#                     height=500
#                 )
            
#             with tab2:
#                 st.json([r.dict() for r in results])

#             # 3. EXPORT AREA
#             st.markdown("<br>", unsafe_allow_html=True)
#             csv = df.to_csv(index=False).encode('utf-8')
            
#             col_d1, col_d2, col_d3 = st.columns([1, 2, 1])
#             with col_d2:
#                 st.download_button(
#                     label="📥 DOWNLOAD INTELLIGENCE REPORT (CSV)",
#                     data=csv,
#                     file_name="Resume_Intelligence_Report.csv",
#                     mime="text/csv",
#                     use_container_width=True
#                 )


# import streamlit as st
# import pandas as pd
# import pdfplumber
# import io
# import json
# import os
# import time
# from dotenv import load_dotenv
# import google.generativeai as genai
# from pydantic import BaseModel, Field
# from typing import List, Optional

# # ==========================================
# # 1. ADVANCED PAGE CONFIG
# # ==========================================
# st.set_page_config(
#     page_title="Resume Intelligence AI",
#     page_icon="🧠",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # ==========================================
# # 2. ADVANCED CSS (IMPROVED GLASSMORPHISM & VISIBILITY)
# # ==========================================
# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
#     /* BACKGROUND & FONT */
#     .stApp {
#         /* A smoother, slightly lighter white gradient for better contrast */
#         background: radial-gradient(circle at top left, #2a2a3e, #12121a);
#         color: #f0f0f0; /* Brighter main text color */
#         font-family: 'Outfit', sans-serif;
#     }
    
#     /* HIDE DEFAULT STREAMLIT UI */
#     #MainMenu, footer, header {visibility: hidden;}
#     section[data-testid="stSidebar"] {display: none;}
    
#     /* HERO SECTION (TITLE) */
#     .hero-container {
#         text-align: center;
#         padding: 4rem 2rem;
#         /* Increased opacity for better text readability */
#         background: rgba(30, 30, 46, 0.7);
#         border: 1px solid rgba(255, 255, 255, 0.1);
#         border-radius: 24px;
#         backdrop-filter: blur(15px);
#         margin-bottom: 3rem;
#         box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.4);
#     }
#     .hero-title {
#         font-size: 4rem;
#         font-weight: 800;
#         /* Brighter gradient for the title */
#         background: linear-gradient(90deg, #40d0ff, #0080ff);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         margin-bottom: 1rem;
#         letter-spacing: -1px;
#     }
#     .hero-subtitle {
#         font-size: 1.4rem;
#         color: #d0d0e0; /* Brighter subtitle text */
#         font-weight: 400;
#     }

#     /* UPLOAD ZONE STYLE */
#     .stFileUploader {
#         background: rgba(30, 30, 46, 0.6);
#         border: 2px dashed #5b5b70;
#         border-radius: 20px;
#         padding: 3rem;
#         transition: all 0.3s ease;
#         text-align: center;
#     }
#     .stFileUploader:hover {
#         border-color: #40d0ff;
#         background: rgba(64, 208, 255, 0.1);
#     }
#     /* Improve visibility of the upload text and button */
#     .stFileUploader > div > div {
#         color: #ffffff;
#     }
#     .stFileUploader button {
#         background: #40d0ff;
#         color: #0a0a12;
#         border: none;
#         font-weight: 600;
#     }

#     /* METRIC CARDS */
#     div[data-testid="stMetric"] {
#         background: rgba(30, 30, 46, 0.7);
#         border: 1px solid rgba(255, 255, 255, 0.1);
#         border-radius: 16px;
#         padding: 20px;
#         box-shadow: 0 8px 16px rgba(0,0,0,0.2);
#         transition: all 0.3s ease;
#         backdrop-filter: blur(10px);
#     }
#     div[data-testid="stMetric"]:hover {
#         transform: translateY(-8px);
#         border-color: #40d0ff;
#         box-shadow: 0 12px 24px rgba(64, 208, 255, 0.3);
#     }
#     /* Improve metric text visibility */
#     div[data-testid="stMetricLabel"] {
#         color: #c0c0d0;
#         font-weight: 500;
#     }
#     div[data-testid="stMetricValue"] {
#         color: #ffffff;
#         font-weight: 700;
#     }
    
#     /* GLOWING BUTTON */
#     div.stButton > button {
#         background: linear-gradient(90deg, #40d0ff 0%, #0080ff 100%);
#         color: white;
#         font-weight: 700;
#         padding: 1rem 3rem;
#         border-radius: 50px;
#         border: none;
#         box-shadow: 0 0 20px rgba(0, 128, 255, 0.6);
#         transition: all 0.3s ease;
#         text-transform: uppercase;
#         letter-spacing: 2px;
#         font-size: 1.1rem;
#     }
#     div.stButton > button:hover {
#         box-shadow: 0 0 35px rgba(0, 128, 255, 0.9);
#         transform: scale(1.03);
#     }
#     div.stButton > button:active {
#         transform: scale(0.98);
#     }

#     /* DATAFRAME STYLING */
#     div[data-testid="stDataFrame"] {
#         background: rgba(30, 30, 46, 0.7);
#         border: 1px solid rgba(255, 255, 255, 0.1);
#         border-radius: 16px;
#         padding: 15px;
#         backdrop-filter: blur(10px);
#     }
#     /* Improve table text visibility */
#     .stDataFrame {
#         color: #f0f0f0;
#     }
#     .stDataFrame [data-testid="stHeader"] {
#         background-color: rgba(255, 255, 255, 0.05);
#         color: #ffffff;
#         font-weight: 600;
#     }
    
#     /* STATUS BOX */
#     .stAlert {
#         background: rgba(30, 30, 46, 0.8);
#         color: #ffffff;
#         border: 1px solid rgba(64, 208, 255, 0.5);
#         backdrop-filter: blur(10px);
#         border-radius: 12px;
#     }
    
#     /* TABS */
#     .stTabs [data-baseweb="tab-list"] {
#         background-color: rgba(30, 30, 46, 0.5);
#         padding: 5px;
#         border-radius: 12px;
#         border: 1px solid rgba(255, 255, 255, 0.1);
#     }
#     .stTabs [data-baseweb="tab"] {
#         color: #c0c0d0;
#         border-radius: 8px;
#         padding: 8px 16px;
#     }
#     .stTabs [aria-selected="true"] {
#         background-color: rgba(64, 208, 255, 0.2);
#         color: #ffffff;
#         font-weight: 600;
#     }
# </style>
# """, unsafe_allow_html=True)

# # ==========================================
# # 3. SETUP & LOGIC
# # ==========================================
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("gemini")

# # Data Models
# class ContactInfo(BaseModel):
#     name: Optional[str] = Field(None)
#     email: Optional[str] = Field(None)
#     phone: Optional[str] = Field(None)
#     linkedin: Optional[str] = Field(None)

# class Project(BaseModel):
#     title: str
#     tech_stack: Optional[str] = Field(None)

# class ResumeData(BaseModel):
#     contact: ContactInfo
#     skills: List[str] = Field(default_factory=list)
#     projects: List[Project] = Field(default_factory=list)
#     education_degree: Optional[str] = Field(None)
#     years_experience: Optional[str] = Field(None)

# def extract_text(file_bytes):
#     try:
#         with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
#             return "\n".join([p.extract_text() or "" for p in pdf.pages])
#     except: return ""

# def analyze_resume(text):
#     if not GOOGLE_API_KEY: return None
#     genai.configure(api_key=GOOGLE_API_KEY)
#     # MODIFIED: Using gemini-2.5-flash as requested
#     model = genai.GenerativeModel('gemini-2.5-flash')
    
#     prompt = f"""
#     Analyze resume. Return JSON.
#     Extract: Name, Email, Phone, LinkedIn, Latest Degree, Exp (Years), Top Skills, ALL Projects.
    
#     RESUME: {text[:8000]}
    
#     JSON SCHEMA:
#     {{
#         "contact": {{ "name": "...", "email": "...", "phone": "...", "linkedin": "..." }},
#         "education_degree": "...",
#         "years_experience": "...",
#         "skills": ["..."],
#         "projects": [ {{ "title": "...", "tech_stack": "..." }} ]
#     }}
#     """
#     try:
#         res = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
#         return ResumeData(**json.loads(res.text))
#     except: return None

# # ==========================================
# # 4. ADVANCED UI LAYOUT
# # ==========================================

# # --- HERO HEADER ---
# st.markdown("""
# <div class="hero-container">
#     <div class="hero-title">Resume Intelligence AI</div>
#     <div class="hero-subtitle">Upload Resumes • Extract Insights • Export Data</div>
# </div>
# """, unsafe_allow_html=True)

# # --- ERROR CHECK ---
# if not GOOGLE_API_KEY:
#     st.error("🔒 **System Locked:** API Key Missing. Please configure your `.env` file.")
#     st.stop()

# # --- MAIN INTERFACE ---
# col1, col2, col3 = st.columns([1, 3, 1])

# with col2:
#     uploaded_files = st.file_uploader("📂 Drag & Drop PDF Resumes", type=["pdf"], accept_multiple_files=True)

# # Only show the "Start" button if files are uploaded
# if uploaded_files:
#     st.markdown("<br>", unsafe_allow_html=True)
    
#     # Centered Button
#     c1, c2, c3 = st.columns([1, 1, 1])
#     with c2:
#         start_process = st.button("🚀 IGNITE ANALYSIS", use_container_width=True)

#     if start_process:
#         # --- PROCESSING UI ---
#         results = []
#         progress_bar = st.progress(0)
#         status_box = st.empty()
        
#         for i, file in enumerate(uploaded_files):
#             status_box.info(f"⚡ Analyzing: **{file.name}**")
#             text = extract_text(file.read())
#             if text:
#                 data = analyze_resume(text)
#                 if data: results.append(data)
            
#             progress_bar.progress((i + 1) / len(uploaded_files))
#             time.sleep(0.05) # UX Animation
            
#         progress_bar.empty()
#         status_box.empty()
        
#         # --- RESULTS DASHBOARD ---
#         if results:
#             st.markdown("---")
#             st.subheader("📊 Intelligence Report")
            
#             # 1. METRICS ROW
#             m1, m2, m3, m4 = st.columns(4)
#             m1.metric("Candidates", len(results))
#             m2.metric("Total Projects", sum(len(r.projects) for r in results))
#             # Simple logic for average experience, can be improved
#             total_exp = 0
#             exp_count = 0
#             for r in results:
#                 if r.years_experience and r.years_experience.lower() != "fresher":
#                     try:
#                         # Extract first number found
#                         import re
#                         match = re.search(r'\d+', r.years_experience)
#                         if match:
#                             total_exp += int(match.group())
#                             exp_count += 1
#                     except: pass
            
#             avg_exp_str = f"{round(total_exp / exp_count, 1)} Yrs" if exp_count > 0 else "N/A"
#             m3.metric("Avg. Experience", avg_exp_str)
#             m4.metric("Success Rate", "100%")

#             # 2. TABBED VIEW
#             tab1, tab2 = st.tabs(["📄 Detailed Table", "💾 JSON Data"])
            
#             # Prepare Data
#             rows = []
#             for r in results:
#                 proj_str = " • ".join([f"{p.title} [{p.tech_stack}]" for p in r.projects])
#                 rows.append({
#                     "Name": r.contact.name,
#                     "Experience": r.years_experience,
#                     "Degree": r.education_degree,
#                     "Projects": proj_str,
#                     "Skills": ", ".join(r.skills[:5]) + "...",
#                     "Email": r.contact.email,
#                     "LinkedIn": r.contact.linkedin
#                 })
#             df = pd.DataFrame(rows)

#             with tab1:
#                 st.dataframe(
#                     df,
#                     column_config={
#                         "Name": st.column_config.TextColumn("Candidate", width="medium"),
#                         "Projects": st.column_config.TextColumn("Key Projects", width="large"),
#                         "LinkedIn": st.column_config.LinkColumn("Profile"),
#                         "Email": st.column_config.LinkColumn("Email"),
#                     },
#                     use_container_width=True,
#                     height=500
#                 )
            
#             with tab2:
#                 st.json([r.dict() for r in results])

#             # 3. EXPORT AREA
#             st.markdown("<br>", unsafe_allow_html=True)
#             csv = df.to_csv(index=False).encode('utf-8')
            
#             col_d1, col_d2, col_d3 = st.columns([1, 2, 1])
#             with col_d2:
#                 st.download_button(
#                     label="📥 DOWNLOAD INTELLIGENCE REPORT (CSV)",
#                     data=csv,
#                     file_name="Resume_Intelligence_Report.csv",
#                     mime="text/csv",
#                     use_container_width=True
#                 )




# import streamlit as st
# import pandas as pd
# import pdfplumber
# import io
# import json
# import os
# import time
# from dotenv import load_dotenv
# import google.generativeai as genai
# from pydantic import BaseModel, Field
# from typing import List, Optional

# # ==========================================
# # 1. ADVANCED PAGE CONFIG
# # ==========================================
# st.set_page_config(
#     page_title="Resume Intelligence A",    
#     page_icon="🧠",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# ==========================================
# 2. ADVANCED CSS (HIGH CONTRAST FIX)
# ==========================================
# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
#     /* GLOBAL TEXT COLOR FIX */
#     .stApp {
#         background: radial-gradient(circle at top left, #1e1e2f, #0a0a12);
#         color: #ffffff !important; /* Force white text everywhere */
#         font-family: 'Outfit', sans-serif;
#     }
    
#     p, h1, h2, h3, h4, h5, h6, span, div {
#         color: #e0e0e0;
#     }
    
#     /* HIDE DEFAULT STREAMLIT UI */
#     #MainMenu, footer, header {visibility: hidden;}
#     section[data-testid="stSidebar"] {display: none;}
    
#     /* HERO SECTION */
#     .hero-container {
#         text-align: center;
#         padding: 4rem 2rem;
#         background: rgba(30, 30, 46, 0.8);
#         border: 1px solid rgba(255, 255, 255, 0.1);
#         border-radius: 24px;
#         backdrop-filter: blur(15px);
#         margin-bottom: 3rem;
#         box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.4);
#     }
#     .hero-title {
#         font-size: 4rem;
#         font-weight: 800;
#         background: linear-gradient(90deg, #40d0ff, #0080ff);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         margin-bottom: 1rem;
#     }
#     .hero-subtitle {
#         font-size: 1.4rem;
#         color: #ffffff !important; /* Force white */
#         font-weight: 400;
#     }

#     /* UPLOAD ZONE - TEXT VISIBILITY FIX */
#     .stFileUploader {
#         background: rgba(255, 255, 255, 0.05);
#         border: 2px dashed #5b5b70;
#         border-radius: 20px;
#         padding: 2rem;
#         text-align: center;
#     }
#     .stFileUploader label {
#         color: #ffffff !important;
#         font-size: 1.1rem;
#     }
#     .stFileUploader div[data-testid="stMarkdownContainer"] p {
#         color: #cccccc !important; /* Small help text */
#     }

#     /* METRIC CARDS - LABEL VISIBILITY FIX */
#     div[data-testid="stMetric"] {
#         background: rgba(40, 40, 60, 0.8);
#         border: 1px solid rgba(255, 255, 255, 0.1);
#         border-radius: 16px;
#         padding: 20px;
#         box-shadow: 0 4px 10px rgba(0,0,0,0.3);
#     }
#     div[data-testid="stMetricLabel"] {
#         color: #b0b0ff !important; /* Light Blue for Labels */
#         font-size: 1rem;
#         font-weight: 600;
#     }
#     div[data-testid="stMetricValue"] {
#         color: #ffffff !important; /* Pure White for Numbers */
#         font-size: 1.8rem;
#         font-weight: 700;
#     }
    
#     /* GLOWING BUTTON */
#     div.stButton > button {
#         background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
#         color: white !important;
#         font-weight: 700;
#         padding: 1rem 3rem;
#         border-radius: 50px;
#         border: none;
#         box-shadow: 0 0 20px rgba(0, 114, 255, 0.6);
#         transition: all 0.3s ease;
#         text-transform: uppercase;
#         letter-spacing: 2px;
#     }
#     div.stButton > button:hover {
#         box-shadow: 0 0 35px rgba(0, 114, 255, 0.9);
#         transform: scale(1.03);
#     }

#     /* DATAFRAME & TABLE FIX */
#     div[data-testid="stDataFrame"] {
#         background: rgba(30, 30, 46, 0.6);
#         border-radius: 16px;
#         padding: 10px;
#     }
#     /* Force table header text to be white */
#     div[data-testid="stDataFrame"] th {
#         color: #ffffff !important;
#         background-color: #2a2a3e !important;
#     }
#     /* Force table body text to be white */
#     div[data-testid="stDataFrame"] td {
#         color: #e0e0e0 !important;
#     }

#     /* TABS */
#     .stTabs [data-baseweb="tab"] {
#         color: #a0a0b0;
#     }
#     .stTabs [aria-selected="true"] {
#         color: #ffffff !important;
#         background-color: rgba(64, 208, 255, 0.2);
#     }
# </style>
# """, unsafe_allow_html=True)



# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("gemini")

# # Data Models
# class ContactInfo(BaseModel):
#     name: Optional[str] = Field(None)
#     email: Optional[str] = Field(None)
#     phone: Optional[str] = Field(None)
#     linkedin: Optional[str] = Field(None)

# class Project(BaseModel):
#     title: str
#     tech_stack: Optional[str] = Field(None)

# class ResumeData(BaseModel):
#     contact: ContactInfo
#     skills: List[str] = Field(default_factory=list)
#     projects: List[Project] = Field(default_factory=list)
#     education_degree: Optional[str] = Field(None)
#     years_experience: Optional[str] = Field(None)

# def extract_text(file_bytes):
#     try:
#         with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
#             return "\n".join([p.extract_text() or "" for p in pdf.pages])
#     except: return ""

# def analyze_resume(text):
#     if not GOOGLE_API_KEY: return None
#     genai.configure(api_key=GOOGLE_API_KEY)
    
#     # --- MODEL SETTING: Using gemini-2.5-flash as requested ---
#     # Note: If this model is not yet available in your region, it may error.
#     # If it errors, fallback to 'gemini-1.5-flash'.
#     model = genai.GenerativeModel('gemini-2.5-flash')
    
#     prompt = f"""
#     Analyze resume. Return JSON.
#     Extract: Name, Email, Phone, LinkedIn, Latest Degree, Exp (Years), Top Skills, ALL Projects.
    
#     RESUME: {text[:8000]}
    
#     JSON SCHEMA:
#     {{
#         "contact": {{ "name": "...", "email": "...", "phone": "...", "linkedin": "..." }},
#         "education_degree": "...",
#         "years_experience": "...",
#         "skills": ["..."],
#         "projects": [ {{ "title": "...", "tech_stack": "..." }} ]
#     }}
#     """
#     try:
#         res = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
#         return ResumeData(**json.loads(res.text))
#     except: return None

# # ==========================================
# # 4. ADVANCED UI LAYOUT
# # ==========================================

# # --- HERO HEADER ---
# st.markdown("""
# <div class="hero-container">
#     <div class="hero-title">Resume Intelligence AI</div>
#     <div class="hero-subtitle">Upload Resumes • Extract Insights • Export Data</div>
# </div>
# """, unsafe_allow_html=True)

# # --- ERROR CHECK ---
# if not GOOGLE_API_KEY:
#     st.error("🔒 **System Locked:** API Key Missing. Please configure your `.env` file.")
#     st.stop()

# # --- MAIN INTERFACE ---
# col1, col2, col3 = st.columns([1, 3, 1])

# with col2:
#     uploaded_files = st.file_uploader("📂 Drag & Drop PDF Resumes", type=["pdf"], accept_multiple_files=True)

# # Only show the "Start" button if files are uploaded
# if uploaded_files:
#     st.markdown("<br>", unsafe_allow_html=True)
    
#     # Centered Button
#     c1, c2, c3 = st.columns([1, 1, 1])
#     with c2:
#         start_process = st.button("🚀 IGNITE ANALYSIS", use_container_width=True)

#     if start_process:
#         # --- PROCESSING UI ---
#         results = []
#         progress_bar = st.progress(0)
#         status_box = st.empty()
        
#         for i, file in enumerate(uploaded_files):
#             status_box.info(f"⚡ Analyzing: **{file.name}**")
#             text = extract_text(file.read())
#             if text:
#                 data = analyze_resume(text)
#                 if data: results.append(data)
            
#             progress_bar.progress((i + 1) / len(uploaded_files))
#             time.sleep(0.05) # UX Animation
            
#         progress_bar.empty()
#         status_box.empty()
        
#         # --- RESULTS DASHBOARD ---
#         if results:
#             st.markdown("---")
#             st.subheader("📊 Intelligence Report")
            
#             # 1. METRICS ROW
#             m1, m2, m3, m4 = st.columns(4)
#             m1.metric("Candidates", len(results))
#             m2.metric("Total Projects", sum(len(r.projects) for r in results))
            
#             # Simple logic for average experience
#             total_exp = 0
#             exp_count = 0
#             for r in results:
#                 if r.years_experience and r.years_experience.lower() != "fresher":
#                     try:
#                         import re
#                         match = re.search(r'\d+', r.years_experience)
#                         if match:
#                             total_exp += int(match.group())
#                             exp_count += 1
#                     except: pass
            
#             avg_exp_str = f"{round(total_exp / exp_count, 1)} Yrs" if exp_count > 0 else "N/A"
#             m3.metric("Avg. Experience", avg_exp_str)
#             m4.metric("Success Rate", "100%")

#             # 2. TABBED VIEW
#             tab1, tab2 = st.tabs(["📄 Detailed Table", "💾 JSON Data"])
            
#             # Prepare Data
#             rows = []
#             for r in results:
#                 proj_str = " • ".join([f"{p.title} [{p.tech_stack}]" for p in r.projects])
#                 rows.append({
#                     "Name": r.contact.name,
#                     "Experience": r.years_experience,
#                     "Degree": r.education_degree,
#                     "Projects": proj_str,
#                     "Skills": ", ".join(r.skills[:5]) + "...",
#                     "Email": r.contact.email,
#                     "LinkedIn": r.contact.linkedin
#                 })
#             df = pd.DataFrame(rows)

#             with tab1:
#                 st.dataframe(
#                     df,
#                     column_config={
#                         "Name": st.column_config.TextColumn("Candidate", width="medium"),
#                         "Projects": st.column_config.TextColumn("Key Projects", width="large"),
#                         "LinkedIn": st.column_config.LinkColumn("Profile"),
#                         "Email": st.column_config.LinkColumn("Email"),
#                     },
#                     use_container_width=True,
#                     height=500
#                 )
            
#             with tab2:
#                 st.json([r.dict() for r in results])

#             # 3. EXPORT AREA
#             st.markdown("<br>", unsafe_allow_html=True)
#             csv = df.to_csv(index=False).encode('utf-8')
            
#             col_d1, col_d2, col_d3 = st.columns([1, 2, 1])
#             with col_d2:
#                 st.download_button(
#                     label="📥 DOWNLOAD INTELLIGENCE REPORT (CSV)",
#                     data=csv,
#                     file_name="Resume_Intelligence_Report.csv",
#                     mime="text/csv",
#                     use_container_width=True
#                 )



# import streamlit as st
# import pandas as pd
# import pdfplumber
# import io
# import json
# import os
# import time
# from dotenv import load_dotenv
# import google.generativeai as genai
# from pydantic import BaseModel, Field
# from typing import List, Optional

# # ==========================================
# # 1. ADVANCED PAGE CONFIG
# # ==========================================
# st.set_page_config(
#     page_title="Resume Intelligence A",
#     page_icon="🧠",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # ==========================================
# # 2. ADVANCED CSS (DARK MODE VISIBILITY FIX)
# # ==========================================
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

# /* GLOBAL */
# .stApp {
#     background: radial-gradient(circle at top left, #1e1e2f, #0a0a12);
#     color: #ffffff !important;
#     font-family: 'Outfit', sans-serif;
# }

# p, h1, h2, h3, h4, h5, h6, span, div {
#     color: #e6e6e6;
# }

# /* HIDE STREAMLIT DEFAULT UI */
# #MainMenu, footer, header {visibility: hidden;}
# section[data-testid="stSidebar"] {display: none;}

# /* HERO */
# .hero-container {
#     text-align: center;
#     padding: 4rem 2rem;
#     background: rgba(30, 30, 46, 0.8);
#     border-radius: 24px;
#     margin-bottom: 3rem;
#     box-shadow: 0 10px 40px rgba(0,0,0,0.4);
# }

# .hero-title {
#     font-size: 4rem;
#     font-weight: 800;
#     background: linear-gradient(90deg, #40d0ff, #0080ff);
#     -webkit-background-clip: text;
#     -webkit-text-fill-color: transparent;
# }

# .hero-subtitle {
#     font-size: 1.4rem;
#     color: #ffffff !important;
# }

# /* FILE UPLOADER */
# .stFileUploader {
#     background: rgba(255,255,255,0.05);
#     border: 2px dashed #5b5b70;
#     border-radius: 20px;
#     padding: 2rem;
# }

# .stFileUploader label {
#     color: #ffffff !important;
#     font-size: 1.1rem;
# }

# .stFileUploader p {
#     color: #cccccc !important;
# }

# /* METRICS */
# div[data-testid="stMetric"] {
#     background: rgba(40,40,60,0.8);
#     border-radius: 16px;
#     padding: 20px;
# }

# div[data-testid="stMetricLabel"] {
#     color: #9fb8ff !important;
#     font-weight: 600;
# }

# div[data-testid="stMetricValue"] {
#     color: #ffffff !important;
#     font-weight: 700;
# }

# /* BUTTON */
# div.stButton > button {
#     background: linear-gradient(90deg, #00c6ff, #0072ff);
#     color: #ffffff !important;
#     font-weight: 700;
#     border-radius: 50px;
#     padding: 1rem 3rem;
#     border: none;
# }

# /* LINKS (EMAIL / LINKEDIN FIX) */
# a, a:visited {
#     color: #40d0ff !important;
#     font-weight: 500;
#     text-decoration: none;
# }

# a:hover {
#     color: #7fe7ff !important;
#     text-decoration: underline;
# }

# /* DATAFRAME */
# div[data-testid="stDataFrame"] {
#     background: rgba(30,30,46,0.6);
#     border-radius: 16px;
# }

# div[data-testid="stDataFrame"] th {
#     background: #2a2a3e !important;
#     color: #ffffff !important;
# }

# div[data-testid="stDataFrame"] td {
#     color: #e0e0e0 !important;
# }

# div[data-testid="stDataFrame"] a {
#     color: #40d0ff !important;
# }

# /* JSON VIEW */
# div[data-testid="stJson"] span {
#     color: #ffffff !important;
# }

# /* TABS */
# .stTabs [data-baseweb="tab"] {
#     color: #a0a0b0;
# }

# .stTabs [aria-selected="true"] {
#     color: #ffffff !important;
#     background-color: rgba(64,208,255,0.2);
# }
# </style>
# """, unsafe_allow_html=True)

# # ==========================================
# # 3. SETUP & LOGIC
# # ==========================================
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("gemini")

# class ContactInfo(BaseModel):
#     name: Optional[str]
#     email: Optional[str]
#     phone: Optional[str]
#     linkedin: Optional[str]

# class Project(BaseModel):
#     title: str
#     tech_stack: Optional[str]

# class ResumeData(BaseModel):
#     contact: ContactInfo
#     skills: List[str] = []
#     projects: List[Project] = []
#     education_degree: Optional[str]
#     years_experience: Optional[str]

# def extract_text(file_bytes):
#     try:
#         with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
#             return "\n".join([p.extract_text() or "" for p in pdf.pages])
#     except:
#         return ""

# def analyze_resume(text):
#     if not GOOGLE_API_KEY:
#         return None

#     genai.configure(api_key=GOOGLE_API_KEY)
#     model = genai.GenerativeModel("gemini-2.5-flash")

#     prompt = f"""
#     Analyze resume and return JSON.

#     Extract:
#     Name, Email, Phone, LinkedIn,
#     Latest Degree, Experience (Years),
#     Skills, Projects.

#     Resume:
#     {text[:8000]}
#     """

#     try:
#         res = model.generate_content(
#             prompt,
#             generation_config={"response_mime_type": "application/json"}
#         )
#         return ResumeData(**json.loads(res.text))
#     except:
#         return None

# # ==========================================
# # 4. UI
# # ==========================================
# st.markdown("""
# <div class="hero-container">
#     <div class="hero-title">Resume Intelligence AI</div>
#     <div class="hero-subtitle">Upload Resumes • Extract Insights • Export Data</div>
# </div>
# """, unsafe_allow_html=True)

# if not GOOGLE_API_KEY:
#     st.error("🔒 API Key Missing")
#     st.stop()

# col1, col2, col3 = st.columns([1,3,1])
# with col2:
#     uploaded_files = st.file_uploader(
#         "📂 Drag & Drop PDF Resumes",
#         type=["pdf"],
#         accept_multiple_files=True
#     )

# if uploaded_files:
#     st.markdown("<br>", unsafe_allow_html=True)
#     c1, c2, c3 = st.columns([1,1,1])
#     with c2:
#         start = st.button("🚀 IGNITE ANALYSIS", use_container_width=True)

#     if start:
#         results = []
#         progress = st.progress(0)
#         status = st.empty()

#         for i, file in enumerate(uploaded_files):
#             status.info(f"Analyzing **{file.name}**")
#             text = extract_text(file.read())
#             if text:
#                 data = analyze_resume(text)
#                 if data:
#                     results.append(data)

#             progress.progress((i+1)/len(uploaded_files))
#             time.sleep(0.05)

#         progress.empty()
#         status.empty()

#         if results:
#             st.subheader("📊 Intelligence Report")

#             m1, m2, m3, m4 = st.columns(4)
#             m1.metric("Candidates", len(results))
#             m2.metric("Total Projects", sum(len(r.projects) for r in results))
#             m3.metric("Avg Experience", "N/A")
#             m4.metric("Success Rate", "100%")

#             rows = []
#             for r in results:
#                 rows.append({
#                     "Name": r.contact.name,
#                     "Experience": r.years_experience,
#                     "Degree": r.education_degree,
#                     "Projects": " • ".join(p.title for p in r.projects),
#                     "Skills": ", ".join(r.skills[:5]),
#                     "Email": r.contact.email,
#                     "LinkedIn": r.contact.linkedin
#                 })

#             df = pd.DataFrame(rows)

#             tab1, tab2 = st.tabs(["📄 Table", "💾 JSON"])

#             with tab1:
#                 st.dataframe(df, use_container_width=True, height=500)

#             with tab2:
#                 st.json([r.dict() for r in results])

#             csv = df.to_csv(index=False).encode("utf-8")
#             st.download_button(
#                 "📥 DOWNLOAD REPORT",
#                 csv,
#                 "Resume_Report.csv",
#                 "text/csv",
#                 use_container_width=True
#             )


# import streamlit as st
# import pandas as pd
# import pdfplumber
# import io
# import json
# import os
# import time
# from dotenv import load_dotenv
# import google.generativeai as genai
# from pydantic import BaseModel, Field
# from typing import List, Optional

# # ==========================================
# # 1. PAGE CONFIGURATION
# # ==========================================
# st.set_page_config(
#     page_title="Resume Intelligence AI",
#     page_icon="🧠",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # ==========================================
# # 2. HIGH-CONTRAST CSS (FIXING VISIBILITY ISSUES)
# # ==========================================
# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
#     /* 1. FORCE DARK BACKGROUND & WHITE TEXT GLOBAL */
#     .stApp {
#         background: radial-gradient(circle at top left, #1e1e2f, #0a0a12);
#         font-family: 'Outfit', sans-serif;
#     }
    
#     /* Force all basic text to be white */
#     p, h1, h2, h3, h4, h5, h6, li, span {
#         color: #ffffff !important;
#     }
    
#     /* HIDE DEFAULT MENU */
#     #MainMenu, footer, header {visibility: hidden;}
#     section[data-testid="stSidebar"] {display: none;}
    
#     /* 2. HERO SECTION */
#     .hero-container {
#         text-align: center;
#         padding: 3rem 2rem;
#         background: rgba(30, 30, 46, 0.8);
#         border: 1px solid rgba(255, 255, 255, 0.1);
#         border-radius: 20px;
#         backdrop-filter: blur(10px);
#         margin-bottom: 2rem;
#         box-shadow: 0 10px 30px rgba(0,0,0,0.5);
#     }
#     .hero-title {
#         font-size: 3.5rem !important;
#         font-weight: 800 !important;
#         background: linear-gradient(90deg, #40d0ff, #0080ff);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent !important; /* Override white for gradient */
#         color: transparent !important;
#         margin-bottom: 0.5rem !important;
#     }
    
#     /* 3. FIX: FILE UPLOADER VISIBILITY */
#     .stFileUploader {
#         background: rgba(255, 255, 255, 0.05);
#         border: 2px dashed #5b5b70;
#         border-radius: 15px;
#         padding: 2rem;
#     }
#     /* This targets the "Drag and drop" text */
#     .stFileUploader div[data-testid="stMarkdownContainer"] p {
#         color: #ffffff !important;
#     }
#     /* This targets the uploaded filename (the invisible text you mentioned) */
#     div[data-testid="stFileUploader"] div[role="listitem"] div {
#         color: #ffffff !important; 
#         font-weight: 500;
#     }
#     .stFileUploader button {
#         color: #000000 !important; /* Button text needs to be black on white button */
#         background-color: #40d0ff !important;
#         border: none;
#     }

#     /* 4. FIX: METRIC CARDS VISIBILITY */
#     div[data-testid="stMetric"] {
#         background: rgba(40, 40, 60, 0.9);
#         border: 1px solid #40d0ff;
#         border-radius: 12px;
#         padding: 15px;
#         box-shadow: 0 4px 10px rgba(0,0,0,0.3);
#     }
#     div[data-testid="stMetricLabel"] {
#         color: #a0c0ff !important; /* Bright Blue Label */
#         font-size: 1rem !important;
#     }
#     div[data-testid="stMetricValue"] {
#         color: #ffffff !important; /* Pure White Value */
#         font-size: 2rem !important;
#     }
    
#     /* 5. FIX: TABLE VISIBILITY */
#     div[data-testid="stDataFrame"] {
#         background: rgba(30, 30, 46, 0.8);
#         border-radius: 10px;
#         padding: 10px;
#     }
#     /* Header background and text */
#     div[data-testid="stDataFrame"] th {
#         background-color: #2a2a3e !important;
#         color: #ffffff !important; 
#         font-size: 1rem !important;
#     }
#     /* Cell text */
#     div[data-testid="stDataFrame"] td {
#         color: #e0e0e0 !important;
#     }

#     /* BUTTON STYLING */
#     div.stButton > button {
#         background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
#         color: white !important;
#         font-weight: 700;
#         padding: 0.8rem 3rem;
#         border-radius: 50px;
#         border: none;
#         box-shadow: 0 0 15px rgba(0, 114, 255, 0.6);
#         font-size: 1.1rem;
#     }
# </style>
# """, unsafe_allow_html=True)

# # ==========================================
# # 3. SETUP & LOGIC
# # ==========================================
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("gemini")

# # --- DATA MODELS ---
# class ContactInfo(BaseModel):
#     name: Optional[str] = Field(None)
#     email: Optional[str] = Field(None)
#     phone: Optional[str] = Field(None)
#     linkedin: Optional[str] = Field(None)

# class Project(BaseModel):
#     title: str
#     tech_stack: Optional[str] = Field(None)

# class ResumeData(BaseModel):
#     contact: ContactInfo
#     skills: List[str] = Field(default_factory=list)
#     projects: List[Project] = Field(default_factory=list)
#     education_degree: Optional[str] = Field(None)
#     years_experience: Optional[str] = Field(None)

# # --- HELPER FUNCTIONS ---
# def extract_text(file_bytes):
#     try:
#         with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
#             return "\n".join([p.extract_text() or "" for p in pdf.pages])
#     except: return ""

# def analyze_resume(text):
#     if not GOOGLE_API_KEY: return None
#     genai.configure(api_key=GOOGLE_API_KEY)
    
#     # Using gemini-2.5-flash as requested
#     model = genai.GenerativeModel('gemini-2.5-flash')
    
#     prompt = f"""
#     Analyze resume. Return JSON.
#     Extract: Name, Email, Phone, LinkedIn, Latest Degree, Exp (Years), Top Skills, ALL Projects.
    
#     RESUME: {text[:8000]}
    
#     JSON SCHEMA:
#     {{
#         "contact": {{ "name": "...", "email": "...", "phone": "...", "linkedin": "..." }},
#         "education_degree": "...",
#         "years_experience": "...",
#         "skills": ["..."],
#         "projects": [ {{ "title": "...", "tech_stack": "..." }} ]
#     }}
#     """
#     try:
#         res = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
#         return ResumeData(**json.loads(res.text))
#     except: return None

# # ==========================================
# # 4. MAIN UI
# # ==========================================

# # HEADER
# st.markdown("""
# <div class="hero-container">
#     <div class="hero-title">Resume Intelligence AI</div>
#     <p style="font-size: 1.2rem; color: #e0e0e0;">Upload Resumes • Extract Insights • Export Data</p>
# </div>
# """, unsafe_allow_html=True)

# # API KEY CHECK
# if not GOOGLE_API_KEY:
#     st.error("🔒 API Key Missing. Please set GOOGLE_API_KEY in your .env file.")
#     st.stop()

# # UPLOAD SECTION
# col1, col2, col3 = st.columns([1, 6, 1])
# with col2:
#     uploaded_files = st.file_uploader("📂 Drag & Drop PDF Resumes Here", type=["pdf"], accept_multiple_files=True)

# if uploaded_files:
#     st.markdown("<br>", unsafe_allow_html=True)
#     c1, c2, c3 = st.columns([1, 1, 1])
#     with c2:
#         start_process = st.button("🚀 IGNITE ANALYSIS", use_container_width=True)

#     if start_process:
#         results = []
#         progress_bar = st.progress(0)
#         status_box = st.empty()
        
#         # PROCESSING LOOP
#         for i, file in enumerate(uploaded_files):
#             status_box.info(f"⚡ Analyzing: {file.name}")
#             text = extract_text(file.read())
#             if text:
#                 data = analyze_resume(text)
#                 if data: results.append(data)
            
#             progress_bar.progress((i + 1) / len(uploaded_files))
#             time.sleep(0.05)
            
#         progress_bar.empty()
#         status_box.empty()
        
#         if results:
#             st.markdown("---")
#             st.subheader("📊 Intelligence Report")
            
#             # 1. METRICS
#             m1, m2, m3, m4 = st.columns(4)
#             m1.metric("Candidates", len(results))
#             m2.metric("Total Projects", sum(len(r.projects) for r in results))
            
#             # Avg Exp Logic
#             total_exp = 0
#             count = 0
#             for r in results:
#                 if r.years_experience and any(char.isdigit() for char in r.years_experience):
#                     import re
#                     nums = re.findall(r'\d+', r.years_experience)
#                     if nums: 
#                         total_exp += int(nums[0])
#                         count += 1
#             avg_exp = f"{round(total_exp/count, 1)} Yrs" if count > 0 else "N/A"
#             m3.metric("Avg. Experience", avg_exp)
#             m4.metric("Success Rate", "100%")

#             # 2. DATA TABLE
#             tab1, tab2 = st.tabs(["📄 Detailed Table", "💾 JSON Data"])
            
#             # Prepare Data Rows
#             rows = []
#             for r in results:
#                 proj_str = " • ".join([f"{p.title} [{p.tech_stack}]" for p in r.projects])
#                 rows.append({
#                     "Name": r.contact.name,
#                     "Skills": ", ".join(r.skills), # Skills moved to 2nd position
#                     "Experience": r.years_experience,
#                     "Degree": r.education_degree,
#                     "Projects": proj_str,
#                     "Email": r.contact.email,
#                     "LinkedIn": r.contact.linkedin
#                 })
            
#             # Create DF and Force Column Order
#             df = pd.DataFrame(rows)
#             # Reorder columns explicitly: Name first, then Skills, then rest
#             column_order = ["Name", "Skills", "Experience", "Degree", "Projects", "Email", "LinkedIn"]
#             # Ensure columns exist before reordering (safety check)
#             final_cols = [c for c in column_order if c in df.columns]
#             df = df[final_cols]

#             with tab1:
#                 st.dataframe(
#                     df,
#                     column_config={
#                         "Name": st.column_config.TextColumn("Candidate Name", width="medium"),
#                         "Skills": st.column_config.TextColumn("Top Skills", width="large"),
#                         "Projects": st.column_config.TextColumn("Key Projects", width="large"),
#                         "LinkedIn": st.column_config.LinkColumn("Profile"),
#                     },
#                     use_container_width=True,
#                     height=500
#                 )
            
#             with tab2:
#                 st.json([r.dict() for r in results])

#             # 3. DOWNLOAD
#             st.markdown("<br>", unsafe_allow_html=True)
#             csv = df.to_csv(index=False).encode('utf-8')
#             col_d1, col_d2, col_d3 = st.columns([1, 2, 1])
#             with col_d2:
#                 st.download_button(
#                     label="📥 DOWNLOAD REPORT (CSV)",
#                     data=csv,
#                     file_name="Resume_Report.csv",
#                     mime="text/csv",
#                     use_container_width=True
#                 )






# import streamlit as st
# import pandas as pd
# import pdfplumber
# import io
# import json
# import os
# import time
# from dotenv import load_dotenv
# import google.generativeai as genai
# from pydantic import BaseModel, Field
# from typing import List, Optional

# # ==========================================
# # 1. PAGE CONFIGURATION
# # ==========================================
# st.set_page_config(
#     page_title="Resume Intelligence AI",
#     page_icon="🧠",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # ==========================================
# # 2. CSS FIXES (VISIBILITY & HOVER)
# # ==========================================
# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
#     /* 1. GLOBAL DARK THEME & TEXT */
#     .stApp {
#         background: radial-gradient(circle at top left, #1e1e2f, #0a0a12);
#         font-family: 'Outfit', sans-serif;
#         color: #ffffff;
#     }
    
#     /* Force standard text to be white */
#     p, h1, h2, h3, h4, h5, h6, li, span, div {
#         color: #ffffff;
#     }

#     /* HIDE DEFAULT MENU */
#     #MainMenu, footer, header {visibility: hidden;}
#     section[data-testid="stSidebar"] {display: none;}
    
#     /* 2. HERO SECTION */
#     .hero-container {
#         text-align: center;
#         padding: 3rem 2rem;
#         background: rgba(30, 30, 46, 0.8);
#         border: 1px solid rgba(255, 255, 255, 0.1);
#         border-radius: 20px;
#         backdrop-filter: blur(10px);
#         margin-bottom: 2rem;
#         box-shadow: 0 10px 30px rgba(0,0,0,0.5);
#     }
#     .hero-title {
#         font-size: 3.5rem !important;
#         font-weight: 800 !important;
#         background: linear-gradient(90deg, #40d0ff, #0080ff);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent !important; 
#         margin-bottom: 0.5rem !important;
#     }
    
#     /* 3. UPLOAD BOX FIXES (CRITICAL) */
    
#     /* The Box Container */
#     .stFileUploader {
#         background: rgba(255, 255, 255, 0.05);
#         border: 2px dashed #5b5b70;
#         border-radius: 15px;
#         padding: 2rem;
#     }
    
#     /* Fix 1: Make Filenames White (The invisible text issue) */
#     div[data-testid="stFileUploader"] div[role="listitem"] div {
#         color: #ffffff !important;
#         font-weight: 600 !important;
#         background-color: transparent !important;
#     }
    
#     /* Fix 2: Small "Limit 200MB" text */
#     div[data-testid="stFileUploader"] small {
#         color: #a0a0a0 !important;
#     }

#     /* Fix 3: Prevent "White Out" on Hover */
#     div[data-testid="stFileUploader"]:hover {
#         background-color: rgba(255, 255, 255, 0.10) !important; /* Slight lighten only */
#     }
    
#     /* Browse Button */
#     .stFileUploader button {
#         background-color: #40d0ff !important;
#         color: #255255255 !important; /* Black text on Blue button */
#         border: none;
#         font-weight: 700;
#     }
    
#     /* Uploaded File Status Icon */
#     div[data-testid="stFileUploader"] svg {
#         fill: #40d0ff !important;
#     }

#     /* 4. METRIC CARDS */
#     div[data-testid="stMetric"] {
#         background: rgba(40, 40, 60, 0.9);
#         border: 1px solid #40d0ff;
#         border-radius: 12px;
#         padding: 15px;
#     }
#     div[data-testid="stMetricLabel"] {
#         color: #a0c0ff !important; 
#         font-size: 1rem !important;
#     }
#     div[data-testid="stMetricValue"] {
#         color: #ffffff !important; 
#         font-size: 2rem !important;
#     }
    
#     /* 5. TABLE VISIBILITY */
#     div[data-testid="stDataFrame"] {
#         background: rgba(30, 30, 46, 0.8);
#         border-radius: 10px;
#         padding: 10px;
#     }
#     div[data-testid="stDataFrame"] th {
#         background-color: #2a2a3e !important;
#         color: #ffffff !important; 
#     }
#     div[data-testid="stDataFrame"] td {
#         color: #e0e0e0 !important;
#     }

#     /* BUTTON STYLING */
#     div.stButton > button {
#         background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
#         color: white !important;
#         font-weight: 700;
#         padding: 0.8rem 3rem;
#         border-radius: 50px;
#         border: none;
#         box-shadow: 0 0 15px rgba(0, 114, 255, 0.6);
#         font-size: 1.1rem;
#     }
# </style>
# """, unsafe_allow_html=True)

# # ==========================================
# # 3. SETUP & LOGIC
# # ==========================================
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("gemini")

# # --- DATA MODELS (Updated for Internships & Certs) ---
# class ContactInfo(BaseModel):
#     name: Optional[str] = Field(None)
#     email: Optional[str] = Field(None)
#     phone: Optional[str] = Field(None)
#     linkedin: Optional[str] = Field(None)

# class Project(BaseModel):
#     title: str
#     tech_stack: Optional[str] = Field(None)

# class ResumeData(BaseModel):
#     contact: ContactInfo
#     skills: List[str] = Field(default_factory=list)
#     internships: List[str] = Field(default_factory=list, description="List of internship roles/companies")
#     projects: List[Project] = Field(default_factory=list)
#     certifications: List[str] = Field(default_factory=list, description="List of certifications")
#     years_experience: Optional[str] = Field(None)

# # --- HELPER FUNCTIONS ---
# def extract_text(file_bytes):
#     try:
#         with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
#             return "\n".join([p.extract_text() or "" for p in pdf.pages])
#     except: return ""

# def analyze_resume(text):
#     if not GOOGLE_API_KEY: return None
#     genai.configure(api_key=GOOGLE_API_KEY)
    
#     model = genai.GenerativeModel('gemini-2.5-flash')
    
#     # UPDATED PROMPT: Extract Internships & Certifications explicitly
#     prompt = f"""
#     Analyze the resume text below and extract data into strict JSON.
    
#     REQUIREMENTS:
#     1. Extract Contact (Name, Email, Phone).
#     2. Extract ALL Technical Skills.
#     3. Extract INTERNSHIPS (Role at Company).
#     4. Extract ALL Projects (Title + Tech Stack).
#     5. Extract CERTIFICATIONS (Name).
#     6. Years of Experience (number or "Fresher").
    
#     RESUME TEXT:
#     {text[:10000]}
    
#     JSON SCHEMA:
#     {{
#         "contact": {{ "name": "...", "email": "...", "phone": "..." }},
#         "skills": ["Python", "SQL", ...],
#         "internships": ["Data Science Intern at Innomatics", ...],
#         "projects": [ {{ "title": "...", "tech_stack": "..." }} ],
#         "certifications": ["AWS Certified", "NPTEL Python", ...],
#         "years_experience": "..."
#     }}
#     """
#     try:
#         res = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
#         return ResumeData(**json.loads(res.text))
#     except: return None

# # ==========================================
# # 4. MAIN UI
# # ==========================================

# # HEADER
# st.markdown("""
# <div class="hero-container">
#     <div class="hero-title">Resume Intelligence AI</div>
#     <p style="font-size: 1.2rem; color: #e0e0e0;">Upload Resumes • Extract Insights • Export Data</p>
# </div>
# """, unsafe_allow_html=True)

# # API KEY CHECK
# if not GOOGLE_API_KEY:
#     st.error("🔒 API Key Missing. Please set GOOGLE_API_KEY in your .env file.")
#     st.stop()

# # UPLOAD SECTION
# col1, col2, col3 = st.columns([1, 6, 1])
# with col2:
#     uploaded_files = st.file_uploader("📂 Drag & Drop PDF Resumes Here", type=["pdf"], accept_multiple_files=True)

# if uploaded_files:
#     st.markdown("<br>", unsafe_allow_html=True)
#     c1, c2, c3 = st.columns([1, 1, 1])
#     with c2:
#         start_process = st.button("🚀 IGNITE ANALYSIS", use_container_width=True)

#     if start_process:
#         results = []
#         progress_bar = st.progress(0)
#         status_box = st.empty()
        
#         # PROCESSING LOOP
#         for i, file in enumerate(uploaded_files):
#             status_box.info(f"⚡ Analyzing: {file.name}")
#             text = extract_text(file.read())
#             if text:
#                 data = analyze_resume(text)
#                 if data: results.append(data)
            
#             progress_bar.progress((i + 1) / len(uploaded_files))
#             time.sleep(0.05)
            
#         progress_bar.empty()
#         status_box.empty()
        
#         if results:
#             st.markdown("---")
#             st.subheader("📊 Intelligence Report")
            
#             # 1. METRICS
#             m1, m2, m3, m4 = st.columns(4)
#             m1.metric("Candidates", len(results))
#             m2.metric("Total Projects", sum(len(r.projects) for r in results))
#             m3.metric("Total Internships", sum(len(r.internships) for r in results))
#             m4.metric("Success Rate", "100%")

#             # 2. DATA TABLE PREP
#             tab1, tab2 = st.tabs(["📄 Detailed Table", "💾 JSON Data"])
            
#             # Prepare Data Rows
#             rows = []
#             for r in results:
#                 # Formatting lists to string for table
#                 proj_str = " • ".join([f"{p.title} ({p.tech_stack})" for p in r.projects])
#                 intern_str = " • ".join(r.internships)
#                 cert_str = " • ".join(r.certifications)
#                 skills_str = ", ".join(r.skills)
                
#                 rows.append({
#                     "Name": r.contact.name,
#                     "Phone": r.contact.phone,
#                     "Email": r.contact.email,
#                     "Technical Skills": skills_str,
#                     "Internship": intern_str,
#                     "Projects": proj_str,
#                     "Certificate": cert_str
#                 })
            
#             # Create DF and Force EXACT User Requested Order
#             df = pd.DataFrame(rows)
#             target_order = ["Name", "Phone", "Email", "Technical Skills", "Internship", "Projects", "Certificate"]
            
#             # Ensure columns exist (handle empty data)
#             for col in target_order:
#                 if col not in df.columns:
#                     df[col] = "" # Fill missing columns with empty string
            
#             df = df[target_order] # Reorder

#             with tab1:
#                 st.dataframe(
#                     df,
#                     column_config={
#                         "Name": st.column_config.TextColumn("Candidate Name", width="medium"),
#                         "Technical Skills": st.column_config.TextColumn("Skills", width="large"),
#                         "Projects": st.column_config.TextColumn("Projects", width="large"),
#                         "Internship": st.column_config.TextColumn("Internships", width="medium"),
#                     },
#                     use_container_width=True,
#                     height=500
#                 )
            
#             with tab2:
#                 st.json([r.dict() for r in results])

#             # 3. DOWNLOAD
#             st.markdown("<br>", unsafe_allow_html=True)
#             csv = df.to_csv(index=False).encode('utf-8')
#             col_d1, col_d2, col_d3 = st.columns([1, 2, 1])
#             with col_d2:
#                 st.download_button(
#                     label="📥 DOWNLOAD REPORT (CSV)",
#                     data=csv,
#                     file_name="Resume_Report.csv",
#                     mime="text/csv",
#                     use_container_width=True
#                 )


# import streamlit as st
# import pandas as pd
# import pdfplumber
# import io
# import json
# import os
# import time
# from dotenv import load_dotenv
# import google.generativeai as genai
# from pydantic import BaseModel, Field
# from typing import List, Optional

# # ==========================================
# # 1. PAGE CONFIGURATION
# # ==========================================
# st.set_page_config(
#     page_title="Resume Intelligence AI",
#     page_icon="🧠",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # ==========================================
# # 2. FINAL CSS FIXES
# # ==========================================
# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
#     /* 1. GLOBAL DARK THEME & TEXT */
#     .stApp {
#         background: radial-gradient(circle at top left, #1e1e2f, #0a0a12);
#         font-family: 'Outfit', sans-serif;
#         color: #ffffff;
#     }
    
#     /* Force standard text to be white */
#     p, h1, h2, h3, h4, h5, h6, li, span, div {
#         color: #ffffff;
#     }

#     /* HIDE DEFAULT MENU */
#     #MainMenu, footer, header {visibility: hidden;}
#     section[data-testid="stSidebar"] {display: none;}
    
#     /* 2. UPLOAD BOX (FIXED FILENAME VISIBILITY) */
#     .stFileUploader {
#         background: rgba(0, 0, 0, 0.05);
#         border: 2px dashed #5b5b70;
#         border-radius: 15px;
#         padding: 2rem;
#     }
#     /* Force ALL text inside the uploader to be white */
#     .stFileUploader * {
#         color: #ffffff !important;
#     }
#     /* Except the small "Limit 200MB" text - make it light gray */
#     .stFileUploader small {
#         color: #a0a0a0 !important;
#     }
#     /* Browse Button */
#     .stFileUploader button {
#         background-color: #40d0ff !important;
#         color: #000000 !important; /* Black text on Blue button */
#         border: none;
#         font-weight: 700;
#     }
#     /* Upload Icon */
#     div[data-testid="stFileUploader"] svg {
#         fill: #40d0ff !important;
#     }

#     /* 3. DOWNLOAD BUTTON (FIXED BACKGROUND) */
#     div.stDownloadButton > button {
#         background-color: transparent !important; /* No Color / Normal */
#         color: #40d0ff !important; /* Blue Text */
#         border: 1px solid #40d0ff !important; /* Blue Border */
#         border-radius: 50px;
#         padding: 0.5rem 2rem;
#         font-weight: 600;
#         transition: all 0.3s ease;
#     }
#     div.stDownloadButton > button:hover {
#         background-color: rgba(64, 208, 255, 0.1) !important;
#         box-shadow: 0 0 10px rgba(64, 208, 255, 0.3);
#     }

#     /* 4. HERO SECTION */
#     .hero-container {
#         text-align: center;
#         padding: 3rem 2rem;
#         background: rgba(30, 30, 46, 0.8);
#         border: 1px solid rgba(255, 255, 255, 0.1);
#         border-radius: 20px;
#         backdrop-filter: blur(10px);
#         margin-bottom: 2rem;
#         box-shadow: 0 10px 30px rgba(0,0,0,0.5);
#     }
#     .hero-title {
#         font-size: 3.5rem !important;
#         font-weight: 800 !important;
#         background: linear-gradient(90deg, #40d0ff, #0080ff);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent !important; 
#         margin-bottom: 0.5rem !important;
#     }

#     /* 5. METRIC CARDS */
#     div[data-testid="stMetric"] {
#         background: rgba(40, 40, 60, 0.9);
#         border: 1px solid #40d0ff;
#         border-radius: 12px;
#         padding: 15px;
#     }
#     div[data-testid="stMetricLabel"] {
#         color: #a0c0ff !important; 
#         font-size: 1rem !important;
#     }
#     div[data-testid="stMetricValue"] {
#         color: #ffffff !important; 
#         font-size: 2rem !important;
#     }
    
#     /* 6. TABLE VISIBILITY */
#     div[data-testid="stDataFrame"] {
#         background: rgba(30, 30, 46, 0.8);
#         border-radius: 10px;
#         padding: 10px;
#     }
#     div[data-testid="stDataFrame"] th {
#         background-color: #2a2a3e !important;
#         color: #ffffff !important; 
#     }
#     div[data-testid="stDataFrame"] td {
#         color: #e0e0e0 !important;
#     }

#     /* PRIMARY BUTTON (IGNITE ANALYSIS) */
#     div.stButton > button {
#         background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
#         color: white !important;
#         font-weight: 700;
#         padding: 0.8rem 3rem;
#         border-radius: 50px;
#         border: none;
#         box-shadow: 0 0 15px rgba(0, 114, 255, 0.6);
#         font-size: 1.1rem;
#     }
# </style>
# """, unsafe_allow_html=True)

# # ==========================================
# # 3. SETUP & LOGIC
# # ==========================================
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("gemini")

# # --- DATA MODELS ---
# class ContactInfo(BaseModel):
#     name: Optional[str] = Field(None)
#     email: Optional[str] = Field(None)
#     phone: Optional[str] = Field(None)
#     linkedin: Optional[str] = Field(None)

# class Project(BaseModel):
#     title: str
#     tech_stack: Optional[str] = Field(None)

# class ResumeData(BaseModel):
#     contact: ContactInfo
#     skills: List[str] = Field(default_factory=list)
#     internships: List[str] = Field(default_factory=list, description="List of internship roles/companies")
#     projects: List[Project] = Field(default_factory=list)
#     certifications: List[str] = Field(default_factory=list, description="List of certifications")
#     years_experience: Optional[str] = Field(None)

# # --- HELPER FUNCTIONS ---
# def extract_text(file_bytes):
#     try:
#         with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
#             return "\n".join([p.extract_text() or "" for p in pdf.pages])
#     except: return ""

# def analyze_resume(text):
#     if not GOOGLE_API_KEY: return None
#     genai.configure(api_key=GOOGLE_API_KEY)
    
#     model = genai.GenerativeModel('gemini-2.5-flash')
    
#     prompt = f"""
#     Analyze the resume text below and extract data into strict JSON.
    
#     REQUIREMENTS:
#     1. Extract Contact (Name, Email, Phone).
#     2. Extract ALL Technical Skills.
#     3. Extract INTERNSHIPS (Role at Company).
#     4. Extract ALL Projects (Title + Tech Stack).
#     5. Extract CERTIFICATIONS (Name).
#     6. Years of Experience (number or "Fresher").
    
#     RESUME TEXT:
#     {text[:10000]}
    
#     JSON SCHEMA:
#     {{
#         "contact": {{ "name": "...", "email": "...", "phone": "..." }},
#         "skills": ["Python", "SQL", ...],
#         "internships": ["Data Science Intern at Innomatics", ...],
#         "projects": [ {{ "title": "...", "tech_stack": "..." }} ],
#         "certifications": ["AWS Certified", "NPTEL Python", ...],
#         "years_experience": "..."
#     }}
#     """
#     try:
#         res = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
#         return ResumeData(**json.loads(res.text))
#     except: return None

# # ==========================================
# # 4. MAIN UI
# # ==========================================

# # HEADER
# st.markdown("""
# <div class="hero-container">
#     <div class="hero-title">Resume Intelligence AI</div>
#     <p style="font-size: 1.2rem; color: #e0e0e0;">Upload Resumes • Extract Insights • Export Data</p>
# </div>
# """, unsafe_allow_html=True)

# # API KEY CHECK
# if not GOOGLE_API_KEY:
#     st.error("🔒 API Key Missing. Please set GOOGLE_API_KEY in your .env file.")
#     st.stop()

# # UPLOAD SECTION
# col1, col2, col3 = st.columns([1, 6, 1])
# with col2:
#     uploaded_files = st.file_uploader("📂 Drag & Drop PDF Resumes Here", type=["pdf"], accept_multiple_files=True)

# if uploaded_files:
#     st.markdown("<br>", unsafe_allow_html=True)
#     c1, c2, c3 = st.columns([1, 1, 1])
#     with c2:
#         start_process = st.button("🚀 IGNITE ANALYSIS", use_container_width=True)

#     if start_process:
#         results = []
#         progress_bar = st.progress(0)
#         status_box = st.empty()
        
#         # PROCESSING LOOP
#         for i, file in enumerate(uploaded_files):
#             status_box.info(f"⚡ Analyzing: {file.name}")
#             text = extract_text(file.read())
#             if text:
#                 data = analyze_resume(text)
#                 if data: results.append(data)
            
#             progress_bar.progress((i + 1) / len(uploaded_files))
#             time.sleep(0.05)
            
#         progress_bar.empty()
#         status_box.empty()
        
#         if results:
#             st.markdown("---")
#             st.subheader("📊 Intelligence Report")
            
#             # 1. METRICS
#             m1, m2, m3, m4 = st.columns(4)
#             m1.metric("Candidates", len(results))
#             m2.metric("Total Projects", sum(len(r.projects) for r in results))
#             m3.metric("Total Internships", sum(len(r.internships) for r in results))
#             m4.metric("Success Rate", "100%")

#             # 2. DATA TABLE PREP
#             tab1, tab2 = st.tabs(["📄 Detailed Table", "💾 JSON Data"])
            
#             # Prepare Data Rows
#             rows = []
#             for r in results:
#                 proj_str = " • ".join([f"{p.title} ({p.tech_stack})" for p in r.projects])
#                 intern_str = " • ".join(r.internships)
#                 cert_str = " • ".join(r.certifications)
#                 skills_str = ", ".join(r.skills)
                
#                 rows.append({
#                     "Name": r.contact.name,
#                     "Phone": r.contact.phone,
#                     "Email": r.contact.email,
#                     "Technical Skills": skills_str,
#                     "Internship": intern_str,
#                     "Projects": proj_str,
#                     "Certificate": cert_str
#                 })
            
#             # Create DF and Force EXACT User Requested Order
#             df = pd.DataFrame(rows)
#             target_order = ["Name", "Phone", "Email", "Technical Skills", "Internship", "Projects", "Certificate"]
            
#             # Ensure columns exist (handle empty data)
#             for col in target_order:
#                 if col not in df.columns:
#                     df[col] = "" 
            
#             df = df[target_order] # Reorder

#             with tab1:
#                 st.dataframe(
#                     df,
#                     column_config={
#                         "Name": st.column_config.TextColumn("Candidate Name", width="medium"),
#                         "Technical Skills": st.column_config.TextColumn("Skills", width="large"),
#                         "Projects": st.column_config.TextColumn("Projects", width="large"),
#                         "Internship": st.column_config.TextColumn("Internships", width="medium"),
#                     },
#                     use_container_width=True,
#                     height=500
#                 )
            
#             with tab2:
#                 st.json([r.dict() for r in results])

#             # 3. DOWNLOAD
#             st.markdown("<br>", unsafe_allow_html=True)
#             csv = df.to_csv(index=False).encode('utf-8')
#             col_d1, col_d2, col_d3 = st.columns([1, 2, 1])
#             with col_d2:
#                 st.download_button(
#                     label="📥 DOWNLOAD REPORT (CSV)",
#                     data=csv,
#                     file_name="Resume_Report.csv",
#                     mime="text/csv",
#                     use_container_width=True
#                 )





# import streamlit as st
# import pandas as pd
# import pdfplumber
# import io
# import json
# import os
# import time
# from dotenv import load_dotenv
# import google.generativeai as genai
# from pydantic import BaseModel, Field
# from typing import List, Optional

# # ==========================================
# # 1. PAGE CONFIGURATION
# # ==========================================
# st.set_page_config(
#     page_title="Resume Intelligence AI",
#     page_icon="🧠",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # ==========================================
# # 2. CSS STYLING (FIXED FILE NAMES)
# # ==========================================
# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
#     /* 1. GLOBAL DARK THEME */
#     .stApp {
#         background: radial-gradient(circle at top left, #1e1e2f, #0a0a12);
#         font-family: 'Outfit', sans-serif;
#         color: #ffffff;
#     }
    
#     /* Force standard text to be white */
#     p, h1, h2, h3, h4, h5, h6, li, span, div {
#         color: #ffffff;
#     }

#     /* HIDE DEFAULT MENU */
#     #MainMenu, footer, header {visibility: hidden;}
#     section[data-testid="stSidebar"] {display: none;}
    
#     /* 2. UPLOAD BOX & FILE NAME FIX */
#     .stFileUploader {
#         background: rgba(255, 255, 255, 0.05);
#         border: 2px dashed #5b5b70;
#         border-radius: 15px;
#         padding: 2rem;
#     }
    
#     /* CRITICAL FIX: Make the uploaded filename WHITE */
#     div[data-testid="stFileUploader"] div[role="listitem"] div {
#         color: #ffffff !important;
#         background-color: transparent !important;
#         font-weight: 600 !important;
#     }
#     /* Ensure the text inside the list item is white */
#     div[data-testid="stFileUploader"] div[role="listitem"] * {
#         color: #ffffff !important;
#     }

#     /* Small 'Limit 200MB' text */
#     .stFileUploader small {
#         color: #a0a0a0 !important;
#     }
    
#     /* Browse Button */
#     .stFileUploader button {
#         background-color: #40d0ff !important;
#         color: #000000 !important;
#         border: none;
#         font-weight: 700;
#     }
#     /* Upload Icon */
#     div[data-testid="stFileUploader"] svg {
#         fill: #40d0ff !important;
#     }

#     /* 3. DOWNLOAD BUTTON */
#     div.stDownloadButton > button {
#         background-color: transparent !important;
#         color: #40d0ff !important;
#         border: 1px solid #40d0ff !important;
#         border-radius: 50px;
#         padding: 0.5rem 2rem;
#         font-weight: 600;
#         transition: all 0.3s ease;
#     }
#     div.stDownloadButton > button:hover {
#         background-color: rgba(64, 208, 255, 0.1) !important;
#         box-shadow: 0 0 10px rgba(64, 208, 255, 0.3);
#     }

#     /* 4. HERO SECTION */
#     .hero-container {
#         text-align: center;
#         padding: 3rem 2rem;
#         background: rgba(30, 30, 46, 0.8);
#         border: 1px solid rgba(255, 255, 255, 0.1);
#         border-radius: 20px;
#         backdrop-filter: blur(10px);
#         margin-bottom: 2rem;
#         box-shadow: 0 10px 30px rgba(0,0,0,0.5);
#     }
#     .hero-title {
#         font-size: 3.5rem !important;
#         font-weight: 800 !important;
#         background: linear-gradient(90deg, #40d0ff, #0080ff);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent !important; 
#         margin-bottom: 0.5rem !important;
#     }

#     /* 5. METRIC CARDS */
#     div[data-testid="stMetric"] {
#         background: rgba(40, 40, 60, 0.9);
#         border: 1px solid #40d0ff;
#         border-radius: 12px;
#         padding: 15px;
#     }
#     div[data-testid="stMetricLabel"] {
#         color: #a0c0ff !important; 
#         font-size: 1rem !important;
#     }
#     div[data-testid="stMetricValue"] {
#         color: #ffffff !important; 
#         font-size: 2rem !important;
#     }
    
#     /* 6. TABLE VISIBILITY */
#     div[data-testid="stDataFrame"] {
#         background: rgba(30, 30, 46, 0.8);
#         border-radius: 10px;
#         padding: 10px;
#     }
#     div[data-testid="stDataFrame"] th {
#         background-color: #2a2a3e !important;
#         color: #ffffff !important; 
#     }
#     div[data-testid="stDataFrame"] td {
#         color: #e0e0e0 !important;
#     }

#     /* PRIMARY BUTTON */
#     div.stButton > button {
#         background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
#         color: white !important;
#         font-weight: 700;
#         padding: 0.8rem 3rem;
#         border-radius: 50px;
#         border: none;
#         box-shadow: 0 0 15px rgba(0, 114, 255, 0.6);
#         font-size: 1.1rem;
#     }
# </style>
# """, unsafe_allow_html=True)

# # ==========================================
# # 3. SETUP & LOGIC
# # ==========================================
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("gemini")

# class ContactInfo(BaseModel):
#     name: Optional[str] = Field(None)
#     email: Optional[str] = Field(None)
#     phone: Optional[str] = Field(None)
#     linkedin: Optional[str] = Field(None)

# class Project(BaseModel):
#     title: str
#     tech_stack: Optional[str] = Field(None)

# class ResumeData(BaseModel):
#     contact: ContactInfo
#     skills: List[str] = Field(default_factory=list)
#     internships: List[str] = Field(default_factory=list)
#     projects: List[Project] = Field(default_factory=list)
#     certifications: List[str] = Field(default_factory=list)
#     years_experience: Optional[str] = Field(None)

# def extract_text(file_bytes):
#     try:
#         with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
#             return "\n".join([p.extract_text() or "" for p in pdf.pages])
#     except: return ""

# def analyze_resume(text):
#     if not GOOGLE_API_KEY: return None
#     genai.configure(api_key=GOOGLE_API_KEY)
    
#     model = genai.GenerativeModel('gemini-2.5-flash')
    
#     prompt = f"""
#     Analyze the resume text below and extract data into strict JSON.
#     REQUIREMENTS:
#     1. Extract Contact (Name, Email, Phone).
#     2. Extract ALL Technical Skills.
#     3. Extract INTERNSHIPS (Role at Company).
#     4. Extract ALL Projects (Title + Tech Stack).
#     5. Extract CERTIFICATIONS (Name).
#     6. Years of Experience (number or "Fresher").
    
#     RESUME TEXT:
#     {text[:10000]}
    
#     JSON SCHEMA:
#     {{
#         "contact": {{ "name": "...", "email": "...", "phone": "..." }},
#         "skills": ["Python", "SQL", ...],
#         "internships": ["Data Science Intern at Innomatics", ...],
#         "projects": [ {{ "title": "...", "tech_stack": "..." }} ],
#         "certifications": ["AWS Certified", "NPTEL Python", ...],
#         "years_experience": "..."
#     }}
#     """
#     try:
#         res = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
#         return ResumeData(**json.loads(res.text))
#     except: return None

# # ==========================================
# # 4. MAIN UI
# # ==========================================

# # HEADER
# st.markdown("""
# <div class="hero-container">
#     <div class="hero-title">Resume Intelligence AI</div>
#     <p style="font-size: 1.2rem; color: #e0e0e0;">Upload Resumes • Extract Insights • Export Data</p>
# </div>
# """, unsafe_allow_html=True)

# # API KEY CHECK
# if not GOOGLE_API_KEY:
#     st.error("🔒 API Key Missing. Please set GOOGLE_API_KEY in your .env file.")
#     st.stop()

# # UPLOAD SECTION
# col1, col2, col3 = st.columns([1, 6, 1])
# with col2:
#     uploaded_files = st.file_uploader("📂 Drag & Drop PDF Resumes Here", type=["pdf"], accept_multiple_files=True)

# if uploaded_files:
#     st.markdown("<br>", unsafe_allow_html=True)
#     c1, c2, c3 = st.columns([1, 1, 1])
#     with c2:
#         start_process = st.button("🚀 IGNITE ANALYSIS", use_container_width=True)

#     if start_process:
#         results = []
#         progress_bar = st.progress(0)
#         status_box = st.empty()
        
#         # PROCESSING LOOP
#         for i, file in enumerate(uploaded_files):
#             status_box.info(f"⚡ Analyzing: {file.name}")
#             text = extract_text(file.read())
#             if text:
#                 data = analyze_resume(text)
#                 if data: results.append(data)
            
#             progress_bar.progress((i + 1) / len(uploaded_files))
#             time.sleep(0.05)
            
#         progress_bar.empty()
#         status_box.empty()
        
#         if results:
#             st.markdown("---")
#             st.subheader("📊 Intelligence Report")
            
#             # 1. METRICS (REMOVED SUCCESS RATE)
#             m1, m2, m3 = st.columns(3)
#             m1.metric("Candidates", len(results))
#             m2.metric("Total Projects", sum(len(r.projects) for r in results))
#             m3.metric("Total Internships", sum(len(r.internships) for r in results))

#             # 2. DATA TABLE PREP
#             tab1, tab2 = st.tabs(["📄 Detailed Table", "💾 JSON Data"])
            
#             rows = []
#             for r in results:
#                 proj_str = " • ".join([f"{p.title} ({p.tech_stack})" for p in r.projects])
#                 intern_str = " • ".join(r.internships)
#                 cert_str = " • ".join(r.certifications)
#                 skills_str = ", ".join(r.skills)
                
#                 rows.append({
#                     "Name": r.contact.name,
#                     "Phone": r.contact.phone,
#                     "Email": r.contact.email,
#                     "Technical Skills": skills_str,
#                     "Internship": intern_str,
#                     "Projects": proj_str,
#                     "Certificate": cert_str
#                 })
            
#             df = pd.DataFrame(rows)
#             target_order = ["Name", "Phone", "Email", "Technical Skills", "Internship", "Projects", "Certificate"]
            
#             for col in target_order:
#                 if col not in df.columns:
#                     df[col] = "" 
            
#             df = df[target_order]

#             with tab1:
#                 st.dataframe(
#                     df,
#                     column_config={
#                         "Name": st.column_config.TextColumn("Candidate Name", width="medium"),
#                         "Technical Skills": st.column_config.TextColumn("Skills", width="large"),
#                         "Projects": st.column_config.TextColumn("Projects", width="large"),
#                         "Internship": st.column_config.TextColumn("Internships", width="medium"),
#                     },
#                     use_container_width=True,
#                     height=500
#                 )
            
#             with tab2:
#                 st.json([r.dict() for r in results])

#             # 3. DOWNLOAD
#             st.markdown("<br>", unsafe_allow_html=True)
#             csv = df.to_csv(index=False).encode('utf-8')
#             col_d1, col_d2, col_d3 = st.columns([1, 2, 1])
#             with col_d2:
#                 st.download_button(
#                     label="📥 DOWNLOAD REPORT (CSV)",
#                     data=csv,
#                     file_name="Resume_Report.csv",
#                     mime="text/csv",
#                     use_container_width=True
#                 )

# import streamlit as st
# import pandas as pd
# import pdfplumber
# import io
# import json
# import os
# import time
# from dotenv import load_dotenv
# import google.generativeai as genai
# from pydantic import BaseModel, Field
# from typing import List, Optional

# # ==========================================
# # 1. PAGE CONFIGURATION
# # ==========================================
# st.set_page_config(
#     page_title="Resume Intelligence AI",
#     page_icon="🧠",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # ==========================================
# # 2. NUCLEAR CSS (FORCING COLORS)
# # ==========================================
# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
#     /* 1. GLOBAL DARK THEME */
#     .stApp {
#         background: radial-gradient(circle at top left, #1e1e2f, #0a0a12);
#         font-family: 'Outfit', sans-serif;
#         color: #ffffff;
#     }
    
#     /* Force standard text to be white */
#     p, h1, h2, h3, h4, h5, h6, li, span, div {
#         color: #ffffff;
#     }

#     /* HIDE DEFAULT MENU */
#     #MainMenu, footer, header {visibility: hidden;}
#     section[data-testid="stSidebar"] {display: none;}
    
#     /* 2. UPLOADER BOX & TEXT VISIBILITY FIX */
#     .stFileUploader {
#         background: rgba(255, 255, 255, 0.05);
#         border: 2px dashed #5b5b70;
#         border-radius: 15px;
#         padding: 2rem;
#     }

#     /* --- THE NUCLEAR FIX FOR FILE NAMES --- */
#     /* This targets the specific row where the file appears */
#     div[data-testid="stFileUploader"] div[role="listitem"] {
#         background-color: transparent !important;
#     }
    
#     /* This forces the FILE NAME (span) to be white */
#     div[data-testid="stFileUploader"] div[role="listitem"] div,
#     div[data-testid="stFileUploader"] div[role="listitem"] span {
#         color: #ffffff !important;
#         font-weight: 600 !important;
#     }
    
#     /* This forces the FILE SIZE (small) to be white/light gray */
#     div[data-testid="stFileUploader"] div[role="listitem"] small {
#         color: #e0e0e0 !important;
#     }

#     /* Browse Button */
#     .stFileUploader button {
#         background-color: #40d0ff !important;
#         color: #000000 !important; /* Black text on Blue button */
#         border: none;
#         font-weight: 700;
#     }
    
#     /* Upload Icon (Cloud arrow) */
#     div[data-testid="stFileUploader"] svg {
#         fill: #40d0ff !important;
#     }

#     /* 3. DOWNLOAD BUTTON (TRANSPARENT/BLACK STYLE) */
#     div.stDownloadButton > button {
#         background-color: transparent !important;
#         color: #40d0ff !important;
#         border: 1px solid #40d0ff !important;
#         border-radius: 50px;
#         padding: 0.5rem 2rem;
#         font-weight: 600;
#         transition: all 0.3s ease;
#     }
#     div.stDownloadButton > button:hover {
#         background-color: rgba(64, 208, 255, 0.1) !important;
#         box-shadow: 0 0 10px rgba(64, 208, 255, 0.3);
#     }

#     /* 4. HERO SECTION */
#     .hero-container {
#         text-align: center;
#         padding: 3rem 2rem;
#         background: rgba(30, 30, 46, 0.8);
#         border: 1px solid rgba(255, 255, 255, 0.1);
#         border-radius: 20px;
#         backdrop-filter: blur(10px);
#         margin-bottom: 2rem;
#         box-shadow: 0 10px 30px rgba(0,0,0,0.5);
#     }
#     .hero-title {
#         font-size: 3.5rem !important;
#         font-weight: 800 !important;
#         background: linear-gradient(90deg, #40d0ff, #0080ff);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent !important; 
#         margin-bottom: 0.5rem !important;
#     }

#     /* 5. METRIC CARDS */
#     div[data-testid="stMetric"] {
#         background: rgba(40, 40, 60, 0.9);
#         border: 1px solid #40d0ff;
#         border-radius: 12px;
#         padding: 15px;
#     }
#     div[data-testid="stMetricLabel"] {
#         color: #a0c0ff !important; 
#         font-size: 1rem !important;
#     }
#     div[data-testid="stMetricValue"] {
#         color: #ffffff !important; 
#         font-size: 2rem !important;
#     }
    
#     /* 6. TABLE VISIBILITY */
#     div[data-testid="stDataFrame"] {
#         background: rgba(30, 30, 46, 0.8);
#         border-radius: 10px;
#         padding: 10px;
#     }
#     div[data-testid="stDataFrame"] th {
#         background-color: #2a2a3e !important;
#         color: #ffffff !important; 
#     }
#     div[data-testid="stDataFrame"] td {
#         color: #e0e0e0 !important;
#     }

#     /* PRIMARY BUTTON */
#     div.stButton > button {
#         background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
#         color: white !important;
#         font-weight: 700;
#         padding: 0.8rem 3rem;
#         border-radius: 50px;
#         border: none;
#         box-shadow: 0 0 15px rgba(0, 114, 255, 0.6);
#         font-size: 1.1rem;
#     }
# </style>
# """, unsafe_allow_html=True)

# # ==========================================
# # 3. SETUP & LOGIC
# # ==========================================
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("gemini")

# class ContactInfo(BaseModel):
#     name: Optional[str] = Field(None)
#     email: Optional[str] = Field(None)
#     phone: Optional[str] = Field(None)
#     linkedin: Optional[str] = Field(None)

# class Project(BaseModel):
#     title: str
#     tech_stack: Optional[str] = Field(None)

# class ResumeData(BaseModel):
#     contact: ContactInfo
#     skills: List[str] = Field(default_factory=list)
#     internships: List[str] = Field(default_factory=list)
#     projects: List[Project] = Field(default_factory=list)
#     certifications: List[str] = Field(default_factory=list)
#     years_experience: Optional[str] = Field(None)

# def extract_text(file_bytes):
#     try:
#         with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
#             return "\n".join([p.extract_text() or "" for p in pdf.pages])
#     except: return ""

# def analyze_resume(text):
#     if not GOOGLE_API_KEY: return None
#     genai.configure(api_key=GOOGLE_API_KEY)
    
#     model = genai.GenerativeModel('gemini-2.5-flash')
    
#     prompt = f"""
#     Analyze the resume text below and extract data into strict JSON.
#     REQUIREMENTS:
#     1. Extract Contact (Name, Email, Phone).
#     2. Extract ALL Technical Skills.
#     3. Extract INTERNSHIPS (Role at Company).
#     4. Extract ALL Projects (Title + Tech Stack).
#     5. Extract CERTIFICATIONS (Name).
#     6. Years of Experience (number or "Fresher").
    
#     RESUME TEXT:
#     {text[:10000]}
    
#     JSON SCHEMA:
#     {{
#         "contact": {{ "name": "...", "email": "...", "phone": "..." }},
#         "skills": ["Python", "SQL", ...],
#         "internships": ["Data Science Intern at Innomatics", ...],
#         "projects": [ {{ "title": "...", "tech_stack": "..." }} ],
#         "certifications": ["AWS Certified", "NPTEL Python", ...],
#         "years_experience": "..."
#     }}
#     """
#     try:
#         res = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
#         return ResumeData(**json.loads(res.text))
#     except: return None

# # ==========================================
# # 4. MAIN UI
# # ==========================================

# # HEADER
# st.markdown("""
# <div class="hero-container">
#     <div class="hero-title">Resume Intelligence AI</div>
#     <p style="font-size: 1.2rem; color: #e0e0e0;">Upload Resumes • Extract Insights • Export Data</p>
# </div>
# """, unsafe_allow_html=True)

# # API KEY CHECK
# if not GOOGLE_API_KEY:
#     st.error("🔒 API Key Missing. Please set GOOGLE_API_KEY in your .env file.")
#     st.stop()

# # UPLOAD SECTION
# col1, col2, col3 = st.columns([1, 6, 1])
# with col2:
#     uploaded_files = st.file_uploader("📂 Drag & Drop PDF Resumes Here", type=["pdf"], accept_multiple_files=True)

# if uploaded_files:
#     st.markdown("<br>", unsafe_allow_html=True)
#     c1, c2, c3 = st.columns([1, 1, 1])
#     with c2:
#         start_process = st.button("🚀 IGNITE ANALYSIS", use_container_width=True)

#     if start_process:
#         results = []
#         progress_bar = st.progress(0)
#         status_box = st.empty()
        
#         # PROCESSING LOOP
#         for i, file in enumerate(uploaded_files):
#             status_box.info(f"⚡ Analyzing: {file.name}")
#             text = extract_text(file.read())
#             if text:
#                 data = analyze_resume(text)
#                 if data: results.append(data)
            
#             progress_bar.progress((i + 1) / len(uploaded_files))
#             time.sleep(0.05)
            
#         progress_bar.empty()
#         status_box.empty()
        
#         if results:
#             st.markdown("---")
#             st.subheader("📊 Intelligence Report")
            
#             # 1. METRICS (REMOVED SUCCESS RATE)
#             m1, m2, m3 = st.columns(3)
#             m1.metric("Candidates", len(results))
#             m2.metric("Total Projects", sum(len(r.projects) for r in results))
#             m3.metric("Total Internships", sum(len(r.internships) for r in results))

#             # 2. DATA TABLE PREP
#             tab1, tab2 = st.tabs(["📄 Detailed Table", "💾 JSON Data"])
            
#             rows = []
#             for r in results:
#                 proj_str = " • ".join([f"{p.title} ({p.tech_stack})" for p in r.projects])
#                 intern_str = " • ".join(r.internships)
#                 cert_str = " • ".join(r.certifications)
#                 skills_str = ", ".join(r.skills)
                
#                 rows.append({
#                     "Name": r.contact.name,
#                     "Phone": r.contact.phone,
#                     "Email": r.contact.email,
#                     "Technical Skills": skills_str,
#                     "Internship": intern_str,
#                     "Projects": proj_str,
#                     "Certificate": cert_str
#                 })
            
#             df = pd.DataFrame(rows)
#             target_order = ["Name", "Phone", "Email", "Technical Skills", "Internship", "Projects", "Certificate"]
            
#             for col in target_order:
#                 if col not in df.columns:
#                     df[col] = "" 
            
#             df = df[target_order]

#             with tab1:
#                 st.dataframe(
#                     df,
#                     column_config={
#                         "Name": st.column_config.TextColumn("Candidate Name", width="medium"),
#                         "Technical Skills": st.column_config.TextColumn("Skills", width="large"),
#                         "Projects": st.column_config.TextColumn("Projects", width="large"),
#                         "Internship": st.column_config.TextColumn("Internships", width="medium"),
#                     },
#                     use_container_width=True,
#                     height=500
#                 )
            
#             with tab2:
#                 st.json([r.dict() for r in results])

#             # 3. DOWNLOAD
#             st.markdown("<br>", unsafe_allow_html=True)
#             csv = df.to_csv(index=False).encode('utf-8')
#             col_d1, col_d2, col_d3 = st.columns([1, 2, 1])
#             with col_d2:
#                 st.download_button(
#                     label="📥 DOWNLOAD REPORT (CSV)",
#                     data=csv,
#                     file_name="Resume_Report.csv",
#                     mime="text/csv",
#                     use_container_width=True
#                 )



import streamlit as st
import pandas as pd
import pdfplumber
import io
import json
import os
import time
from dotenv import load_dotenv
import google.generativeai as genai
from pydantic import BaseModel, Field
from typing import List, Optional

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Resume Intelligence AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. AGGRESSIVE CSS FIXES
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    /* 1. GLOBAL DARK THEME */
    .stApp {
        background: radial-gradient(circle at top left, #1e1e2f, #0a0a12);
        font-family: 'Outfit', sans-serif;
        color: #ffffff;
    }
    
    p, h1, h2, h3, h4, h5, h6, li, span, div {
        color: #ffffff;
    }

    #MainMenu, footer, header {visibility: hidden;}
    section[data-testid="stSidebar"] {display: none;}
    
    /* 2. UPLOADER BOX STYLE */
    .stFileUploader {
        background: rgba(255, 255, 255, 0.05);
        border: 2px dashed #5b5b70;
        border-radius: 15px;
        padding: 2rem;
    }

    /* --- CRITICAL FIX FOR FILE NAMES --- */
    /* This targets the exact text element for the filename */
    div[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"] + div div {
        color: white !important;
    }
    
    /* Brute force: Make every span and div inside the uploaded file list white */
    div[data-testid="stFileUploader"] div[role="listitem"] span {
        color: white !important;
        font-weight: 600 !important;
    }
    div[data-testid="stFileUploader"] div[role="listitem"] div {
        color: white !important;
    }
    div[data-testid="stFileUploader"] div[role="listitem"] small {
        color: #cccccc !important; /* File size slightly lighter */
    }
    
    /* Browse Button */
    .stFileUploader button {
        background-color: #40d0ff !important;
        color: #000000 !important;
        border: none;
        font-weight: 700;
    }
    
    /* Upload Icon */
    div[data-testid="stFileUploader"] svg {
        fill: #40d0ff !important;
    }

    /* 3. DOWNLOAD BUTTON */
    div.stDownloadButton > button {
        background-color: transparent !important;
        color: #40d0ff !important;
        border: 1px solid #40d0ff !important;
        border-radius: 50px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    div.stDownloadButton > button:hover {
        background-color: rgba(64, 208, 255, 0.1) !important;
        box-shadow: 0 0 10px rgba(64, 208, 255, 0.3);
    }

    /* 4. HERO SECTION */
    .hero-container {
        text-align: center;
        padding: 3rem 2rem;
        background: rgba(30, 30, 46, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        backdrop-filter: blur(10px);
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .hero-title {
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        background: linear-gradient(90deg, #40d0ff, #0080ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent !important; 
        margin-bottom: 0.5rem !important;
    }

    /* 5. METRIC CARDS */
    div[data-testid="stMetric"] {
        background: rgba(40, 40, 60, 0.9);
        border: 1px solid #40d0ff;
        border-radius: 12px;
        padding: 15px;
    }
    div[data-testid="stMetricLabel"] {
        color: #a0c0ff !important; 
        font-size: 1rem !important;
    }
    div[data-testid="stMetricValue"] {
        color: #ffffff !important; 
        font-size: 2rem !important;
    }
    
    /* 6. TABLE VISIBILITY */
    div[data-testid="stDataFrame"] {
        background: rgba(30, 30, 46, 0.8);
        border-radius: 10px;
        padding: 10px;
    }
    div[data-testid="stDataFrame"] th {
        background-color: #2a2a3e !important;
        color: #ffffff !important; 
    }
    div[data-testid="stDataFrame"] td {
        color: #e0e0e0 !important;
    }

    /* PRIMARY BUTTON */
    div.stButton > button {
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
        color: white !important;
        font-weight: 700;
        padding: 0.8rem 3rem;
        border-radius: 50px;
        border: none;
        box-shadow: 0 0 15px rgba(0, 114, 255, 0.6);
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. SETUP & LOGIC
# ==========================================
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("gemini")

class ContactInfo(BaseModel):
    name: Optional[str] = Field(None)
    email: Optional[str] = Field(None)
    phone: Optional[str] = Field(None)
    linkedin: Optional[str] = Field(None)

class Project(BaseModel):
    title: str
    tech_stack: Optional[str] = Field(None)

class ResumeData(BaseModel):
    contact: ContactInfo
    skills: List[str] = Field(default_factory=list)
    internships: List[str] = Field(default_factory=list)
    projects: List[Project] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    years_experience: Optional[str] = Field(None)

def extract_text(file_bytes):
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            return "\n".join([p.extract_text() or "" for p in pdf.pages])
    except: return ""

def analyze_resume(text):
    if not GOOGLE_API_KEY: return None
    genai.configure(api_key=GOOGLE_API_KEY)
    
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    Analyze the resume text below and extract data into strict JSON.
    REQUIREMENTS:
    1. Extract Contact (Name, Email, Phone).
    2. Extract ALL Technical Skills.
    3. Extract INTERNSHIPS (Role at Company).
    4. Extract ALL Projects (Title + Tech Stack).
    5. Extract CERTIFICATIONS (Name).
    6. Years of Experience (number or "Fresher").
    
    RESUME TEXT:
    {text[:10000]}
    
    JSON SCHEMA:
    {{
        "contact": {{ "name": "...", "email": "...", "phone": "..." }},
        "skills": ["Python", "SQL", ...],
        "internships": ["Data Science Intern at Innomatics", ...],
        "projects": [ {{ "title": "...", "tech_stack": "..." }} ],
        "certifications": ["AWS Certified", "NPTEL Python", ...],
        "years_experience": "..."
    }}
    """
    try:
        res = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        return ResumeData(**json.loads(res.text))
    except: return None

# ==========================================
# 4. MAIN UI
# ==========================================

# HEADER
st.markdown("""
<div class="hero-container">
    <div class="hero-title">Resume Intelligence AI</div>
    <p style="font-size: 1.2rem; color: #e0e0e0;">Upload Resumes • Extract Insights • Export Data</p>
</div>
""", unsafe_allow_html=True)

# API KEY CHECK
if not GOOGLE_API_KEY:
    st.error("🔒 API Key Missing. Please set GOOGLE_API_KEY in your .env file.")
    st.stop()

# UPLOAD SECTION
col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    uploaded_files = st.file_uploader("📂 Drag & Drop PDF Resumes Here", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        start_process = st.button("🚀 IGNITE ANALYSIS", use_container_width=True)

    if start_process:
        results = []
        progress_bar = st.progress(0)
        status_box = st.empty()
        
        # PROCESSING LOOP
        for i, file in enumerate(uploaded_files):
            status_box.info(f"⚡ Analyzing: {file.name}")
            text = extract_text(file.read())
            if text:
                data = analyze_resume(text)
                if data: results.append(data)
            
            progress_bar.progress((i + 1) / len(uploaded_files))
            time.sleep(0.05)
            
        progress_bar.empty()
        status_box.empty()
        
        if results:
            st.markdown("---")
            st.subheader("📊 Intelligence Report")
            
            # 1. METRICS
            m1, m2, m3 = st.columns(3)
            m1.metric("Candidates", len(results))
            m2.metric("Total Projects", sum(len(r.projects) for r in results))
            m3.metric("Total Internships", sum(len(r.internships) for r in results))

            # 2. DATA TABLE PREP
            tab1, tab2 = st.tabs(["📄 Detailed Table", "💾 JSON Data"])
            
            rows = []
            for r in results:
                proj_str = " • ".join([f"{p.title} ({p.tech_stack})" for p in r.projects])
                intern_str = " • ".join(r.internships)
                cert_str = " • ".join(r.certifications)
                skills_str = ", ".join(r.skills)
                
                rows.append({
                    "Name": r.contact.name,
                    "Phone": r.contact.phone,
                    "Email": r.contact.email,
                    "Technical Skills": skills_str,
                    "Internship": intern_str,
                    "Projects": proj_str,
                    "Certificate": cert_str
                })
            
            df = pd.DataFrame(rows)
            target_order = ["Name", "Phone", "Email", "Technical Skills", "Internship", "Projects", "Certificate"]
            
            for col in target_order:
                if col not in df.columns:
                    df[col] = "" 
            
            df = df[target_order]

            with tab1:
                st.dataframe(
                    df,
                    column_config={
                        "Name": st.column_config.TextColumn("Candidate Name", width="medium"),
                        "Technical Skills": st.column_config.TextColumn("Skills", width="large"),
                        "Projects": st.column_config.TextColumn("Projects", width="large"),
                        "Internship": st.column_config.TextColumn("Internships", width="medium"),
                    },
                    use_container_width=True,
                    height=500
                )
            
            with tab2:
                st.json([r.dict() for r in results])

            # 3. DOWNLOAD
            st.markdown("<br>", unsafe_allow_html=True)
            csv = df.to_csv(index=False).encode('utf-8')
            col_d1, col_d2, col_d3 = st.columns([1, 2, 1])
            with col_d2:
                st.download_button(
                    label="📥 DOWNLOAD REPORT (CSV)",
                    data=csv,
                    file_name="Resume_Report.csv",
                    mime="text/csv",
                    use_container_width=True
                )
