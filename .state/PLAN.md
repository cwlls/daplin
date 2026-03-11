# Daplin Documentation Site — Implementation Plan

> **Status:** Complete — all tasks implemented and validated (2026-03-11)
> **Phase:** 0 (Documentation Site)
> **Target:** daplin.org via GitHub Pages
> **Reference:** `.state/ARCHITECTURE.md` §8

---

## Overview

This plan builds the Jekyll-based GitHub Pages site described in ARCHITECTURE.md §8. The site uses the `eecs485staff/primer-spec` remote theme and will be served at `daplin.org`. All work happens in the `docs/` directory.

The existing files `docs/daplin-spec-v0.2.0.md` and `docs/project-description.md` are retained as source material. New files are created alongside them. The legacy files are excluded from the site's navigation via front matter (`excludeFromSitemap: true`).

---

## Task Sequence

### Task 1: Jekyll scaffolding (`_config.yml`)

**File:** `docs/_config.yml`

Create the Jekyll configuration file with primer-spec as a remote theme.

```yaml
remote_theme: eecs485staff/primer-spec
plugins:
  - jekyll-remote-theme
  - jekyll-optional-front-matter
  - jekyll-readme-index
  - jekyll-relative-links
  - jemoji
kramdown:
  input: GFM
readme_index:
  remove_originals: true
  with_frontmatter: true

title: Daplin
description: >-
  Dignified Attestation Protocol for Linked Identity Networks —
  an open protocol for decentralized digital identity, cryptographic
  public key exchange, and social trust.
url: https://daplin.org
baseurl: ""

primerSpec:
  sitemap:
    label: ""
```

**Key decisions:**
- `sitemap` is enabled with an empty label so the sidebar shows page links without a heading label cluttering the UI
- `kramdown.input: GFM` is required for primer-spec's TOC generation and markdown features
- All recommended primer-spec plugins are included
- `readme_index` settings prevent the repo-root `README.md` from interfering with the site

**Acceptance:** File exists, valid YAML, contains all required keys.

---

### Task 2: CNAME file

**File:** `docs/CNAME`

```
daplin.org
```

Single line, no trailing newline. This tells GitHub Pages to serve the site at the custom domain.

**Acceptance:** File contains exactly `daplin.org`.

---

### Task 3: Gitignore additions for Jekyll

**File:** `.gitignore` (append)

Add Jekyll build artifacts to the existing `.gitignore`:

```gitignore
# Jekyll (GitHub Pages local preview)
docs/_site/
docs/.sass-cache/
docs/.jekyll-cache/
docs/.jekyll-metadata
```

**Acceptance:** Jekyll artifacts are ignored. Existing gitignore content is preserved.

---

### Task 4: Exclude legacy files from site navigation

**Files:** `docs/daplin-spec-v0.2.0.md`, `docs/project-description.md`

Add front matter to both legacy files so they are still rendered by Jekyll (for direct URL access) but excluded from the primer-spec sitemap sidebar:

```yaml
---
layout: spec
excludeFromSitemap: true
---
```

Prepend this front matter block to each file. Do not modify any content below the front matter.

**Acceptance:** Both files have front matter with `excludeFromSitemap: true`. Existing content is unchanged.

---

### Task 5: Protocol Specification page (`spec.md`)

**File:** `docs/spec.md`

Create from `docs/daplin-spec-v0.2.0.md` with these modifications:

1. **Add front matter:**
   ```yaml
   ---
   layout: spec
   title: Protocol Specification
   subtitle: Daplin v0.2.0 — DRAFT
   sitemapOrder: 2
   ---
   ```

2. **Remove the manual Table of Contents section** — delete everything from `## Table of Contents` through the `---` separator that follows the TOC list (lines 12–32 of the source file). Primer Spec's sidebar TOC replaces this.

3. **Remove the title block** at the top of the file (lines 1–9: the `# Daplin`, `## Dignified Attestation...`, `**Specification v0.2.0 — DRAFT**`, date, and separator). This information is now in the front matter `title` and `subtitle`.

4. **All remaining content is preserved verbatim** — every section from `## 1. Introduction` through `*End of Daplin Protocol Specification v0.2.0*`.

