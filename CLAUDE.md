# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Daplin (Dignified Attestation Protocol for Linked Identity Networks) is an open protocol for decentralized digital identity, cryptographic public key exchange, and social trust. Licensed under Apache 2.0.

**Current status:** Design and specification phase. The protocol spec (v0.2.0 draft) and architectural overview are complete. Phase 0 (documentation site at daplin.org) is complete. No server implementation code exists yet.

## Repository Structure

This is a **monorepo**. The instance server lives in `server/` (not yet created). Future client libraries, CLIs, and SDKs will be sibling directories.

- `docs/` — Jekyll site served via GitHub Pages at daplin.org (theme: `carlosperate/jekyll-theme-rtd@v1.0.0`)
  - `docs/_config.yml` — Jekyll configuration
  - `docs/index.md`, `docs/spec.md`, `docs/rationale.md`, `docs/naming.md`, `docs/ai-collaboration.md`, `docs/contributing.md` — published site pages
  - `docs/src/` — source material excluded from Jekyll build (`daplin-spec-v0.2.0.md`, `project-description.md`)
- `.state/ARCHITECTURE.md` — Architectural overview and all resolved design decisions
- `.state/PLAN.md` — Phase 0 implementation plan (complete)
- `server/` — Instance server (Python/FastAPI) — **not yet created, v0.1 target**

## Language & Tooling (Planned)

- **Python 3.12+** with async/await throughout
- **FastAPI** — web framework (async-first)
- **SQLAlchemy 2.0 async** — ORM (SQLite for dev, PostgreSQL for prod)
- **Alembic** — database migrations
- **Pydantic v2** — validation and serialization
- **pydantic-settings** — configuration via env vars
- **PyNaCl** — cryptography (Ed25519, X25519, XChaCha20-Poly1305, Argon2id, BLAKE2b)
- **mnemonic** — BIP39 seed phrase generation (Trezor reference implementation)
- **multiformats** — CIDv1 content identifiers
- **httpx** — async HTTP client for federation
- **nats-py** — NATS JetStream client for event queue
- **Ruff** — linting and formatting
- **mypy** — strict type checking
- **pytest + pytest-asyncio** — testing

No build/test/lint configuration exists yet — update this file when tooling is added.

## Key Architecture Decisions

Refer to `.state/ARCHITECTURE.md` for full details. Summary:

- **Cards** use JSON-LD (W3C DID Document compatible)
- **Federation activities** use DIDComm v2 message envelopes
- **Event queue** is powered by NATS + JetStream (WebSocket push primary, HTTP polling fallback, in-memory for dev/test)
- **Content storage** uses CIDv1-compatible hashing (filesystem backend for dev, IPFS/Kubo for prod)
- **Identity sharing** uses deep links (`daplin://did:key:...@instance.domain`) shared as QR codes or NFC payloads — no human-readable handles
- **Database** stores only indexing/reference data (handles, content refs, known instances) — never identity documents or events

## v0.1 Goal

Two-instance federation with card exchange: identity creation, card publishing, DID resolution, cross-instance activity delivery, and card exchange between Alice on Instance A and Bob on Instance B.
