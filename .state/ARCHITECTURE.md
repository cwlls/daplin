# Daplin — Architectural Overview

> **Status:** Draft v0.2 · Phase 0 complete · Last updated: 2026-03-11
> **Scope:** Instance server reference implementation (v0.1 vertical slice) + project documentation site

---

## 1. Vision & Goals

Daplin is an open protocol for decentralized digital identity, cryptographic public key exchange, and social trust. This repository is the **reference implementation of a Daplin instance server** — the federated node that routes encrypted activities, resolves handles, manages event queues, and points to IPFS-anchored identity documents.

The instance server is deliberately **thin**: it carries encrypted payloads it cannot read, maintains transient event queues, and resolves handles to DIDs. It is a postman, not a reader.

### v0.1 Milestone: Two-Instance Federation with Card Exchange

The first deliverable is a vertical slice proving the federation model works end-to-end:

1. **Identity creation** — generate a key hierarchy from a BIP39 seed, produce a DID, register a handle
2. **Card publishing** — publish an identity card (display name, visual seal, public mediums) anchored to storage
3. **Handle resolution** — resolve `alice>instance-a.example.com` to a DID and card, both locally and across instances
4. **Federation** — two instances discover each other via `/.well-known/daplin`, exchange activities
5. **Card exchange** — Alice on Instance A exchanges cards with Bob on Instance B via remote handle flow
6. **Event queue** — activities are delivered to per-user transient inboxes and consumed on retrieval

### What v0.1 Intentionally Defers

- Local device exchange (NFC/WiFi Direct) — client-side concern
- Capability key tiers beyond `public_key` — only the public tier in v0.1
- Introduction flows — requires capability keys and depth tracking
- Social recovery / guardian designation — requires attestation graph
- Proof of Work — stub/bypass for development; interface defined but not enforced
- did:web — v1.1 per the spec roadmap
- Full attestation graph and degree-of-separation computation

---

## 2. Repository Structure (Monorepo)

```
daplin/
├── docs/                        # Jekyll site served via GitHub Pages at daplin.org
│   ├── _config.yml              # Jekyll config (primer-spec theme, site metadata)
│   ├── CNAME                    # Custom domain: daplin.org
│   ├── index.md                 # Landing page (home)
│   ├── spec.md                  # Protocol specification (v0.2.0)
│   ├── rationale.md             # Project rationale and design philosophy
│   ├── naming.md                # On the name "Daplin" — origin and commitment
│   ├── ai-collaboration.md      # AI-human collaboration in protocol design
│   ├── contributing.md          # How to contribute
│   └── src/                     # Source material (excluded from Jekyll build)
│       ├── project-description.md   # Original project description
│       └── daplin-spec-v0.2.0.md   # Original spec source (v0.2.0 snapshot)
├── server/                      # Instance server (Python/FastAPI) ← v0.1 focus
│   ├── src/
│   │   └── daplin_server/
│   │       ├── __init__.py
│   │       ├── main.py              # FastAPI app factory, lifespan
│   │       ├── config.py            # Settings via pydantic-settings
│   │       ├── api/
│   │       │   ├── __init__.py
│   │       │   ├── well_known.py    # /.well-known/daplin endpoint
│   │       │   ├── handles.py       # Handle resolution
│   │       │   ├── cards.py         # Card publishing and retrieval
│   │       │   ├── events.py        # Event queue (push/consume)
│   │       │   └── federation.py    # Cross-instance activity delivery
│   │       ├── core/
│   │       │   ├── __init__.py
│   │       │   ├── identity.py      # DID generation, key hierarchy
│   │       │   ├── cards.py         # Card model, validation, serialization
│   │       │   ├── activities.py    # Activity types and DIDComm envelope logic
│   │       │   ├── federation.py    # Instance discovery, activity relay
│   │       │   └── crypto.py        # Cryptographic primitives (thin PyNaCl wrapper)
│   │       ├── queue/
│   │       │   ├── __init__.py
│   │       │   ├── base.py          # Abstract event queue interface
│   │       │   ├── nats.py          # NATS JetStream backend (primary)
│   │       │   └── memory.py        # In-memory backend (dev/test fallback)
│   │       ├── storage/
│   │       │   ├── __init__.py
│   │       │   ├── base.py          # Abstract storage backend interface
│   │       │   ├── filesystem.py    # Local disk backend (dev/test)
│   │       │   └── ipfs.py          # IPFS/Kubo backend (production)
│   │       ├── db/
│   │       │   ├── __init__.py
│   │       │   ├── models.py        # SQLAlchemy/SQLModel models
│   │       │   ├── session.py       # Async engine + session factory
│   │       │   └── migrations/      # Alembic migrations
│   │       └── schemas/
│   │           ├── __init__.py
│   │           └── *.py             # Pydantic request/response schemas
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── unit/
│   │   ├── integration/
│   │   └── federation/              # Two-instance integration tests
│   ├── pyproject.toml
│   └── Dockerfile
├── .state/                      # Architectural state (this file)
├── docker-compose.yml           # Multi-instance dev stack
├── LICENSE
├── README.md
└── CLAUDE.md
```

