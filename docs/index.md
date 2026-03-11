---
layout: spec
title: Daplin
subtitle: Dignified Attestation Protocol for Linked Identity Networks
sitemapOrder: 1
---

Your identity, your relationships, and your communications are yours. Not because a company promises to protect them, but because the protocol makes it structurally impossible for anyone else to own them.

The hard problem in secure communication has never been encryption — it has been trust. How do you know the key you received belongs to the person you think it does? Existing solutions either ask you to trust a central authority, or present a complexity that defeats most people before they begin. Neither is dignified.

Daplin solves the trust problem the same way humans have always solved it — through relationships, through vouching, through the web of people who already know each other. It wraps that human reality in an open protocol that is portable, federated, and requires no one's permission to use. The result is secure communication that feels like trust, because it is.

---

## Core Principles

- **Privacy is the only mode.** There is no public graph, no passive discovery, no opt-in privacy. All users are indistinguishable from the outside.
- **Identity is independent of host.** Your identity is derived from your cryptographic key, not from the server you use.
- **Vouching, not transferring.** Contact information is never passed between parties. Only introductions are made; the subject controls their own data.
- **Physical presence is the strongest trust signal.** In-person key exchange via local device communication carries more weight than any remote interaction.
- **Servers know as little as possible.** Instances are thin routing and discovery layers. They carry encrypted payloads they cannot read.
- **Daplin is a protocol, not a product.** Anyone can implement it, run an instance, or build applications on top of it.
- **Portable and self-hostable.** Users can migrate between instances without losing identity, attestations, or contact relationships.

---

## What Daplin Is

Daplin is an open protocol for decentralized digital identity, cryptographic public key exchange, and social trust. It gives people portable digital identity cards anchored to their own cryptographic keys — not to any server, company, or service. Identity is derived from keys, not from whoever happens to be hosting your account today.

The trust model is built on human relationships. Two people who know each other can attest to each other's identity. Those attestations form a graph — not a public one, but a private one that exists only on the devices of the people involved. Trust is computed from the shortest path between two parties in that graph, combined with how well they personally know each other. No central authority decides who trusts whom.

Daplin is infrastructure, not an application. It does not replace Signal, email, or any other communication platform. Those platforms build on top of Daplin — using it to solve the key distribution problem that has always been their hardest challenge. Daplin handles identity and trust; applications handle communication.

---

## Project Status

Daplin is in the **design and specification phase**. The v0.2.0 protocol specification is complete as a draft. No implementation code exists yet.

The next milestone is a reference server implementation in Python/FastAPI — a federated instance server that proves the protocol works end-to-end with two instances exchanging identity cards.

The specification is open for review and feedback. If you find ambiguities, missing edge cases, or design problems, [open an issue](https://github.com/cwlls/daplin/issues).

---

## Explore

- [**Protocol Specification**](spec.md) — The full Daplin v0.2.0 protocol specification
- [**Project Rationale**](rationale.md) — Why Daplin is designed the way it is
- [**On the Name**](naming.md) — The origin and meaning of "Daplin"
- [**AI-Human Collaboration**](ai-collaboration.md) — How this project was built
- [**Contributing**](contributing.md) — How to get involved
- [**GitHub Repository**](https://github.com/cwlls/daplin) — Source code and issue tracker

---

Daplin is licensed under the [Apache License 2.0](https://github.com/cwlls/daplin/blob/main/LICENSE).
