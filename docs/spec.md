---
layout: spec
title: Protocol Specification
subtitle: Daplin v0.2.0 — DRAFT
sitemapOrder: 2
---

## 1. Introduction

Your identity, your relationships, and your communications are yours. Not because a company promises to protect them, but because the protocol makes it structurally impossible for anyone else to own them. That is the premise Daplin is built on.

The hard problem in secure communication has never been encryption — it has been trust. How do you know the key you received belongs to the person you think it does? Existing solutions either ask you to trust a central authority, or present a complexity that defeats most people before they begin. Neither is dignified.

Daplin solves the trust problem the same way humans have always solved it — through relationships, through vouching, through the web of people who already know each other. It wraps that human reality in an open protocol that is portable, federated, and requires no one's permission to use. The result is secure communication that feels like trust, because it is.

### 1.1 Core Principles

- **Privacy is the only mode.** There is no public graph, no passive discovery, no opt-in privacy. All users are indistinguishable from the outside.
- **Identity is independent of host.** Your identity is derived from your cryptographic key, not from the server you use.
- **Vouching, not transferring.** Contact information is never passed between parties. Only introductions are made; the subject controls their own data.
- **Physical presence is the strongest trust signal.** In-person key exchange via local device communication carries more weight than any remote interaction.
- **Servers know as little as possible.** Instances are thin routing and discovery layers. They carry encrypted payloads they cannot read.
- **Daplin is a protocol, not a product.** Anyone can implement it, run an instance, or build applications on top of it.
- **Portable and self-hostable.** Users can migrate between instances without losing identity, attestations, or contact relationships.

### 1.2 Scope

This specification defines:

- Identity representation and the DID-based identity model
- The card format and visual identity system
- The trust model including degrees of separation and relationship depth
- Capability keys and access-controlled contact information
- The federation protocol and event queue model
- Activity types and their serialization
- Key recovery procedures
- Proof-of-work requirements
- Versioning and governance

This specification does not define end-to-end encrypted messaging protocols, specific UI implementations, or application-layer behavior beyond what is necessary for protocol compliance.

---

## 2. Terminology

| Term | Definition |
|------|-----------|
| **CID** | Content Identifier. IPFS's addressing scheme. A hash of a document's content that uniquely identifies it. Distinct from a DID: a CID identifies *what* something is; a DID identifies *who* someone is. |
| **DID** | Decentralized Identifier. A W3C standard URI that identifies a person or entity without requiring a central authority. |
| **Global DID** | A publicly resolvable DID (`did:key` or `did:web`) that anchors a user's identity and attestation chain. |
| **Pairwise DID** | A `did:peer` created privately between two parties at the moment of exchange. Never published. Supports per-relationship key rotation. |
| **Pairwise Channel** | The shared key agreement between two parties derived from their pairwise DID exchange. Managed silently by the app. Not a persistent connection. |
| **Deep Link** | A URI encoding a user's DID and instance endpoint, used to share identity and initiate connections. Format: `daplin://did:key:...@instance.domain` |
| **Seal Endpoint** | A known URL pattern on every instance that serves a user's visual seal as an SVG, derived deterministically from their DID hash. |
| **Card** | A signed JSON document containing a person's public identity information, anchored to their DID. |
| **Instance** | A server running the Daplin protocol. Users are homed to an instance but their identity is portable. |
| **Attestation** | A cryptographically signed declaration by one party vouching for another's key ownership. |
| **Capability Key** | An intermediate symmetric key used to encrypt a tier of contact information for eligible recipients. |
| **Relationship Depth** | A classification of how well two parties know each other personally, independent of network topology. |
| **Degree** | Network distance between two parties in the trust graph. Direct connections are 1st degree. |
| **Epoch** | A defined time period after which capability keys rotate. Each tier has its own epoch length. |
| **PoW** | Proof of Work. A computational puzzle required before certain protocol actions. |

---

## 3. Identity

### 3.1 DID Methods — Two-Layer Model

