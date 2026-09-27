#!/usr/bin/env python3
"""Turn a filled audit checklist CSV into markdown and HTML status reports."""

from __future__ import annotations

import argparse
import csv
import html
from collections import Counter
from datetime import date
from pathlib import Path


def normalized_status(raw_status: str, due: date, today: date) -> str:
    status = raw_status.strip().lower()
    if status == "erledigt":
        return "erledigt"
    if due < today:
        return "ueberfaellig"
    return "offen"


def read_rows(csv_path: Path, today: date) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with csv_path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            due = date.fromisoformat(row["faellig_am"])
            row["status_report"] = normalized_status(row["status"], due, today)
            rows.append(row)
    return rows


def status_label(status: str) -> str:
    return {"ueberfaellig": "ueberfaellig", "offen": "offen", "erledigt": "erledigt"}[status]


def write_md(rows: list[dict[str, str]], out: Path, today: date) -> None:
    counts = Counter(row["status_report"] for row in rows)
    lines = [
        "# Begehungs-Tracker Status-Report",
        "",
        "Praxis: Demo-Praxis Musterstadt",
        f"Stichtag: {today.isoformat()}",
        "",
        f"- erledigt: {counts['erledigt']}",
        f"- offen: {counts['offen']}",
        f"- ueberfaellig: {counts['ueberfaellig']}",
        "",
        "| ID | Fundstelle | Pruefpunkt | Verantwortung | Faellig am | Status | Bemerkung |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['id']} | {row['fundstelle']} | {row['pruefpunkt']} | "
            f"{row['verantwortung']} | {row['faellig_am']} | "
            f"{status_label(row['status_report'])} | {row['bemerkung']} |"
        )
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_html(rows: list[dict[str, str]], out: Path, today: date) -> None:
    counts = Counter(row["status_report"] for row in rows)
    table_rows = []
    for row in rows:
        status = status_label(row["status_report"])
        table_rows.append(
            f'<tr class="{html.escape(row["status_report"])}">'
            f"<td>{html.escape(row['id'])}</td>"
            f"<td>{html.escape(row['fundstelle'])}</td>"
            f"<td>{html.escape(row['pruefpunkt'])}</td>"
            f"<td>{html.escape(row['verantwortung'])}</td>"
            f"<td>{html.escape(row['faellig_am'])}</td>"
            f"<td>{html.escape(status)}</td>"
            f"<td>{html.escape(row['bemerkung'])}</td>"
            "</tr>"
        )
    out.write_text(
        f"""<!doctype html>
<html lang="de">
<meta charset="utf-8">
<title>Begehungs-Tracker Status-Report</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 32px; color: #1f2933; }}
h1 {{ font-size: 24px; margin: 0 0 8px; }}
.summary {{ display: flex; gap: 12px; margin: 18px 0; }}
.summary span {{ border: 1px solid #b8c2cc; padding: 6px 10px; }}
table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
th, td {{ border: 1px solid #b8c2cc; padding: 7px; vertical-align: top; }}
th {{ background: #eef2f7; text-align: left; }}
tr.erledigt td {{ background: #eef8ef; }}
tr.offen td {{ background: #fff8e6; }}
tr.ueberfaellig td {{ background: #fdeeee; }}
@media print {{ body {{ margin: 12mm; }} .summary {{ display: block; }} table {{ font-size: 10px; }} }}
</style>
<h1>Begehungs-Tracker Status-Report</h1>
<p>Demo-Praxis Musterstadt · Stichtag {today.isoformat()}</p>
<div class="summary">
  <span>erledigt: {counts['erledigt']}</span>
  <span>offen: {counts['offen']}</span>
  <span>ueberfaellig: {counts['ueberfaellig']}</span>
</div>
<table>
<thead><tr><th>ID</th><th>Fundstelle</th><th>Pruefpunkt</th><th>Verantwortung</th><th>Faellig am</th><th>Status</th><th>Bemerkung</th></tr></thead>
<tbody>
{''.join(table_rows)}
</tbody>
</table>
</html>
""",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, type=Path)
    parser.add_argument("--out-md", required=True, type=Path)
    parser.add_argument("--out-html", required=True, type=Path)
    parser.add_argument("--today", default=date.today().isoformat())
    args = parser.parse_args()

    today = date.fromisoformat(args.today)
    rows = read_rows(args.csv, today)
    write_md(rows, args.out_md, today)
    write_html(rows, args.out_html, today)
    print(f"{len(rows)} Tracker-Zeilen ausgewertet: {args.out_md}")
    print(f"HTML erzeugt: {args.out_html}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
