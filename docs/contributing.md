---
layout: spec
title: Contributing
subtitle: How to get involved with Daplin
sitemapOrder: 6
---

## Project Status

Daplin is in the design and specification phase. The v0.2.0 protocol specification is complete as a draft. No implementation code exists yet. A reference server implementation in Python/FastAPI is planned as the next major milestone.

This means the most valuable contributions right now are not code — they are careful reading, critical thinking, and substantive feedback on the protocol itself.

---

## What We Need Now

### Specification Review

Read the [Protocol Specification](spec.md) carefully. Look for:

- **Ambiguities** — places where the spec could be interpreted two different ways
- **Missing edge cases** — scenarios the spec doesn't address but should
- **Internal inconsistencies** — places where two sections contradict each other
- **Underspecified behavior** — areas where an implementor would have to guess

Open a GitHub issue for each finding. Be specific: quote the relevant section, describe the problem, and if you have a proposed resolution, include it.

### Security Analysis

The cryptographic architecture, trust model, and threat model in the spec (§14) are designed to be sound, but independent review is essential. If you have expertise in:

- Cryptographic protocol design
- Decentralized identity systems
- Threat modeling
- Privacy engineering

...your analysis is particularly valuable. Open an issue or start a discussion.

### Protocol Design Feedback

If you have substantive feedback on a design decision — the trust model, the capability key tiers, the federation model, the DID method choices — use the RFC process described below.

### Documentation

If you find errors, unclear explanations, or missing context in the specification or this site, open an issue or submit a pull request with the correction.

---

## How to Propose Changes

The Daplin protocol uses an open RFC process, as described in the [Protocol Specification §13.4](spec.md#134-governance).

1. **Open a GitHub issue** describing the proposed change. Title it clearly: `RFC: <brief description>`.
2. **Include rationale** — explain why the current design is insufficient and what problem your proposal solves.
3. **Describe the impact** — note any effects on existing protocol behavior, backwards compatibility, or security properties.
4. **Discussion period** — substantive changes require a minimum 60-day discussion period before any decision is made. This is not a formality; it is how the protocol earns trust.
5. **Consensus** — the protocol belongs to its community of implementors. No single organization controls it.

Minor corrections (typos, clarifications that don't change behavior) can be submitted directly as pull requests without a formal RFC.

---

## Code Contributions

No implementation code exists yet, so code contributions are not yet applicable. This section will be expanded when the reference server implementation begins.

When it does, contributions will follow standard open-source practices:

- Fork the repository and create a feature branch
- Write tests alongside your implementation
- Submit a pull request with a clear description of what you've done and why
- Code style: [Ruff](https://docs.astral.sh/ruff/) for formatting and linting, [mypy](https://mypy.readthedocs.io/) in strict mode for type checking

---

## Community Expectations

This project takes its name and its values seriously. Contributions should reflect that spirit.

- Be respectful and constructive. Critique ideas, not people.
- Be specific. Vague objections are not useful; precise analysis is.
- Be honest. If you're uncertain, say so. If you disagree, say why.
- Discrimination, harassment, and bad-faith engagement are not tolerated.

---

## License

Daplin is licensed under the [Apache License 2.0](https://github.com/cwlls/daplin/blob/main/LICENSE).

By submitting a contribution — whether a pull request, an issue, or a discussion comment that is incorporated into the specification — you agree that your contribution will be licensed under the same terms.
