#!/usr/bin/env python3
"""Write sibling .html for PWI .md files that do not have one yet.

Does not overwrite existing HTML. Safe to run alone.
"""

from __future__ import annotations

import html
import re
import sys
from datetime import datetime
from pathlib import Path

ACCENT = "#8A5A00"
PWI_NAME = re.compile(r"^(\d{4}-\d{2}-\d{2})---pwi---(.+)\.md$")
SOURCE = re.compile(r"^- (\S+)\s+—\s+(.*)$")
H = re.compile(r"^(#{1,3})\s+(.*)$")

CANVAS = ["Buyer", "Pain", "Channel", "Money", "Edge", "Test"]


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


def parse_log(text: str) -> list[str]:
    rows: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("- "):
            rows.append(line[2:].strip())
    return rows


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


def details(title: str, icon: str, count: str, inner: str, open: bool = False) -> str:
    flag = " open" if open else ""
    return f"""
<details class="block"{flag}>
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
.pill.status {{
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
.body, .prose p {{
  font-size: 15px;
  font-weight: 500;
  line-height: 1.45;
  color: var(--ink);
  margin: 0 0 8px;
}}
.body p:last-child, .prose p:last-child {{ margin-bottom: 0; }}
.loglist {{
  margin: 0;
  padding-left: 20px;
  font-size: 15px;
  font-weight: 500;
  line-height: 1.6;
}}
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
    match = PWI_NAME.match(path.name)
    slug = meta.get("slug") or (match.group(2) if match else path.stem)
    run = meta.get("run") or (match.group(1) if match else "")
    title = meta.get("title", slug)
    source = meta.get("source", "")
    status = meta.get("status", "parked")

    why = section(body, "Why kept")
    slots = [(name, section(body, name)) for name in CANVAS]
    filled = sum(1 for _name, content in slots if content and content != "unwritten")
    sources = parse_sources(section(body, "Sources"))
    log = parse_log(section(body, "Log"))

    when = pretty_date(run) if run else path.stem
    page_title = f"PWI · {slug}"

    canvas_cards = []
    for name, content in slots:
        shown = content if content else "unwritten"
        canvas_cards.append(card(name.lower(), "", shown))
    canvas_html = f'<div class="cards">{"".join(canvas_cards)}</div>'

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

    log_html = (
        f'<div class="prose card"><ul class="loglist">{"".join(f"<li>{esc(e)}</li>" for e in log)}</ul></div>'
        if log
        else '<p class="empty">No log entries.</p>'
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(page_title)}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;800&display=swap" rel="stylesheet">
  <script src="https://unpkg.com/lucide@latest"></script>
  <style>{CSS}</style>
</head>
<body>
  <main class="page">
    <p class="eyebrow">Potential winner idea</p>
    <h1>{esc(slug.replace("-", " "))}</h1>
    <p class="lede">{esc(title)}</p>
    <div class="meta">
      <span class="pill status"><i data-lucide="trophy"></i>{esc(status)}</span>
      <span class="pill">{esc(when)}</span>
      <span class="pill">{esc(source or "new spark")}</span>
    </div>
    <div class="stats">
      <div class="stat"><div class="stat-n">{filled}/6</div><p class="eyebrow">Canvas filled</p></div>
      <div class="stat"><div class="stat-n">{len(sources)}</div><p class="eyebrow">Sources</p></div>
      <div class="stat"><div class="stat-n">{len(log)}</div><p class="eyebrow">Log entries</p></div>
    </div>
    {details("Why kept", "bookmark", "1", f'<div class="prose card">{inline(why)}</div>', open=True)}
    {details("Canvas", "layout-grid", f"{filled}/6", canvas_html, open=True)}
    {details("Sources", "link", str(len(sources)), sources_html)}
    {details("Log", "history", str(len(log)), log_html)}
  </main>
  <script>lucide.createIcons();</script>
</body>
</html>
"""


def pending(root: Path, requested: list[Path]) -> list[Path]:
    if requested:
        paths = requested
    else:
        paths = sorted((root / "potential-winner-ideas").glob("*.md"))
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