The `server/` directory is a self-contained Python package. The `docs/` directory doubles as the Jekyll-based GitHub Pages site. Future additions (client libraries, CLI tools, mobile SDKs) will be sibling directories in the monorepo.

---

## 3. Technology Stack

| Concern | Choice | Rationale |
|---------|--------|-----------|
| **Language** | Python 3.12+ | Team familiarity, rapid prototyping, strong async ecosystem |
| **Web framework** | FastAPI | Async-first, automatic OpenAPI docs, Pydantic integration |
| **Async model** | async/await throughout | Federation requires concurrent HTTP, DB, and storage I/O |
| **Database (dev)** | SQLite via aiosqlite | Zero-config, single-file, good enough for dev/test |
| **Database (prod)** | PostgreSQL via asyncpg | Proven at scale, JSONB for flexible document storage |
| **ORM** | SQLAlchemy 2.0 async | Mature, supports both SQLite and PostgreSQL |
| **Migrations** | Alembic | Standard for SQLAlchemy projects |
| **Validation** | Pydantic v2 | FastAPI-native, strict typing, serialization |
| **Configuration** | pydantic-settings | Env-var and .env file support |
| **Cryptography** | PyNaCl (libsodium) | Ed25519, X25519, XChaCha20-Poly1305, Argon2id, BLAKE2b |
| **BIP39** | `mnemonic` (Trezor) | Reference BIP-0039 implementation, pure Python |
| **Content identifiers** | `multiformats` | CIDv1 encoding/decoding, multihash, multicodec |
| **HTTP client** | httpx | Async, HTTP/2, used for federation calls |
| **Event queue** | NATS + JetStream | Lightweight pub/sub with durable per-user streams |
| **NATS client** | nats-py | Official async Python NATS client |
| **Content storage (dev)** | Local filesystem | Simulates IPFS with file-backed content-addressable store |
| **Content storage (prod)** | IPFS via Kubo HTTP API | Cards, attestations, key rotation records |
| **Linting** | Ruff | Fast, replaces flake8/isort/black |
| **Type checking** | mypy (strict mode) | Catch type errors before runtime |
| **Testing** | pytest + pytest-asyncio | Async test support, fixtures, parametrize |
| **Containerization** | Docker + docker-compose | Multi-instance federation testing and deployment |

---

## 4. Key Architectural Decisions

### 4.1 Storage Backend Abstraction

Content-addressable storage (cards, attestations, key records) is accessed through an abstract interface:

```
StorageBackend (ABC)
├── put(content) → content_hash     # Store content, return its hash
├── get(content_hash) → content     # Retrieve by hash
├── exists(content_hash) → bool     # Check existence
└── delete(content_hash) → None     # Remove (dev/admin only)
```

