# import streamlit as st
# import pandas as pd
# import pdfplumber
# import zipfile
# import io
# import json 
# import google.generativeai as genai
# from pydantic import BaseModel, Field
# from typing import List, Optional

# # ==========================================
# # 1. UNIVERSAL DATA STRUCTURE (Updated for your Image)
# # ==========================================

# class ContactInfo(BaseModel):
#     name: Optional[str] = Field(None, description="Full Name")
#     email: Optional[str] = Field(None, description="Email Address")
#     phone: Optional[str] = Field(None, description="Phone Number")
#     location: Optional[str] = Field(None, description="City, Country")
#     linkedin: Optional[str] = Field(None, description="LinkedIn URL")
#     github: Optional[str] = Field(None, description="GitHub URL")
#     portfolio: Optional[str] = Field(None, description="Portfolio/Website URL")

# class Project(BaseModel):
#     title: str = Field(..., description="Project Title")
#     tech_stack: Optional[str] = Field(None, description="Tech used (e.g., 'Python, EDA')")
#     link: Optional[str] = Field(None, description="Project URL/Link if present")
#     description: List[str] = Field(default_factory=list, description="Bullet points")

# class Experience(BaseModel):
#     company: str = Field(..., description="Company Name")
#     role: str = Field(..., description="Job Role/Title")
#     duration: Optional[str] = Field(None, description="Dates (e.g., 'Feb 2025')")
#     description: List[str] = Field(default_factory=list, description="Job responsibilities")

# class Education(BaseModel):
#     institution: str = Field(..., description="College/University Name")
#     degree: str = Field(..., description="Degree (e.g., B.E. ECE)")
#     year: Optional[str] = Field(None, description="Graduation Year")
#     location: Optional[str] = Field(None, description="City, State")

# class Certification(BaseModel):
#     name: str = Field(..., description="Name of certification (e.g., 'Python for Data Science')")
#     issuer: Optional[str] = Field(None, description="Issuing Organization (e.g., 'NPTEL')")
#     year: Optional[str] = Field(None, description="Year obtained")

# class SkillSet(BaseModel):
#     languages: List[str] = Field(default_factory=list, description="Python, Java, C++...")
#     frameworks_libraries: List[str] = Field(default_factory=list, description="Pandas, Keras, React...")
#     tools_platforms: List[str] = Field(default_factory=list, description="GitHub, Docker, AWS...")
#     ml_ai_concepts: List[str] = Field(default_factory=list, description="EDA, Regression, NLP...")
#     core_competencies: List[str] = Field(default_factory=list, description="Web Scraping, Model Tuning...")

# class ResumeData(BaseModel):
#     contact: ContactInfo
#     summary: Optional[str] = Field(None, description="Profile Summary/Objective")
#     skills: SkillSet
#     projects: List[Project]
#     experience: List[Experience]
#     education: List[Education]
#     certifications: List[Certification] = Field(default_factory=list)

# # ==========================================
# # 2. AI EXTRACTION ENGINE
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

# def analyze_resume_with_ai(raw_text: str, api_key: str) -> Optional[ResumeData]:
#     """
#     Uses Gemini AI to map ANY resume text to our strict Pydantic Schema.
#     """
#     try:
#         genai.configure(api_key=api_key)
#         model = genai.GenerativeModel('gemini-2.5-flash')

#         prompt = f"""
#         Act as a professional Resume Parser. Extract data from the text below into strictly structured JSON.
        
#         CRITICAL INSTRUCTIONS:
#         1. **Capture Every Detail:** Do not summarize. Extract full bullet points for projects and experience.
#         2. **Certifications:** Look for a "Certifications" or "Achievements" section.
#         3. **Projects:** Extract the Title, the Tech Stack (often next to title), ANY Links, and the description.
#         4. **Skills:** Categorize skills intelligently based on the text (e.g., put 'Web Scraping' under 'Core Competencies' or 'Project Skills').
        
#         RESUME TEXT:
#         {raw_text}
        
