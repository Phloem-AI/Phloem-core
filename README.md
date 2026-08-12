# Phloem-core

Phloem is a multi-vendor AI agent interoperability layer built around a secure MCP server.

It is designed to help one agent hand work to another with explicit semantics, policy enforcement, and auditability. The open-source core in this repository is licensed under Apache-2.0. The website and private frontend live in a separate proprietary repository.

## Why Phloem Exists

Most agent-to-agent coordination breaks down in the same places:

- different vendors use different vocabularies for the same business concept
- handoffs lose meaning when context is copied loosely between systems
- agents can collide on the same task or overwrite each other’s work
- sensitive data can leak into the wrong place if policies are implicit
- audit trails are often incomplete or unavailable

Phloem is meant to make those handoffs explicit, policy-driven, and machine-checkable.

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

## License

Apache License 2.0

See the `LICENSE` file for the full text.

## Contributing

Please read [CONTRIBUTING.md](./CONTRIBUTING.md) before opening a pull request.