Daplin uses two complementary DID methods serving distinct purposes:

| Layer | Method | Purpose |
|-------|--------|---------|
| Global Identity | `did:key` or `did:web` | How strangers find and verify you. Publicly resolvable. Anchors the attestation chain. Exists before any relationships are formed. |
| Pairwise Identity | `did:peer` | A private key agreement between two specific parties, established at the moment of exchange. Never publicly visible. Supports per-relationship key rotation without any infrastructure. |

In v1.0, the global DID is derived directly from the user's Ed25519 master public key — the DID *is* the key.

The global DID is permanent and immutable. It is not tied to any instance, domain, or service. Attestations and activities reference the global DID. Pairwise DIDs are created per relationship and stored only on the two parties' devices — they are never published, never federated, and leave no observable trace on the network.

> **Note:** Future protocol versions will support `did:web` for users who want true global key rotation via their own domain. All DID methods coexist permanently. No method is ever sunset. The activity format is DID-method agnostic, and unknown methods must be handled with graceful degradation.

### 3.2 Key Hierarchy

Every user maintains a key hierarchy rooted in a master key:

| Key | Purpose |
|-----|---------|
| **Master Key** | Root of identity. Derives the DID. Used only to sign subkeys and recovery declarations. Must be kept cold. |
| **Signing Subkey** | Signs activities and attestations. Device-specific. Expires annually. |
| **Encryption Subkey** | Encrypts messages and capability keys. Device-specific. Expires annually. |
| **Authentication Subkey** | Proves identity to instances. Device-specific. Expires annually. |
| **Recovery Subkey** | Used exclusively for key recovery declarations. Purpose-limited. Stored cold. Expires every 5 years. |

Subkeys are device-specific. Each device a user operates receives its own set of subkeys, signed by the master key. Compromising one device's subkeys does not compromise any other device or the master key.

### 3.3 Identity Sharing — Deep Links and Seal Endpoints

Daplin does not use human-readable handles. Handles introduce spoofing risk by conditioning users to trust a text string rather than a cryptographic identity — the same mistake that makes phishing possible. The DID is the canonical identity. Display names are convenience labels on cards, not identifiers.

Identity is shared via deep links that encode the DID and instance endpoint directly:

```
daplin://did:key:z6MkhaXgBZ...@bigtime.daplin.io
```

Deep links are shared as QR codes, clickable links, or NFC payloads. They are never typed by users. Applications resolve the instance endpoint from the link and fetch the current card CID from the instance.

#### 3.3.1 Seal Endpoint

Every instance serves a seal endpoint that generates the user's visual seal from their DID hash. This enables seal images to be embedded anywhere — blog footers, email signatures, forum profiles — in the same way Gravatar provides avatar images at a known URL.

```
https://bigtime.daplin.io/seal/{did-hash}.svg
```

The seal endpoint returns an SVG. Instances apply the user's stored palette and border preferences to the base seal. Used together with a deep link:

```html
<a href="daplin://did:key:z6MkhaXgBZ...@bigtime.daplin.io">
  <img src="https://bigtime.daplin.io/seal/z6MkhaXgBZ.svg"/>
</a>
```

The seal has two tiers:

| Tier | Description |
|------|-------------|
| **Base seal** | Deterministic geometry generated from the DID hash alone. Generatable by any Daplin client without contacting any server. Always identical for a given DID regardless of instance. |
| **Personalised seal** | Base seal with user's chosen palette and border applied. Served by the user's instance. Falls back to base seal if instance is offline. |

> **Note:** The instance can serve the personalised seal but cannot falsify the locked geometry — any tampering is detectable by anyone who runs the base seal generation algorithm against the DID. Palette and border preferences are cosmetic and not security-relevant.

### 3.4 Master Key Ceremony

The master key ceremony is a required part of user onboarding. It must not be skippable, though it may be deferred by a maximum of 72 hours after account creation.

The ceremony consists of:

