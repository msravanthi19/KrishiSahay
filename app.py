
import streamlit as st
import requests
from gtts import gTTS
from streamlit_mic_recorder import speech_to_text

# --- 1. PAGE CONFIGURATION (App laaga kanipinchadaniki) ---
st.set_page_config(page_title="KrishiSahay", page_icon="🌾", layout="centered")

# --- 2. PREMIUM CSS STYLING (Streamlit default look ni hide cheyadaniki) ---
st.markdown("""
<style>
    /* Default Streamlit Menu, Header, Footer hide chestunnam */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Background & Font */
    .stApp {
        background-color: #f7faf5;
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* Custom Modern Header */
    .app-header {
        background: linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%);
        padding: 30px 20px;
        border-radius: 0 0 30px 30px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        margin-top: -60px;
        margin-bottom: 30px;
    }
    .app-header h1 { color: white; font-size: 2.8rem; margin: 0; font-weight: 800; letter-spacing: 1px;}
    .app-header p { color: #c8e6c9; font-size: 1.1rem; margin-top: 8px; font-weight: 500; }
    
    /* Clean Cards for Output */
    .answer-card {
        background: white;
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #e0e0e0;
        border-top: 8px solid #4caf50;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin-top: 20px;
        font-size: 20px;
        color: #1b5e20;
        line-height: 1.7;
    }
    
    /* Input Box Styling */
    .stTextInput>div>div>input {
        border-radius: 12px;
        border: 2px solid #c8e6c9;
        padding: 15px;
        font-size: 18px;
        background-color: white;
    }
    .stTextInput>div>div>input:focus {
        border-color: #4caf50;
        box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
    }
    
    /* Premium Buttons */
    .stButton>button {
        background: #4caf50;
        color: white;
        border-radius: 12px;
        padding: 12px 20px;
        font-weight: bold;
        font-size: 18px;
        border: none;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(76, 175, 80, 0.2);
    }
    .stButton>button:hover {
        background: #388e3c;
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(56, 142, 60, 0.3);
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: white;
        padding: 10px;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        border-radius: 10px;
        padding: 0 25px;
        font-size: 18px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e8f5e9;
        color: #2e7d32;
        font-weight: bold;
        border-bottom: none;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. CUSTOM APP HEADER ---
st.markdown("""
<div class="app-header">
    <h1>🌾 కృషీసహాయ్</h1>
    <p>రైతులకు స్నేహితుడు • సాంకేతిక తోడు</p>
</div>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR (Clean Settings) ---
with st.sidebar:
    st.markdown("<h2 style='color:#2e7d32;'>⚙️ సెట్టింగ్స్</h2>", unsafe_allow_html=True)
    lang = st.selectbox("భాష (Language):", ["Telugu", "English", "Hindi"])
    mode = st.radio("నెట్‌వర్క్:", ["Online (AI Brain)", "Offline (Local DB)"])
    st.markdown("---")
    st.caption("KrishiSahay AI Engine")

# --- 5. HELPER FUNCTION ---
def play_voice(text, language):
    codes = {'Telugu': 'te', 'English': 'en', 'Hindi': 'hi'}
    try:
        tts = gTTS(text=text, lang=codes.get(language, 'te'))
        tts.save("answer.mp3")
        st.markdown(f'<p style="color:#e65100; font-weight:bold; margin-top:15px;">🔊 వినండి:</p>', unsafe_allow_html=True)
        st.audio("answer.mp3")
    except: pass

# --- 6. MAIN TABS ---
tab1, tab2 = st.tabs(["🎙️ వాయిస్ / చాట్", "📸 ఆకు పరీక్ష"])

# === TAB 1: CHAT BOT ===
with tab1:
    st.markdown("<h4 style='color:#1b5e20;'>మీ సమస్యను చెప్పండి:</h4>", unsafe_allow_html=True)
    
    # డైరెక్ట్ వాయిస్ ప్రాసెసింగ్ (Browser in-built AI)
    lang_code = {'Telugu': 'te-IN', 'English': 'en-IN', 'Hindi': 'hi-IN'}.get(lang, 'te-IN')
    
    spoken_text = speech_to_text(
        language=lang_code,
        start_prompt="🎙️ ఇక్కడ నొక్కి మాట్లాడండి",
        stop_prompt="⏹️ ఆపడానికి నొక్కండి",
        just_once=True,
        key='STT'
    )
    
    st.markdown("<p style='text-align:center; color:#757575; font-size:14px; margin: 10px 0;'>— లేదా —</p>", unsafe_allow_html=True)
    
    typed_q = st.text_input("", placeholder="ఇక్కడ టైప్ చేయండి...", label_visibility="collapsed")
    submit_btn = st.button("సమాధానం తీసుకురా")

    final_query = ""
    if spoken_text:
        st.success(f"🗣️ మీరు అడిగింది: **{spoken_text}**")
        final_query = spoken_text
    elif submit_btn and typed_q:
        final_query = typed_q

    # Backend Request
    if final_query:
        with st.spinner("సమాధానం వెతుకుతున్నాను..."):
            try:
                res = requests.post("http://127.0.0.1:8000/query", 
                                    json={"text": final_query, "mode": "online" if "Online" in mode else "offline", "language": lang})
                if res.status_code == 200:
                    ans = res.json().get("response", "Error")
                    st.markdown(f'<div class="answer-card"><b>సలహా:</b><br><br>{ans}</div>', unsafe_allow_html=True)
                    play_voice(ans, lang)
                else:
                    st.error("సర్వర్ తో కనెక్ట్ కాలేకపోయాను.")
            except:
                st.error("బ్యాకెండ్ సర్వర్ రన్ అవ్వట్లేదు. Uvicorn టెర్మినల్ చెక్ చేయండి.")

# === TAB 2: PLANT DOCTOR ===
with tab2:
    st.markdown("<h4 style='color:#1b5e20;'>ఫోటో అప్‌లోడ్ చేయండి:</h4>", unsafe_allow_html=True)
    
    img = st.file_uploader("", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
    
    if img:
        st.image(img, use_column_width=True, caption="మీరు పెట్టిన ఫోటో")
        if st.button("రిపోర్ట్ చూడండి"):
            with st.spinner("విశ్లేషిస్తున్నాను..."):
                try:
                    response = requests.post(
                        "http://127.0.0.1:8000/analyze_image", 
                        files={"file": img.getvalue()}, 
                        data={"query": "Identify disease", "language": lang}
                    )
                    if response.status_code == 200:
                        ans = response.json().get("response", "Error")
                        st.markdown(f'<div class="answer-card" style="border-top-color:#d32f2f;"><b>రిపోర్ట్:</b><br><br>{ans}</div>', unsafe_allow_html=True)
                        play_voice(ans, lang)
                except:
                    st.error("సర్వర్ తో కనెక్ట్ కాలేకపోయాను.")