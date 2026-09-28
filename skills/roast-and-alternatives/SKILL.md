---
name: roast-and-alternatives
description: >-
  Roasts a business idea, model, line of business, or ramble, then offers
  alternatives that might make money, each with a cheap test. Searches the
  web. Writes a new dated markdown file under roasts/, then runs to-html.py
  to write a sibling .html one-pager. Use when the user says
  "now roast this, please", "let's use our roast skill", or otherwise
  explicitly invokes this skill with an idea, a file, or some text. Do not
  use for coding, career work, or unsolicited idea evaluation.
---

# Roast and alternatives

This skill **is** one new roast file per invocation. Canonical files live here. Do not author under `.cursor/skills/` (discovery symlinks).

The user provides a file or some text: a topic, a question, a line of business, a business model, or a ramble. They invoke it by saying **now roast this, please** or **let's use our roast skill**.

It **searches the web**. It writes a **roast**: pessimistic, specific, slightly rough, and fun — why this fails and *how* it fails. Then **sides / alternatives**: variations that might actually work, each with a cheap test.

It is not a cheerleader. Most of these ideas will be bad; that is the joke. Roast the idea, not the person.

Your constraints and preferences live in [`constraints-and-preferences/`](../../constraints-and-preferences/README.md). Read them every run. Do not copy them into this skill. Do not assume generic defaults (big company, fundraising, growing a team) when this pack says otherwise — or when it is silent.

Before writing, read [templates.md](templates.md), [research.md](research.md), and [examples.md](examples.md).

## Your context (optional)

The roast reads `constraints-and-preferences/` every run — copy it from
`constraints-and-preferences.example/` first (see the repo README), then make
it yours. If you keep personal notes elsewhere (background, expertise,
network), point the agent at them in chat and it will use them as an
additional overlay.

Do not paste PII into roast files (area-level "Austin" is fine; no street
address, phone, email).

## Do not

- Invent market facts, competitors, TAM, or shutdown stories
- Pretend you read a paywall
- Soften the roast in the same breath (“but you never know”)
- Collapse every idea into “doesn’t fit the pack” before the market roast
- Assume they want a big company, fundraising, or a growing team
- Recommend hiring past 3 people, fundraising as a plan, or hyperscale
- Waive language or location friction in `constraints-and-preferences/location.md`
- Ignore `constraints-and-preferences/already-tried.md` and resurrect a corpse as a fresh alternative
- Invent answers to `constraints-and-preferences/gaps.md` (hours, distribution appetite, sales willingness, …)
- Fill a gap with a generic startup default
- Ask for a pre-committed budget; capital-before-it-pays is a **research result**
- Call the main idea an **unlikely win** to look nice
- Produce an alternative that is the original idea with “niche down” in the title
- Put a cheap test on a **kill** of the main idea
- Skip a cheap test on an alternative
- Build the business, a landing page, or an MVP as part of this run
- Overwrite or edit an existing roast file
- Write the `.html` by hand, or overwrite an existing sibling `.html`
- Dump the roast into chat; write the files, then point at them

## Workflow

### 1. Orient

Read this file, [templates.md](templates.md), [research.md](research.md), [examples.md](examples.md). Then **all** of `constraints-and-preferences/` using the load order in [`constraints-and-preferences/README.md`](../../constraints-and-preferences/README.md). Do not rely on memory of a previous roast.

### 2. Name the target

Restate the idea in a few lines: who pays, for what, why they would switch, how money comes in, what “working” means.

If the idea is fog, ask **at most 1–2** sharpening questions, then proceed with an explicit **assumed** version so the roast has a target. Do not invent the answer while waiting; if you must proceed, label assumptions.

If they named a mode (`roast this as side income`), that mode is the verdict bar. Otherwise roast against **both** modes in `constraints-and-preferences/time-and-income.md`.

### 3. Research (mandatory, web)

Follow [research.md](research.md). Do not vibe the market.

At least one search must be **where the buyer already looks**, not only “competitors named X”.

At least one search must check **competitor health** — who is struggling, stalled, or shut down.

Every load-bearing claim needs a source or an explicit **unverified / inferred**. Invented competitors or invented TAM are a skill failure.

Estimate **capital the idea would need before it pays**. That is output, not a budget they must pre-commit.

### 4. Two passes

**Pass 1 — market roast (pack-blind).** Why this fails in the world: demand, distribution, unit economics, incumbents, regulation, switching costs, who actually pays, why similar things died. Cite the web. Specific kill mechanisms, not mood. Fun is allowed; mush is not. See [examples.md](examples.md).

