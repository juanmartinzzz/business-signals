---
name: potential-winner-ideas
description: Promote roast alternatives or brand-new sparks into dated, research-backed keeper files under potential-winner-ideas/. Use when the user says "make this a PWI", "save as a potential winner", "promote A2", "keep this one", or otherwise asks to archive an idea from a roast for later.
---

# Potential Winner Ideas

A PWI (potential winner idea) is a keeper: an alternative from a roast worth thinking through later, or a brand-new spark the user had while reading one. One file per idea. Each PWI is a **canvas snapshot** — buyer, pain, channel, money, edge, test — with its load-bearing facts checked on the web so the file is not bullshit. No roast, no verdict, no kill cards; that already happened (or is not wanted).

## Inputs

The user gives one of:

1. **Roast alternatives**: a roast file plus alternative numbers ("promote A1 and A3 from today's drain roast"). Each alternative gets its **own** PWI file.
2. **A new spark**: free text for something not in any roast ("PWI: paid Spanish newsletter for LATAM nurses targeting Canada").

If the roast file is ambiguous, ask. If they gave no reason for keeping it, ask at most one question ("why keep this one?"), then proceed — `Why kept` may say `unwritten` rather than block.

## Workflow

1. Read the source roast file (for alternative promotions) so the canvas is grounded in what was actually written, not memory.
2. Draft the canvas: buyer, pain, channel, money, edge, test.
3. Research (light, web, mandatory). Verify the load-bearing fact behind each slot: buyer demand exists, the channel exists and reaches them, money figures (prices, program values, envelope vs the mode bar) are real, the edge is honest. A few searches, not a roast. Every slot ends sourced or marked `unwritten` / `unverified` — never filled with vibes.
4. Write a **new** file: `potential-winner-ideas/YYYY-MM-DD---pwi---<slug>.md`. Today's date. Slug is kebab-case, short, distinct from the roast slug. Same-day collision: different slug. Never overwrite an existing file.
5. Set frontmatter `status: parked`.
6. Run the HTML script for each new file (never write HTML by hand, never overwrite an existing `.html`):

```bash
python3 skills/potential-winner-ideas/scripts/to-html.py potential-winner-ideas/YYYY-MM-DD---pwi---<slug>.md
```

7. Reply with a pointer to each new file plus its one-line pitch. Do not paste the files into chat.

## File shape (contract)

```markdown
---
slug: <slug>
title: <short name>
source: roasts/<roast-file>.md#A2
run: YYYY-MM-DD
status: parked
---

# pwi: <slug>

## Why kept

<user's reason, or `unwritten`>

## Buyer

<who pays, specifically — or `unwritten`>

## Pain

<the acute problem they already spend to solve — or `unwritten`>

## Channel

<where they already hang out and how 1–3 people reach them — or `unwritten`>

## Money

<price × volume against the mode bar in constraints-and-preferences/time-and-income.md; which mode it could hit>

## Edge

<the honest unfair advantage vs incumbents — or `unwritten`>

## Test

<the falsifying cheap test: who / what / time box / what kills it / what does not count>

## Sources

- https://example.com — what it supported
- unverified: <claim without a source>

## Log

- YYYY-MM-DD: promoted from <source>
```

`source` is `new spark` when the idea came from free text instead of a roast.

`status` lifecycle: `parked` → `testing` → `graduated` or `killed`. Only the user moves it; append a `Log` line on every move.

## Do not

- Overwrite or edit an existing PWI file (append `Log` lines only, on user instruction)
- Invent market facts, prices, demand, or channel reach — mark `unverified`
- Re-roast the idea or add kill cards and verdicts
- Invent the user's reason for keeping it
- Write one file for multiple alternatives
- Write the `.html` by hand, or overwrite an existing sibling `.html`
- Paste the PWI into chat; point at the file
