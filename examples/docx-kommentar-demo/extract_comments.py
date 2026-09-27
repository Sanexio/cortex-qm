#!/usr/bin/env python3
"""Extract Word comments and referenced text from a DOCX file."""

from __future__ import annotations

import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
W_ID = f"{{{NS['w']}}}id"


def text_content(element: ET.Element) -> str:
    return "".join(node.text or "" for node in element.findall(".//w:t", NS)).strip()


def read_comments(docx_path: Path) -> tuple[dict[str, str], bytes]:
    with zipfile.ZipFile(docx_path) as docx:
        comments_xml = docx.read("word/comments.xml")
        document_xml = docx.read("word/document.xml")

    comments_root = ET.fromstring(comments_xml)
    comments = {
        comment.attrib[W_ID]: text_content(comment)
        for comment in comments_root.findall(".//w:comment", NS)
    }
    return comments, document_xml


def extract_targets(document_xml: bytes) -> dict[str, str]:
    root = ET.fromstring(document_xml)
    targets: dict[str, list[str]] = {}
    active: list[str] = []

    for paragraph in root.findall(".//w:p", NS):
        for child in paragraph:
            if child.tag == f"{{{NS['w']}}}commentRangeStart":
                comment_id = child.attrib[W_ID]
                active.append(comment_id)
                targets.setdefault(comment_id, [])
            elif child.tag == f"{{{NS['w']}}}commentRangeEnd":
                comment_id = child.attrib[W_ID]
                if comment_id in active:
                    active.remove(comment_id)
            elif child.tag == f"{{{NS['w']}}}r":
                run_text = text_content(child)
                for comment_id in active:
                    targets.setdefault(comment_id, []).append(run_text)

    return {comment_id: " ".join(parts).strip() for comment_id, parts in targets.items()}


def derive_action(comment: str) -> str:
    lower = comment.lower()
    if "r-001" in lower or "freigabe" in lower:
        return "R-001 pruefen: Version, Review-Datum und Freigabe dokumentieren."
    if "themenordner 01" in lower or "r&d-plan" in lower:
        return "Themenordner 01 sichten und Hygiene-/R&D-Verweis nachtragen."
    if "themenordner 10" in lower or "geraetedaten" in lower:
        return "Themenordner 10 gegen fiktiven Demo-Bestand pruefen; keine Echtdaten erfassen."
    return "Kommentar als Arbeitsauftrag aufnehmen und vor Freigabe loeschen."


def write_markdown(out_path: Path, rows: list[tuple[str, str, str]]) -> None:
    lines = [
        "# DOCX-Kommentar-Auswertung",
        "",
        "Quelle: `fixture_qm_kommentare.docx`",
        "",
        "| Fundstelle | Kommentar | abgeleitete QM-Massnahme |",
        "|---|---|---|",
    ]
    for target, comment, action in rows:
        lines.append(f"| {target} | {comment} | {action} |")
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: extract_comments.py INPUT.docx OUTPUT.md", file=sys.stderr)
        return 2

    docx_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])
    comments, document_xml = read_comments(docx_path)
    targets = extract_targets(document_xml)
    rows = [
        (targets.get(comment_id, "(keine Fundstelle gefunden)"), comment, derive_action(comment))
        for comment_id, comment in sorted(comments.items(), key=lambda item: int(item[0]))
    ]
    write_markdown(out_path, rows)
    print(f"{len(rows)} Kommentare extrahiert: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
