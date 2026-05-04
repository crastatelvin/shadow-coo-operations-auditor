from langgraph.graph import StateGraph, END
from agents.nodes import COOState, snoop_node, auditor_node, strategist_node

def create_coo_graph():
    workflow = StateGraph(COOState)
    
    workflow.add_node("snoop", snoop_node)
    workflow.add_node("audit", auditor_node)
    workflow.add_node("strategize", strategist_node)
    
    workflow.set_entry_point("snoop")
    workflow.add_edge("snoop", "audit")
    workflow.add_edge("audit", "strategize")
    workflow.add_edge("strategize", END)
    
    return workflow.compile()
