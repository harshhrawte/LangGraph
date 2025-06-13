from fastapi import FastAPI
from langgraph_app.graph import run_langgraph

app = FastAPI()

@app.get("/generate-report")
def generate():
    result = run_langgraph()
    return {"report": result["report"]}
