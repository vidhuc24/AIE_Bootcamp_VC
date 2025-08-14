import os
import asyncio
from typing import Any, Dict, List

import httpx
from a2a.client import A2ACardResolver, A2AClient
from a2a.types import MessageSendParams, SendStreamingMessageRequest
from a2a.utils.constants import AGENT_CARD_WELL_KNOWN_PATH
from langchain_core.tools import tool


PROVIDER_BASE_URL = os.getenv("PROVIDER_BASE_URL", "http://localhost:10000")


def _extract_texts_from_chunk_dict(obj: Any, results: List[str]) -> None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "text" and isinstance(v, str):
                results.append(v)
            else:
                _extract_texts_from_chunk_dict(v, results)
    elif isinstance(obj, list):
        for item in obj:
            _extract_texts_from_chunk_dict(item, results)


async def _query_provider_async(query: str, base_url: str) -> str:
    timeout = httpx.Timeout(60.0)
    async with httpx.AsyncClient(timeout=timeout) as httpx_client:
        resolver = A2ACardResolver(httpx_client=httpx_client, base_url=base_url)
        agent_card = await resolver.get_agent_card(relative_card_path=AGENT_CARD_WELL_KNOWN_PATH)
        client = A2AClient(httpx_client=httpx_client, agent_card=agent_card)

        payload: Dict[str, Any] = {
            "message": {
                "role": "user",
                "parts": [
                    {"kind": "text", "text": query}
                ],
                "message_id": os.urandom(8).hex(),
            },
        }
        streaming_request = SendStreamingMessageRequest(
            id=os.urandom(8).hex(),
            params=MessageSendParams(**payload),
        )

        texts: List[str] = []
        async for chunk in client.send_message_streaming(streaming_request):
            # Convert chunk to dict and mine all text fields
            chunk_dict = chunk.model_dump(mode="json", exclude_none=True)
            _extract_texts_from_chunk_dict(chunk_dict, texts)

        # Fallback if nothing extracted
        if not texts:
            return "No text received from provider."

        # Return the last meaningful text block
        # Deduplicate while preserving order, then join last few messages
        dedup: List[str] = []
        seen = set()
        for t in texts:
            if t not in seen and t.strip():
                dedup.append(t)
                seen.add(t)
        return dedup[-1] if dedup else texts[-1]


@tool("call_provider_agent", return_direct=False)
def call_provider_agent(query: str) -> str:
    """Use this tool to delegate a user query to the external provider agent via the A2A protocol. Input must be the user's question in plain text. The tool returns the provider's final textual response."""
    base_url = PROVIDER_BASE_URL
    return asyncio.run(_query_provider_async(query, base_url)) 