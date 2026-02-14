from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import faiss, pickle, io
from PIL import Image
from models.gemini_llm import GeminiLLM

app = FastAPI()
model = SentenceTransformer('all-MiniLM-L6-v2')
gemini = GeminiLLM()

# మీ పాత డేటాబేస్ ని లోడ్ చేస్తున్నాం
try:
    index = faiss.read_index("embeddings/krishi_faiss.index")
    with open("embeddings/meta.pkl", "rb") as f: metadata = pickle.load(f)
except: print("⚠️ డేటాబేస్ ఫైల్స్ దొరకలేదు!")

class QueryRequest(BaseModel):
    text: str
    mode: str
    language: str

@app.post("/query")
def text_search(req: QueryRequest):
    try:
        query_vec = model.encode([req.text])
        _, indices = index.search(query_vec, k=1)
        context = metadata['a'][indices[0][0]]
        
        if req.mode == "online":
            return {"response": gemini.get_answer(context, req.text, req.language)}
        return {"response": context}
    except Exception as e:
        return {"response": "క్షమించండి అన్న, సర్వర్ లో చిన్న సమస్య వచ్చింది."}

# IMAGE ERROR ఫिक्स ఇక్కడే ఉంది (Form data వాడటం)
@app.post("/analyze_image")
async def analyze_plant(file: UploadFile = File(...), query: str = Form(...), language: str = Form(...)):
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))
        res = gemini.analyze_image(image, query, language)
        return {"response": res}
    except Exception as e:
        return {"response": "ఫోటో చూడటంలో ఇబ్బంది వచ్చింది అన్న. మళ్ళీ ట్రై చేయండి."}