- **FilesystemBackend** — stores files in a local directory, named by their BLAKE2b hash. Used for development and testing.
- **IPFSBackend** — calls the Kubo RPC API (`/api/v0/add`, `/api/v0/cat`). Used in production via docker-compose.

This lets us develop and test without IPFS infrastructure while maintaining the same content-addressing semantics.

### 4.2 Database Scope

The instance database stores **only indexing and reference data** — never identity documents or transient events:

| Table | Purpose |
|-------|---------|
| `handles` | Maps `handle → DID` for local users |
| `content_refs` | Maps `DID → storage_hash` for locally-hosted cards/attestations |
| `known_instances` | Discovered federation peers + metadata |

Identity documents (cards, attestations) live in content-addressable storage. Transient activity delivery is handled by NATS JetStream (see §4.4). The database holds pointers, not payloads or queues.

### 4.3 Federation Model

Instances communicate via signed HTTP POST requests:

1. **Discovery:** `GET /.well-known/daplin` returns instance metadata (DID, supported protocol version, endpoints)
2. **Handle resolution:** `GET /api/v1/handles/{handle}` returns the DID and a storage pointer to the card
3. **Activity delivery:** `POST /api/v1/federation/inbox` accepts a signed, encrypted activity envelope
4. **Signature verification:** Each instance has its own Ed25519 keypair; all federation messages are signed

Cross-instance communication is **async and fire-and-forget** for delivery. The sending instance enqueues the activity; the receiving instance places it in the target user's event queue. Retries with exponential backoff handle transient failures.

### 4.4 Event Queue (NATS JetStream)

The event queue is powered by **NATS with JetStream**, providing durable per-user message delivery:

**Architecture:**
- Each user's event queue is a **NATS subject**: `daplin.events.{did}`
- A **JetStream stream** (`DAPLIN_EVENTS`) captures all subjects matching `daplin.events.>`
- Each user has a **durable consumer** that tracks their delivery/acknowledgment state
- Activities are published by the server (from federation or local actions) and persist until acknowledged

**Delivery modes (all supported by the same NATS infrastructure):**
- **WebSocket push (primary):** The server maintains a NATS subscription per connected client and pushes events in real-time over a WebSocket connection
- **HTTP polling (fallback):** `GET /events` reads pending messages from the user's JetStream consumer for clients that cannot hold a persistent connection
- **Acknowledgment:** Client acks events (via WebSocket ack frame or `DELETE /events/{id}`); JetStream removes the message from the consumer's pending set

**Characteristics:**
- Consumed activities are deleted — the queue is not an archive
- Offline users accumulate messages in JetStream; backlog is delivered on reconnect
- Activity types in v0.1 scope: `Publish`, `Attest` (stub), `Migrate` (stub)
- JetStream retention policy: `WorkQueue` (messages deleted after ack) with a configurable max age as a safety net

**Local development:** For running without Docker, the server can embed a fallback in-memory queue that implements the same publish/subscribe interface. Tests use this by default; integration and federation tests use a real NATS server.

### 4.5 Cryptographic Architecture

All cryptographic operations are wrapped in a `crypto` module that provides a clean interface over PyNaCl:

| Operation | Primitive | Library |
|-----------|-----------|---------|
| Identity key generation | Ed25519 | PyNaCl `nacl.signing` |
| Subkey derivation | BLAKE2b keyed hash with `person` tag | PyNaCl `nacl.hash.blake2b` |
| Key agreement (pairwise) | X25519 via Ed25519→Curve25519 conversion | PyNaCl `nacl.public` |
| Symmetric encryption | XChaCha20-Poly1305 AEAD | PyNaCl `nacl.secret.Aead` |
| Proof of Work | Argon2id | PyNaCl `nacl.pwhash.argon2id` |
| Seed phrases | BIP39 12-word mnemonic | `mnemonic` |
| Content hashing | BLAKE2b | PyNaCl `nacl.hash.blake2b` |

