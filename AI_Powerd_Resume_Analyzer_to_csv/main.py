# import streamlit as st
# import pandas as pd
# import pdfplumber
# import io
# import json
# import os
# from dotenv import load_dotenv
# import google.generativeai as genai
# from pydantic import BaseModel, Field
# from typing import List, Optional

# # ==========================================
# # 1. CONFIGURATION (LOAD FROM .ENV)
# # ==========================================

# # Load environment variables
# load_dotenv()

# # Fetch the key securely
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("gemini")

# if not GOOGLE_API_KEY:
#     st.error("Google API Key not found. Please set it in environment variables.")
#     st.stop()

# # ==========================================
# # 2. DATA STRUCTURE
# # ==========================================

# class ContactInfo(BaseModel):
#     name: Optional[str] = Field(None, description="Full Name")
#     email: Optional[str] = Field(None, description="Email Address")
#     phone: Optional[str] = Field(None, description="Phone Number")
#     linkedin: Optional[str] = Field(None, description="LinkedIn URL")

# class Project(BaseModel):
#     title: str = Field(..., description="Project Title")
#     tech_stack: Optional[str] = Field(None, description="Tech used")

# class ResumeData(BaseModel):
#     contact: ContactInfo
#     skills: List[str] = Field(default_factory=list, description="List of all technical skills")
#     projects: List[Project] = Field(default_factory=list, description="ALL projects found in resume")
#     education_degree: Optional[str] = Field(None, description="Latest Degree Name")
#     education_college: Optional[str] = Field(None, description="College Name")
#     years_experience: Optional[str] = Field(None, description="Total years of experience or 'Fresher'")

# # ==========================================
# # 3. CORE LOGIC
# # ==========================================

# def extract_text_from_pdf(file_bytes):
#     """Extracts text from PDF bytes."""
#     text = ""
#     try:
#         with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
#             for page in pdf.pages:
#                 extracted = page.extract_text()
#                 if extracted:
#                     text += extracted + "\n"
#     except Exception as e:
#         st.error(f"Error reading PDF: {e}")
#     return text

# def analyze_resume_with_ai(raw_text: str) -> Optional[ResumeData]:
#     """
#     Sends text to Gemini using the key from .env
#     """
#     # FIX 1: Use the correct variable name GOOGLE_API_KEY (not API_KEY)
#     if not GOOGLE_API_KEY:
#         st.error("❌ API Key Missing!")
#         return None

#     try:
#         genai.configure(api_key=GOOGLE_API_KEY)
#         model = genai.GenerativeModel('gemini-2.5-flash') # Using stable model name

#         prompt = f"""
#         Extract the following details from the resume text below into JSON format:
#         1. Contact Info (Name, Email, Phone, LinkedIn)
#         2. Latest Education (Degree, College)
#         3. All Technical Skills (as a simple list of strings)
#         4. ALL Projects (Title and Tech Stack only). 
#            **CRITICAL INSTRUCTION: Do not limit the number of projects. If the resume has 4 projects, extract 4. If it has 10, extract 10. Extract EVERY project listed.**
#         5. Years of Experience (or "Fresher")

#         RESUME TEXT:
#         {raw_text}
        
#         Return strictly valid JSON matching this schema:
#         {{
#             "contact": {{ "name": "", "email": "", "phone": "", "linkedin": "" }},
#             "education_degree": "",
#             "education_college": "",
#             "skills": ["Python", "SQL", ...],
#             "projects": [
#                 {{ "title": "Project 1", "tech_stack": "Python, Pandas" }},
#                 {{ "title": "Project 2", "tech_stack": "React, Node" }},
#                 ... (Extract ALL projects found)
#             ],
#             "years_experience": ""
#         }}
#         """

#         response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
#         json_data = json.loads(response.text)
#         return ResumeData(**json_data)

#     except Exception as e:
#         st.error(f"AI Error: {e}")
#         return None

# def convert_to_csv(resumes: List[ResumeData]):
#     """
#     Converts the list of Resume objects into a CSV string.
#     """
#     csv_rows = []
#     for r in resumes:
#         # Flatten ALL projects into a single string
#         project_str = " | ".join([f"{p.title} ({p.tech_stack})" for p in r.projects])
        