- Generation of a 12-word BIP39 seed phrase derived from the master key
- Presentation of the seed phrase to the user, one word at a time
- Confirmation of 3 randomly selected words to verify the user has recorded them
- Optional: encrypted backup to a user-chosen cloud provider (iCloud Keychain, Google Password Manager)

> **Note:** The master key must never be transmitted over the network. The seed phrase backup is an encrypted local export. Cloud providers receive only ciphertext.

---

## 4. The Card

### 4.1 Card Structure

A card is a signed JSON document anchored to a DID. It contains a public skeleton visible to all, and encrypted tiers accessible only to eligible contacts.

```json
{
  "daplin": "1.0.0",
  "did": "did:key:z6MkhaXgBZ...",
  "cardVersion": 3,
  "previousCard": "bafybeig9a2p...",
  "displayName": "Alice",
  "sealPalette": "midnight",
  "sealBorder": "clean",
  "publicMediums": [],
  "encryptedTiers": {
    "community": "<ciphertext>",
    "extended": "<ciphertext>",
    "close": "<ciphertext>",
    "guardian": "<ciphertext>"
  },
  "signature": "..."
}
```

### 4.2 Visual Identity

Each card has a deterministic visual seal generated from the user's public key hash. The seal is the primary visual identifier for a user and functions as a security primitive: any change to the underlying key produces a completely different seal.

| Seal Property | Status |
|---------------|--------|
| Core geometry | Locked — deterministic from key hash |
| Inner pattern structure | Locked — deterministic from key hash |
| Proportions and symmetry | Locked — deterministic from key hash |
| Colour palette | User-chosen from curated sets |
| Border style | User-chosen |
| Background texture | User-chosen |

The visual generation algorithm is defined as part of the protocol version. A card declares its protocol version; the rendering algorithm is implied. If the protocol version changes the visual algorithm, cards on the old version continue to render correctly because they declare their version.

Applications should display a subtle notice when a contact's seal changes, as this indicates their key has changed.

### 4.3 Card Versioning

Cards are immutable once published to IPFS. Profile updates produce a new card with an incremented `cardVersion` and a `previousCard` pointer to the prior card's CID. This creates an auditable history of all identity changes.

---

## 5. Trust Model

### 5.1 Two Independent Axes

Trust in Daplin is expressed across two completely independent dimensions:

| Axis | Description |
|------|-------------|
| **Network Topology (Degrees)** | The shortest path between two parties in the attestation graph. Reflects how you were connected. Immutable history; new connections create shorter paths but old paths remain. |
| **Relationship Depth** | A personal classification of how well you know someone. Set deliberately by the user. Independent of network position. Grows over time. |

### 5.2 Relationship Depth Levels

| Level | Meaning | Typical Trigger |
|-------|---------|----------------|
| `INTRODUCED` | Accepted an introduction. No personal attestation. | Default when accepting any introduction. |
| `ACQUAINTANCE` | Basic trust established. Have interacted. | You would recognise them in person. |
| `CONTACT` | Established relationship. | You would recommend them. |
| `TRUSTED` | Deep personal trust. | You would vouch for them to others. |
| `GUARDIAN` | Maximum trust. Recovery participant. | You would rely on them in an emergency. |

> **Note:** Accepting an introduction is NOT an attestation. It creates an `INTRODUCED` relationship only. Attestation is a separate, deliberate action.

### 5.3 Degrees of Separation

The effective degree between two parties is the length of the shortest current path in the attestation graph. As new direct attestations are created, shorter paths emerge and become the effective degree. Historical paths remain permanently recorded on IPFS.

### 5.4 Exchange Method

The method by which two parties first exchanged cards is recorded in the initial attestation and contributes to trust weight:

| Method | Trust Weight |
|--------|-------------|
| `local_device` | Strongest. Physical presence verified via NFC + WiFi Direct. |
| `introduction` | Strong. A trusted mutual contact vouched for the connection. |
| `remote_link` | Moderate. Initiated via deep link, no prior context. |

