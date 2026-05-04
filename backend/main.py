from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agents.graph import create_coo_graph
from utils.rag import RAGManager
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

graph = create_coo_graph()
rag = RAGManager()

@app.on_event("startup")
async def startup():
    # Index SOPs on startup
    sop_path = os.path.join("..", "data", "sops", "catering_standard.md")
    if os.path.exists(sop_path):
        rag.ingest_sop(sop_path)
        print("SOPs indexed.")

@app.get("/audit")
async def run_audit():
    log_path = os.path.join("..", "data", "logs", "daily_ops.csv")
    initial_state = {
        "ops_log_path": log_path,
        "parsed_logs": [],
        "violations": [],
        "report": "",
        "health_score": 100
    }
    result = graph.invoke(initial_state)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) # Use 8001 to avoid conflict with Project 5
