from langgraph.graph import StateGraph
from langgraph_app.agents.fetch_agent import fetch_customer_data
from langgraph_app.agents.report_agent import generate_report
from typing import TypedDict, List, Dict, Any

class AgentState(TypedDict):
    data: List[Dict[str, Any]]
    report: str

def run_langgraph():
    graph = StateGraph(AgentState) 

    def fetch_step(state: AgentState) -> AgentState:
        data = fetch_customer_data()
        return {"data": data}

    def report_step(state: AgentState) -> AgentState:
        report = generate_report(state["data"])
        return {"report": report}

    graph.add_node("fetch_data", fetch_step)
    graph.add_node("generate_report", report_step)

    graph.set_entry_point("fetch_data")
    graph.add_edge("fetch_data", "generate_report")
    graph.set_finish_point("generate_report")

    compiled = graph.compile()
    return compiled.invoke({})