### 5.5 Proof of Work

Certain protocol actions require a computational proof of work to prevent spam, bot farms, and graph scraping. Daplin uses memory-hard puzzles (Argon2id) that are resistant to parallelization and ASIC optimization.

Difficulty is adaptive: the puzzle is tuned so that the time cost remains approximately constant across devices of varying capability, while the actual computational cost scales with device power.

| Action | PoW Requirement | Approx. Time Cost |
|--------|----------------|-------------------|
| Attestation (local exchange) | Reduced | ~5 seconds |
| Attestation (remote) | Standard | ~30 seconds |
| Guardian designation | Maximum | ~10 minutes |

---

## 6. Capability Keys and Contact Access

### 6.1 Model

Contact information in Daplin is never stored by anyone other than its owner. Each person publishes their own contact information on their instance. A received card functions as a permission token: possession of a valid signed card proves the right to fetch the card owner's profile.

Capability keys are intermediate symmetric keys that encrypt tiers of contact information. They allow Alice to encrypt her data once per tier rather than once per recipient. When Alice changes her phone number, she re-encrypts with the same `close_key` and all eligible recipients automatically have access to the update.

### 6.2 Capability Key Tiers

| Key | Encrypts | Epoch |
|-----|----------|-------|
| `public_key` | Display name, visual seal, public mediums | Never rotates |
| `community_key` | Community handles (Fediverse, Matrix, etc.) | 180 days |
| `extended_key` | Personal email, preferred messaging | 90 days |
| `close_key` | Phone, Signal, high-sensitivity mediums | 30 days |
| `guardian_key` | Recovery-related information | Guardian only |

### 6.3 Access Matrix

Access to capability keys is determined by the combination of relationship depth and effective degree. These are defaults and may be overridden per-contact by the user.

| Depth Required | Degree Required | Keys Issued |
|----------------|-----------------|-------------|
| `INTRODUCED` | Any | `public_key` |
| `ACQUAINTANCE` | ≤6 | + `community_key` |
| `CONTACT` | ≤3 | + `extended_key` |
| `TRUSTED` | 1 (direct only) | + `close_key` |
| `GUARDIAN` | Any | + `guardian_key` |

Local device exchange grants a one-tier depth bonus.

### 6.4 Epoch Rotation

Capability keys rotate automatically at the end of each epoch. This is the primary mechanism for access revocation: excluded contacts simply do not receive the new key at the next rotation.

Instance-level access is cut off immediately upon revocation regardless of key rotation status. The instance will reject profile fetch requests from revoked contacts at once. Key epoch rotation provides cryptographic completeness over time.

An emergency full rotation is available for safety-critical situations. This immediately generates new keys for all tiers and re-issues them to all eligible contacts. Applications must make this option accessible but clearly labeled as an emergency action.

### 6.5 Key Issuance

- **Local exchange:** Keys are exchanged directly device-to-device via WiFi Direct after NFC tap initiation. The instance is not involved.
- **Remote connection:** Keys are issued by the instance upon completion of an introduction flow, after the subject approves.

In both cases, capability keys are encrypted for the recipient using the recipient's encryption subkey before transmission.

---

## 7. Medium Descriptors

### 7.1 Format

Contact information is declared as an ordered list of medium descriptors. Each descriptor specifies a communication channel in a uniform, machine-readable format. The same medium type may appear multiple times with different values (e.g. a work email and a personal email are both `type: email`).

### 7.2 Fields

| Field | Description |
|-------|-------------|
| `type` | Machine-readable medium identifier. From the Daplin Medium Registry or `custom:` prefix for unregistered types. |
| `value` | The address or handle for this medium. |
| `protocol` | URI scheme for app-link launching (e.g. `sgnl://`, `mailto:`, `tel:`). |
| `label` | Human-readable context label (e.g. "Work", "Personal"). Required when the same type appears more than once. |
| `preference` | An opaque lexicographically sortable token expressing the owner's global preference ordering across all mediums. Reveals no information about total medium count or position of hidden mediums. |
| `tier` | The capability key tier required to decrypt this medium. |

