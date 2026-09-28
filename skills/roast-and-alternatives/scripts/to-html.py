#!/usr/bin/env python3
"""Write sibling .html for roast .md files that do not have one yet.

Does not overwrite existing HTML. Safe to run alone.
"""

from __future__ import annotations

import html
import re
import sys
from datetime import datetime
from pathlib import Path

ACCENT = "#145C45"
ROAST_NAME = re.compile(r"^(\d{4}-\d{2}-\d{2})---roast---(.+)\.md$")
FIELD = re.compile(r"^- ([^:]+):\s*(.*)$")
SOURCE = re.compile(r"^- (\S+)\s+—\s+(.*)$")
H = re.compile(r"^(#{1,3})\s+(.*)$")

REQUIRED_H2 = [
    "Sources",
    "Target",
    "Market roast",
    "Kings of the hill",
    "Obituaries: Respect for the Fallen",
    "Constraints overlay",
    "Alternatives",
    "Verdict",
]

KING_FIELDS = [
    "What they do",
    "Moat",
    "Lesson",
]

OBIT_FIELDS = [
    "What they did",
    "Status",
    "Cause of death",
    "Lesson",
]

ALT_FIELDS = [
    "Change",
    "Why it might live",
    "How it still dies",
    "Mode",
    "Fit",
    "Cheap test",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def pretty_date(iso: str) -> str:
    try:
        day = datetime.strptime(iso, "%Y-%m-%d")
    except ValueError:
        return iso
    return day.strftime("%Y-%b-%d")


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, text
    raw = text[4:end]
    body = text[end + 5 :]
    meta: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        meta[key.strip()] = val.strip().strip('"').strip("'")
    return meta, body


def blocks(body: str) -> list[tuple[int, str, str]]:
    """Return (level, title, content) for each heading, content until next heading of same or higher."""
    lines = body.splitlines()
    found: list[tuple[int, str, int]] = []
    for i, line in enumerate(lines):
        m = H.match(line)
        if m:
            found.append((len(m.group(1)), m.group(2).strip(), i))
    out: list[tuple[int, str, str]] = []
    for i, (level, title, start) in enumerate(found):
        end = len(lines)
        for level2, _title2, start2 in found[i + 1 :]:
            if level2 <= level:
                end = start2
                break
        content = "\n".join(lines[start + 1 : end]).strip()
        out.append((level, title, content))
    return out


def section(body: str, title: str) -> str:
    for level, heading, content in blocks(body):
        if level == 2 and heading == title:
            return content
    return ""


def children(body: str, title: str) -> list[tuple[str, str]]:
    capture = False
    out: list[tuple[str, str]] = []
    for level, heading, content in blocks(body):
        if level == 2:
            capture = heading == title
            continue
        if capture and level == 3:
            out.append((heading, content))
    return out


def parse_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    current: str | None = None
    chunks: list[str] = []
    for line in text.splitlines():
        m = FIELD.match(line)
        if m:
            if current is not None:
                fields[current] = "\n".join(chunks).strip()
            current = m.group(1).strip()
            chunks = [m.group(2)]
            continue
        if current is not None:
            chunks.append(line.strip())
    if current is not None:
        fields[current] = "\n".join(chunks).strip()
    return fields


def parse_sources(text: str) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("- "):
            continue
        m = SOURCE.match(line)
        if m:
            rows.append((m.group(1), m.group(2)))
            continue
        rest = line[2:]
        if rest.lower().startswith("unverified:"):
            rows.append(("unverified", rest.split(":", 1)[1].strip()))
        else:
            rows.append(("", rest))
    return rows


def parse_kills(kids: list[tuple[str, str]]) -> list[tuple[str, str]]:
    kills: list[tuple[str, str]] = []
    for title, content in kids:
        if re.match(r"^K\d+\s+—\s+", title):
            kills.append((re.sub(r"^K\d+\s+—\s+", "", title), content))
    return kills


def named(kids: list[tuple[str, str]], name: str) -> str:
    for title, content in kids:
        if title == name:
            return content
    return ""


def parse_constraints(kids: list[tuple[str, str]]) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for title, content in kids:
        if re.match(r"^C\d+\s+—\s+", title):
            rows.append((re.sub(r"^C\d+\s+—\s+", "", title), content))
    return rows


def parse_alts(kids: list[tuple[str, str]]) -> list[tuple[str, dict[str, str]]]:
    alts: list[tuple[str, dict[str, str]]] = []
    for title, content in kids:
        if re.match(r"^A\d+\s+—\s+", title):
            alts.append((re.sub(r"^A\d+\s+—\s+", "", title), parse_fields(content)))
    return alts


def parse_kings(kids: list[tuple[str, str]]) -> list[tuple[str, dict[str, str]]]:
    kings: list[tuple[str, dict[str, str]]] = []
    for title, content in kids:
        if re.match(r"^H\d+\s+—\s+", title):
            kings.append((re.sub(r"^H\d+\s+—\s+", "", title), parse_fields(content)))
    return kings


def parse_obits(kids: list[tuple[str, str]]) -> list[tuple[str, dict[str, str]]]:
    obits: list[tuple[str, dict[str, str]]] = []
    for title, content in kids:
        if re.match(r"^O\d+\s+—\s+", title):
            obits.append((re.sub(r"^O\d+\s+—\s+", "", title), parse_fields(content)))
    return obits


def inline(text: str) -> str:
    text = esc(text)
    text = re.sub(r"\n\n+", "</p><p>", text)
    text = text.replace("\n", "<br>")
    return f"<p>{text}</p>" if text else ""


def card(eyebrow: str, title: str, body: str, extra: str = "") -> str:
    parts = ['<article class="card">']
    if eyebrow:
        parts.append(f'<p class="eyebrow">{esc(eyebrow)}</p>')
    if title:
        parts.append(f"<h3>{esc(title)}</h3>")
    if body:
        parts.append(f'<div class="body">{inline(body)}</div>')
    if extra:
        parts.append(extra)
    parts.append("</article>")
    return "".join(parts)


def field_dl(fields: dict[str, str], order: list[str] | None = None) -> str:
    rows = []
    for key in order or ALT_FIELDS:
        val = fields.get(key, "")
        if not val:
            continue
        rows.append(
            f"<div><dt>{esc(key)}</dt><dd>{inline(val)}</dd></div>"
        )
    if not rows:
        return ""
    return f'<dl class="fields">{"".join(rows)}</dl>'


def details(title: str, icon: str, count: str, inner: str) -> str:
    return f"""
<details class="block">
  <summary>
    <span class="block-title"><i data-lucide="{esc(icon)}"></i>{esc(title)}</span>
    <span class="block-count">{esc(count)}</span>
  </summary>
  <div class="block-body">
    {inner}
  </div>
</details>
"""


CSS = f"""
:root {{
  --ink: #121512;
  --muted: #5c635e;
  --paper: #f3f1ec;
  --card: #fffcf7;
  --line: #d8d4cb;
  --accent: {ACCENT};
}}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; }}
body {{
  background: var(--paper);
  color: var(--ink);
  font-family: Outfit, Helvetica Neue, Helvetica, Arial, sans-serif;
  font-weight: 500;
}}
a {{ color: var(--accent); font-weight: 700; text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
.page {{
  max-width: 920px;
  margin: 0 auto;
  padding: 48px 24px 96px;
}}
.eyebrow {{
  margin: 0;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--accent);
}}
h1 {{
  font-size: clamp(40px, 8vw, 64px);
  font-weight: 800;
  letter-spacing: -0.04em;
  word-spacing: 0.16em;
  line-height: 0.95;
  margin: 10px 0 12px;
  text-transform: uppercase;
}}
.lede {{
  font-size: 1.15rem;
  font-weight: 600;
  line-height: 1.35;
  max-width: 42rem;
  margin: 0 0 28px;
}}
.meta {{
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 0 0 36px;
}}
.pill {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border: 1px solid var(--line);
  border-radius: 9999px;
  padding: 6px 12px;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  background: var(--card);
}}
.pill.verdict {{
  background: var(--accent);
  color: var(--paper);
  border-color: var(--accent);
}}
.pill i {{ width: 14px; height: 14px; }}
.stats {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 28px;
}}
.stat {{
  background: var(--card);
  border: 1px solid var(--line);
  padding: 16px 18px;
}}
.stat-n {{
  font-size: 40px;
  font-weight: 800;
  letter-spacing: -0.06em;
  line-height: 1;
  color: var(--accent);
}}
.block {{ margin: 0 0 12px; }}
.block summary {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  cursor: pointer;
  list-style: none;
  background: var(--card);
  border: 1px solid var(--line);
  padding: 16px 18px;
}}
.block summary::-webkit-details-marker {{ display: none; }}
.block[open] summary {{ border-color: var(--accent); }}
.block-title {{
  font-size: 22px;
  font-weight: 800;
  letter-spacing: -0.03em;
  word-spacing: 0.14em;
  display: flex;
  align-items: center;
  gap: 10px;
  text-transform: uppercase;
}}
.block-title i {{ width: 20px; height: 20px; color: var(--accent); }}
.block-count {{
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--accent);
  white-space: nowrap;
}}
.block-body {{ padding: 18px 0 8px; }}
.cards {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}}
.card {{
  background: var(--card);
  border: 1px solid var(--line);
  padding: 20px;
}}
.card h3 {{
  margin: 6px 0 10px;
  font-size: 22px;
  font-weight: 800;
  letter-spacing: -0.02em;
  word-spacing: 0.08em;
  line-height: 1.15;
}}
.body, .fields dd p, .prose p {{
  font-size: 15px;
  font-weight: 500;
  line-height: 1.45;
  color: var(--ink);
  margin: 0 0 8px;
}}
.body p:last-child, .fields dd p:last-child, .prose p:last-child {{ margin-bottom: 0; }}
.fields {{
  display: grid;
  gap: 12px;
  margin: 12px 0 0;
}}
.fields dt {{
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 4px;
}}
.fields dd {{ margin: 0; }}
.empty {{
  color: var(--muted);
  font-weight: 700;
}}
.go {{
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  margin-top: 10px;
}}
.go i {{ width: 14px; height: 14px; }}
@media (max-width: 720px) {{
  .stats, .cards {{ grid-template-columns: 1fr; }}
  .block-title {{ font-size: 18px; }}
}}
"""


def page(path: Path, text: str) -> str:
    meta, body = split_frontmatter(text)
    match = ROAST_NAME.match(path.name)
    slug = meta.get("slug") or (match.group(2) if match else path.stem)
    run = meta.get("run") or (match.group(1) if match else "")
    idea = meta.get("idea", slug)
    assumed = meta.get("assumed", "none")
    mode_bar = meta.get("mode_bar", "both")
    verdict = meta.get("verdict", "")
    if not verdict:
        fields = parse_fields(section(body, "Verdict"))
        verdict = fields.get("Main", "")

    sources = parse_sources(section(body, "Sources"))
    target = section(body, "Target")
    market_kids = children(body, "Market roast")
    envelope = named(market_kids, "Envelope")
    capital = named(market_kids, "Capital before it pays")
    kills = parse_kills(market_kids)
    king_section = section(body, "Kings of the hill").strip()
    kings = [] if king_section == "none" else parse_kings(children(body, "Kings of the hill"))
    obit_section = section(body, "Obituaries: Respect for the Fallen").strip()
    obits = [] if obit_section == "none" else parse_obits(children(body, "Obituaries: Respect for the Fallen"))
    constraints = parse_constraints(children(body, "Constraints overlay"))
    alt_section = section(body, "Alternatives").strip()
    alts = [] if alt_section == "none" else parse_alts(children(body, "Alternatives"))
    verdict_fields = parse_fields(section(body, "Verdict"))
    cheap = named(children(body, "Verdict"), "Cheap test")

    when = pretty_date(run) if run else path.stem
    title = f"Roast · {slug}"

    source_cards = []
    for url, note in sources:
        if url == "unverified":
            source_cards.append(card("unverified", note, ""))
        elif url.startswith("http"):
            go = (
                f'<a class="go" href="{esc(url)}" target="_blank" rel="noopener noreferrer">'
                f'<i data-lucide="arrow-up-right"></i>Open</a>'
            )
            source_cards.append(card("source", note, url, go))
        else:
            source_cards.append(card("source", url or note, note if url else ""))
    sources_html = (
        f'<div class="cards">{"".join(source_cards)}</div>'
        if source_cards
        else '<p class="empty">No sources.</p>'
    )

    market_cards = []
    if envelope:
        market_cards.append(card("envelope", "Users × price", envelope))
    if capital:
        market_cards.append(card("capital", "Before it pays", capital))
    for i, (ktitle, kbody) in enumerate(kills, start=1):
        market_cards.append(card(f"K{i}", ktitle, kbody))
    market_html = (
        f'<div class="cards">{"".join(market_cards)}</div>'
        if market_cards
        else '<p class="empty">No market roast.</p>'
    )

    if king_section in ("none", ""):
        kings_html = '<p class="empty">none</p>'
    else:
        king_cards = []
        for i, (hname, fields) in enumerate(kings, start=1):
            king_cards.append(
                card(f"H{i}", hname, "", field_dl(fields, KING_FIELDS))
            )
        kings_html = (
            f'<div class="cards">{"".join(king_cards)}</div>'
            if king_cards
            else '<p class="empty">none</p>'
        )

    if obit_section in ("none", ""):
        obits_html = '<p class="empty">none</p>'
    else:
        obit_cards = []
        for i, (oname, fields) in enumerate(obits, start=1):
            obit_cards.append(
                card(f"O{i}", oname, "", field_dl(fields, OBIT_FIELDS))
            )
        obits_html = (
            f'<div class="cards">{"".join(obit_cards)}</div>'
            if obit_cards
            else '<p class="empty">none</p>'
        )

    constraint_cards = [
        card("constraint", fname, cbody) for fname, cbody in constraints
    ]
    constraints_html = (
        f'<div class="cards">{"".join(constraint_cards)}</div>'
        if constraint_cards
        else '<p class="empty">No overlay.</p>'
    )

    if alt_section == "none":
        alts_html = '<p class="empty">none</p>'
    else:
        alt_cards = []
        for i, (aname, fields) in enumerate(alts, start=1):
            alt_cards.append(
                card(f"A{i}", aname, "", field_dl(fields))
            )
        alts_html = (
            f'<div class="cards">{"".join(alt_cards)}</div>'
            if alt_cards
            else '<p class="empty">none</p>'
        )

    verdict_extra = ""
    if cheap:
        verdict_extra = card("cheap test", "Unlikely win test", cheap)
    verdict_bits = []
    for key in ("Main", "Side", "Primary"):
        if verdict_fields.get(key):
            verdict_bits.append(card(key, verdict_fields[key], ""))
    verdict_html = (
        f'<div class="cards">{"".join(verdict_bits)}{verdict_extra}</div>'
        if verdict_bits or cheap
        else '<p class="empty">No verdict.</p>'
    )

    assumed_html = (
        f'<p class="lede"><strong>Assumed.</strong> {esc(assumed)}</p>'
        if assumed and assumed != "none"
        else ""
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;800&display=swap" rel="stylesheet">
  <script src="https://unpkg.com/lucide@latest"></script>
  <style>{CSS}</style>
</head>
<body>
  <main class="page">
    <p class="eyebrow">Roast and alternatives</p>
    <h1>{esc(slug.replace("-", " "))}</h1>
    <p class="lede">{esc(idea)}</p>
    {assumed_html}
    <div class="meta">
      <span class="pill verdict"><i data-lucide="tree-pine"></i>{esc(verdict or "—")}</span>
      <span class="pill">{esc(when)}</span>
      <span class="pill">mode {esc(mode_bar)}</span>
    </div>
    <div class="stats">
      <div class="stat"><div class="stat-n">{len(kills)}</div><p class="eyebrow">Kills</p></div>
      <div class="stat"><div class="stat-n">{0 if alt_section == "none" else len(alts)}</div><p class="eyebrow">Alternatives</p></div>
      <div class="stat"><div class="stat-n">{len(sources)}</div><p class="eyebrow">Sources</p></div>
    </div>
    {details("Target", "crosshair", "1", f'<div class="prose card">{inline(target)}</div>')}
    {details("Sources", "link", str(len(sources)), sources_html)}
    {details("Market roast", "flame", str(len(kills)), market_html)}
    {details("Kings of the hill", "crown", "none" if king_section in ("none", "") else str(len(kings)), kings_html)}
    {details("Obituaries: Respect for the Fallen", "skull", "none" if obit_section in ("none", "") else str(len(obits)), obits_html)}
    {details("Constraints overlay", "sliders-horizontal", str(len(constraints)), constraints_html)}
    {details("Alternatives", "sprout", "none" if alt_section == "none" else str(len(alts)), alts_html)}
    {details("Verdict", "gavel", verdict or "—", verdict_html)}
  </main>
  <script>lucide.createIcons();</script>
</body>
</html>
"""


def pending(root: Path, requested: list[Path]) -> list[Path]:
    if requested:
        paths = requested
    else:
        paths = sorted((root / "roasts").glob("*.md"))
        paths = [p for p in paths if p.name != "README.md"]
    out: list[Path] = []
    for path in paths:
        if path.suffix != ".md":
            print(f"SKIP not markdown: {path}", file=sys.stderr)
            continue
        html_path = path.with_suffix(".html")
        if html_path.is_file():
            print(f"SKIP exists {html_path.relative_to(root)}")
            continue
        if not path.is_file():
            print(f"SKIP missing {path}", file=sys.stderr)
            continue
        out.append(path)
    return out


def main() -> int:
    root = repo_root()
    requested = [Path(a).resolve() for a in sys.argv[1:]]
    wrote = 0
    for path in pending(root, requested):
        html_path = path.with_suffix(".html")
        html_path.write_text(page(path, path.read_text()), encoding="utf-8")
        try:
            shown = html_path.relative_to(root)
        except ValueError:
            shown = html_path
        print(f"WROTE {shown}")
        wrote += 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
