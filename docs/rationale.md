---
layout: default
title: Project Rationale
excerpt: Why Daplin is designed the way it is — the design philosophy behind the protocol.
nav_order: 3
---

## The Problem

Secure communication has a trust problem that encryption alone cannot solve. Encryption is well understood. The hard part is knowing that the key you received actually belongs to the person you think it does.

The solutions that exist today fall into two camps. The first asks you to trust a central authority — a certificate authority, a platform, a company — to vouch for the binding between a person and their key. This works until the authority is compromised, coerced, or simply decides your interests are not its priority. The second presents a complexity that defeats most people before they begin: key servers, fingerprint verification, manual out-of-band confirmation. Neither approach is dignified. Neither scales to the way people actually form trust.

Daplin is built on a different premise: the trust problem is a social problem, and it already has a social solution. People establish trust through relationships. They vouch for each other. They form webs of mutual recognition that carry real information about who can be trusted and how much. Daplin wraps that human reality in a protocol.

---

## Identity Without a Landlord

Most digital identity is rented. Your email address belongs to Google or Microsoft. Your social media identity belongs to the platform. When the platform changes its terms, suspends your account, or shuts down, your identity goes with it.

Daplin identity is owned. Your identity is derived directly from your cryptographic master key — a key that lives on your device and never leaves it. The DID (Decentralized Identifier) that represents you globally *is* your key. No server issued it. No server can revoke it.

This is implemented through a two-layer DID architecture:

- **Global identity (`did:key`)** — publicly resolvable, anchors your attestation chain, exists before any relationships are formed. Permanent and immutable.
- **Pairwise identity (`did:peer`)** — a private key agreement created between two specific parties at the moment of exchange. Never published, never federated, leaves no observable trace on the network.

When you migrate from one instance to another, your DID does not change. Your attestations — the record of who has vouched for you — do not change. Your relationships do not change. The instance is infrastructure you use, not identity you depend on.

---

## Trust Through Relationships

Trust in Daplin is expressed across two completely independent dimensions.

The first is **network topology**: the shortest path between two parties in the attestation graph. If Alice has attested to Bob, and Bob has attested to Carol, then Alice and Carol are two degrees apart. This is an objective measure of how the network connects two people. It is immutable — new connections can create shorter paths, but old paths remain permanently recorded.

The second is **relationship depth**: a personal classification that each user sets deliberately. `INTRODUCED`, `ACQUAINTANCE`, `CONTACT`, `TRUSTED`, `GUARDIAN`. These are not computed — they are chosen. They reflect how well you personally know someone, independent of how the network connects you.

These two axes combine to determine what access a contact receives. A direct connection (`TRUSTED`, 1 degree) gets access to your most sensitive contact information. A distant introduction (`INTRODUCED`, 6 degrees) gets only your public identity.

One design decision deserves emphasis: **accepting an introduction is not an attestation**. When Carol introduces Alice to Bob, Alice accepting that introduction creates an `INTRODUCED` relationship — nothing more. Attestation is a separate, deliberate action. This distinction matters because it preserves the social cost of vouching. An attestation means something. It should require a conscious choice.

Physical presence is the strongest trust signal in the system. A card exchange completed via NFC tap and WiFi Direct — two devices in the same room — carries more weight than any remote interaction. This is not a technical preference; it reflects how trust actually works in human relationships.

---

## Tiered Access, Not All-or-Nothing

Contact information in Daplin is never stored by anyone other than its owner. There is no central database of phone numbers, email addresses, or messaging handles. Each person publishes their own contact information on their own instance, encrypted in tiers.

Capability keys are intermediate symmetric keys that encrypt tiers of contact information. Alice encrypts her phone number once with her `close_key` — not once per recipient. Every contact who has earned access to that tier can decrypt it. When Alice changes her phone number, she re-encrypts with the same key, and all eligible contacts automatically have access to the update.

The tiers are:

| Key | Encrypts | Rotates |
|-----|----------|---------|
| `public_key` | Display name, visual seal, public mediums | Never |
| `community_key` | Community handles (Fediverse, Matrix, etc.) | Every 180 days |
| `extended_key` | Personal email, preferred messaging | Every 90 days |
| `close_key` | Phone, Signal, high-sensitivity mediums | Every 30 days |
| `guardian_key` | Recovery-related information | Guardian only |

Revocation is built into the rotation model. When a capability key rotates at the end of its epoch, excluded contacts simply do not receive the new key. There is no revocation list to maintain, no notification to send. The excluded contact's access expires naturally at the next rotation.

---

## Federation Without a Center

Daplin instances are deliberately thin. They do not store contact information. They do not maintain social graphs. They carry encrypted payloads they cannot read. They are postmen, not readers.

An instance's responsibilities are narrow: resolve a DID to its current card, manage a transient event queue for protocol activities, coordinate with IPFS to keep documents available. That is all.

This thinness is a security property. An instance that is compromised, subpoenaed, or simply shut down cannot expose what it does not have. Cards and attestations live on IPFS — content-addressed, immutable, not controlled by any single server. Pairwise keys live on devices. Contact information lives only with its owner.

Federation between instances uses a well-known discovery endpoint and signed HTTP activities. Instances can choose to federate or defederate from each other based on their own policies. Defederation affects activity delivery but does not affect the validity of identities or attestations that already exist on IPFS. The network is resilient to individual instances going offline or going bad.

Migration is a first-class operation. A user who wants to move from one instance to another publishes a signed `Migrate` activity. Their DID does not change. Their attestations remain valid. The old instance forwards resolution requests for a minimum of 90 days. No searchable user directories exist — instances must not implement them.

---

## Why No Blockchain

Blockchain-based identity systems have been proposed and built. Daplin does not use one, and does not plan to.

The reasons are practical, not ideological:

- **Complexity** — Blockchain integration adds significant implementation complexity with no corresponding benefit for the use cases Daplin addresses.
- **Cost** — Transaction fees and gas costs create barriers to participation that are incompatible with a protocol designed to be accessible to everyone.
- **External dependencies** — Tying identity to a specific blockchain creates a dependency on that chain's continued operation, governance, and economic viability.
- **Environmental concerns** — Proof-of-work chains carry environmental costs that are difficult to justify for an identity protocol.

The DID methods Daplin uses — `did:key` and `did:peer` in v1.0, with `did:web` planned for v1.1 — require no blockchain. They are self-certifying: the DID is derived from the key, and the key is the proof. No external ledger is needed to verify that a DID is valid.

---

## Infrastructure, Not Application

Daplin is a protocol, not a product. It does not have a user interface. It does not send messages. It does not store your conversations.

What it does is solve the key distribution problem — the hard part that every secure communication application has to solve before it can do anything else. How do you know the key you received belongs to the person you think it does? Daplin answers that question.

Messaging clients, email systems, and other communication tools build on top of Daplin rather than replicating it. A Signal-like application built on Daplin would use Daplin to establish that Alice's key really belongs to Alice, and then use its own end-to-end encryption for the messages themselves. Daplin handles identity and trust. The application handles communication.

This separation of concerns is intentional. Daplin does one thing and does it well. The applications that build on it can do their one thing well too.