The unique identifier for a medium entry is the combination of `type + value + label`.

### 7.3 Preference Matching

Applications may compute a suggested contact medium by comparing the preference-ordered mediums of both parties:

1. Find the intersection: mediums of the same type present in both lists.
2. Score by combined preference rank.
3. On a tie, the subject's preference wins.

This matching computation is an application-layer convenience, not a protocol requirement.

### 7.4 Medium Registry

The Daplin Medium Registry is an open registry of known medium types and their canonical protocol URIs. Core types defined in this specification include: `email`, `phone`, `signal`, `whatsapp`, `telegram`, `matrix`, `fediverse`, `xmpp`, `url`. Community types may be submitted for registration. Unregistered custom types are supported using the `custom:` prefix.

### 7.5 Graceful Degradation

Applications encountering an unknown medium type must not fail. They must display the label and value as plain text with a copy option, and may attempt to launch the protocol URI if present. No medium type may cause a card to fail to render.

---

## 8. Introductions

### 8.1 Principle

Contact information in Daplin is never transferred between parties. When Carol knows both Alice and Bob, she cannot give Bob Alice's contact details. She may only make an introduction: a signed request to Alice on Bob's behalf, carrying Carol's attestation and Bob's card.

This principle ensures that the subject of an introduction always controls whether the connection is made. It also means that introductions carry the introducer's reputation: Carol is implicitly vouching with her relationship to Alice, creating a natural social cost to frivolous introductions.

### 8.2 Introduction Flow

Introductions are a two-phase protocol:

1. **IntroductionRequest:** Carol sends Alice a signed activity containing Bob's card, Carol's attestation of Bob, and an optional note. Bob is not notified at this stage.
2. **IntroductionAccepted:** Alice approves. Alice's card is sent to Bob. Both parties may now exchange capability keys and establish a relationship at `INTRODUCED` depth.
3. **IntroductionDeclined:** Alice declines. Carol is notified privately. Bob is not informed that an introduction was attempted.

> **Note:** Accepting an introduction creates an `INTRODUCED` relationship only. It does not constitute an attestation and does not grant access to any capability keys beyond `public_key`.

### 8.3 Blind Introductions

An optional blind introduction variant allows Carol to conceal her identity from Bob (or from both parties). Alice sees that someone who knows her has facilitated an introduction, but the facilitator's identity is not revealed unless Alice explicitly requests it. This protects the introducer's privacy in sensitive contexts.

---

## 9. Storage

### 9.1 IPFS

All permanent signed documents in Daplin are stored on IPFS and addressed by their CID (Content Identifier). This means any document can be verified for integrity by anyone who has its CID, and no single server can alter or destroy a published document.

| Stored on IPFS | Never stored on IPFS |
|----------------|----------------------|
| Cards and card history | Pairwise DIDs (`did:peer`) — device only |
| Attestations | Profile field values — encrypted blobs on IPFS, keys device only |
| Key rotation records | Capability keys — device only |
| Migration declarations | Private messages — device only |
| Recovery declarations | Event queue contents — transient, instance only |
| Accepted introduction activities | |

Profile field values are encrypted via capability keys and stored on IPFS as opaque blobs. The blobs are publicly retrievable but unreadable without the appropriate capability key. Pairwise DIDs must never be published to IPFS under any circumstances — even encrypted, their presence would constitute an observable graph edge.

### 9.2 IPFS as a Separate Concern

The Daplin instance software communicates with IPFS via a defined storage interface. IPFS is not bundled into the instance software. This separation ensures each component does one job well and allows operators to choose their own IPFS backend:

| Backend Option | Best For |
|----------------|----------|
| **Docker Compose stack (recommended)** | Self-hosters wanting a single-command install. The reference deployment ships as a Docker Compose stack pairing the Daplin instance with an IPFS node (`ipfs/kubo`). |
| **External IPFS node** | Operators who already run IPFS infrastructure or want full control over their node configuration. |
| **Pinning service** (e.g. Pinata) | Managed hosting scenarios where operators do not want to maintain a node directly. |

