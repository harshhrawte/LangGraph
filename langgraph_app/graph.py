from langgraph.graph import StateGraph
from langgraph_app.agents.fetch_agent import fetch_customer_data
from langgraph_app.agents.report_agent import generate_report
from typing import TypedDict, List, Dict, Any

# 1. Define your LangGraph state
class AgentState(TypedDict):
    data: List[Dict[str, Any]]
    report: str

# 2. Run the LangGraph agent
def run_langgraph():
    graph = StateGraph(AgentState)  # ✅ FIXED: Passed the state schema

    # Step 1: Fetch data from PostgreSQL
    def fetch_step(state: AgentState) -> AgentState:
        data = fetch_customer_data()
        return {"data": data}

    # Step 2: Generate LLM report
    def report_step(state: AgentState) -> AgentState:
        report = generate_report(state["data"])
        return {"report": report}

    # Setup flow
    graph.add_node("fetch_data", fetch_step)
    graph.add_node("generate_report", report_step)

    graph.set_entry_point("fetch_data")
    graph.add_edge("fetch_data", "generate_report")
    graph.set_finish_point("generate_report")

    compiled = graph.compile()
    return compiled.invoke({})
