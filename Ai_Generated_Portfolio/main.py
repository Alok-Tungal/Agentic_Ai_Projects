import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import zipfile
import PyPDF2
import re
import streamlit.components.v1 as components

# -----------------------------
# 1. Configuration & Setup
# -----------------------------
# load_dotenv()
# os.environ["GOOGLE_API_KEY"] = os.getenv("gemini")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("gemini")

if not GOOGLE_API_KEY:
    st.error("Google API Key not found. Please set it in environment variables.")
    st.stop()


st.set_page_config(
    page_title="Portfolio.AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# 2. "Cosmic Intelligence" Premium CSS (Streamlit UI)
# -----------------------------
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #020617; /* Deep Navy */
        background-image: 
            radial-gradient(at 0% 0%, #1e1b4b 0px, transparent 50%),
            radial-gradient(at 100% 0%, #312e81 0px, transparent 50%);
    }

    /* Typography */
    h1, h2, h3, p, div {
        font-family: 'Inter', sans-serif !important;
        color: white;
    }
    
    .gradient-text {
        background: linear-gradient(135deg, #22d3ee 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }

    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: rgba(30, 41, 59, 0.5);
        border: 2px dashed #475569;
        border-radius: 12px;
        padding: 20px;
        transition: border 0.3s ease;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #22d3ee;
        background: rgba(30, 41, 59, 0.8);
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #0ea5e9, #8b5cf6);
        border: none;
        color: white;
        font-weight: 600;
        padding: 12px 24px;
        border-radius: 8px;
        width: 100%;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 14px 0 rgba(139, 92, 246, 0.5);
        color: white;
    }

    /* Preview Box */
    .preview-box {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid #1e293b;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        color: #94a3b8;
        height: 300px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
    }
    
    /* Success Messages */
    .stSuccess {
        background-color: rgba(16, 185, 129, 0.1);
        border: 1px solid #10b981;
        color: #10b981;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 3. Header Section
# -----------------------------
st.markdown("<h1 style='text-align: center;'>AI <span class='gradient-text'>Portfolio Generator</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; margin-bottom: 40px;'>Upload your resume, and let AI build you a stunning personal website in seconds.</p>", unsafe_allow_html=True)

# -----------------------------
# 4. Helper Functions
# -----------------------------
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def parse_generated_content(content):
    """
    Parses the AI response into HTML, CSS, and JS blocks.
    """
    html_pattern = r"```html(.*?)```"
    css_pattern = r"```css(.*?)```"
    js_pattern = r"```javascript(.*?)```"
    
    html = re.search(html_pattern, content, re.DOTALL)
    css = re.search(css_pattern, content, re.DOTALL)
    js = re.search(js_pattern, content, re.DOTALL)
    
    return {
        "html": html.group(1).strip() if html else "",
        "css": css.group(1).strip() if css else "/* Error generating CSS */",
        "js": js.group(1).strip() if js else "// Error generating JS"
    }

# -----------------------------
# 5. Main Application Logic
# -----------------------------

# Session State
if 'preview_html' not in st.session_state:
    st.session_state['preview_html'] = None
if 'zip_path' not in st.session_state:
    st.session_state['zip_path'] = None

col1, col2 = st.columns([1, 1], gap="large")

# --- COLUMN 1: INPUT ---
with col1:
    st.markdown("### 1. Upload Resume")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="hidden")

    st.markdown("---")
    
    generate_btn = st.button("🚀 Generate Website Specification", type="primary")

    if uploaded_file and generate_btn:
        with st.spinner("✨ Analyzing Resume & Coding Website..."):
            try:
                # 1. Extract
                resume_text = extract_text_from_pdf(uploaded_file)

                # 2. Prompt (MULTI-FILE ARCHITECTURE)
                system_prompt = """
                You are a Senior Frontend Architect.
                
                GOAL: Create a Professional Portfolio Website based on the user's resume.
                
                DESIGN THEME (Cosmic Intelligence):
                - Background: #0f172a (Dark Slate)
                - Primary Accent: #38bdf8 (Sky Blue)
                - Secondary Accent: #818cf8 (Indigo)
                - Text: White / Light Gray
                - Font: 'Inter', sans-serif
                
                CRITICAL INSTRUCTIONS FOR FILE LINKING:
                1. You must generate 3 separate code blocks: HTML, CSS, and JavaScript.
                2. Inside the HTML, you MUST include this EXACT line in the <head>:
                   <link rel="stylesheet" href="style.css">
                3. Inside the HTML, you MUST include this EXACT line at the end of the <body>:
                   <script src="script.js"></script>
                4. Do NOT use internal <style> or <script> blocks. Use external files.
                
                OUTPUT FORMAT:
                Return exactly 3 markdown blocks:
                
                ```html
                ```
                
                ```css
                /* CSS Code */
                ```
                
                ```javascript
                /* JS Code */
                ```
                """
                
                model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=1.0)
                messages = [("system", system_prompt), ("human", resume_text)]
                response = model.invoke(messages)
                
                # 3. Parse Response
                parsed = parse_generated_content(response.content)
                
                # 4. Save Separate Files for ZIP
                with open("index.html", "w", encoding="utf-8") as f:
                    f.write(parsed['html'])
                with open("style.css", "w", encoding="utf-8") as f:
                    f.write(parsed['css'])
                with open("script.js", "w", encoding="utf-8") as f:
                    f.write(parsed['js'])
                
                # 5. Create ZIP with all 3 files
                with zipfile.ZipFile("portfolio.zip", "w") as z:
                    z.write("index.html")
                    z.write("style.css")
                    z.write("script.js")
                
                st.session_state['zip_path'] = "portfolio.zip"

                # 6. Create Preview HTML (Injecting CSS/JS specifically for the preview window)
                # We inject them here so the preview works in Streamlit without needing a server,
                # but the download ZIP still contains the separate files.
                preview_content = f"""
                <style>{parsed['css']}</style>
                {parsed['html']}
                <script>{parsed['js']}</script>
                """
                st.session_state['preview_html'] = preview_content
                
                st.success("Generation Complete! Files prepared.")

            except Exception as e:
                st.error(f"Error: {e}")

# --- COLUMN 2: PREVIEW & DOWNLOAD ---
with col2:
    st.markdown("### 2. Website Preview")
    
    if st.session_state['preview_html']:
        # Show the live preview
        components.html(st.session_state['preview_html'], height=450, scrolling=True)
    else:
        # Show the Placeholder
        st.markdown("""
        <div class="preview-box">
            <div style="font-size: 40px; margin-bottom: 10px;">💻</div>
            <div style="font-weight: bold;">Website preview will appear here</div>
            <div style="font-size: 0.9rem;">Upload your resume to start</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 3. Download Source Code")
    
    if st.session_state['zip_path']:
        with open(st.session_state['zip_path'], "rb") as fp:
            st.download_button(
                label="⬇️ Download Source Code (ZIP)",
                data=fp,
                file_name="My_Portfolio_Website.zip",
                mime="application/zip"
            )
    else:
        st.button("⬇️ Download Source Code (ZIP)", disabled=True)
        st.caption("Generate the website to enable the download button.")



        # var1="--html--htmlcode--html-- --css--csscode--css--  --js--javascript--js--"
        # var1.split('--html--')[1]
        # op :- htmlcode
        # var1.split('--css--')[1]
        # op :- csscode
        # var1.split('--js--')[1]
        # op :- jscode
