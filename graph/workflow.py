from graph.agent import *
from langgraph.graph import START, END, StateGraph

graph = StateGraph(State)

graph.add_node("question_generator", question_generator)
graph.add_node("evaluator", evaluator)

graph.add_conditional_edges(START, intent_router_node,{"evaluator":"evaluator", "question_generator" : "question_generator"})
graph.add_edge("evaluator", END)
graph.add_edge("question_generator", END)

app = graph.compile()