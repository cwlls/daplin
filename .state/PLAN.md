# Daplin Implementation State

## Status Notes

**Task 1 (Project Scaffolding):** Complete. Full `server/` directory structure created with `pyproject.toml`, all dependencies configured, ruff/mypy/pytest verified working. Python 3.13 venv at `server/.venv`. Ready for Phase 1 foundation tasks.

---

| # | Task | Priority | Agent | Status | Depends On | Notes |
|:--|:-----|:---------|:------|:-------|:-----------|:------|
| 1 | Project scaffolding | high | @developer | [x] complete | — | pyproject.toml, ruff, mypy, pytest, directory structure |
| 2 | Crypto module | high | @developer | [ ] pending | 1 | Ed25519, BLAKE2b, BIP39, key hierarchy |
| 3 | DID:key generation | high | @developer | [ ] pending | 2 | Multicodec encoding, did:key resolution |
| 4 | Pydantic models (identity + card) | high | @developer | [ ] pending | 3 | Card JSON-LD, activity envelope, API schemas |
| 5 | Filesystem storage backend | high | @developer | [ ] pending | 1 | CIDv1-compatible content-addressable store |
| 6 | Database models + async session | high | @developer | [ ] pending | 1 | SQLAlchemy 2.0 async, Alembic, SQLite dev |
| 7 | Event queue abstraction + in-memory backend | high | @developer | [ ] pending | 1 | ABC interface, in-memory impl for dev/test |
| 8 | FastAPI app + health check | high | @developer | [ ] pending | 1, 6 | App factory, lifespan, config, /health |
| 9 | Identity registration endpoint | high | @developer | [ ] pending | 4, 6, 8 | POST /api/v1/identity |
| 10 | Card publishing + retrieval | high | @developer | [ ] pending | 4, 5, 6, 8 | POST + GET /api/v1/cards |
| 11 | DID resolution endpoint | high | @developer | [ ] pending | 6, 8 | GET /api/v1/identity/{did} |
| 12 | Well-known endpoint | high | @developer | [ ] pending | 8 | GET /.well-known/daplin |
| 13 | Authentication (challenge-response) | high | @developer | [ ] pending | 2, 6, 8 | Nonce, Ed25519 sig verify, JWT |
| 14 | NATS JetStream event queue backend | medium | @developer | [ ] pending | 7 | Durable per-user streams |
| 15 | WebSocket event push | medium | @developer | [ ] pending | 7, 8, 13 | WS /api/v1/events/ws |
| 16 | HTTP polling event fallback | medium | @developer | [ ] pending | 7, 8, 13 | GET + DELETE /api/v1/events |
| 17 | DIDComm v2 activity envelope | high | @developer | [ ] pending | 2, 4 | Sign/verify/encrypt/decrypt |
| 18 | Instance discovery (well-known) | high | @developer | [ ] pending | 8, 12 | Fetch + cache remote /.well-known/daplin |
| 19 | Federation inbox | high | @developer | [ ] pending | 7, 8, 17 | POST /api/v1/federation/inbox |
| 20 | Cross-instance DID resolution | high | @developer | [ ] pending | 11, 18 | Resolve remote DID via federation |
| 21 | Card exchange flow | high | @developer | [ ] pending | 9, 10, 17, 19 | Request → queue → accept → return |
| 22 | Docker Compose (two-instance) | high | @developer | [ ] pending | 8, 14, 19 | instance-a, instance-b, nats |
| 23 | Federation integration tests | high | @developer | [ ] pending | 21, 22 | End-to-end two-instance card exchange |
| 24 | IPFS storage backend | medium | @developer | [ ] pending | 5 | Kubo HTTP API integration |
| 25 | PostgreSQL support | medium | @developer | [ ] pending | 6 | asyncpg, production config |
| 26 | Production Docker Compose | medium | @developer | [ ] pending | 22, 24, 25 | NATS + Kubo + Postgres |
| 27 | PoW enforcement (Argon2id) | low | @developer | [ ] pending | 2, 17 | Stub → real enforcement |
| 28 | Rate limiting + input validation + error handling | medium | @developer | [ ] pending | 8 | Production hardening |
| 29 | OpenAPI documentation review | low | @developer | [ ] pending | 8 | Verify auto-generated docs |

