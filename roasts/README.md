# Roasts

Outputs from [`skills/roast-and-alternatives/`](../skills/roast-and-alternatives/). Always a **new** markdown file. The skill then runs `scripts/to-html.py`, which writes a sibling `.html` and does not overwrite.

```
YYYY-MM-DD---roast---<slug>.md
YYYY-MM-DD---roast---<slug>.html
```

Date is first-written. Same-day: distinguish in the slug, no sequence token.

The skill writes these. You cull. Delete the `.html` if you need to regenerate it.

Your roasts live here at the top level and are **gitignored** — they contain
your constraints overlay and stay on your machine. [`samples/`](samples/) holds
one committed example (fictional persona) so you can see the shape before
running the skill.
