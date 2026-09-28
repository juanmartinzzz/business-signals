# Roast file shape

Path: `roasts/YYYY-MM-DD---roast---<slug>.md`. Always a new file. No sequence token. Same-day: distinguish in the slug.

This shape is a **contract**. A script reads it and writes a sibling `.html`. Do not invent headings or field names. Do not write the HTML by hand.

After the markdown exists:

```bash
python3 skills/roast-and-alternatives/scripts/to-html.py roasts/YYYY-MM-DD---roast---<slug>.md
```

The script does not overwrite an existing `.html`. Delete the sibling to regenerate.

## Contract

YAML frontmatter (required). Values on one line.

```yaml
---
slug: short-slug
idea: one-line restatement
assumed: none
run: YYYY-MM-DD
mode_bar: both
verdict: kill
---
```

`mode_bar` is `both` / `side` / `primary`. `verdict` is `kill` / `unlikely win`. `assumed` is `none` or the assumptions.

Heading `# roast: <slug>` must match `slug` and the filename slug.

Exact `##` names, in this order:

1. `Sources`
2. `Target`
3. `Market roast`
4. `Kings of the hill`
5. `Obituaries: Respect for the Fallen`
6. `Constraints overlay`
7. `Alternatives`
8. `Verdict`

### Sources

One bullet per source:

```markdown
- https://example.com — what it supported
- unverified: conversion rate inferred
```

### Target

Prose. Who pays, for what, why they would switch, how money enters, what “working” means.

### Market roast

Fixed `###` names, then kill cards:

```markdown
### Envelope
users × price arithmetic against both income modes

### Capital before it pays
range and what you assumed

### K1 — Short kill title
How it dies. Cite sources in the prose.

### K2 — Another kill title
…
```

`K` numbers start at 1. One card per kill. Do not skip numbers.

### Kings of the hill

The living. Who owns the hill and why you cannot displace them: the moat,
the default, the distribution you do not have.

If none: the body is exactly `none`.

Otherwise one `###` per incumbent. Field names are exact.

```markdown
### H1 — Name
- What they do: one line
- Moat: why they hold the hill
- Lesson: why you cannot displace them
```

`H` numbers start at 1. Do not skip numbers.

### Obituaries: Respect for the Fallen

The graveyard. Struggling and dead comps are kill evidence. At least one
entry when dead or dying comps exist — an empty obituary next to a pile
of corpses is a smell.

If none: the body is exactly `none`.

Otherwise one `###` per fallen comp. Field names are exact.

```markdown
### O1 — Name
- What they did: one line
- Status: struggling / dead / unverified
- Cause of death: shutdown post, layoffs, stall… with a source in Sources
- Lesson: what their death warns about the main idea
```

`O` numbers start at 1. Do not skip numbers. Do not invent competitors or shutdown stories.

### Constraints overlay

```markdown
### C1 — location.md
What fails against that file.

### C2 — scale.md
…
```

Cite the filename in the heading. Do not invent `gaps.md` answers.

### Alternatives

If none: the body is exactly `none`.

Otherwise one `###` per alternative. Field names are exact. Value may wrap on following indented lines.

```markdown
### A1 — Short name
- Change: what is different from the main idea
- Why it might live: …
- How it still dies: …
- Mode: side
- Fit: scale.md; skills.md
- Cheap test: who / what / time box / what kills it / what does not count
```

`Mode` is `side` / `primary` / `both`. `A` numbers start at 1.

### Verdict

```markdown
- Main: kill
- Side: …
- Primary: …
```

If `verdict` in frontmatter is `unlikely win`, `Main` must say `unlikely win` and you **must** add:

```markdown
### Cheap test
who / what / time box / what kills it
```

If `Main` is `kill`, do not add `### Cheap test`.

## Cheap tests (content)

A cheap test falsifies “this could make money” without building the business.

Prefer, in order: someone pays; last-time-it-hurt plus past spend; a manual job for 1–3 people this week.

Does not count: likes, waitlists, “sounds interesting,” hypothetical surveys, building an MVP “to see.”

If it cannot be tested without becoming the business, say so. That is a finding, not a test.

## Voice

Blunt, specific, light, fun. Slightly rude to the *idea*. No startup-speak. No “disruption.” No “interesting if executed well.”