#         csv_rows.append({
#             "Name": r.contact.name,
#             "Email": r.contact.email,
#             "Phone": r.contact.phone,
#             "LinkedIn": r.contact.linkedin,
#             "Degree": r.education_degree,
#             "College": r.education_college,
#             "Experience": r.years_experience,
#             "Skills": ", ".join(r.skills[:15]),
#             "Total Projects": len(r.projects),
#             "Projects Details": project_str
#         })
    
#     df = pd.DataFrame(csv_rows)
#     return df.to_csv(index=False).encode('utf-8')

# # ==========================================
# # 4. STREAMLIT UI
# # ==========================================

# st.set_page_config(page_title="Resume to CSV", layout="wide")

# st.title("📄 Secure Resume Batch Processor")
# st.markdown("Upload resumes. Extracts **ALL** projects and details.")

# # FIX 2: UNCOMMENT THIS LINE so uploaded_files actually exists!
# uploaded_files = st.file_uploader("Upload PDF Resumes", type=["pdf"], accept_multiple_files=True)

# if uploaded_files and GOOGLE_API_KEY:
#     if st.button(f"Process {len(uploaded_files)} Files"):
        
#         results = []
#         progress_bar = st.progress(0)
        
#         for idx, file in enumerate(uploaded_files):
#             # 1. Read
#             file_bytes = file.read()
#             raw_text = extract_text_from_pdf(file_bytes)
            
#             # 2. Analyze
#             with st.spinner(f"Reading {file.name}..."):
#                 data = analyze_resume_with_ai(raw_text)
#                 if data:
#                     results.append(data)
            
#             progress_bar.progress((idx + 1) / len(uploaded_files))
        
#         if results:
#             st.success("✅ Done! All projects extracted.")
            
#             # Convert to CSV
#             csv_data = convert_to_csv(results)
            
#             # Show Preview
#             df_preview = pd.read_csv(io.BytesIO(csv_data))
#             st.dataframe(df_preview, use_container_width=True)
            
