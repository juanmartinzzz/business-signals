# AGENTS.md — business-signals

Roast a business idea, then look at alternatives that might actually make money.

## Project layout

- Skill: [`skills/roast-and-alternatives/`](skills/roast-and-alternatives/) — invoke when the user says "now roast this, please" or "let's use our roast skill"
- [`skills/potential-winner-ideas/`](skills/potential-winner-ideas/) — archive keeper ideas
- [`constraints-and-preferences.example/`](constraints-and-preferences.example/) — fictional worked example ("Alex in Austin"); never edit, never treat as the user's facts
- `constraints-and-preferences/` — the user's real pack (gitignored; they copy it from the example). If it doesn't exist, roast against the market only and tell them to create it.
- [`roasts/`](roasts/), [`potential-winner-ideas/`](potential-winner-ideas/) — outputs (gitignored at top level); `samples/` subdirs hold the committed examples

## Rules

- Never copy PII into roast or PWI files (area-level city is fine; no street address, phone, email).
- Never write output files by hand into `samples/` — samples are curated, not skill output.
- The `.html` sibling is always produced by the skill's `to-html.py`, never written by hand, never overwritten.
