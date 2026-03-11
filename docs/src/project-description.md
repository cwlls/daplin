# Daplin — Project Description

**Dignified Attestation Protocol for Linked Identity Networks**

## What is Daplin?

Daplin is an open protocol for decentralized digital identity, cryptographic public key exchange, and social trust. The name is a backronym: each word earns its place — *Dignified* reflects the privacy-first, human-respecting philosophy; *Attestation* is the core trust mechanism; *Protocol* signals infrastructure rather than a product; *Linked* captures the social graph concept; *Identity* names the fundamental problem being solved; *Networks* reflects federation and decentralization with no central authority.

Daplin wraps this hard problem in a human-friendly layer — portable digital identity cards, a social trust graph, and a federation model that requires no central authority. It is infrastructure, not an application. Messaging clients, email systems, and other communication tools build on top of Daplin rather than replicating it.

---

## Core Principles

- **Privacy is the only mode.** There is no public graph, no passive discovery, no opt-in privacy. All users are indistinguishable from outside the network.
- **Identity is independent of host.** Identity is derived from cryptographic keys, not the server a user happens to use.
- **Vouching, not transferring.** Contact information is never passed between parties. Only introductions are made; the subject always controls their own data.
- **Physical presence is the strongest trust signal.** In-person key exchange via local device communication carries more weight than any remote interaction.
- **Servers know as little as possible.** Instances are thin routing layers that carry encrypted payloads they cannot read.
- **Daplin is a protocol, not a product.** Anyone can implement it, run an instance, or build applications on top of it.
- **Portable and self-hostable.** Users can migrate between instances without losing identity, attestations, or contact relationships.

---

## Identity Model

### Two-Layer DID Architecture

Daplin uses two complementary DID (Decentralized Identifier) methods:

- **Global Identity (did:key / did:web):** Publicly resolvable. Anchors the attestation chain. Exists before any relationships are formed. In v1.0, the DID is derived directly from the user's Ed25519 master public key — the DID *is* the key.
- **Pairwise Identity (did:peer):** A private key agreement created between two specific parties at the moment of exchange. Never published, never federated, leaves no observable trace. Supports per-relationship key rotation without any infrastructure.

No blockchain methods are used or planned.

### Key Hierarchy

Every user maintains a key hierarchy:
- **Master Key** — root of identity, kept cold, never used for daily operations
- **Signing Subkey** — signs activities and attestations, device-specific, expires annually
- **Encryption Subkey** — encrypts messages and capability keys, device-specific
- **Authentication Subkey** — proves identity to instances, device-specific
- **Recovery Subkey** — purpose-limited to recovery declarations only, stored cold

### Handles

Daplin handles use the `>` sigil: `alice>bigtime.daplin.io`

The `>` was chosen for distinctiveness, directionality, and being unclaimed by any other protocol.

### Master Key Ceremony

Required during onboarding: a 12-word BIP39 seed phrase plus optional encrypted cloud backup. Users confirm 3 random words to prove they've recorded it. Private keys never leave the device.

---

## Trust Model

### Two Independent Axes

Trust is expressed across two completely independent dimensions:

1. **Network Topology (Degrees of Separation):** The shortest path between two parties in the attestation graph. Immutable history — new connections create shorter paths but old paths remain. Computed on demand via zero-knowledge path proofs; no publicly traversable graph exists.

2. **Relationship Depth:** A personal classification set deliberately by the user:
   - `INTRODUCED` — accepted an introduction, no personal attestation
   - `ACQUAINTANCE` — basic trust, interacted
   - `CONTACT` — established relationship
   - `TRUSTED` — deep personal trust
   - `GUARDIAN` — maximum trust, recovery participant

Accepting an introduction is NOT an attestation. They are separate deliberate actions.

### Exchange Method

Recorded in the attestation, contributes to trust weight:
- `local_device` — strongest; physical presence verified via NFC + WiFi Direct
- `introduction` — strong; mutual contact vouched
- `remote_handle` — moderate; no prior context

### Proof of Work

Memory-hard puzzles (Argon2id) are required for attestations and graph traversal queries. Adaptive difficulty keeps time cost constant across devices while making bot farms and bulk graph scraping economically unviable. Difficulty scales with action sensitivity: reduced for local exchanges, maximum for guardian designation.

---

## Capability Keys and Contact Access

### Model

Contact information is never stored by anyone other than its owner. Each person publishes their own data on their instance. A received card functions as a permission token.

Capability keys are intermediate symmetric keys encrypting tiers of contact information. Alice encrypts her data once per tier — not once per recipient. When she updates her phone number, all eligible contacts get the update automatically.

### Tiers

| Key | Encrypts | Epoch |
|-----|----------|-------|
| `public_key` | Display name, visual seal, public mediums | Never |
| `community_key` | Community handles (Fediverse, Matrix, etc.) | 180 days |
| `extended_key` | Personal email, preferred messaging | 90 days |
| `close_key` | Phone, Signal, high-sensitivity mediums | 30 days |
| `guardian_key` | Recovery-related information | Guardian only |

### Access Matrix (defaults, user-overridable)

| Depth Required | Degree Required | Keys Issued |
|----------------|-----------------|-------------|
| INTRODUCED | Any | public_key |
| ACQUAINTANCE | ≤6 | + community_key |
| CONTACT | ≤3 | + extended_key |
| TRUSTED | 1 (direct) | + close_key |
| GUARDIAN | Any | + guardian_key |

Local device exchange grants a one-tier depth bonus.

### Epoch Rotation