---

# Daplin Task Descriptions

## Phase 1: Foundation (Tasks 1–7)

Build the core libraries and abstractions that every subsequent task depends on. No HTTP server yet — just the building blocks.

---

### Task 1: Project Scaffolding

**File:** `server/pyproject.toml` + directory tree

Create the `server/` directory as a self-contained Python package with the full directory structure from ARCHITECTURE.md §2.

**pyproject.toml configuration:**

```toml
[project]
name = "daplin-server"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115",
    "uvicorn[standard]>=0.34",
    "sqlalchemy[asyncio]>=2.0",
    "aiosqlite>=0.20",
    "alembic>=1.14",
    "pydantic>=2.10",
    "pydantic-settings>=2.7",
    "pynacl>=1.5",
    "mnemonic>=0.21",
    "multiformats>=0.3",
    "httpx>=0.28",
    "nats-py>=2.9",
    "pyjwt>=2.10",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3",
    "pytest-asyncio>=0.25",
    "ruff>=0.9",
    "mypy>=1.14",
]

[tool.ruff]
target-version = "py312"
line-length = 99

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP", "B", "SIM", "TCH"]

[tool.mypy]
python_version = "3.12"
strict = true
plugins = ["pydantic.mypy"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

**Directory tree to create:**

```
server/
├── src/
│   └── daplin_server/
│       ├── __init__.py
│       ├── main.py
│       ├── config.py
│       ├── api/
│       │   └── __init__.py
│       ├── core/
│       │   └── __init__.py
│       ├── queue/
│       │   └── __init__.py
│       ├── storage/
│       │   └── __init__.py
│       ├── db/
│       │   └── __init__.py
│       └── schemas/
│           └── __init__.py
├── tests/
│   ├── conftest.py
│   ├── unit/
│   ├── integration/
│   └── federation/
└── pyproject.toml
```

**`config.py`** — pydantic-settings `Settings` class:

```python
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DAPLIN_")

    instance_domain: str = "localhost"
    instance_name: str = "Daplin Dev"
    database_url: str = "sqlite+aiosqlite:///./daplin.db"
    storage_backend: Literal["filesystem", "ipfs"] = "filesystem"
    storage_path: Path = Path("./storage")
    ipfs_api_url: str = "http://localhost:5001"
    nats_url: str | None = None  # None = use in-memory queue
    jwt_secret: str = "dev-secret-change-me"
    jwt_expiry_minutes: int = 60
    federation_enabled: bool = True
```

**Acceptance:** `pip install -e ".[dev]"` succeeds. `ruff check .` passes. `mypy .` passes. `pytest` discovers test directory (0 tests collected is fine).

---

### Task 2: Crypto Module

**File:** `server/src/daplin_server/core/crypto.py`

Thin wrapper over PyNaCl that provides typed key objects and enforces correct usage. Raw key bytes are never exposed to the API layer.

**Types to define:**

```python
@dataclass(frozen=True)
class MasterKey:
    signing_key: nacl.signing.SigningKey
    verify_key: nacl.signing.VerifyKey

@dataclass(frozen=True)
class SubkeySet:
    signing: nacl.signing.SigningKey
    encryption: nacl.public.PrivateKey
    authentication: nacl.signing.SigningKey

@dataclass(frozen=True)
class SeedPhrase:
    words: list[str]  # 12 BIP39 words
