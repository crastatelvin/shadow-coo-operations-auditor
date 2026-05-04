from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agents.graph import create_coo_graph
from utils.rag import RAGManager
from utils.watcher import LogWatcher
import os
import threading

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

graph = create_coo_graph()
rag = RAGManager()

def on_log_change(file_path):
    print(f"Auto-Audit Triggered for: {file_path}")
    # Simple trick: we just call the logic in a new thread or wait
    # For now, we'll just log it. The next /audit call will see the new data.
    # Alternatively, we could run the graph immediately.
    initial_state = {
        "ops_log_path": file_path,
        "parsed_logs": [],
        "violations": [],
        "report": "",
        "health_score": 100
    }
    graph.invoke(initial_state)

@app.on_event("startup")
async def startup():
    # Index SOPs on startup
    sop_path = os.path.join("..", "data", "sops", "catering_standard.md")
    if os.path.exists(sop_path):
        rag.ingest_sop(sop_path)
        print("SOPs indexed.")
    
    # Start Log Watcher
    log_dir = os.path.join("..", "data", "logs")
    watcher = LogWatcher(log_dir, on_log_change)
    thread = threading.Thread(target=watcher.start, daemon=True)
    thread.start()

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
    
    # Archive the report
    try:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"report_{timestamp}.md"
        report_path = os.path.join("..", "data", "reports", report_filename)
        
        with open(report_path, 'w') as f:
            f.write(f"# COO Executive Report - {timestamp}\n\n")
            f.write(result["report"])
            
    except Exception as e:
        print(f"Failed to archive report: {e}")
        
    return result

@app.get("/history")
async def get_history():
    reports_dir = os.path.join("..", "data", "reports")
    if not os.path.exists(reports_dir):
        return []
    
    files = os.listdir(reports_dir)
    # Return just the filenames for now
    return sorted(files, reverse=True)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) # Use 8001 to avoid conflict with Project 5