#         Output must match this JSON schema exactly:
#         {{
#             "contact": {{ "name": "", "email": "", "phone": "", "linkedin": "", "github": "", "location": "" }},
#             "summary": "",
#             "skills": {{
#                 "languages": [],
#                 "frameworks_libraries": [],
#                 "tools_platforms": [],
#                 "ml_ai_concepts": [],
#                 "core_competencies": [] 
#             }},
#             "projects": [
#                 {{ "title": "", "tech_stack": "", "link": "", "description": ["..."] }}
#             ],
#             "experience": [
#                 {{ "company": "", "role": "", "duration": "", "description": ["..."] }}
#             ],
#             "education": [
#                 {{ "institution": "", "degree": "", "year": "", "location": "" }}
#             ],
#             "certifications": [
#                 {{ "name": "", "issuer": "", "year": "" }}
#             ]
#         }}
#         """

#         response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
#         json_data = json.loads(response.text)
#         return ResumeData(**json_data)

#     except Exception as e:
#         st.error(f"AI Extraction Error: {e}")
#         return None

# # ==========================================
# # 3. FILE GENERATION LOGIC
# # ==========================================

# def create_zip_bundle(resumes: List[ResumeData]):
#     """Creates a ZIP with 1 Summary CSV and N JSON files."""
    
#     # 1. Create CSV
#     csv_rows = []
#     for r in resumes:
#         # Join skills for CSV readability
#         all_skills = (r.skills.languages + r.skills.frameworks_libraries)
        
#         csv_rows.append({
#             "Candidate Name": r.contact.name,
#             "Email": r.contact.email,
#             "Phone": r.contact.phone,
#             "Latest Degree": r.education[0].degree if r.education else "N/A",
#             "University": r.education[0].institution if r.education else "N/A",
#             "Latest Role": r.experience[0].role if r.experience else "Fresher",
#             "Total Projects": len(r.projects),
#             "Certifications": len(r.certifications),
#             "Key Skills": ", ".join(all_skills[:8]) # First 8 skills
#         })
    
#     df = pd.DataFrame(csv_rows)
#     csv_buffer = io.StringIO()
#     df.to_csv(csv_buffer, index=False)

#     # 2. Create ZIP
#     zip_buffer = io.BytesIO()
#     with zipfile.ZipFile(zip_buffer, "w") as zf:
#         # Add CSV
#         zf.writestr("Resume_Batch_Summary.csv", csv_buffer.getvalue())
        
#         # Add JSONs
#         for r in resumes:
#             safe_name = (r.contact.name or "Unknown").replace(" ", "_")
#             filename = f"{safe_name}.json"
#             zf.writestr(filename, r.model_dump_json(indent=2))
            
#     return zip_buffer.getvalue(), df

# # ==========================================
# # 4. STREAMLIT UI
# # ==========================================

# st.set_page_config(page_title="Universal Resume Parser", layout="wide")

# st.title("📄 Universal AI Resume Parser")
# st.markdown("""
# **Upload any resume (PDF).** This system uses AI to extract:
# - Contact Info & Social Links
# - **Certifications & Achievements** (New!)
# - **Detailed Project Links & Tech Stacks**
# - Granular Skills (ML Concepts, Tools, etc.)
# """)

# # Sidebar
# with st.sidebar:
#     st.header("🔑 API Key")
#     api_key = st.text_input("Enter Google Gemini API Key", type="password")
#     st.caption("[Get Free Key](https://aistudio.google.com/app/apikey)")
#     st.warning("Required for AI extraction.")

# uploaded_files = st.file_uploader("Upload Resumes", type=["pdf"], accept_multiple_files=True)

# if uploaded_files and st.button(f"Process {len(uploaded_files)} Resumes"):
    
#     if not api_key:
#         st.error("Please enter your API Key in the sidebar.")
#     else:
#         processed_data = []
#         progress_bar = st.progress(0)
        
#         for i, file in enumerate(uploaded_files):
#             # 1. Read
#             file_bytes = file.read()
#             text = extract_text_from_pdf(file_bytes)
            
#             # 2. Analyze
#             with st.spinner(f"Extracting data from {file.name}..."):
#                 data = analyze_resume_with_ai(text, api_key)
#                 if data:
#                     processed_data.append(data)
            
#             progress_bar.progress((i + 1) / len(uploaded_files))
        
#         # 3. Result
#         if processed_data:
#             zip_file, df = create_zip_bundle(processed_data)
            
#             st.success("✅ Extraction Complete!")
            