```

**Functions to implement:**

| Function | Purpose | Primitives |
|----------|---------|------------|
| `generate_master_key() → (MasterKey, SeedPhrase)` | Generate Ed25519 master key + BIP39 seed phrase | `mnemonic`, `nacl.signing` |
| `recover_master_key(seed_phrase: SeedPhrase) → MasterKey` | Reconstruct master key from seed phrase | `mnemonic`, `nacl.signing` |
| `derive_subkeys(master: MasterKey, device_id: str) → SubkeySet` | Derive device-specific subkeys via BLAKE2b keyed hash | `nacl.hash.blake2b` with `person` tag |
| `sign(key: nacl.signing.SigningKey, message: bytes) → bytes` | Sign a message | `nacl.signing` |
| `verify(verify_key: nacl.signing.VerifyKey, signed: bytes) → bytes` | Verify a signature | `nacl.signing` |
| `content_hash(content: bytes) → str` | BLAKE2b hash, return hex string | `nacl.hash.blake2b` |

**Tests:** `tests/unit/test_crypto.py`
- Generate master key, verify seed phrase is 12 words
- Recover master key from seed phrase, verify same verify_key
- Derive subkeys for two different device_ids, verify they differ
- Sign and verify round-trip
- Content hash is deterministic

**Acceptance:** All tests pass. `mypy` passes with strict mode.

---

### Task 3: DID:key Generation

**File:** `server/src/daplin_server/core/identity.py`

Implement `did:key` generation and resolution per the W3C did:key method spec. A `did:key` is derived directly from the Ed25519 public key using multicodec encoding.

**Functions to implement:**

| Function | Purpose |
|----------|---------|
| `did_from_master_key(master: MasterKey) → str` | Encode verify_key as `did:key:z6Mk...` |
| `verify_key_from_did(did: str) → nacl.signing.VerifyKey` | Decode `did:key:z6Mk...` back to verify_key |
| `is_valid_did_key(did: str) → bool` | Validate format and decodability |

**Encoding:** The Ed25519 public key (32 bytes) is prefixed with the multicodec varint for Ed25519 (`0xed01`), then base58btc-encoded with a `z` prefix. The full DID is `did:key:z` + base58btc(multicodec_prefix + public_key_bytes).

**Tests:** `tests/unit/test_identity.py`
- Generate a DID from a master key, verify it starts with `did:key:z6Mk`
- Round-trip: generate DID → decode back to verify_key → verify it matches
- Invalid DID strings return False from `is_valid_did_key`

**Acceptance:** All tests pass. DID encoding matches the W3C did:key spec for Ed25519.

---

### Task 4: Pydantic Models (Identity + Card + Activity)

**Files:**
- `server/src/daplin_server/schemas/identity.py`
- `server/src/daplin_server/schemas/card.py`
- `server/src/daplin_server/schemas/activity.py`

Define Pydantic v2 models for the core protocol data structures.

**Identity schemas:**

```python
class IdentityCreate(BaseModel):
    did: str  # did:key:z6Mk...
    display_name: str
    instance_domain: str

class IdentityResponse(BaseModel):
    did: str
    display_name: str
    instance_domain: str
    card_cid: str | None
    created_at: datetime
```

**Card schema (per spec §4.1):**

```python
class Card(BaseModel):
    daplin: str = "1.0.0"
    did: str
    card_version: int
    previous_card: str | None = None
    display_name: str
    seal_palette: str | None = None
    seal_border: str | None = None
    public_mediums: list[MediumDescriptor] = []
    encrypted_tiers: dict[str, str] = {}  # tier_name → ciphertext
    signature: str

class MediumDescriptor(BaseModel):
    type: str
    value: str
    protocol: str | None = None
    label: str | None = None
    preference: str | None = None
    tier: str
```

**Activity envelope (per spec §11.1):**

```python
class Activity(BaseModel):
    daplin: str = "1.0.0"
    type: ActivityType
    id: str  # UUID
    actor: str  # DID
    timestamp: datetime
    pow: ProofOfWork | None = None
    payload: dict[str, Any]
    signature: str

class ActivityType(str, Enum):
    PUBLISH = "Publish"
    ATTEST = "Attest"
    MIGRATE = "Migrate"
    # ... other types from spec §11.2