**Acceptance:** File renders with primer-spec sidebar TOC. No duplicate TOC. Title appears via front matter. All spec sections §1–§15 and appendices are present and unmodified.

---

### Task 6: Landing page (`index.md`)

**File:** `docs/index.md`

Purpose-written landing page. Not a copy-paste of the spec introduction — a standalone welcome page that draws on the spec §1 and `project-description.md` to orient visitors.

**Front matter:**
```yaml
---
layout: spec
title: Daplin
subtitle: Dignified Attestation Protocol for Linked Identity Networks
sitemapOrder: 1
---
```

**Content structure:**

1. **Opening hook** — Adapted from spec §1 Introduction, paragraphs 1–3. The "your identity, your relationships, your communications are yours" framing. Rewritten as a landing page introduction (not a spec preamble). Should feel like a mission statement, not a technical document.

2. **Core Principles** — The 7 principles from spec §1.1 / `project-description.md`. Presented as a bulleted list with bold lead phrases, exactly as they appear in the spec.

3. **What Daplin Is** — A brief (2–3 paragraph) explanation synthesized from `project-description.md` §"What is Daplin?". Covers: open protocol (not a product), portable digital identity cards, social trust graph, federation model, infrastructure that messaging/email/etc. build on top of.

4. **Project Status** — A short section noting: specification v0.2.0 draft is complete, no implementation exists yet, the project is in design and specification phase, a reference server implementation in Python/FastAPI is planned.

