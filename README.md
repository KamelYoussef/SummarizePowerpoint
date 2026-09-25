"""
A more complete AI agent example: multi-tool ReAct agent running on
LangGraph, backed by a local vLLM deployment via ChatOpenAI.

pip install langgraph langchain-openai

Run:
    python agent_example.py
"""

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver


# ---------------------------------------------------------------------
# 1. LLM — pointed at your local vLLM pipeline
# ---------------------------------------------------------------------
llm = ChatOpenAI(
    model="gemma3:12b",
    base_url="http://localhost:8000/v1",
    api_key="not-needed",
    temperature=0,
)


# ---------------------------------------------------------------------
# 2. Tools — each @tool function is something the agent can decide to call.
#    Docstrings matter: the model reads them to decide when/how to use it.
# ---------------------------------------------------------------------
@tool
def calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression, e.g. '12 * (3 + 4)'."""
    try:
        # eval is fine here only because this is a local demo tool
        return str(eval(expression, {"__builtins__": {}}))
    except Exception as e:
        return f"Error evaluating expression: {e}"


@tool
def lookup_docs(query: str) -> str:
    """Search internal documentation for a given query and return a snippet."""
    # stub — replace with a real vector store / retriever call
    fake_docs = {
        "vllm": "vLLM is a high-throughput inference engine for LLMs.",
        "langgraph": "LangGraph lets you build stateful, graph-based agent workflows.",
    }
    for key, snippet in fake_docs.items():
        if key in query.lower():
            return snippet
    return "No matching documentation found."


@tool
def get_current_date() -> str:
    """Return today's date."""
    from datetime import date
    return date.today().isoformat()


tools = [calculator, lookup_docs, get_current_date]


# ---------------------------------------------------------------------
# 3. Agent — create_react_agent wires up the reason/act/observe loop.
#    A checkpointer gives the agent memory across turns of a conversation,
#    keyed by thread_id.
# ---------------------------------------------------------------------
checkpointer = InMemorySaver()

agent = create_react_agent(
    llm,
    tools=tools,
    checkpointer=checkpointer,
    prompt="You are a precise technical assistant. Use tools when they help "
           "you give an accurate answer, and cite which tool you used.",
)


# ---------------------------------------------------------------------
# 4. Run a multi-turn conversation — same thread_id keeps memory.
# ---------------------------------------------------------------------
if __name__ == "__main__":
    config = {"configurable": {"thread_id": "demo-session-1"}}

    turns = [
        "What's 42 * (17 - 5)?",
        "What is LangGraph, based on our docs?",
        "What was the first number I asked you to multiply?",  # tests memory
    ]

    for turn in turns:
        print(f"\n>>> USER: {turn}")
        result = agent.invoke({"messages": [("human", turn)]}, config=config)
        result["messages"][-1].pretty_print()