```

**Tests:** `tests/unit/test_schemas.py`
- Card model validates the example JSON from spec §4.1
- Activity model validates the example JSON from spec §11.1
- Invalid data raises `ValidationError`

**Acceptance:** All models serialize/deserialize correctly. `mypy` passes.

---

### Task 5: Filesystem Storage Backend

**Files:**
- `server/src/daplin_server/storage/base.py`
- `server/src/daplin_server/storage/filesystem.py`

Implement the storage backend abstraction (ARCHITECTURE.md §4.1) and the filesystem implementation.

**Abstract interface:**

```python
class StorageBackend(ABC):
    @abstractmethod
    async def put(self, content: bytes) -> str: ...  # Returns CID string

    @abstractmethod
    async def get(self, cid: str) -> bytes: ...

    @abstractmethod
    async def exists(self, cid: str) -> bool: ...

    @abstractmethod
    async def delete(self, cid: str) -> None: ...
```

**FilesystemBackend:**
- Stores files in a configurable directory, named by their CIDv1 string
- Hashing: SHA-256 (matching IPFS defaults), wrapped in CIDv1 (raw multicodec + multihash + base32lower encoding) via the `multiformats` library
- `put()` hashes content → generates CID → writes file → returns CID
- `get()` reads file by CID filename → returns bytes
- `exists()` checks file existence
- `delete()` removes file

**Tests:** `tests/unit/test_storage.py`
- `put` + `get` round-trip returns identical content
- `put` same content twice returns same CID (content-addressable)
- `exists` returns True after put, False for unknown CID
- `delete` removes the file, subsequent `get` raises
- CID format matches CIDv1 base32lower pattern (`bafy...`)

**Acceptance:** All tests pass. CIDs are deterministic and CIDv1-compliant.

---

### Task 6: Database Models + Async Session

**Files:**
- `server/src/daplin_server/db/models.py`
- `server/src/daplin_server/db/session.py`
- `server/src/daplin_server/db/migrations/` (Alembic init)

**Database tables (per ARCHITECTURE.md §4.2):**

```python
class Identity(Base):
    __tablename__ = "identities"
    did: Mapped[str] = mapped_column(String, primary_key=True)
    display_name: Mapped[str] = mapped_column(String, nullable=False)
    instance_domain: Mapped[str] = mapped_column(String, nullable=False)
    card_cid: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

class ContentRef(Base):
    __tablename__ = "content_refs"
    cid: Mapped[str] = mapped_column(String, primary_key=True)
    did: Mapped[str] = mapped_column(String, ForeignKey("identities.did"), nullable=False)
    content_type: Mapped[str] = mapped_column(String, nullable=False)  # "card", "attestation"
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

class KnownInstance(Base):
    __tablename__ = "known_instances"
    domain: Mapped[str] = mapped_column(String, primary_key=True)
    daplin_version: Mapped[str] = mapped_column(String, nullable=False)
    federation_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    last_seen: Mapped[datetime] = mapped_column(DateTime, default=func.now())
```

**Session factory:**

```python
async def get_engine(database_url: str) -> AsyncEngine: ...
async def get_session(engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]: ...
```

**Alembic:** Initialize with `alembic init`, configure for async SQLAlchemy, generate initial migration from models.

**Tests:** `tests/unit/test_db.py`
- Create an in-memory SQLite database
- Insert and query an Identity record
- Insert and query a ContentRef record
- Foreign key constraint works (ContentRef.did must exist in identities)

**Acceptance:** All tests pass. Alembic migration applies cleanly. `mypy` passes.

---

### Task 7: Event Queue Abstraction + In-Memory Backend

**Files:**
- `server/src/daplin_server/queue/base.py`
- `server/src/daplin_server/queue/memory.py`

**Abstract interface:**

```python
class EventQueue(ABC):
    @abstractmethod
    async def publish(self, subject: str, data: bytes) -> None: ...

    @abstractmethod
    async def subscribe(self, subject: str) -> AsyncIterator[Event]: ...

    @abstractmethod
    async def pull(self, subject: str, batch_size: int = 10) -> list[Event]: ...

    @abstractmethod
    async def ack(self, subject: str, event_id: str) -> None: ...

@dataclass
class Event:
    id: str
    subject: str
    data: bytes
    timestamp: datetime