> **Note:** The reference Docker Compose stack is the recommended starting point for self-hosters. It requires no prior IPFS knowledge and is brought up with a single command. Operators who want to substitute their own IPFS backend simply omit the IPFS service from the compose stack and configure the storage interface to point at their preferred endpoint.

### 9.3 Device Storage

The device is the most trusted storage layer in Daplin. All cryptographic material lives here and never leaves except as encrypted payloads to intended recipients.

| Storage Location | Contents |
|-----------------|----------|
| **Secure Enclave** | Master key, device subkeys, pairwise keys (one per relationship) |
| **App Local Storage** (encrypted) | Card CIDs (contact list), received capability keys, offline activity queue |
| **Never stored locally** | Other users' contact information — always fetched fresh on demand |

Applications do not store copies of other users' contact information. Profile data is always fetched fresh from the subject's instance using the card as a permission token, with the capability key used to decrypt the response.

### 9.4 Pairwise Channel Transport

Pairwise DIDs and their associated keys are exchanged directly between devices using local transport. The instance is never involved. The transport layer is used only for delivery — once keys are on both devices, the transport is irrelevant and no persistent connection is maintained.

| Transport | Role |
|-----------|------|
| **NFC** | Initiates the handshake. Tap to signal intent to connect. Short range prevents interception. |
| **WiFi Direct** | Transfers card data and pairwise keys. Fast, offline, no internet required. Primary payload transport. |
| **Event Queue** (remote only) | Encrypted re-establishment activity when in-person exchange is not possible. Instance sees only ciphertext. |

From the user's perspective, the entire exchange is a single tap. The app silently generates the pairwise keypair, completes the exchange via WiFi Direct, verifies the counterpart's global DID signature, stores the pairwise keys in the secure enclave, issues capability keys, and queues any attestation for later publication.

### 9.5 Pairwise Channel Re-establishment

If a device is lost, pairwise keys for all relationships on that device are gone. Re-establishment does not require a new introduction — the existing global DID attestation and relationship depth are preserved. The app initiates a re-establishment flow:

- **In person:** NFC tap and WiFi Direct exchange generates new pairwise keys. Strongest option.
- **Remote:** Alice sends a signed re-establishment activity via the event queue, signed with her global DID signing subkey to prove continuity. Bob's app verifies and updates the pairwise record silently.

> **Note:** Re-establishment is not visible to the user beyond a brief confirmation. It does not affect relationship depth, attestations, or capability key access.

### 9.6 Instances

Instances are thin infrastructure layers. They do not store contact information, social graphs, pairwise DIDs, or message content. Their responsibilities are:

- Resolving a DID to its current card CID and instance endpoint
- Event queue management: temporary delivery of protocol activities
- IPFS pinning: coordinating with the configured IPFS backend to ensure their users' documents remain available
- Capability key issuance: mediating access control for remote connections

An instance that goes offline does not destroy user data. Cards and attestations remain on IPFS. Pairwise keys remain on devices. Users can migrate to a new instance and resume normal operation.

---

## 10. Federation

### 10.1 Instance Discovery

Every compliant Daplin instance must expose a well-known endpoint describing its capabilities:

```
GET /.well-known/daplin
```

```json
{
  "daplin": "1.0.0",
  "instance": "bigtime.daplin.io",
  "name": "Bigtime",
  "federation": true,
  "registrations": "invite-only"
}
```

### 10.2 Cross-Instance Resolution

When a user on one instance needs to resolve a DID homed on another instance, their instance fetches the current card CID from the remote instance and caches it. The actual card content is fetched from IPFS using the CID, not from the remote instance. Instances are routing layers, not data stores.

### 10.3 Portability and Migration

Identity portability is a core protocol guarantee. Users must be able to migrate between instances without losing identity, attestations, or contact relationships.