The `crypto` module never exposes raw key bytes to the API layer. Keys are wrapped in typed objects that enforce correct usage.

### 4.6 DID Methods (v0.1)

- **did:key** — derived directly from the user's Ed25519 master public key. The DID *is* the key. Used as the global, publicly resolvable identifier.
- **did:peer** — created at exchange time between two specific parties. Never published, never stored on the instance. Entirely client-side in v0.1.

---

## 5. API Surface (v0.1)

### Public / Federation Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/.well-known/daplin` | Instance metadata and discovery |
| `GET` | `/api/v1/handles/{handle}` | Resolve handle → DID + card pointer |
| `POST` | `/api/v1/federation/inbox` | Receive a signed activity from another instance |

### Authenticated User Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| `POST` | `/api/v1/identity` | Register a new identity (DID + handle) |
| `GET` | `/api/v1/identity/{did}` | Retrieve identity metadata |
| `POST` | `/api/v1/cards` | Publish or update a card |
| `GET` | `/api/v1/cards/{did}` | Retrieve a card by DID |
| `GET` | `/api/v1/events` | Poll event queue (fallback for non-WebSocket clients) |
| `DELETE` | `/api/v1/events/{event_id}` | Acknowledge/consume an event |
| `WS` | `/api/v1/events/ws` | WebSocket for real-time event push + acknowledgment |
| `POST` | `/api/v1/exchange/request` | Initiate a card exchange with a remote handle |

### Authentication

Users authenticate to their home instance using their **authentication subkey** (Ed25519 signature over a challenge). v0.1 uses a simple challenge-response flow:

1. Client requests a nonce from the server
2. Client signs the nonce with their authentication subkey
3. Server verifies the signature against the registered DID
4. Server issues a short-lived JWT (or opaque token) for subsequent requests

---

## 6. Data Flow: Card Exchange (v0.1)

```
Alice (Instance A)                                    Bob (Instance B)
       │                                                      │
       ├─── POST /exchange/request {bob>instance-b}           │
       │         │                                            │
       │    Instance A resolves bob>instance-b:               │
       │    GET instance-b/.well-known/daplin                 │
       │    GET instance-b/api/v1/handles/bob                 │
       │         │                                            │
       │    Instance A sends DIDComm activity to Instance B:  │
       │    POST instance-b/api/v1/federation/inbox           │
       │         │                                            │
       │         │                    Instance B publishes to │
       │         │                    NATS: daplin.events.{bob}│
       │         │                    JetStream persists msg  │
       │         │                                            │
       │         │          Bob receives via WebSocket push   │
       │         │          (or polls GET /events)            │
       │         │          Bob sees exchange request         │
       │         │          Bob accepts                       │
       │         │                                            │
       │         │              Instance B sends Alice's card │
       │         │              back via federation inbox      │
       │         │                                            │
       │    NATS publishes to daplin.events.{alice}           │
       │    Alice receives Bob's card via WebSocket           │
       │                                                      │
```

---

## 7. Deployment Model

### Development

```bash
# Single instance (in-memory queue, filesystem storage, SQLite)
cd server && uvicorn daplin_server.main:app --reload

# Single instance with NATS (requires local nats-server or Docker)
DAPLIN_NATS_URL=nats://localhost:4222 uvicorn daplin_server.main:app --reload

# Two-instance federation testing
docker-compose up  # Starts instance-a, instance-b, nats, (optional) kubo
```

### Production

```yaml
# docker-compose.yml sketch
services:
  daplin:
    build: ./server
    environment:
      - DAPLIN_DATABASE_URL=postgresql+asyncpg://...
      - DAPLIN_STORAGE_BACKEND=ipfs
      - DAPLIN_IPFS_API_URL=http://kubo:5001
      - DAPLIN_NATS_URL=nats://nats:4222
      - DAPLIN_INSTANCE_DOMAIN=my-instance.example.com
    ports:
      - "8000:8000"
  nats:
    image: nats:latest
    command: ["--jetstream", "--store_dir", "/data"]
    volumes:
      - nats_data:/data
    ports:
      - "4222:4222"
  kubo:
    image: ipfs/kubo:latest
    # ...
  postgres:
    image: postgres:16
    # ...
volumes:
  nats_data:
```