#             # Show Table
#             st.subheader("📊 Candidate Overview")
#             st.dataframe(df, use_container_width=True)
            
#             # Show Detailed JSON for the first person (Verification)
#             with st.expander("🔍 View Extracted Data (First Candidate)"):
#                 st.json(processed_data[0].model_dump_json())

#             # Download
#             st.download_button(
#                 label="📥 Download ZIP (CSV + JSONs)",
#                 data=zip_file,
#                 file_name="Universal_Resume_Data.zip",
#                 mime="application/zip"
#             )



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

# # Load environment variables from the .env file
# load_dotenv()

# # Fetch the key securely
# API_KEY = os.getenv("gemini")

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
#     projects: List[Project] = Field(default_factory=list)
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
#     if not API_KEY:
#         st.error("❌ API Key Missing! Please create a .env file with GOOGLE_API_KEY=...")
#         return None

#     try:
#         genai.configure(api_key=API_KEY)
#         model = genai.GenerativeModel('gemini-2.5-flash')

#         prompt = f"""
#         Extract the following details from the resume text below into JSON format:
#         1. Contact Info (Name, Email, Phone, LinkedIn)
#         2. Latest Education (Degree, College)
#         3. All Technical Skills (as a simple list of strings)
#         4. All Projects (Title and Tech Stack only)
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
#                 {{ "title": "Project 1", "tech_stack": "Python, Pandas" }}
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
#         # Flatten projects into a single string for the CSV cell
#         project_str = " | ".join([f"{p.title} ({p.tech_stack})" for p in r.projects])
        
#         csv_rows.append({
#             "Name": r.contact.name,
#             "Email": r.contact.email,
#             "Phone": r.contact.phone,
#             "LinkedIn": r.contact.linkedin,
#             "College": r.education_college,
#             "Experience": r.years_experience,
#             "Skills": ", ".join(r.skills[:10]), # Top 10 skills
#             "Projects": project_str
#         })
    
#     df = pd.DataFrame(csv_rows)
#     return df.to_csv(index=False).encode('utf-8')

# # ==========================================
# # 4. STREAMLIT UI
# # ==========================================

# st.set_page_config(page_title="Resume to CSV", layout="wide")

# st.title("📄 Secure Resume Batch Processor")
# st.markdown("Upload resumes. Processing secured via `.env`.")

# # Check for API Key on startup
# if not API_KEY:
#     st.warning("⚠️ No API Key found. Please check your .env file.")
# else:
#     st.success("✅ API Key Loaded Securely")

# uploaded_files = st.file_uploader("Upload PDF Resumes", type=["pdf"], accept_multiple_files=True)

# if uploaded_files and API_KEY:
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
#             st.success("✅ Done!")
            
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
from dotenv import load_dotenv
import google.generativeai as genai
from pydantic import BaseModel, Field
from typing import List, Optional

# ==========================================
# 1. CONFIGURATION (LOAD FROM .ENV)
# ==========================================

# Load environment variables from the .env file
# load_dotenv()

# # Fetch the key securely
# API_KEY = os.getenv("gemini")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("gemini")

if not GOOGLE_API_KEY:
    st.error("Google API Key not found. Please set it in environment variables.")
    st.stop()

# ==========================================
# 2. DATA STRUCTURE
# ==========================================

class ContactInfo(BaseModel):
    name: Optional[str] = Field(None, description="Full Name")
    email: Optional[str] = Field(None, description="Email Address")
    phone: Optional[str] = Field(None, description="Phone Number")
    linkedin: Optional[str] = Field(None, description="LinkedIn URL")

class Project(BaseModel):
    title: str = Field(..., description="Project Title")
    tech_stack: Optional[str] = Field(None, description="Tech used")

class ResumeData(BaseModel):
    contact: ContactInfo
    skills: List[str] = Field(default_factory=list, description="List of all technical skills")
    projects: List[Project] = Field(default_factory=list, description="ALL projects found in resume")
    education_degree: Optional[str] = Field(None, description="Latest Degree Name")
    education_college: Optional[str] = Field(None, description="College Name")
    years_experience: Optional[str] = Field(None, description="Total years of experience or 'Fresher'")

# ==========================================
# 3. CORE LOGIC
# ==========================================

def extract_text_from_pdf(file_bytes):
    """Extracts text from PDF bytes."""
    text = ""
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
    return text

