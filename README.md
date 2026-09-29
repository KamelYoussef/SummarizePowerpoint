"""
LangGraph ReAct agent backed by a local Gemma 4 model running in Ollama.

Install:
    pip install langchain-ollama langgraph langchain-core

Make sure Ollama is running and the model is pulled, e.g.:
    ollama pull gemma4        # or whatever tag you used, e.g. gemma4:4b
"""

from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent

MODEL_NAME = "gemma4"  # must match `ollama list` exactly, e.g. "gemma4:4b"


# ---------------------------------------------------------------------------
# 1) Define tools with the @tool decorator. The docstring + type hints
#    become the schema the model sees, so keep them accurate.
# ---------------------------------------------------------------------------
@tool
def get_current_weather(location: str, unit: str = "celsius") -> dict:
    """Get the current weather for a location.

    Args:
        location: City and country/state, e.g. "Tokyo, JP".
        unit: "celsius" or "fahrenheit".
    """
    # Replace with a real API call
    return {"location": location, "temperature": 15, "unit": unit, "weather": "sunny"}


@tool
def add_numbers(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b


tools = [get_current_weather, add_numbers]

# ---------------------------------------------------------------------------
# 2) Create the model. temperature=0 keeps tool-selection more deterministic.
# ---------------------------------------------------------------------------
llm = ChatOllama(model=MODEL_NAME, temperature=0)

# ---------------------------------------------------------------------------
# 3) Build the agent. create_react_agent wires up the loop:
#    call model -> if tool_calls, run tools -> feed results back -> repeat
#    until the model replies with plain text.
# ---------------------------------------------------------------------------
agent = create_react_agent(llm, tools)


def ask(prompt: str) -> str:
    result = agent.invoke({"messages": [{"role": "user", "content": prompt}]})
    return result["messages"][-1].content


if __name__ == "__main__":
    print(ask("What's the weather in Tokyo, and what is 12.5 + 30?"))

    # To see every step (model turns + tool calls + tool results):
    for step in agent.stream(
        {"messages": [{"role": "user", "content": "What's the weather in Paris?"}]},
        stream_mode="values",
    ):
        step["messages"][-1].pretty_print()