---

## 8. Documentation Site (daplin.org)

### 8.1 Overview

The project documentation is published as a static site at **daplin.org**, built with Jekyll and hosted on GitHub Pages. The site lives in the `docs/` directory of the monorepo and is deployed automatically when changes to `docs/` are pushed to `main`.

### 8.2 Theme: Leap Day

The site uses the native GitHub Pages `jekyll-theme-leap-day` theme, configured via `theme:` (not `remote_theme:`), which requires no plugin list and no remote theme fetching at build time. Pages use `layout: default`. Primer-spec-specific front matter fields (`subtitle`, `sitemapOrder`, `excludeFromSitemap`) are no longer used.

### 8.3 Domain Configuration

- **Custom domain:** `daplin.org` (root domain, no subdomain)
- **CNAME file:** `docs/CNAME` contains `daplin.org`
- **DNS:** The domain's DNS must be configured with either an `A` record pointing to GitHub Pages IPs or a `CNAME` record (if using `www` subdomain). HTTPS is enforced via GitHub Pages settings.
- **Base URL:** `/` (root-hosted, no path prefix)

### 8.4 Site Structure and Pages

The site is a multi-page documentation hub. Each page is a standalone markdown file with Primer Spec front matter.

#### Landing Page (`index.md`)

The home page introduces Daplin to new visitors. Its content is drawn from the spec's compelling §1 Introduction — the "your identity, your relationships, your communications are yours" framing — adapted into a standalone landing page. It includes:

- The core thesis: trust solved through human relationships, wrapped in an open protocol
- The core principles (privacy-first, identity independent of host, vouching not transferring, etc.) — drawn from the spec §1.1 and `project-description.md`
- Navigation links to all other pages on the site
- Project status (design/specification phase, no implementation yet)

The landing page is *not* a copy-paste of the spec introduction — it is a purpose-written welcome that draws on that material and the project description to orient visitors before they dive into technical content.

#### Protocol Specification (`spec.md`)

The v0.2.0 protocol specification in full. This is the canonical rendering of `daplin-spec-v0.2.0.md` with two modifications:

1. The manually-authored `## Table of Contents` section is **removed** — Primer Spec's sidebar TOC replaces it
2. Front matter is added for title, subtitle, and any theme-specific settings

The spec content itself is unchanged. As the spec evolves, `spec.md` is the living document; the original `daplin-spec-v0.2.0.md` is retained as a point-in-time snapshot.

#### Project Rationale (`rationale.md`)

Why Daplin exists — the design philosophy and the problem space it addresses. Content is synthesized from `project-description.md`, covering:

- The trust problem in secure communication (central authorities vs. complexity)
- The two-layer DID architecture and why it matters
- The capability key model and tiered access
- Why federation without a central authority
- Why no blockchain

This page answers the question: "I understand *what* Daplin is — why was it designed this way?"

#### On the Name (`naming.md`)

The full statement on the origin of the name "Daplin" — the history of the dap among Black American soldiers in Vietnam, the alignment between that history and the protocol's purpose, and the developer's commitment to honoring that heritage. This content is provided verbatim as authored by the lead developer. It is not a marketing page — it is a statement of intention and respect.

#### AI-Human Collaboration (`ai-collaboration.md`)

A philosophical reflection on how AI-human collaboration made this project possible. This page is **not** a dry disclosure — it is a thoughtful take on augmentation over replacement. Key themes:

