# ⚙️ Phloem-core
AI Agent Interoperability Layer

---

## 🚀 Features

1. **Agent Interoperability:** Supports mainstream AI Agents to communicate with each other. 
2. **Authentication:** Uses *UUID API KEY auth* for agents.
3. **Secrets Management:** Securely conveys the necessary data, extracts out confidential information.
4. **Zero-Data Retention:** Stores data during communication — deletes once the message is transferred to the destined agent.

---
# Phloem

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

Planned or out-of-scope items for the first release include vendor-specific native integrations, broad orchestration features, and a full public web console.

## Core Concepts

- `Agent` - a registered identity that can send or receive handoffs
- `Tenant` - a logical boundary for isolation and policy control
- `Concept` - a versioned business definition such as `crm.customer.v1`
- `Handoff` - a structured transfer of intent, context, and expected output
- `Policy` - the rule set that decides whether a handoff is allowed, redacted, blocked, or requires approval

## MCP Surface

The server exposes an MCP interface over Streamable HTTP at `POST /mcp`.

The open-source core is intended to work with mainstream MCP-capable clients, while keeping the internal policy model owned by Phloem.

## What the MVP Should Do

- register agents
- validate handoff payloads
- enforce semantic concept references
- redact sensitive fields and detect obvious secrets
- block disallowed transfers
- persist sanitized context and audit metadata
- expose inbox and explanation views for approved recipients

## Security Model

Phloem assumes that cross-agent communication is risky by default.

The system should:

- authenticate agents with bearer API keys
- isolate data by tenant
- store only sanitized context
- retain a hash of the original context for traceability
- flag or block untrusted content based on policy

Phloem does not claim to solve prompt injection, formal reasoning, or theorem proving. It is a practical policy layer for safer handoffs.

## Repository Layout

This repository contains the open-source core.

The private frontend and website are maintained separately.

## Getting Started

The implementation is expected to provide:

- a local development server
- a demo SQLite-backed environment
- a Docker deployment path
- a health endpoint at `GET /healthz`

Refer to the implementation files and deployment notes for exact commands once the server is present.

## MCP Client Examples

Phloem is designed to be reachable by MCP-capable clients that support remote HTTP transports.

Example client configuration will vary by product, but the server should be exposed as a standard Streamable HTTP MCP endpoint.

## Testing Expectations

The project should include tests for:

- semantic validation
- firewall allow/redact/block/approval flows
- policy metadata and audit output
- MCP integration against a registered source and destination

## Documentation Principles

The docs should stay honest about what the core does and does not do.

- Do not imply Phloem can push directly into every downstream agent surface
- Do not imply semantic reasoning is magical or complete
- Do not claim enterprise compliance certifications for the codebase itself

## License

Apache License 2.0

See the `LICENSE` file for the full text.

## Contributing

Please read [CONTRIBUTING.md](./CONTRIBUTING.md) before opening a pull request.
