# Consumer Agent (LangGraph) using A2A to call provider in `app/`

## Run Provider

```bash
uv run python -m app --host localhost --port 10000
```

## Run Consumer

```bash
# Optionally set the provider URL (defaults to http://localhost:10000)
export PROVIDER_BASE_URL=http://localhost:10000

# Ensure your OpenAI key is available for the local LLM bindings
export OPENAI_API_KEY=...

# Call through the consumer agent
uv run python -m consumer --query "What are the latest developments in artificial intelligence?"
```

## Notes
- The consumer uses `a2a-sdk` to resolve the provider's `AgentCard` and streams the response.
- You may adjust the model via `CONSUMER_LLM_MODEL`, or inherit from `TOOL_LLM_NAME`.
- Increase timeouts by editing `consumer/a2a_tool.py` if needed. 