Capability keys rotate automatically at epoch boundaries. Revocation = exclusion from next rotation. Instance-level access is cut off immediately. Emergency full rotation is available for safety-critical situations.

---

## Medium Descriptors

Contact information is declared as an ordered list of medium descriptors. The same type may appear multiple times (e.g. work email and personal email are both `type: email`).

Each descriptor contains:
- `type` — machine-readable medium identifier (from the Daplin Medium Registry or `custom:` prefix)
- `value` — the address or handle
- `protocol` — URI scheme for app-link launching (e.g. `sgnl://`, `mailto:`, `tel:`)
- `label` — human-readable context (e.g. "Work", "Personal")
- `preference` — opaque lexicographically sortable token expressing global preference order; reveals nothing about total number of mediums or hidden entries
- `tier` — capability key tier required to decrypt

The unique identifier for a medium entry is `type + value + label`.

Apps may compute a suggested contact medium by matching both parties' preference-ordered mediums — a "matchmaking" layer that suggests the best shared channel.

---

## Introductions

Contact information is never transferred between parties. Carol cannot give Bob Alice's details. She can only make an introduction:

1. **IntroductionRequest** — Carol sends Alice a signed activity with Bob's card, her attestation of Bob, and an optional note. Bob is not notified.
2. **IntroductionAccepted** — Alice approves; her card is sent to Bob. Relationship starts at INTRODUCED depth.
3. **IntroductionDeclined** — Alice declines; Carol is notified privately. Bob is never informed.

A blind introduction variant allows Carol to conceal her facilitation from one or both parties.

---

## Storage Architecture

### What Lives Where

| Layer | Contents |
|-------|----------|
| **IPFS** (public, permanent) | Cards, attestations, key rotation records, migration declarations, recovery declarations |
| **Device Secure Enclave** | Master key, device subkeys, pairwise keys (one per relationship) |
| **App Local Storage** (encrypted) | Card hashes (contact list), received capability keys, offline activity queue |
| **Instance** (transient only) | Event queue, handle resolution index, IPFS pointers |
| **Never stored anywhere** | Other users' contact details (always fetched fresh) |

Pairwise DIDs must never be published to IPFS — even encrypted, their presence would constitute an observable graph edge.

### Pairwise Channel Transport

Exchange happens locally, app-managed, invisible to the user:
- **NFC** — tap to initiate handshake
- **WiFi Direct** — transfer card data and pairwise keys (no internet required)
- **Event Queue** — encrypted re-establishment for remote scenarios only

If a device is lost, pairwise keys can be re-established without a new introduction — global DID attestations and relationship depth are preserved.

---

## Federation

- Instances expose `/.well-known/daplin` for discovery
- Cross-instance DID resolution is instance-mediated, content fetched from IPFS
- Federated activities carry encrypted payloads — instances are postmen, not readers
- Migration via signed `Migrate` activity; old instance forwards for minimum 90 days
- DID never changes during migration; all attestations remain valid
- Instances may defederate; this does not affect existing IPFS-anchored documents
- No searchable user directories — instances must not implement them

---

## Event Queue

The event queue is a per-user transient inbox on each instance for protocol activities only. It is not a messaging system. Activities are consumed and deleted once delivered.

**Activity types:** `Publish`, `Attest`, `RevokeAttestation`, `Introduce`, `IntroductionAccepted`, `IntroductionDeclined`, `IssueSubkey`, `RevokeSubkey`, `KeyRecovery`, `Migrate`, `RevokeCard`, `RotateCapabilityKey`

Daplin is identity infrastructure. It does not replicate Signal, email, or any other communication platform. Those platforms build on Daplin.

---

## Key Recovery

Hybrid model — either method alone can trigger recovery:

1. **Seed phrase recovery** — 12-word BIP39 phrase reconstructs the master key directly
2. **Social recovery** — M of N designated guardians co-sign a `KeyRecovery` activity

Recovery produces a new master keypair. The old DID is tombstoned. A signed `KeyRecovery` activity links old to new permanently. Attestations transfer to the new DID automatically. Message history encrypted to the old key is irrecoverable — this is an intentional and honest property of E2EE.

Guardian designation requires maximum PoW. Minimum 3 guardians, threshold of 2 recommended.

---

## Versioning and Governance

- **Semantic versioning:** MAJOR.MINOR.PATCH
- **Postel principle:** conservative in what you produce, liberal in what you accept
- **Unknown fields** are always silently ignored
- **Unknown activity types** are always silently discarded
- **No method is ever sunset** — did:key, did:web, and did:peer coexist permanently
- **Major version transitions** require 6-month notice, dual support period, graceful sunset
- **Governance:** open RFC process; the protocol belongs to its community of implementors

---

## DID Method Roadmap (Blockchain-Free)

| Version | Method | Notes |
|---------|--------|-------|
| v1.0 | did:key + did:peer | Global identity + pairwise channels. No infrastructure. |
| v1.1 | + did:web | Optional for self-hosters wanting true global key rotation via their own domain. |
| Future | did:peer enhancements | Improved re-establishment flows, group pairwise channels TBD. |

No blockchain methods are planned. Complexity, cost, external dependencies, and environmental concerns all weigh against them.

---

## Current Status

Specification v0.1.0 draft complete. No implementation exists yet. The project is in the design and specification phase. The spec covers identity, trust model, capability keys, medium descriptors, introductions, storage, federation, activities, key recovery, versioning, security considerations, and privacy considerations.

**Key open questions for future discussion:**
- did:web integration details for v1.1
- did:peer group channels (for future consideration)
- Medium registry governance process
- Reference implementation language and architecture choices