# Contributing to Phloem

Thanks for helping build Phloem.

This repository contains the open-source MCP core for the project. The contributions here should focus on the core server, policy engine, schema validation, tests, docs, and deployment support.

## Project Goals

Phloem is meant to be a secure, vendor-neutral layer for agent handoffs.

Good contributions should improve one or more of the following:

- interoperability between MCP-capable agents
- semantic validation of handoff payloads
- policy enforcement and redaction
- auditability and observability
- local development and deployment ergonomics
- tests that reduce the risk of data leakage or broken handoffs

## Before You Start

Please keep the following in mind:

- be precise about behavior, especially around security and redaction
- prefer small, focused pull requests
- avoid scope creep into product surfaces that belong in the private frontend repo
- keep new dependencies minimal unless they clearly reduce risk or complexity

## Contribution Types

We welcome:

- bug fixes
- test coverage
- documentation improvements
- schema and validation improvements
- policy engine enhancements
- observability and audit improvements
- Docker and deployment improvements

We are especially interested in contributions that make the MCP core easier to run, test, and trust.

## Development Expectations

When contributing code:

1. keep changes narrow and well-scoped
2. add or update tests for behavior changes
3. preserve deterministic behavior where possible
4. avoid adding hidden vendor lock-in
5. do not persist raw secrets or blocked sensitive content

If your change touches policies, semantic validation, or redaction logic, tests should demonstrate the exact expected outcome.

## Security Expectations

Security is central to the project.

Do not:

- log raw secrets
- store blocked payloads in cleartext
- weaken tenant isolation
- add unaudited shortcuts around policy evaluation
- claim compliance or certification guarantees in code or docs

If you discover a vulnerability, please report it privately rather than opening a public issue. (Find email in footer at: phloem-ai.netlify.app)

## Style Guide

Use the existing codebase style and keep implementations practical.

- prefer readable, explicit code over clever abstractions
- keep names precise and domain-aligned
- use typed validation for external inputs
- keep public behavior documented

## Tests

Any meaningful code change should be backed by tests.

At minimum, please verify:

- the happy path still works
- policy edge cases behave as expected
- rejection and redaction paths are covered
- the MCP interface still responds correctly

## Pull Requests

Please include in your pull request:

- a short summary of the change
- the problem it solves
- tests you added or updated
- any security or compatibility notes