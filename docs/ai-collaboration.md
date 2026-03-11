---
layout: default
title: AI-Human Collaboration — Daplin
---

## Opening

This project exists because of a collaboration between a human developer and AI. Not as a novelty, not as an experiment, but because the collaboration made it possible to move from ideas to a structured protocol specification at a pace that neither could achieve alone.

That is worth being honest about — both what it means and what it does not mean.

---

## The Gap Between Having Ideas and Building Them

The developer had a clear vision: a decentralized identity protocol built on human trust relationships, designed for the people who need it most — activists, journalists, abuse survivors, anyone who needs to establish trusted communication without depending on institutions that may not have their interests at heart.

The challenge was not the ideas themselves. The challenge was the work of giving them form: structuring a coherent specification, resolving design tensions, maintaining consistency across a large body of technical writing, and producing the kind of precise, unambiguous language that a protocol requires.

A protocol specification is not a blog post. It must define every term it uses. It must address edge cases. It must be internally consistent across fifteen sections written over multiple sessions. It must anticipate the questions an implementor will ask and answer them before they are asked. That is a significant volume of careful, disciplined work.

AI bridged the gap between having ideas and building them. Not by generating the ideas — those came from the developer — but by helping externalize, organize, and refine them into a document that says what the developer means.

---

## Augmentation, Not Replacement

AI did not design Daplin.

The vision is human. The values are human. The decision that privacy should be the only mode — not a setting, not an option, but the only state — is a human judgment about what matters. The decision to build a trust model on human relationships rather than cryptographic proofs alone is a human insight about how trust actually works. The insistence that the protocol should be usable by people with elevated privacy needs, not just technically sophisticated users, is a human commitment.

The naming decision is perhaps the clearest example. AI cannot decide that a protocol should be named after a trust gesture born under oppression, carried by Black soldiers who were punished for using it, and used anyway because the people on the other side of that handshake were worth protecting. AI cannot feel the weight of that decision, or sit with it long enough to know whether it is right. That required a human — one who encountered that history, recognized the alignment, and chose to proceed with intention and respect.

What AI can do is take human intent and help give it structure. It can draft, challenge consistency, propose alternatives, and iterate until the specification says what the developer means. It is a capable and tireless drafting partner. It is not the architect.

---

## The Collaboration Model

The collaboration works like this: the developer provides direction, constraints, and judgment. AI drafts, proposes, and iterates. The developer accepts, rejects, or redirects. It is a conversation, not a delegation.

In practice, this looks like: the developer describes a design decision — say, how capability key access should be determined. AI drafts a model. The developer reads it, identifies what is wrong or missing, and redirects. AI revises. The developer refines the language. The result is a section of the specification that reflects the developer's intent, expressed with the precision that a protocol requires.

The developer remains the architect throughout. Every significant decision — what the trust model should be, how introductions should work, what the threat model should address, what the protocol should explicitly not do — was made by the developer. AI helped execute those decisions, not make them.

---

## What AI Contributed

To be specific about what AI contributed to this project:

- **Drafting** — The protocol specification, the architectural overview, and this documentation site were drafted with AI assistance. The developer directed the content; AI produced the text; the developer reviewed, revised, and approved.
- **Consistency** — Maintaining consistency across a large specification is difficult. AI helped identify places where two sections used different terminology for the same concept, or where a design decision in one section had implications for another that had not been addressed.
- **Edge cases** — AI helped surface edge cases that the developer had not explicitly considered, prompting design decisions that made the specification more complete.
- **Technical writing** — Protocol specifications require a particular kind of precise, unambiguous prose. AI is good at this style of writing, and helped produce text that meets that standard.

What AI did not contribute: the core ideas, the value judgments, the ethical commitments, or the decisions about what the protocol should be and who it should serve.

---

## What AI Cannot Do

AI cannot care about the people this protocol is for.

It cannot understand why privacy matters to an abuse survivor who needs to communicate safely with a support network without leaving a record that an abuser could find. It cannot understand why a journalist in an authoritarian country needs identity that no government can revoke. It cannot understand why a whistleblower needs to establish trusted contact with a reporter without either party's identity being observable by a third party.

These are not abstract use cases. They are the reason the protocol is designed the way it is — with privacy as the only mode, with no public graph, with instances that carry encrypted payloads they cannot read. The design reflects a human judgment about what matters and who deserves protection.

AI cannot feel the responsibility of naming software after a gesture of solidarity created under fire. It cannot weigh whether borrowing that name is appropriate, or what it would mean to do so carelessly. It cannot make the commitment that the [naming statement](naming.md) makes.

These things require a human. The protocol has them because a human insisted on them.

---

## Looking Forward

This page will evolve as the project moves from specification into implementation.

The collaboration model may change as the work shifts from writing to coding. Implementation work has different rhythms — more iteration, more debugging, more places where the right answer is not obvious until you try it. How AI fits into that work remains to be seen.

What will not change is the principle: AI augments human capability. It does not replace human judgment. The developer decides what to build and why. AI helps build it.

That is the honest account of how this project was made, and how it will continue to be made.
