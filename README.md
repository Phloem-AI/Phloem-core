# Phloem-core

Using different AI Agents for different parts of your work?

Phloem makes those **agents collaborate autonomously**. So when one Agent writes project plan, you don't have to paste it manually into the other Agent to implement it. Phloem will do it for you (for free!).

## Features

1. **Agent Interoperability:** Supports mainstream AI Agents to communicate with each other. 
2. **Authentication:** Uses *UUID API KEY auth* for agents.
3. **Secrets Management:** Securely conveys the necessary data, extracts out confidential information.
4. **Zero-Data Retention:** Stores data during communication — deletes once the message is transferred to the destined agent.

## Why Phloem Exists

Most agent-to-agent coordination breaks down in the same places:

- different vendors use different vocabularies for the same business concept
- handoffs lose meaning when context is copied loosely between systems
- agents can collide on the same task or overwrite each other’s work
- sensitive data can leak into the wrong place if policies are implicit
- audit trails are often incomplete or unavailable

Phloem is meant to make those handoffs explicit, policy-driven, and machine-checkable.

---

# Quick Start Guide

### → Hosted Version

Get Phloem now through the [website](https://phloem-ai.netlify.app)


### → Local Setup 

**Prerequisite:** Install python 

Clone the repo & *cd in backend*, then run ```python -m venv venv```

Activate the venv, and then run ```pip install -r requirements.txt```

Setup the *.env* file:

```
cp .env.example .env
```

Run the MCP server by: ```python main.py```

This runs the server on *localhost:8000*

---

## License

Apache License 2.0

See the [LICENSE.md](./LICENSE.md) file for the full text.

## Contributing

Please read [CONTRIBUTING.md](./CONTRIBUTING.md) before opening a pull request.
