from fastapi import FastAPI
from pydantic import BaseModel
import ollama

class PromptRequest(BaseModel):
    prompt: str

app = FastAPI()

@app.post("/generate")
def generate(request: PromptRequest):
    prompt = request.prompt
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    return {"response": response["message"]["content"]}