```

**InMemoryQueue:**
- Uses `asyncio.Queue` per subject
- `publish()` appends to the subject's queue
- `subscribe()` yields events as they arrive (async generator)
- `pull()` drains up to `batch_size` events from the queue
- `ack()` removes the event from a pending set
- Events persist in memory until acked (simulates JetStream WorkQueue retention)

**Tests:** `tests/unit/test_queue.py`
- Publish an event, pull it back, verify data matches
- Publish to two different subjects, verify isolation
- Ack an event, verify it's no longer returned by pull
- Subscribe receives events published after subscription starts

**Acceptance:** All tests pass. Interface is clean enough that NATS backend (Task 14) can implement it without changes.

---

## Phase 2: Single Instance (Tasks 8–17)

Stand up the HTTP server and implement all endpoints for a single instance. No federation yet.

---

### Task 8: FastAPI App + Health Check

**Files:**
- `server/src/daplin_server/main.py`
- `server/src/daplin_server/config.py` (extend from Task 1)

Create the FastAPI application factory with lifespan management.

**App factory:**

```python
def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    app = FastAPI(title="Daplin Instance", version="0.1.0")

    @app.on_event("startup")  # or lifespan context manager
    async def startup():
        # Initialize DB engine, run migrations, init storage, init queue
        ...

    @app.get("/health")
    async def health():
        return {"status": "ok", "instance": settings.instance_domain}

    # Include API routers
    ...
    return app