Migration is initiated by publishing a signed `Migrate` activity, which is federated to all known contacts' instances. The old instance must continue to forward resolution requests for a minimum of 90 days after a migration is declared.

The user's DID never changes during migration. All attestations, which reference the DID rather than any instance, remain valid.

### 10.4 Instance Trust

Instances may choose to federate or defederate from other instances based on their own policies. Defederation prevents activities from being exchanged between instances but does not affect the validity of identities or attestations that already exist on IPFS.

---

## 11. Activities

### 11.1 Common Fields

All activities share a common envelope:

```json
{
  "daplin": "1.0.0",
  "type": "Attest",
  "id": "<uuid>",
  "actor": "did:key:z6MkhaXgBZ...",
  "timestamp": "2026-03-11T10:00:00Z",
  "pow": { "nonce": "...", "hash": "..." },
  "payload": {},
  "signature": "..."
}
```

### 11.2 Activity Reference

| Type | Description | PoW Required |
|------|-------------|-------------|
| `Publish` | Publishes a new or updated card to IPFS. | Yes |
| `Attest` | Issues a cryptographic attestation of another party's key ownership. | Yes |
| `RevokeAttestation` | Withdraws a previously issued attestation. | No |
| `Introduce` | Requests an introduction between two parties. | Yes |
| `IntroductionAccepted` | Subject accepts an introduction. | No |
| `IntroductionDeclined` | Subject declines an introduction (private). | No |
| `IssueSubkey` | Registers a new device subkey signed by the master key. | No |
| `RevokeSubkey` | Revokes a device subkey. | No |
| `KeyRecovery` | Declares a key recovery event linking old DID to new DID. | Yes |
| `Migrate` | Declares migration to a new instance. | No |
| `RevokeCard` | Tombstones a card. | Yes |
| `RotateCapabilityKey` | Announces a capability key epoch rotation. | No |

---

## 12. Key Recovery

### 12.1 Recovery Methods

Daplin supports two complementary recovery methods. Either method alone is sufficient to initiate recovery:

- **Seed phrase recovery:** The 12-word BIP39 phrase generated during the master key ceremony reconstructs the master key directly.
- **Social recovery:** A threshold of M designated guardians (out of N total) co-sign a `KeyRecovery` activity on behalf of the user. The threshold is chosen by the user at guardian designation time.

### 12.2 Recovery Process

Key recovery produces a new master keypair and a new DID. The old DID is tombstoned. The `KeyRecovery` activity, signed by guardians or derived from the seed phrase, links the old DID to the new DID and serves as the permanent public record of the transition.

All previous attestations, which reference the old DID, remain valid and are considered transferred to the new DID by the `KeyRecovery` activity. Contacts who receive the federated `KeyRecovery` activity update their records automatically.

### 12.3 What Recovery Cannot Restore

Key recovery cannot restore the ability to decrypt messages encrypted to the old key. This is an intentional property of end-to-end encryption and must be communicated clearly to users during the master key ceremony.

### 12.4 Guardian Designation

Guardian designation requires maximum proof of work and is recorded as a signed activity. Users should designate a minimum of 3 guardians and select a threshold of 2. Guardians should be people reachable through independent communication channels in an emergency.

---

## 13. Versioning and Governance

### 13.1 Versioning Scheme

Daplin uses semantic versioning in the format `MAJOR.MINOR.PATCH`:

| Component | Meaning |
|-----------|---------|
| MAJOR | Breaking changes to the activity format or identity model. |
| MINOR | Backwards-compatible additions (new activity types, new fields). |
| PATCH | Bug fixes and clarifications. No format changes. |

### 13.2 Compatibility Rules

All compliant implementations must follow the Postel principle: be conservative in what you produce, liberal in what you accept. Implementations must never remove support for existing activity types or change the meaning of existing fields. New fields are always optional. Unknown fields are silently ignored. Unknown activity types are silently discarded.

### 13.3 Major Version Transitions

