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
# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="Resume Intelligence AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. CSS STYLING (FIXED FILE NAMES)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    /* 1. GLOBAL DARK THEME */
    .stApp {
        background: radial-gradient(circle at top left, #1e1e2f, #0a0a12);
        font-family: 'Outfit', sans-serif;
        color: #ffffff;
    }
    
    /* Force standard text to be white */
    p, h1, h2, h3, h4, h5, h6, li, span, div {
        color: #ffffff;
    }

    /* HIDE DEFAULT MENU */
    #MainMenu, footer, header {visibility: hidden;}
    section[data-testid="stSidebar"] {display: none;}
    
    /* 2. UPLOAD BOX & FILE NAME FIX */
    .stFileUploader {
        background: rgba(255, 255, 255, 0.05);
        border: 2px dashed #5b5b70;
        border-radius: 15px;
        padding: 2rem;
    }
    
    # /* --- CRITICAL FIX: FORCE WHITE TEXT FOR FILE NAMES --- */
    # div[data-testid="stFileUploader"] div[role="listitem"] {
    #     color: white !important;
    # }
    # div[data-testid="stFileUploader"] div[role="listitem"] div {
    #     color: white !important;
    # }
    # div[data-testid="stFileUploader"] div[role="listitem"] span {
    #     color: white !important;
    # }
    # /* ----------------------------------------------------- */
    

`    /* Force ALL text inside the uploader to be white */

    .stFileUploader * {

        color: #ffffff !important;

    }

    /* Except the small "Limit 200MB" text - make it light gray */

    .stFileUploader small {

        color: #a0a0a0 !important;

    }


    /* Small 'Limit 200MB' text */
    .stFileUploader small {
        color: #a0a0a0 !important;
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

# 3. SETUP & LOGIC
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("gemini")

class ContactInfo(BaseModel):
    name: Optional[str] = Field(None) # Optional → Controls whether field is required
    email: Optional[str] = Field(None)
    phone: Optional[str] = Field(None) # Field → Adds metadata & validation
    linkedin: Optional[str] = Field(None)

class Project(BaseModel):
    title: str
    tech_stack: Optional[str] = Field(None)

class ResumeData(BaseModel):
    contact: ContactInfo
    skills: List[str] = Field(default_factory=list)
    internships: List[str] = Field(default_factory=list) #Each object gets its own empty list
    projects: List[Project] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    years_experience: Optional[str] = Field(None)

def extract_text(file_bytes):
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            return "\n".join([p.extract_text() or "" for p in pdf.pages])
    except: return ""

def analyze_resume(text):
    if not GOOGLE_API_KEY: 
        st.error("API Key missing.")
        return None
        
    genai.configure(api_key=GOOGLE_API_KEY)
    
    model = genai.GenerativeModel('gemini-2.5-flash-lite')
    
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
    except Exception as e:
        # Added Error Printing so you know why it fails
        st.error(f"AI Error: {e}")
        return None

# 4. MAIN UI
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
                if data: 
                    results.append(data)
                else:
                    st.warning(f"Failed to analyze {file.name}")
            
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