```

**Lifespan:** Initialize database engine, storage backend, and event queue on startup. Tear down on shutdown. Store references in `app.state`.

**Tests:** `tests/integration/test_app.py`
- App starts without error
- `GET /health` returns 200 with instance domain

**Acceptance:** `uvicorn daplin_server.main:app` starts. Health check responds.

---

### Task 9: Identity Registration Endpoint

**File:** `server/src/daplin_server/api/identity.py`

**Endpoint:** `POST /api/v1/identity`

**Request body:** `IdentityCreate` (did, display_name, instance_domain)

**Logic:**
1. Validate the DID is a well-formed `did:key`
2. Verify the request is signed by the DID's key (authentication — may use a simplified flow for v0.1)
3. Check the DID is not already registered
4. Insert into `identities` table
5. Return `IdentityResponse`

**Tests:** `tests/integration/test_identity.py`
- Register a new identity, verify 201 response
- Attempt duplicate registration, verify 409 Conflict
- Invalid DID format, verify 422

**Acceptance:** Identity registration works end-to-end with SQLite.

---

### Task 10: Card Publishing + Retrieval

**File:** `server/src/daplin_server/api/cards.py`

**Endpoints:**
- `POST /api/v1/cards` — publish or update a card
- `GET /api/v1/cards/{did}` — retrieve a card by DID

**Publish logic:**
1. Validate the card JSON against the Card Pydantic model
2. Verify the card signature matches the DID's key
3. Store the card content in the storage backend → get CID
4. Update `content_refs` table (DID → CID, type="card")
5. Update `identities.card_cid` with the new CID
6. Publish a `Publish` activity to the event queue
7. Return the CID

**Retrieve logic:**
1. Look up the DID in `identities` → get `card_cid`
2. Fetch the card content from storage by CID
3. Return the card JSON

**Tests:** `tests/integration/test_cards.py`
- Publish a card, retrieve it by DID, verify content matches
- Publish an updated card (incremented cardVersion), verify previousCard points to old CID
- Retrieve card for unknown DID, verify 404

**Acceptance:** Card publish + retrieve round-trip works.

---

### Task 11: DID Resolution Endpoint

**File:** `server/src/daplin_server/api/identity.py` (extend)

**Endpoint:** `GET /api/v1/identity/{did}`

**Logic:**
1. Look up DID in `identities` table
2. Return `IdentityResponse` including `card_cid`
3. 404 if not found

**Tests:** Covered by Task 9 tests (register then retrieve).

---

### Task 12: Well-Known Endpoint

**File:** `server/src/daplin_server/api/well_known.py`

**Endpoint:** `GET /.well-known/daplin`

**Response (per spec §10.1):**

```json
{
    "daplin": "1.0.0",
    "instance": "my-instance.example.com",
    "name": "My Instance",
    "federation": true,
    "registrations": "open"
}
```

Values are drawn from `Settings`.

**Tests:** `tests/integration/test_well_known.py`
- Verify response matches config values
- Verify `daplin` version is `"1.0.0"`

---

### Task 13: Authentication (Challenge-Response)

**File:** `server/src/daplin_server/api/auth.py`

Implement the challenge-response authentication flow from ARCHITECTURE.md §5.

**Endpoints:**
- `POST /api/v1/auth/challenge` — returns a nonce
- `POST /api/v1/auth/verify` — accepts DID + signed nonce, returns JWT

**Logic:**
1. Server generates a random nonce, stores it with a short TTL (e.g., 5 minutes)
2. Client signs the nonce with their authentication subkey
3. Server looks up the DID in `identities`, retrieves the verify_key
4. Server verifies the signature
5. Server issues a JWT containing the DID, with configurable expiry

**Middleware:** A FastAPI dependency that extracts and validates the JWT from the `Authorization: Bearer` header, making the authenticated DID available to endpoint handlers.

**Tests:** `tests/integration/test_auth.py`
- Full challenge-response flow succeeds, returns valid JWT
- Invalid signature returns 401
- Expired nonce returns 401
- JWT is accepted by protected endpoints

---

### Task 14: NATS JetStream Event Queue Backend

**File:** `server/src/daplin_server/queue/nats.py`

Implement the `EventQueue` interface using NATS with JetStream (ARCHITECTURE.md §4.4).

**Configuration:**
- Stream name: `DAPLIN_EVENTS`
- Subject pattern: `daplin.events.{did}`
- Retention: `WorkQueue` (messages deleted after ack)
- Durable consumer per user DID

**Implementation:**
- `publish()` → `js.publish(subject, data)`
- `subscribe()` → create/bind durable consumer, yield messages
- `pull()` → `consumer.fetch(batch_size)`
- `ack()` → `msg.ack()`

**Tests:** `tests/integration/test_nats_queue.py` (requires running NATS server — skip in CI if unavailable)
- Publish + pull round-trip
- Ack removes message from pending
- Messages persist across reconnect (durable consumer)

---

### Task 15: WebSocket Event Push

**File:** `server/src/daplin_server/api/events.py`

**Endpoint:** `WS /api/v1/events/ws`

**Logic:**
1. Authenticate via JWT (passed as query param or first message)
2. Subscribe to the user's event queue subject (`daplin.events.{did}`)
3. Push events to the client as they arrive
4. Accept ack frames from the client → call `queue.ack()`
5. Clean up subscription on disconnect

**Tests:** `tests/integration/test_events_ws.py`
- Connect via WebSocket, publish an event, verify it's received
- Send ack, verify event is consumed

---

### Task 16: HTTP Polling Event Fallback

**File:** `server/src/daplin_server/api/events.py` (extend)

**Endpoints:**
- `GET /api/v1/events` — pull pending events (authenticated)
- `DELETE /api/v1/events/{event_id}` — acknowledge an event

**Logic:**
1. `GET` calls `queue.pull(subject, batch_size)` for the authenticated user's DID
2. Returns list of events as JSON
3. `DELETE` calls `queue.ack(subject, event_id)`

**Tests:** `tests/integration/test_events_http.py`
- Publish event, poll, verify it appears
- Ack event, poll again, verify it's gone

---

### Task 17: DIDComm v2 Activity Envelope

**File:** `server/src/daplin_server/core/activities.py`

Implement DIDComm v2 message envelope construction and verification for federation activities.

**Functions:**

| Function | Purpose |
|----------|---------|
| `create_activity(type, actor_did, actor_key, payload) → Activity` | Build and sign an activity envelope |
| `verify_activity(activity: Activity) → bool` | Verify the signature against the actor's DID |
| `wrap_didcomm(activity: Activity, sender_key, recipient_did) → dict` | Wrap in DIDComm v2 envelope (JWS signed, optionally JWE encrypted) |
| `unwrap_didcomm(envelope: dict, recipient_key) → Activity` | Unwrap and verify a DIDComm envelope |

**v0.1 scope:** Signed but not encrypted (encryption requires pairwise keys, which are deferred). The interface supports encryption so it can be added later without API changes.

**Tests:** `tests/unit/test_activities.py`
- Create an activity, verify signature
- Wrap in DIDComm, unwrap, verify round-trip
- Tampered activity fails verification

---

## Phase 3: Federation (Tasks 18–23)

Connect two instances and prove the card exchange flow works end-to-end.

---

### Task 18: Instance Discovery

**File:** `server/src/daplin_server/core/federation.py`

**Logic:**
1. Given a remote instance domain, fetch `GET https://{domain}/.well-known/daplin`
2. Parse and validate the response
3. Cache the result in `known_instances` table
4. Return the instance metadata

