# Multi-Agent Research Flow Chart

## Simplified Flow for: "What are the current quantum computing research breakthroughs and underlying theory?"

```
User Query
    │
    ▼
┌─────────────┐
│ Supervisor  │
│   Agent     │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│   Search    │
│   Agent     │
│ (Tavily)    │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ Supervisor  │
│   Agent     │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ ArxivRetri- │
│   ever      │
│  Agent      │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ Supervisor  │
│   Agent     │
└─────┬───────┘
      │
      ▼
  FINISH
```

## Flow Summary:
**User Query** → **Supervisor** → **Search** → **Supervisor** → **ArxivRetriever** → **Supervisor** → **FINISH**

## Agent Roles:
- **Supervisor**: Routes between agents, evaluates completeness
- **Search**: Current developments and industry news
- **ArxivRetriever**: Academic papers and theoretical research 