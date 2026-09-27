#!/usr/bin/env python3
"""Generate an audit checklist from the markdown rules directory."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


def parse_categories(path: Path) -> list[dict[str, object]]:
    text = path.read_text(encoding="utf-8")
    matches = list(re.finditer(r"^## (\d{2}) ([^\n]+)$", text, flags=re.MULTILINE))
    categories: list[dict[str, object]] = []

    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[start:end]
        required = parse_bullets_after_label(block, "Pflicht-Inhalte")
        anchors = parse_inline_value(block, "Regulatorische Anker")
        categories.append(
            {
                "nr": match.group(1),
                "name": match.group(2).strip(),
                "required": required,
                "anchors": anchors,
            }
        )
    return categories


def parse_bullets_after_label(block: str, label: str) -> list[str]:
    label_match = re.search(rf"^\*\*{re.escape(label)}(?: [^*]+)?:\*\*$", block, flags=re.MULTILINE)
    if not label_match:
        return []
    section = block[label_match.end() :]
    next_label = re.search(r"^\*\*[^*]+:\*\*", section, flags=re.MULTILINE)
    if next_label:
        section = section[: next_label.start()]
    bullets: list[str] = []
    current: list[str] = []
    for line in section.splitlines():
        if line.startswith("- "):
            if current:
                bullets.append(" ".join(current))
            current = [line[2:].strip()]
        elif current and line.startswith("  "):
            current.append(line.strip())
        elif current and not line.strip():
            continue
        elif current:
            break
    if current:
        bullets.append(" ".join(current))
    return bullets


def parse_inline_value(block: str, label: str) -> str:
    marker = f"**{label}:**"
    if marker not in block:
        return ""
    section = block.split(marker, 1)[1].strip()
    lines: list[str] = []
    for line in section.splitlines():
        if not line.strip() or line.startswith("**"):
            break
        lines.append(line.strip())
    return " ".join(lines)


def checklist_rows(categories: list[dict[str, object]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for category in categories:
        required = category["required"] or ["Pflicht-Inhalte im Tenant-Kontext pruefen"]
        for number, item in enumerate(required, start=1):
            rows.append(
                {
                    "id": f"CHK-{category['nr']}-{number:02d}",
                    "bereich": f"{category['nr']} {category['name']}",
                    "pruefpunkt": str(item),
                    "anker": str(category["anchors"]),
                }
            )
    return rows


def write_md(rows: list[dict[str, str]], out: Path) -> None:
    lines = [
        "# Begehungs-Checkliste",
        "",
        "Praxis: Demo-Praxis Musterstadt",
        "Rollen: QM-Beauftragte, Aerztliche Leitung",
        "",
        "| ID | Bereich | Pruefpunkt | Regulatorischer Anker | Status | Notiz |",
        "|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['id']} | {row['bereich']} | {row['pruefpunkt']} | "
            f"{row['anker']} | offen |  |"
        )
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_html(rows: list[dict[str, str]], out: Path) -> None:
    body = "\n".join(
        "<tr>"
        f"<td>{html.escape(row['id'])}</td>"
        f"<td>{html.escape(row['bereich'])}</td>"
        f"<td>{html.escape(row['pruefpunkt'])}</td>"
        f"<td>{html.escape(row['anker'])}</td>"
        "<td>offen</td><td></td>"
        "</tr>"
        for row in rows
    )
    out.write_text(
        f"""<!doctype html>
<html lang="de">
<meta charset="utf-8">
<title>Begehungs-Checkliste</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 32px; color: #1f2933; }}
h1 {{ font-size: 24px; margin: 0 0 8px; }}
p {{ margin: 0 0 20px; }}
table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
th, td {{ border: 1px solid #b8c2cc; padding: 7px; vertical-align: top; }}
th {{ background: #eef2f7; text-align: left; }}
@media print {{ body {{ margin: 12mm; }} table {{ font-size: 10px; }} }}
</style>
<h1>Begehungs-Checkliste</h1>
<p>Demo-Praxis Musterstadt · Rollen: QM-Beauftragte, Aerztliche Leitung</p>
<table>
<thead><tr><th>ID</th><th>Bereich</th><th>Pruefpunkt</th><th>Regulatorischer Anker</th><th>Status</th><th>Notiz</th></tr></thead>
<tbody>
{body}
</tbody>
</table>
</html>
""",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rules-dir", required=True, type=Path)
    parser.add_argument("--out-md", required=True, type=Path)
    parser.add_argument("--out-html", required=True, type=Path)
    args = parser.parse_args()

    categories = parse_categories(args.rules_dir / "CATEGORIES_EXAMPLE.md")
    rows = checklist_rows(categories)
    write_md(rows, args.out_md)
    write_html(rows, args.out_html)
    print(f"{len(rows)} Pruefpunkte erzeugt: {args.out_md}")
    print(f"HTML erzeugt: {args.out_html}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