#             # Download Button
#             st.download_button(
#                 label="📥 Download CSV Report",
#                 data=csv_data,
#                 file_name="resume_report.csv",
#                 mime="text/csv"
#             )

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
# 1. PAGE CONFIG & STYLING (MUST BE FIRST)
# ==========================================
st.set_page_config(
    page_title="AI Resume Analyzer Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for "Best-in-Class" UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    /* Global Styles */
    .stApp {
        background-color: #0f1116; /* Dark background */
        font-family: 'Inter', sans-serif; 
    }
    
    /* Hide Default Streamlit Menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Custom Header Card */
    .header-card {
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .header-card h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 800;
    }
    .header-card p {
        margin-top: 10px;
        font-size: 1.1rem;
        opacity: 0.9;
    }

    /* Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #1e2329;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #2d333b;
    }
    div[data-testid="stMetricValue"] {
        color: #58a6ff !important;
    }

    /* Primary Button Styling */
    div.stButton > button {
        background: linear-gradient(45deg, #238636, #2ea043);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: 600;
        border-radius: 8px;
        width: 100%;
        transition: transform 0.2s;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(46, 160, 67, 0.4);
    }

    /* Success Message */
    .success-box {
        padding: 1rem;
        background-color: #0d1117;
        border: 1px solid #3fb950;
        border-radius: 8px;
        color: #3fb950;
        text-align: center;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. SETUP & SECURITY
# ==========================================
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("gemini")

# Sidebar Configuration
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=50)
    st.header("⚙️ Configuration")
    
    # API Key Input (Fallback)
    if not GOOGLE_API_KEY:
        st.warning("⚠️ API Key not detected")
        GOOGLE_API_KEY = st.text_input("Enter Gemini API Key", type="password")
    else:
        st.success("✅ API Key Active")
    
    st.divider()
    st.markdown("**Model:** `gemini-1.5-flash`")
    st.markdown("**Mode:** `Batch Processing`")
    st.caption("Designed by Alok Mahadev Tungal")

if not GOOGLE_API_KEY:
    st.stop()

# ==========================================
# 3. DATA MODELS
# ==========================================
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
    projects: List[Project] = Field(default_factory=list)
    education_degree: Optional[str] = Field(None)
    years_experience: Optional[str] = Field(None)

# ==========================================
# 4. LOGIC FUNCTIONS
# ==========================================
def extract_text_from_pdf(file_bytes):
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            return "\n".join([page.extract_text() or "" for page in pdf.pages])
    except Exception:
        return ""

def analyze_resume(text):
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Analyze this resume text and return a valid JSON object.
    Extract:
    1. Contact (Name, Email, Phone, LinkedIn)
    2. Latest Degree
    3. Years of Experience (e.g. "2 years" or "Fresher")
    4. Top 10 Technical Skills (list)
    5. ALL Projects (Title and Tech Stack) - Extract every single project found.

    RESUME TEXT:
    {text[:8000]} 

    JSON SCHEMA:
    {{
        "contact": {{ "name": "...", "email": "...", "phone": "...", "linkedin": "..." }},
        "education_degree": "...",
        "years_experience": "...",
        "skills": ["...", "..."],
        "projects": [
            {{ "title": "...", "tech_stack": "..." }}
        ]
    }}
    """
    try:
        response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        return ResumeData(**json.loads(response.text))
    except Exception as e:
        return None

# ==========================================
# 5. MAIN UI LAYOUT
# ==========================================

# HEADER
st.markdown("""
<div class="header-card">
    <h1>🚀 AI Resume Analyzer Pro</h1>
    <p>Extract insights and projects from bulk PDFs in seconds</p>
</div>
""", unsafe_allow_html=True)

# UPLOAD SECTION
uploaded_files = st.file_uploader("📂 Drop PDF Resumes Here", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    st.markdown(f"**Selected:** `{len(uploaded_files)} files` ready for processing.")
    
    # ACTION BUTTON
    if st.button("✨ Start AI Analysis", use_container_width=True):
        
        results = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # PROCESSING LOOP
        for i, file in enumerate(uploaded_files):
            status_text.markdown(f"🔄 Processing: **{file.name}**")
            
            # Read & Analyze
            text = extract_text_from_pdf(file.read())
            if text:
                data = analyze_resume(text)
                if data:
                    results.append(data)
            
            # Update Progress
            progress_bar.progress((i + 1) / len(uploaded_files))
            time.sleep(0.1) # Smooth animation
            
        progress_bar.empty()
        status_text.empty()
        
        # RESULTS DASHBOARD
        if results:
            st.markdown('<div class="success-box">✅ Analysis Complete!</div>', unsafe_allow_html=True)
            st.divider()
            
            # 1. METRICS ROW
            c1, c2, c3 = st.columns(3)
            c1.metric("Resumes Processed", len(results))
            
            total_projects = sum(len(r.projects) for r in results)
            c2.metric("Total Projects Found", total_projects)
            
            avg_skills = int(sum(len(r.skills) for r in results) / len(results))
            c3.metric("Avg Skills / Candidate", avg_skills)
            
            st.divider()
            
            # 2. DATA TABLE PREPARATION
            table_data = []
            for r in results:
                # Format projects as a clean list for the table
                proj_list = [f"• {p.title} ({p.tech_stack})" for p in r.projects]
                proj_str = "\n".join(proj_list)
                
                table_data.append({
                    "Name": r.contact.name,
                    "Experience": r.years_experience,
                    "Degree": r.education_degree,
                    "Skills": ", ".join(r.skills),
                    "Projects Extracted": proj_str, 
                    "Email": r.contact.email
                })
            
            df = pd.DataFrame(table_data)
            
            # 3. INTERACTIVE DATAFRAME
            st.subheader("📊 Candidate Database")
            st.dataframe(
                df,
                column_config={
                    "Name": st.column_config.TextColumn("Candidate Name", width="medium"),
                    "Projects Extracted": st.column_config.TextColumn("Projects", width="large"),
                    "Email": st.column_config.LinkColumn("Email"),
                },
                use_container_width=True,
                height=400
            )
            
            # 4. DOWNLOAD CSV
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Full Report (CSV)",
                data=csv,
                file_name="AI_Resume_Report.csv",
                mime="text/csv",
                use_container_width=True
            )


