import pandas as pd
from typing import TypedDict, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from utils.rag import RAGManager
import os

# Initialize components
llm = ChatOpenAI(
    base_url="http://localhost:8080/v1",
    api_key="not-needed",
    model="qwen"
)
rag = RAGManager()

class COOState(TypedDict):
    ops_log_path: str
    parsed_logs: List[dict]
    violations: List[str]
    report: str
    health_score: int

def snoop_node(state: COOState):
    print("---SNOOPING ON LOGS---")
    df = pd.read_csv(state["ops_log_path"])
    return {"parsed_logs": df.to_dict('records')}

def auditor_node(state: COOState):
    print("---AUDITING OPERATIONS---")
    logs = state["parsed_logs"]
    violations = []
    
    for log in logs:
        # Check rule for each activity
        query = f"What are the rules for {log['Activity']}?"
        rules = rag.query_sops(query)
        
        prompt = f"""
        Compare this operational log entry against the business rules.
        LOG ENTRY: {log}
        RULES: {rules}
        
        If there is a violation (e.g. time delay, temperature error), describe it clearly.
        If no violation, respond with 'PASS'.
        """
        response = llm.invoke([HumanMessage(content=prompt)])
        if "PASS" not in response.content:
            violations.append(f"Task {log['Task_ID']}: {response.content}")
            
    return {"violations": violations}

def strategist_node(state: COOState):
    print("---GENERATING COO REPORT---")
    violations = "\n".join(state["violations"])
    
    prompt = f"""
    Based on these operational violations:
    {violations}
    
    1. Calculate a Health Score (0-100%).
    2. Provide 3 specific strategic recommendations for the Business Owner.
    3. Write a brief executive summary.
    
    Format:
    HEALTH_SCORE: [Score]
    SUMMARY: [Summary]
    TIPS: [Tips]
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    
    # Extract score (very simple parser)
    score = 100
    try:
        if "HEALTH_SCORE:" in response.content:
            score = int(response.content.split("HEALTH_SCORE:")[1].split("\n")[0].strip().replace("%", ""))
    except:
        pass
        
    return {"report": response.content, "health_score": score}
