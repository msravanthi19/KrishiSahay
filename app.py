import streamlit as st
import requests
from gtts import gTTS
import base64

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="KrishiSahay Pro",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. PROFESSIONAL STYLING (CSS) ---
st.markdown("""
<style>
    /* Main Background with Soft Gradient */
    .stApp {
        background: linear-gradient(135deg, #f1f8e9 0%, #dcedc8 100%);
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 2px solid #a5d6a7;
    }

    /* Header Title */
    .main-title {
        color: #1b5e20;
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 0px;
    }
    
    .sub-title {
        color: #558b2f;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 30px;
        font-weight: 500;
    }

    /* Result Card - The "Wow" Factor */
    .result-box {
        background-color: #ffffff;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border-left: 10px solid #2e7d32;
        margin-top: 20px;
        animation: slideIn 0.5s ease-out;
    }
    
    .result-text {
        font-size: 20px;
        color: #2e7d32;
        line-height: 1.8;
        font-weight: 500;
    }

    /* Custom Buttons */
    .stButton>button {
        background: linear-gradient(45deg, #2e7d32, #43a047);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 15px 30px;
        font-size: 18px;
        font-weight: bold;
        width: 100%;
        box-shadow: 0 4px 15px rgba(46, 125, 50, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(46, 125, 50, 0.4);
    }

    /* Animations */
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Input Fields */
    .stTextInput>div>div>input {
        border-radius: 15px;
        border: 2px solid #a5d6a7;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. HEADER SECTION ---
st.markdown('<div class="main-title">🌾 KrishiSahay <span style="color:#43a047">Pro</span></div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">AI Powered • Farmer Friendly • Voice Enabled</div>', unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3022/3022984.png", width=100)
    st.markdown("## ⚙️ Control Panel")
    
    lang = st.selectbox("🗣️ Language / భాష:", ["Telugu", "English", "Hindi"])
    mode = st.radio("📡 Connection Mode:", ["Online (AI Brain)", "Offline (Local DB)"])
    
    st.markdown("---")
    st.info("💡 **Pro Tip:** Upload clear photos of leaves for better diagnosis.")
    st.markdown("---")
    st.caption("Ver 2.0 | Made with ❤️")

# --- AUDIO FUNCTION ---
def play_voice(text, language):
    codes = {'Telugu': 'te', 'English': 'en', 'Hindi': 'hi'}
    try:
        tts = gTTS(text=text, lang=codes.get(language, 'te'))
        tts.save("response.mp3")
        
        # Audio Player with Custom Header
        st.markdown(f'<p style="color:#1b5e20; font-weight:bold; margin-top:10px;">🔊 Listen to Advice ({language}):</p>', unsafe_allow_html=True)
        st.audio("response.mp3")
    except: 
        st.warning("Audio generation failed.")

# --- 5. MAIN INTERFACE (TABS) ---
tab1, tab2 = st.tabs(["💬 **Krishi Chat**", "📸 **Plant Doctor**"])

# === TAB 1: CHAT BOT ===
with tab1:
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"### 👋 Namaste! Ask in **{lang}**")
        q = st.text_input("Type your farming query here...", label_visibility="collapsed", placeholder="Example: వరిలో అగ్గి తెగులు నివారణ ఎలా?")
    
    with col2:
        st.write("") # Spacing
        st.write("") 
        submit = st.button("🚀 Get Advice")

    if submit and q:
        with st.spinner("🤖 Consulting Agriculture Expert..."):
            try:
                res = requests.post("http://127.0.0.1:8000/query", 
                                    json={"text": q, "mode": "online" if "Online" in mode else "offline", "language": lang}).json()
                ans = res["response"]
                
                # Pro Result Card
                st.markdown(f"""
                <div class="result-box">
                    <h3 style="color:#2e7d32; margin-top:0;">✅ Expert Suggestion:</h3>
                    <hr style="border:1px dashed #a5d6a7;">
                    <div class="result-text">{ans}</div>
                </div>
                """, unsafe_allow_html=True)
                
                play_voice(ans, lang)
            except Exception as e:
                st.error("Server connection failed. Is Backend running?")

# === TAB 2: PLANT DOCTOR ===
with tab2:
    st.markdown("### 🩺 AI Disease Diagnosis")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("""
        <div style="background:white; padding:20px; border-radius:15px; border:2px dashed #a5d6a7; text-align:center;">
            <h4>📂 Upload Crop Photo</h4>
            <small>Supports JPG, PNG</small>
        </div>
        """, unsafe_allow_html=True)
        img = st.file_uploader("", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
        
        if img:
            st.image(img, caption="Preview", use_column_width=True)

    with c2:
        if img:
            st.write("")
            st.write("")
            if st.button("🔬 Start Diagnosis"):
                with st.spinner("🔍 Scanning leaf cells with AI Vision..."):
                    try:
                        response = requests.post(
                            "http://127.0.0.1:8000/analyze_image", 
                            files={"file": img.getvalue()}, 
                            data={"query": "Identify", "language": lang}
                        )
                        if response.status_code == 200:
                            ans = response.json().get("response", "Error")
                            
                            # Pro Diagnosis Card
                            st.markdown(f"""
                            <div class="result-box" style="border-left: 10px solid #d32f2f;">
                                <h3 style="color:#d32f2f; margin-top:0;">🦠 Diagnosis Report:</h3>
                                <div class="result-text" style="color:#333;">{ans}</div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            play_voice(ans, lang)
                        else:
                            st.error("Backend Error.")
                    except Exception as e:
                        st.error(f"Error: {e}")
        else:
            st.info("👈 Please upload an image on the left to start.")
            st.image("https://cdn-icons-png.flaticon.com/512/10609/10609222.png", width=200)