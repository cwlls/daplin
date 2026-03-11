# Daplin

**Dignified Attestation Protocol for Linked Identity Networks**

> **Project Status: Design & Specification Phase**
>
> Daplin is in active design. The protocol specification (v0.2.0 draft) is complete. The documentation site is live at [daplin.org](https://daplin.org). No server implementation code exists yet. Everything described below reflects the intended design, not current functionality.

---

## What is Daplin?

Daplin is an open protocol for digital identity and contact exchange. It lets people share contact information securely, without relying on any single company or platform to hold their data.

Think of it as a digital business card system where:

- **You own your identity.** Your identity is based on cryptographic keys that live on your device, not an account on someone else's server. You can move between providers without losing your identity, your contacts, or the trust you've built.
- **You control your information.** Your contact details (phone number, email, social handles) are encrypted and stored by you. When you share a card with someone, you're granting them a key to access specific tiers of your information — not handing over a copy they keep forever.
- **No one can see the social graph.** There is no public directory of users. No one — not even the servers that route messages — can see who knows whom. Privacy is the default and only mode.
- **Trust is built through people, not platforms.** Trust comes from real relationships: meeting someone in person, or being introduced by a mutual contact. The protocol tracks how you met and how closely you're connected, and uses that to determine what information you're comfortable sharing.

## How It Works (Simplified)

1. **Create an identity.** You generate a set of cryptographic keys on your device. These keys *are* your identity — no registration with a central authority required.

2. **Share your identity.** You share your identity via a deep link (like `daplin://did:key:...@instance.example.com`) or QR code. The link encodes your DID and the instance that routes messages on your behalf. The instance is a postman: it delivers sealed envelopes but cannot read them.

3. **Exchange cards.** When you meet someone (in person or remotely), you exchange cards. Each card is a signed document containing your public identity and encrypted layers of contact information.

4. **Control access with tiers.** Your contact information is organized into tiers — public details, community handles, personal email, phone number — each encrypted with a different key. You decide which tier each contact can access, and you can revoke access at any time.

5. **Get introduced.** A mutual contact can introduce you to someone new. Importantly, they cannot share your information — they can only ask if you'd like to be introduced. You always have the final say.

## Core Principles

- **Privacy is the only mode.** No public profiles, no searchable directories, no opt-in privacy toggles.
- **Identity is portable.** Switch servers without losing anything. Your identity, contacts, and trust relationships travel with you.
- **Servers are thin.** Instances route encrypted activities and resolve DIDs. They cannot read your data, see your contacts, or map your relationships.
- **No blockchain.** Identity is anchored to cryptographic keys and content-addressed storage (IPFS), not a blockchain. No tokens, no gas fees, no environmental cost.
- **Open protocol, not a product.** Daplin is infrastructure. Anyone can implement it, run an instance, or build applications on top of it.

## Project Status

| Component | Status |
|-----------|--------|
| Protocol specification (v0.2.0) | Draft complete |
| Architectural design | Complete |
| Documentation site (daplin.org) | Complete |
| Reference server implementation | Not started |
| Client libraries | Not started |
| Federation testing | Not started |

The immediate goal is a **reference implementation of the instance server** in Python — a vertical slice that proves two instances can federate and exchange cards. This is pre-alpha software that does not exist yet.

## Documentation

The full project documentation is published at **[daplin.org](https://daplin.org)**, a static site built with Jekyll and hosted on GitHub Pages. The site includes:

- **Protocol Specification** — The complete v0.2.0 protocol specification
- **Project Rationale** — Design philosophy and the problem space Daplin addresses
- **Naming Statement** — The origin and significance of the name "Daplin"
- **AI-Human Collaboration** — A reflection on how AI augmented the design process
- **Contributing Guide** — How to contribute to the project

## License

Apache License 2.0 — see [LICENSE](LICENSE) for details.