def analyze_resume_with_ai(raw_text: str) -> Optional[ResumeData]:
    """
    Sends text to Gemini using the key from .env
    """
    if not API_KEY:
        st.error("❌ API Key Missing! Please create a .env file with GOOGLE_API_KEY=...")
        return None

    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash-lite')

        # UPDATED PROMPT: STRICT INSTRUCTION TO EXTRACT ALL PROJECTS
        prompt = f"""
        Extract the following details from the resume text below into JSON format:
        1. Contact Info (Name, Email, Phone, LinkedIn)
        2. Latest Education (Degree, College)
        3. All Technical Skills (as a simple list of strings)
        4. ALL Projects (Title and Tech Stack only). 
           **CRITICAL INSTRUCTION: Do not limit the number of projects. If the resume has 4 projects, extract 4. If it has 10, extract 10. Extract EVERY project listed.**
        5. Years of Experience (or "Fresher")

        RESUME TEXT:
        {raw_text}
        
        Return strictly valid JSON matching this schema:
        {{
            "contact": {{ "name": "", "email": "", "phone": "", "linkedin": "" }},
            "education_degree": "",
            "education_college": "",
            "skills": ["Python", "SQL", ...],
            "projects": [
                {{ "title": "Project 1", "tech_stack": "Python, Pandas" }},
                {{ "title": "Project 2", "tech_stack": "React, Node" }},
                ... (Extract ALL projects found)
            ],
            "years_experience": ""
        }}
        """

        response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        json_data = json.loads(response.text)
        return ResumeData(**json_data)

    except Exception as e:
        st.error(f"AI Error: {e}")
        return None

def convert_to_csv(resumes: List[ResumeData]):
    """
    Converts the list of Resume objects into a CSV string.
    """
    csv_rows = []
    for r in resumes:
        # Flatten ALL projects into a single string for the CSV cell
        # Format: "Title (Tech) | Title (Tech)"
        # This loop will now include every single project found in the list
        project_str = " | ".join([f"{p.title} ({p.tech_stack})" for p in r.projects])
        
        csv_rows.append({
            "Name": r.contact.name,
            "Email": r.contact.email,
            "Phone": r.contact.phone,
            "LinkedIn": r.contact.linkedin,
            "Degree": r.education_degree,
            "College": r.education_college,
            "Experience": r.years_experience,
            "Skills": ", ".join(r.skills[:15]), # Increased limit to show more skills
            "Total Projects": len(r.projects), # Added column to verify count
            "Projects Details": project_str
        })
    
    df = pd.DataFrame(csv_rows)
    return df.to_csv(index=False).encode('utf-8')

# ==========================================
# 4. STREAMLIT UI
# ==========================================

st.set_page_config(page_title="Resume to CSV", layout="wide")

st.title("📄 Secure Resume Batch Processor")
st.markdown("Upload resumes. Extracts **ALL** projects and details.")

# Check for API Key on startup
if not GOOGLE_API_KEY:
    st.warning("⚠️ No API Key found. Please check your .env file.")
else:
    st.success("✅ API Key Loaded Securely")

uploaded_files = st.file_uploader("Upload PDF Resumes", type=["pdf"], accept_multiple_files=True)

if uploaded_files and GOOGLE_API_KEY:
    if st.button(f"Process {len(uploaded_files)} Files"):
        
        results = []
        progress_bar = st.progress(0)
        
        for idx, file in enumerate(uploaded_files):
            # 1. Read
            file_bytes = file.read()
            raw_text = extract_text_from_pdf(file_bytes)
            
            # 2. Analyze
            with st.spinner(f"Reading {file.name}..."):
                data = analyze_resume_with_ai(raw_text)
                if data:
                    results.append(data)
            
            progress_bar.progress((idx + 1) / len(uploaded_files))
        
        if results:
            st.success("✅ Done! All projects extracted.")
            
            # Convert to CSV
            csv_data = convert_to_csv(results)
            
            # Show Preview
            df_preview = pd.read_csv(io.BytesIO(csv_data))
            st.dataframe(df_preview, use_container_width=True)
            
            # Download Button
            st.download_button(
                label="📥 Download CSV Report",
                data=csv_data,
                file_name="resume_report.csv",
                mime="text/csv"

            )