Name the living and the dead ([templates.md](templates.md)). `Kings of the hill` holds the incumbents you cannot displace: what they do, why they hold the hill. `Obituaries: Respect for the Fallen` honors the dead: what they did, cause of death, what it warns about the main idea. Struggling and dead comps are kill evidence — point at them from the kill cards.

**Pass 2 — constraints and preferences overlay.** Why this fails *against your guidance* even if it works for someone chasing a big company. Cite which file (location, scale, time-and-income, skills, languages, already-tried). Do not invent gap answers. Do not fill silence with generic founder defaults.

Keep the passes visible in the output so one can be disagreed with without throwing out the other.

### 5. Alternatives (sides)

A handful (about 2–4). These are the only things this skill is allowed to call potentially good / money-making.

Not “try harder” or “add AI.” Actual variations: different buyer, different wedge, different revenue shape, different geography/language, product vs service vs widget, side-income version vs kill-as-primary.

Each alternative:

- what changes
- why it might live
- how it still dies
- fit against `constraints-and-preferences/` (cite files)
- which income mode it could hit
- **a cheap test** (required)

If there is no honest alternative, say so. Fake hope is worse than a clean kill.

Skip anything listed in `constraints-and-preferences/already-tried.md` unless that file explicitly allows a retry.

### 6. Verdict on the main idea

Default: **kill**. The roast already said not to do it. **No cheap test** on the main idea.

Rare exception — **unlikely win**: you actually stumbled into something that could be a really good idea. Say that in those words. Then, and only then, give the main idea a cheap test. Expect this almost never. Do not water a kill into an unlikely win.

Also note side vs primary when it matters. Avoid “interesting if executed well.”

### 7. Critic pass (before writing)

Re-read the draft as an adversary. Finding no problems is suspicious. Fix, then write.

- Any mush, TAM theater, or “execution is everything”?
- Fake **unlikely win**?
- Alternative that is just the original, niched down?
- Cheap test that is “build it” or “see if people like it”?
- Missing capital-before-it-pays?
- Empty obituary while comps died, or invented shutdown stories?
- Constraints overlay happened *instead of* a market roast?
- Already-tried item recycled?

### 8. Write

Always a **new** file: `roasts/YYYY-MM-DD---roast---<slug>.md`. Shape: [templates.md](templates.md). Today’s date. No sequence token. Same-day collision: different slug. Do not overwrite.

Heading is `# roast: <slug>`. Frontmatter `slug` / `verdict` / `run` must match the file.

### 9. HTML

Independent of the roast prose. Run after the markdown exists. Do not write HTML by hand. Do not overwrite an existing `.html`.

```bash
python3 skills/roast-and-alternatives/scripts/to-html.py roasts/YYYY-MM-DD---roast---<slug>.md
```

Include the `WROTE` path in the report.

### 10. Chat reply

Pointer to the `.md` and the sibling `.html`. Verdict on the main idea (`kill` or `unlikely win`). Names of the alternatives. Stop. Do not paste the roast.

## Quality

Copy this checklist. Fail = fix, then re-check.

```text
- [ ] New file at roasts/YYYY-MM-DD---roast---<slug>.md
- [ ] Frontmatter present; heading # roast: <slug>; Run matches the filename date
- [ ] Exact ## names from templates.md; K/H/O/C/A headings numbered; king, obituary, and alternative field names exact
- [ ] Target named; assumptions labeled
- [ ] Web research done; sources listed; unverified marked
- [ ] At least one distribution-first search (where the buyer already looks)
- [ ] At least one competitor-health search (struggling / shutdown signals)
- [ ] Capital-before-it-pays estimated
- [ ] Market roast has kill mechanisms, not vibes
- [ ] Kings of the hill and Obituaries: Respect for the Fallen present (or an honest `none`); causes of death sourced, not invented
- [ ] Constraints overlay cites `constraints-and-preferences/` files; gaps not invented; no generic big-company defaults
- [ ] already-tried respected
- [ ] 2–4 alternatives (or an honest `none`) each with a cheap test
- [ ] Main idea is kill with no cheap test, or unlikely win named in those words plus a cheap test
- [ ] Fun roast of the idea, not of the person
- [ ] Sibling .html written by to-html.py (not by hand); WROTE path in the report
- [ ] Chat is pointer + verdict, not a second copy
```
