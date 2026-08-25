# Phloem-core

Using different AI Agents for different parts of your work?

Phloem makes those **agents collaborate autonomously**. So when one Agent writes project plan, you don't have to paste it manually into the other Agent to implement it. Phloem will do it for you (for free!).


## Features

1. **Agent Interoperability:** Supports mainstream AI Agents to communicate with each other. 
2. **Authentication:** Uses *UUID API KEY auth* for agents.
3. **Secrets Management:** Securely conveys the necessary data, extracts out confidential information.
4. **Zero-Data Retention:** Stores data during communication — deletes once the message is transferred to the destined agent.

## What Phloem Is

Phloem is an MCP-native semantic context firewall for cross-vendor agent handoffs.

It is not:

- a generic MCP proxy
- a full agent orchestration platform
- a marketplace for agents
- a vendor-specific integration layer that depends on one ecosystem

## Current Scope

The MVP focuses on the core open-source server:

1. semantic handoff contracts
2. context firewall and sanitization

## Local Setup Guide

**Prerequisite:** Install python 

Clone the repo & *cd in backend*, then run ```python -m venv venv```

Activate the venv, and then run ```pip install -r requirements.txt```

Setup the *.env* file:

```
cp .env.example .env
```

Run the MCP server by: ```python main.py```

This runs the server on *localhost:8000*

## License

Apache License 2.0

See the `LICENSE` file for the full text.

## Contributing

Please read [CONTRIBUTING.md](./CONTRIBUTING.md) before opening a pull request.
