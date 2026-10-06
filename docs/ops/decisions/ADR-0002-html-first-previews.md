---
id: ADR-0002
status: accepted
date: 2026-10-06
affected_modules:
  - materials
supersedes: null
superseded_by: null
---

# ADR-0002: HTML first; teachers approve a preview before anything is finalized

## Context

ADR-0001 had the teacher confirm a written pattern report. The owner noted
that HTML is the fastest output for Claude to produce, and that teacher
preferences should be confirmed on a preview, not finalized from a list.
Teachers judge a page faster and more accurately than a description of one.

## Decision

- `/learn-style` builds a short, self-contained HTML style preview per course
  and category (`local/previews/<alias>/<category>.html`): 1-2 items in the
  learned style, an answer-key page, and a screen-only notes panel citing the
  evidence for each pattern.
- The teacher reviews it in the browser and Claude revises it in place until
  the teacher approves. Conventions are written only for approved previews,
  and the approved preview is kept as the visual reference.
- `bin/materials status` shows an unapproved preview as a TODO.
- For all materials, the order is HTML preview, then teacher approval, then
  the final format (PDF, LMS post).

## Options Considered

- Text-only confirmation (ADR-0001 as first written): faster to produce, but
  teachers miss layout and wording problems until real materials come out wrong.
- Generating PDFs or Word files directly: slower to iterate, and harder for
  Claude to revise.

## Consequences

- One more step in `/learn-style`, but fewer wrong conventions.
- Material skills get a concrete visual reference in addition to the text rules.
