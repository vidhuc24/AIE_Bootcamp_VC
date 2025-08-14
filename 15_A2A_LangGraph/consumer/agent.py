import os
from typing import Any, Dict

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from consumer.a2a_tool import call_provider_agent


class ConsumerAgent:
    SYSTEM_INSTRUCTION = (
        "You are a simple routing agent. Prefer to delegate the user's question to the external provider via the 'call_provider_agent' tool. "
        "Summarize or clarify only if strictly necessary."
    )

    def __init__(self) -> None:
        self.model = ChatOpenAI(
            model=os.getenv("CONSUMER_LLM_MODEL", os.getenv("TOOL_LLM_NAME", "gpt-4o-mini")),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_api_base=os.getenv("TOOL_LLM_URL", "https://api.openai.com/v1"),
            temperature=0,
        )
        self.memory = MemorySaver()
        self.graph = create_react_agent(
            self.model,
            tools=[call_provider_agent],
            checkpointer=self.memory,
            prompt=self.SYSTEM_INSTRUCTION,
        )

    def stream(self, query: str, thread_id: str) -> Any:
        inputs: Dict[str, Any] = {"messages": [("user", query)]}
        config: Dict[str, Any] = {"configurable": {"thread_id": thread_id}}
        return self.graph.stream(inputs, config, stream_mode="values") 