Uses `httpx.AsyncClient` for the HTTP call.

**Tests:** `tests/unit/test_federation.py` (mock httpx)
- Successful discovery returns parsed metadata
- Failed discovery (404, timeout) raises appropriate error
- Cached instance is returned without re-fetching

---

### Task 19: Federation Inbox

**File:** `server/src/daplin_server/api/federation.py`

**Endpoint:** `POST /api/v1/federation/inbox`

**Logic:**
1. Receive a DIDComm v2 envelope
2. Unwrap and verify the activity signature
3. Validate the activity type is known
4. Route the activity to the target user's event queue
5. Return 202 Accepted

**Signature verification:** The sending instance signs the envelope with its instance key. The receiving instance verifies against the key published in the sender's `/.well-known/daplin` response.

**Tests:** `tests/integration/test_federation_inbox.py`
- Valid activity is accepted and routed to event queue
- Invalid signature returns 401
- Unknown activity type returns 400

---

### Task 20: Cross-Instance DID Resolution

**File:** `server/src/daplin_server/core/federation.py` (extend)

**Logic:**
1. If a DID is not found locally, check `known_instances` for the DID's home instance
2. Fetch `GET https://{remote_domain}/api/v1/identity/{did}`
3. Fetch the card from the remote instance's storage (or via CID from the response)
4. Cache the result locally

**Tests:** `tests/integration/test_cross_resolution.py` (mock remote instance)
- Remote DID is resolved and card is fetched
- Cached result is returned on subsequent calls

---

### Task 21: Card Exchange Flow

**File:** `server/src/daplin_server/api/exchange.py`

**Endpoint:** `POST /api/v1/exchange/request`

Implement the full card exchange flow from ARCHITECTURE.md §6:

1. Alice's client sends `POST /exchange/request` with Bob's DID and instance domain
2. Alice's instance discovers Bob's instance via well-known
3. Alice's instance resolves Bob's DID on the remote instance
4. Alice's instance sends a DIDComm `ExchangeRequest` activity to Bob's instance federation inbox
5. Bob's instance routes the activity to Bob's event queue
6. Bob's client receives the request, accepts it
7. Bob's instance sends Alice's card back via federation inbox
8. Alice receives Bob's card via her event queue

**Tests:** `tests/integration/test_exchange.py`
- Full exchange flow with mocked remote instance
- Exchange request for unknown DID returns 404

---

### Task 22: Docker Compose (Two-Instance)

**Files:**
- `docker-compose.yml` (repo root)
- `server/Dockerfile`

**Dockerfile:** Multi-stage build — install dependencies, copy source, run uvicorn.

**docker-compose.yml:**

```yaml
services:
  instance-a:
    build: ./server
    environment:
      DAPLIN_INSTANCE_DOMAIN: instance-a.localhost
      DAPLIN_NATS_URL: nats://nats:4222
      DAPLIN_DATABASE_URL: sqlite+aiosqlite:///./daplin-a.db
    ports: ["8001:8000"]
  instance-b:
    build: ./server
    environment:
      DAPLIN_INSTANCE_DOMAIN: instance-b.localhost
      DAPLIN_NATS_URL: nats://nats:4222
      DAPLIN_DATABASE_URL: sqlite+aiosqlite:///./daplin-b.db
    ports: ["8002:8000"]
  nats:
    image: nats:latest
    command: ["--jetstream", "--store_dir", "/data"]
    ports: ["4222:4222"]
```