Major version changes require a minimum 6-month notice period before the new version is declared stable. During the transition period, instances must support both versions simultaneously. Instances on the old version must never be forcibly broken; they may continue to federate with other old-version instances indefinitely.

### 13.4 Governance

Protocol changes are governed by an open RFC process. Any party may submit a proposal. Proposals are publicly discussed for a minimum of 60 days before any decision is made. The protocol belongs to its community of implementors, not to any single organization.

---

## 14. Security Considerations

### 14.1 Threat Model

| Threat | Mitigation | Residual Risk |
|--------|-----------|---------------|
| Impersonation via fake key | Attestation chain and visual seal verification. | Low |
| Bot farm attestations | Proof of work on all attestations. | Medium |
| Instance compromise | Instances hold only encrypted payloads and transient events. | Low |
| Graph enumeration | No public directory. PoW on traversal queries. ZK path proofs. | Low |
| Social engineering of guardians | Guardian designation requires PoW and deliberate action. | Medium |
| Device loss | Pairwise re-establishment without new introduction. Seed phrase recovery. | Low |

### 14.2 Metadata

Even with encrypted content, metadata — who communicates with whom, when, and how frequently — can be revealing. Daplin minimizes metadata at the protocol level by ensuring instances carry only encrypted activities and transient event queues. Applications building messaging on top of Daplin should implement sealed sender patterns to further reduce metadata exposure.

### 14.3 Key Loss

If both the seed phrase and all guardians are unavailable, the identity cannot be recovered. This is an intentional and honest property of a system that cannot be controlled by any third party. Users must be clearly informed of this during the master key ceremony.

---

## 15. Privacy Considerations

### 15.1 Privacy as Default

Privacy is not a mode or a setting in Daplin — it is the only state. There is no opt-in privacy, no public profile, and no passive discovery. All users are structurally indistinguishable from the outside.

### 15.2 Data Minimization

The protocol is designed around data minimization. Instances store pointers and transient events, not data. Contact information lives only with its owner. Social graphs exist only in encrypted form on clients. The only information an instance operator can observe is that their user sent or received an activity, not what it contained.

### 15.3 Right to Erasure

Because each user owns and publishes their own data, erasure is straightforward: a user who deletes their profile from their instance removes the only authoritative source of their contact information. Cards and attestations on IPFS are immutable, but they contain only public-key-anchored identity information, not contact details.

### 15.4 High-Risk Users

Daplin is designed to be safe for activists, journalists, abuse survivors, and others with elevated privacy needs. These users benefit from the same privacy guarantees as all users. Additional recommendations for high-risk users include:

- Use `did:key` rather than `did:web` to avoid domain-linked identity
- Designate guardians who are reachable through entirely separate communication channels
- Use local device exchange exclusively; avoid remote connections where possible
- Self-host or use a trusted small instance rather than a large public instance

---

## Appendix A: Parking Lot

The following items were identified during the design process as warranting future discussion but are not yet incorporated into the specification:

- **Personal emblem on card:** Decided against in v1. May be reconsidered in future versions.
- **`did:web` support:** Planned for v1.1. Enables true global key rotation via a user's own domain.
- **Subkey-based key rotation:** Subkeys provide practical rotation; master key rotation remains tied to DID method.
- **Sealed sender for messaging layers:** Recommended but out of scope for this specification.
- **Medium registry governance:** Process for community submission and review of new medium types to be defined separately.

---

## Appendix B: Change Log

| Version | Notes |
|---------|-------|
| 0.1.0 | Initial draft. Core identity, trust, capability key, federation, and activity models defined. |
| 0.2.0 | New introduction. Handles removed; replaced with deep link format and seal endpoint. Two-layer DID model (global + pairwise). CID terminology corrected throughout. IPFS separated as external concern with Docker Compose reference deployment. Pairwise channel transport and re-establishment documented. Capability key epoch rotation model added. Blockchain references removed. |

---

*End of Daplin Protocol Specification v0.2.0*
