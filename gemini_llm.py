import os
import google.generativeai as genai
from dotenv import load_dotenv

# Path setup
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
env_path = os.path.join(root_dir, ".env")
load_dotenv(env_path)

class GeminiLLM:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        
        # --- YOUR EXACT MAGIC FIX LIST ---
        # మీ అకౌంట్ కి పర్ఫెక్ట్ గా పని చేసిన మోడల్స్ ఇవే
        self.models_to_try = [
            'gemini-2.5-flash',          # Newest Model (Likely Free)
            'gemini-2.0-flash-lite',     # Lite Model (Low Usage)
            'gemini-flash-latest',       # Generic Fallback
            'gemini-1.5-flash'           # Last Resort
        ]
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            print(f"✅ Gemini AI Configured. Will try: {self.models_to_try}")
        else:
            print("❌ API Key Missing! Please check .env file.")

    def get_answer(self, context, query, language="Telugu"):
        if not self.api_key:
            return "API Key Missing. Please check server logs."
        
        # Farmer-friendly, human-like prompt
        prompt = f"""
        Role: Friendly Agriculture Expert (KrishiSahay).
        Context: {context}
        Question: {query}
        
        STRICT RULES:
        1. Start with a warm greeting like 'Namaste Anna' or 'Namaste Bhayya'.
        2. Answer ONLY in {language}.
        3. Give exactly 3 simple bullet points. Tell what to DO practically.
        4. Speak like a human, use local farmer language.
        """

        # Loop through your proven model list
        for model_name in self.models_to_try:
            try:
                print(f"🔄 Trying Model: {model_name}...")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                
                print(f"✅ Success with {model_name}!")
                return response.text
                
            except Exception as e:
                # 404 (Not Found) లేదా 429 (Quota) వస్తే నెక్స్ట్ మోడల్ కి వెళ్తుంది
                print(f"⚠️ Failed with {model_name}: {e}")
                continue 
        
        return "క్షమించండి అన్న, సర్వర్ కొంచెం బిజీగా ఉంది. పక్కన ఉన్న 'Offline Mode' వాడుకోవా."

    def analyze_image(self, image, query, language="Telugu"):
        # Human-like prompt for images
        prompt = f"నమస్తే అన్న! ఈ ఫోటోని చూసి, జబ్బు ఏంటో, దానికి ఏ మందు కొట్టాలో 3 ముక్కల్లో స్నేహితుడిలా చెప్పు. భాష: {language}."
        
        for model_name in self.models_to_try:
            try:
                print(f"📸 Vision: Trying Model: {model_name}...")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content([prompt, image])
                return response.text
            except Exception as e:
                print(f"⚠️ Vision failed with {model_name}: {e}")
                continue
                
        return "అన్న, ఫోటో సరిగ్గా అర్థం కావట్లేదు. సర్వర్ బిజీగా ఉంది."