**Acceptance:** `docker-compose up` starts both instances and NATS. Both instances respond to `/health` and `/.well-known/daplin`.

---

### Task 23: Federation Integration Tests

**File:** `tests/federation/test_card_exchange.py`

End-to-end test proving the v0.1 milestone:

1. Start two instances (via docker-compose or in-process with different configs)
2. Register Alice on Instance A
3. Register Bob on Instance B
4. Alice publishes a card on Instance A
5. Bob publishes a card on Instance B
6. Alice initiates a card exchange with Bob
7. Bob receives the exchange request via his event queue
8. Bob accepts the exchange
9. Alice receives Bob's card via her event queue
10. Verify both parties have each other's cards

**Acceptance:** The test passes. The v0.1 milestone is proven.

---

## Phase 4: Hardening & Production Readiness (Tasks 24–29)

---

### Task 24: IPFS Storage Backend

**File:** `server/src/daplin_server/storage/ipfs.py`

Implement `StorageBackend` using the Kubo HTTP RPC API:
- `put()` → `POST /api/v0/add`
- `get()` → `POST /api/v0/cat`
- `exists()` → `POST /api/v0/block/stat`
- `delete()` → `POST /api/v0/pin/rm` (unpin only; IPFS GC handles actual deletion)

**Tests:** `tests/integration/test_ipfs_storage.py` (requires running Kubo — skip if unavailable)

---

### Task 25: PostgreSQL Support

**File:** `server/src/daplin_server/db/session.py` (extend)

Add `asyncpg` as an optional dependency. The session factory already accepts a `database_url` — PostgreSQL support is primarily a matter of:
1. Adding `asyncpg` to dependencies
2. Testing that Alembic migrations apply cleanly to PostgreSQL
3. Verifying all queries work with PostgreSQL's stricter type system

**Tests:** `tests/integration/test_db_postgres.py` (requires running PostgreSQL — skip if unavailable)

---

### Task 26: Production Docker Compose

**File:** `docker-compose.prod.yml`

Extends the dev compose with:
- PostgreSQL service
- Kubo (IPFS) service
- Persistent volumes for all data
- Production environment variables

---

### Task 27: PoW Enforcement (Argon2id)

**File:** `server/src/daplin_server/core/crypto.py` (extend)

Implement proof-of-work generation and verification using Argon2id (per spec §5.5):
- `generate_pow(difficulty, data) → ProofOfWork`
- `verify_pow(pow: ProofOfWork, difficulty, data) → bool`

Difficulty levels per spec: reduced (~5s), standard (~30s), maximum (~10min).

v0.1 has a bypass flag (`DAPLIN_POW_ENABLED=false`) for development.

---

### Task 28: Rate Limiting + Input Validation + Error Handling

Production hardening:
- Rate limiting on federation inbox and public endpoints
- Comprehensive input validation on all request bodies
- Structured error responses (consistent JSON error format)
- Request ID tracking for debugging

---

### Task 29: OpenAPI Documentation Review

Review the auto-generated FastAPI OpenAPI spec:
- Verify all endpoints are documented
- Add descriptions and examples to schemas
- Ensure response codes are accurate

---

## Task Dependency Graph

```
Phase 1 (Foundation):
  1 ──┬── 2 ── 3 ── 4
      ├── 5
      ├── 6
      └── 7

Phase 2 (Single Instance):
  1,6 ── 8 ──┬── 9 ──┐
              ├── 11  ├── 10
              ├── 12  │
              └── 13 ─┼── 15
                      └── 16
  2,4 ── 17
  7 ── 14

Phase 3 (Federation):
  8,12 ── 18 ── 20
  7,8,17 ── 19
  9,10,17,19 ── 21
  8,14,19 ── 22
  21,22 ── 23

Phase 4 (Hardening):
  5 ── 24
  6 ── 25
  22,24,25 ── 26
  2,17 ── 27
  8 ── 28
  8 ── 29
```