5. **Explore** — Navigation links to the other pages:
   - [Protocol Specification](spec.md) — The full v0.2.0 protocol spec
   - [Project Rationale](rationale.md) — Why Daplin is designed the way it is
   - [On the Name](naming.md) — The origin and meaning of "Daplin"
   - [AI-Human Collaboration](ai-collaboration.md) — How this project was built
   - [Contributing](contributing.md) — How to get involved
   - [GitHub Repository](https://github.com/wellsmd/daplin) — Source code and issue tracker

6. **License** — One line: "Daplin is licensed under the Apache License 2.0."

**Acceptance:** Page renders as the site home page. Contains mission statement, principles, status, and working links to all other pages.

---

### Task 7: Project Rationale page (`rationale.md`)

**File:** `docs/rationale.md`

**Front matter:**
```yaml
---
layout: spec
title: Project Rationale
subtitle: Why Daplin is designed the way it is
sitemapOrder: 3
---
```

**Content structure — synthesized from `project-description.md`:**

1. **The Problem** — The trust problem in secure communication. Central authorities vs. complexity. Neither is dignified. Draw from spec §1 intro paragraphs and project description §"What is Daplin?".

2. **Identity Without a Landlord** — The two-layer DID architecture (global + pairwise) and why it matters. Your DID is your key, not your server. Migration without identity loss. Draw from project description §"Identity Model" and §"Two-Layer DID Architecture".

3. **Trust Through Relationships** — The two-axis trust model (degrees of separation + relationship depth). Why accepting an introduction is not an attestation. Why physical presence is the strongest signal. Draw from project description §"Trust Model".

4. **Tiered Access, Not All-or-Nothing** — The capability key model. Why contact information is never stored by anyone but its owner. Why encryption is per-tier, not per-recipient. Epoch rotation as revocation. Draw from project description §"Capability Keys and Contact Access".

5. **Federation Without a Center** — Why instances are thin routing layers. Why they carry encrypted payloads they cannot read. Why migration is a first-class operation. Why no searchable directories. Draw from project description §"Federation".

6. **Why No Blockchain** — Complexity, cost, external dependencies, environmental concerns. The DID method roadmap is blockchain-free by design. Draw from project description §"DID Method Roadmap".

7. **Infrastructure, Not Application** — Daplin is a protocol, not a product. Messaging clients, email systems, and other tools build on top of it. It does not replicate Signal, email, or any other platform. Draw from project description §"Event Queue" closing statement.

**Acceptance:** Page covers all 7 sections. Content is synthesized (not copy-pasted) from source material. Reads as a cohesive design philosophy document.

---

### Task 8: Naming statement page (`naming.md`)

**File:** `docs/naming.md`

**Front matter:**
```yaml
---
layout: spec
title: On the Name
subtitle: A statement on naming from the lead developer
sitemapOrder: 4
---
```

**Content:** The naming statement provided by the lead developer, reproduced verbatim. The three sections are:

1. **Where the name comes from** — History of the dap among Black American soldiers in Vietnam
2. **Why this name, from this developer** — The developer's personal statement on choosing this name
3. **A commitment** — The dedication and commitment to honoring the name's heritage

The content is used exactly as provided. No editorial changes, no summarization, no reframing. The front matter title/subtitle replaces the original `# On the Name Daplin` heading and `*A statement on naming from the lead developer*` subtitle from the source text, so those lines are omitted from the body to avoid duplication.

**Acceptance:** Page renders the full naming statement. Content matches the developer's original text verbatim (minus the title/subtitle which are in front matter).

---

### Task 9: AI-Human Collaboration page (`ai-collaboration.md`)

**File:** `docs/ai-collaboration.md`

**Front matter:**
```yaml
---
layout: spec
title: AI-Human Collaboration
subtitle: How this project was built
sitemapOrder: 5
---
```

**Content structure — philosophical reflection, not a dry disclosure:**

1. **Opening** — This project exists because of a collaboration between a human developer and AI. Not as a novelty or an experiment, but because the collaboration made it possible to move from ideas to a structured protocol specification at a pace that neither could achieve alone.

2. **The Gap Between Having Ideas and Building Them** — The developer had a clear vision: a decentralized identity protocol built on human trust relationships. The challenge was not the ideas themselves — it was the work of structuring them into a coherent specification, resolving design tensions, and producing the volume of precise technical writing that a protocol spec demands. AI bridged that gap — not by generating ideas, but by helping externalize, organize, and refine them.

3. **Augmentation, Not Replacement** — AI did not design Daplin. The vision, the values, the ethical commitments, the naming decision, the insistence on privacy as the only mode — these are irreducibly human choices. AI cannot decide that a protocol should be named after a trust gesture born under oppression. AI cannot feel the weight of that decision. What AI can do is take that human intent and help give it structure, challenge its consistency, draft and redraft until the specification says what the developer means.

4. **The Collaboration Model** — How it actually works: the developer provides direction, constraints, and judgment. AI drafts, proposes, and iterates. The developer accepts, rejects, or redirects. It is a conversation, not a delegation. The developer remains the architect; AI is a capable and tireless drafting partner.

5. **What AI Contributed** — Honest accounting: AI helped draft the protocol specification, the architectural overview, and this documentation site. It helped identify edge cases, suggest design patterns, and maintain consistency across a large body of technical writing. It did not originate the core ideas, make value judgments, or decide what the protocol should be.

6. **What AI Cannot Do** — AI cannot care about the people this protocol is for. It cannot understand why privacy matters to an abuse survivor, or why a journalist needs identity that no government can revoke. It cannot feel the responsibility of naming software after a gesture of solidarity created under fire. These things require a human. The protocol has them because a human insisted on them.

7. **Looking Forward** — This page will evolve as the project moves from specification into implementation. The collaboration model may change as the work shifts from writing to coding. What will not change is the principle: AI augments human capability. It does not replace human judgment.

**Tone:** Thoughtful, honest, neither defensive nor promotional. Written in the spirit of the project itself — dignified, direct, and respectful of what matters.

**Acceptance:** Page covers all 7 sections. Tone is philosophical, not disclosure-style. Reads as a genuine reflection on the collaboration.

---

### Task 10: Contributing page (`contributing.md`)

**File:** `docs/contributing.md`

**Front matter:**
```yaml
---
layout: spec
title: Contributing
subtitle: How to get involved with Daplin
sitemapOrder: 6
---
```

**Content structure:**

1. **Project Status** — Daplin is in the design and specification phase. The v0.2.0 protocol specification is complete as a draft. No implementation code exists yet. A reference server implementation in Python/FastAPI is planned.

2. **What We Need Now** — The most valuable contributions at this stage:
   - **Specification review** — Read the spec, find ambiguities, identify missing edge cases, challenge design decisions
   - **Security analysis** — Review the cryptographic architecture, trust model, and threat model
   - **Protocol design feedback** — Propose improvements via the RFC process described in the spec §13
   - **Documentation** — Improve clarity, fix errors, suggest better explanations

3. **How to Propose Changes** — The protocol uses an open RFC process (per spec §13.4):
   - Open a GitHub issue describing the proposed change
   - Include rationale and any impact on existing protocol behavior
   - Discussion period: minimum 60 days for substantive changes
   - The protocol belongs to its community of implementors

4. **Code Contributions** — Not yet applicable (no implementation exists). This section will be expanded when the reference server implementation begins. When it does, contributions will follow standard open-source practices:
   - Fork the repository
   - Create a feature branch
   - Write tests
   - Submit a pull request
   - Code style: Ruff for formatting/linting, mypy strict mode for type checking

5. **Community Expectations** — Be respectful, constructive, and specific. This project takes its name and its values seriously. Contributions should reflect that spirit. Discrimination, harassment, and bad-faith engagement are not tolerated.

6. **License** — All contributions are made under the Apache License 2.0. By submitting a contribution, you agree that your work will be licensed under the same terms.

**Acceptance:** Page covers all 6 sections. Accurately reflects current project status. Links to spec §13 governance model.

---

### Task 11: Verify and cross-check

After all files are created, verify:

1. **File inventory** — All 8 new files exist in `docs/`:
   - `_config.yml`
   - `CNAME`
   - `index.md`
   - `spec.md`
   - `rationale.md`
   - `naming.md`
   - `ai-collaboration.md`
   - `contributing.md`

2. **Front matter consistency** — Every `.md` file has `layout: spec`. All site pages have `sitemapOrder` values (1–6). Legacy files have `excludeFromSitemap: true`.

3. **Link integrity** — All inter-page links in `index.md` use relative paths (`spec.md`, `rationale.md`, etc.) and point to files that exist.

4. **Spec content integrity** — `spec.md` contains all sections §1–§15 and both appendices from the original `daplin-spec-v0.2.0.md`. The only removals are the title block and the manual TOC section.

5. **Gitignore** — Jekyll build artifacts are excluded.

6. **No secrets or sensitive data** — No API keys, tokens, or credentials in any file.

**Acceptance:** All checks pass. Site is ready to push to `main` for GitHub Pages deployment.

---

## Post-Deployment (Manual, Owner-Performed)

These steps are performed by the repository owner after the code is pushed:

1. **GitHub Pages settings** — Configure the repository to serve GitHub Pages from the `docs/` directory on the `main` branch.

2. **DNS configuration** — Configure `daplin.org` DNS:
   - Option A (recommended for apex domain): Four `A` records pointing to GitHub Pages IPs:
     - `185.199.108.153`
     - `185.199.109.153`
     - `185.199.110.153`
     - `185.199.111.153`
   - Option B: `CNAME` record for `www` subdomain pointing to `<username>.github.io`

3. **Enforce HTTPS** — Enable "Enforce HTTPS" in the GitHub Pages settings after DNS propagation.

4. **Verify rendering** — Visit `https://daplin.org` and confirm:
   - Landing page loads with primer-spec theme
   - Sidebar shows sitemap links to all pages
   - Sidebar TOC works on the spec page
   - All inter-page links work
   - Dark mode toggle works
   - Mobile layout is responsive

---

## Task Dependency Graph

```
Task 1 (_config.yml)  ──┐
Task 2 (CNAME)         ──┤
Task 3 (.gitignore)    ──┤
Task 4 (legacy files)  ──┼── All independent, can be done in parallel
Task 5 (spec.md)       ──┤
Task 6 (index.md)      ──┤
Task 7 (rationale.md)  ──┤
Task 8 (naming.md)     ──┤
Task 9 (ai-collab.md)  ──┤
Task 10 (contributing) ──┘
                          │
                          ▼
                    Task 11 (verify)
                          │
                          ▼
                    Push to main
                          │
                          ▼
                    Post-deployment (manual)
```

Tasks 1–10 have no dependencies on each other and can be executed in any order or in parallel. Task 11 depends on all of them being complete.
