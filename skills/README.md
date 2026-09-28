# Agent skills

Canonical files live here. `.claude/` indexes them. Discovery symlinks may exist under `.claude/skills/` and `.cursor/skills/` — do not author there.

| Skill | When |
|---|---|
| [`roast-and-alternatives/`](roast-and-alternatives/) | User says **now roast this, please** or **let's use our roast skill** and provides an idea, file, or ramble. Searches the web. Writes one new markdown file under `roasts/`, then a sibling `.html`. |
| [`potential-winner-ideas/`](potential-winner-ideas/) | User says **make this a PWI**, **promote A2**, or **keep this one** to archive an alternative or new spark. Researches lightly. Writes one new file under `potential-winner-ideas/`, then a sibling `.html` via script. |