- AI as a tool for externalizing and structuring ideas that exist in the developer's head
- The distinction between having ideas and being able to sketch/conceptualize/refine them — AI enables the latter at a pace that matches the former
- AI does not replace the human element: the vision, the values, the naming decision, the ethical considerations — these are irreducibly human
- The collaboration model: human intent and direction, AI as a thinking partner that can draft, challenge, and iterate
- Honest acknowledgment of what AI contributed and what it cannot

This page will evolve as the project moves from specification into implementation.

#### Contributing (`contributing.md`)

How to get involved with the Daplin project. Covers:

- The project's current status and what kinds of contributions are most valuable now
- How to propose changes to the protocol specification (RFC-style process per the spec's §13 governance model)
- Code contribution guidelines (to be expanded when the reference implementation begins)
- Code of conduct and community expectations
- Licensing (Apache 2.0)

#### Future Pages (not yet created)

- **Reference Server** — documentation for the Python/FastAPI reference implementation, added when the server reaches a usable state
- **API Reference** — auto-generated or hand-curated endpoint documentation, added when the API surface stabilizes
- **Implementor's Guide** — guidance for third parties building Daplin-compatible software

### 8.5 Jekyll Configuration (`_config.yml`)

Key configuration values:

| Setting | Value | Purpose |
|---------|-------|---------|
| `theme` | `jekyll-theme-leap-day` | Native GitHub Pages theme |
| `title` | `Daplin` | Site title in header/tab |
| `description` | `Dignified Attestation Protocol for Linked Identity Networks` | Meta description, SEO |
| `url` | `https://daplin.org` | Canonical site URL |
| `baseurl` | `` (empty) | Root-hosted, no path prefix |

Individual pages use front matter to control layout behavior (e.g., `title`, `layout`).

### 8.6 Deployment

- **Source:** GitHub Pages configured to serve from the `docs/` directory on the `main` branch
- **Build:** Jekyll build is handled by GitHub Pages automatically on push
- **No CI/CD pipeline needed** — GitHub Pages' native Jekyll support handles everything
- **Preview:** Contributors can run `bundle exec jekyll serve` locally from `docs/` for preview, but this is optional — the theme renders correctly on GitHub Pages without local testing

---

## 9. Implementation Phases

### Phase 0: Documentation Site ✅ Complete
- [x] Jekyll configuration (`_config.yml` with primer-spec remote theme)
- [x] CNAME file for `daplin.org`
- [x] Landing page (`index.md`) — adapted from spec introduction and project description
- [x] Protocol spec page (`spec.md`) — v0.2.0 spec with TOC section removed, front matter added
- [x] Project rationale page (`rationale.md`) — synthesized from project description
- [x] Naming statement page (`naming.md`) — verbatim developer statement on the name's origin
- [x] AI collaboration page (`ai-collaboration.md`) — philosophical reflection on AI-human collaboration
- [x] Contributing page (`contributing.md`) — contribution guidelines and community expectations
- [x] DNS configuration for `daplin.org` → GitHub Pages
- [x] Verify site renders correctly at `daplin.org`

### Phase 1: Foundation
- [ ] Project scaffolding (pyproject.toml, ruff, mypy, pytest config)
- [ ] Crypto module (key generation, signing, BLAKE2b subkey derivation)
- [ ] DID:key generation and encoding
- [ ] Identity and card Pydantic models (JSON-LD with DID Core context)
- [ ] Filesystem storage backend
- [ ] Database models and async session setup
- [ ] Event queue abstraction + in-memory backend

### Phase 2: Single Instance
- [ ] FastAPI app with health check
- [ ] Identity registration endpoint
- [ ] Card publishing and retrieval
- [ ] Handle resolution (with validation rules)
- [ ] `/.well-known/daplin` endpoint
- [ ] Authentication (challenge-response)
- [ ] NATS JetStream event queue backend
- [ ] WebSocket event push endpoint
- [ ] HTTP polling event fallback endpoint
- [ ] DIDComm v2 activity envelope (sign/verify/encrypt/decrypt)

### Phase 3: Federation
- [ ] Instance discovery via well-known
- [ ] Federation inbox (receive DIDComm activities)
- [ ] Cross-instance handle resolution
- [ ] Card exchange flow (request → queue → accept → return)
- [ ] Two-instance docker-compose configuration
- [ ] Two-instance integration tests

### Phase 4: Hardening & Production Readiness
- [ ] IPFS storage backend
- [ ] PostgreSQL support
- [ ] Production docker-compose configuration (with NATS, Kubo, Postgres)
- [ ] Proof of Work enforcement (Argon2id)
- [ ] Rate limiting, input validation, error handling
- [ ] OpenAPI documentation review

---

## 10. Resolved Design Decisions

### 10.1 Card Format: JSON-LD

Cards are serialized as **JSON-LD**, aligning with the W3C DID Document specification. Every Daplin card is a valid DID Document consumable by standard DID tooling. This ensures interoperability with the broader decentralized identity ecosystem from day one.

Cards include a `@context` field referencing the DID Core context and a Daplin-specific context for protocol extensions (medium descriptors, capability tiers, etc.).

### 10.2 Activity Envelope Format: DIDComm v2

Federation activities use **DIDComm v2** message envelopes. DIDComm provides authenticated encryption, signing, and routing between DIDs — exactly the semantics Daplin federation requires. This eliminates the need for a bespoke wire format and aligns with the JSON-LD and DID ecosystem choices.

DIDComm v2 uses JOSE (JWS/JWE) under the hood but provides a well-defined profile that constrains algorithm choices and eliminates common JOSE pitfalls.

### 10.3 Handle Validation Rules

Daplin handles follow the format `{local_part}>{domain}` with these rules:

**Local part:**
- Character set: `[a-z0-9_-]` (lowercase ASCII letters, digits, underscores, hyphens)
- Must start and end with an alphanumeric character: `[a-z0-9][a-z0-9_-]{0,30}[a-z0-9]`
- Length: 2–32 characters
- Case-insensitive; normalized to lowercase on registration and resolution
- Reserved names (cannot be registered): `admin`, `system`, `instance`, `root`, `postmaster`, `abuse`, `security`, `support`, `daplin`, `well-known`, `api`

**Domain part:**
- Valid DNS hostname per RFC 1123
- Punycode (IDN) domains are supported — internationalized domain names are encoded as ASCII-compatible `xn--` labels
- Clients SHOULD display the decoded Unicode form when available

**Future:** Internationalized local parts may be added in a future protocol version via a PRECIS profile (RFC 8264), which is the IETF's purpose-built framework for safe Unicode in protocol identifiers. This is not planned for v1.0.

---

### 10.4 Event Queue: NATS with JetStream

The event queue uses **NATS with JetStream** for durable per-user message delivery. This provides real-time WebSocket push as the primary delivery mode and HTTP polling as a fallback — both backed by the same infrastructure. An in-memory queue implementation provides a zero-dependency fallback for local development and unit tests. See §4.4 for full details.

---

### 10.5 Storage Hashing: CID-Compatible from Day One

Both the filesystem and IPFS storage backends use **CIDv1 content identifiers** as the canonical reference format. The filesystem backend hashes content with SHA-256 (matching IPFS defaults), wraps the result in a CIDv1 structure (raw multicodec + multihash + base32 encoding), and uses the CID string as the filename. This means:

- The `content_refs` database table stores CID strings regardless of backend
- Small files (like cards) produce **identical CIDs** on both filesystem and IPFS backends, since IPFS does not chunk files below 256KB
- Migrating from filesystem to IPFS is a simple re-pin: content is already addressed correctly
- No schema migration required when switching backends

This adds a dependency on `multiformats` (or `py-cid` + `py-multihash`) for CID encoding/decoding.

---

## 11. Open Questions

No open questions remain. All design decisions for v0.1 have been resolved.
