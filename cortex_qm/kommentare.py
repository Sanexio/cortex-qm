"""Word-Kommentare (DOCX) als QM-Arbeitsanweisungen auswerten (R-002).

Stdlib-only: ``zipfile`` + ``xml.etree.ElementTree``. Liest
``word/comments.xml`` und ordnet jedem Kommentar die kommentierte
Textstelle aus ``word/document.xml`` zu.
"""

from __future__ import annotations

import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

from . import CortexQmFehler

NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
W_ID = f"{{{NS['w']}}}id"

KEINE_FUNDSTELLE = "(keine Fundstelle gefunden)"


def _text_inhalt(element: ET.Element) -> str:
    return "".join(node.text or "" for node in element.findall(".//w:t", NS)).strip()


def lese_kommentare(docx_pfad: Path) -> Tuple[Dict[str, str], bytes]:
    """Kommentar-Map (id -> Text) und das Dokument-XML einer DOCX lesen."""
    if not docx_pfad.is_file():
        raise CortexQmFehler(f"DOCX nicht gefunden: {docx_pfad}")
    try:
        with zipfile.ZipFile(docx_pfad) as docx:
            try:
                comments_xml = docx.read("word/comments.xml")
            except KeyError:
                raise CortexQmFehler(
                    f"{docx_pfad.name}: enthaelt keine Word-Kommentare "
                    "(word/comments.xml fehlt)."
                ) from None
            document_xml = docx.read("word/document.xml")
    except zipfile.BadZipFile:
        raise CortexQmFehler(f"{docx_pfad.name}: keine gueltige DOCX-Datei.") from None

    comments_root = ET.fromstring(comments_xml)
    kommentare = {
        comment.attrib[W_ID]: _text_inhalt(comment)
        for comment in comments_root.findall(".//w:comment", NS)
    }
    return kommentare, document_xml


def fundstellen(document_xml: bytes) -> Dict[str, str]:
    """Je Kommentar-ID den Text zwischen commentRangeStart/-End einsammeln."""
    root = ET.fromstring(document_xml)
    ziele: Dict[str, List[str]] = {}
    aktiv: List[str] = []

    for absatz in root.findall(".//w:p", NS):
        for kind in absatz:
            if kind.tag == f"{{{NS['w']}}}commentRangeStart":
                kommentar_id = kind.attrib[W_ID]
                aktiv.append(kommentar_id)
                ziele.setdefault(kommentar_id, [])
            elif kind.tag == f"{{{NS['w']}}}commentRangeEnd":
                kommentar_id = kind.attrib[W_ID]
                if kommentar_id in aktiv:
                    aktiv.remove(kommentar_id)
            elif kind.tag == f"{{{NS['w']}}}r":
                run_text = _text_inhalt(kind)
                for kommentar_id in aktiv:
                    ziele.setdefault(kommentar_id, []).append(run_text)

    return {kid: " ".join(teile).strip() for kid, teile in ziele.items()}


def massnahme_ableiten(kommentar: str) -> str:
    """Heuristik: Kommentartext auf eine QM-Standardmassnahme abbilden."""
    lower = kommentar.lower()
    if "r-001" in lower or "freigabe" in lower:
        return "R-001 pruefen: Version, Review-Datum und Freigabe dokumentieren."
    if "themenordner 01" in lower or "r&d-plan" in lower:
        return "Themenordner 01 sichten und Hygiene-/R&D-Verweis nachtragen."
    if "themenordner 10" in lower or "geraetedaten" in lower:
        return "Themenordner 10 gegen fiktiven Demo-Bestand pruefen; keine Echtdaten erfassen."
    return "Kommentar als Arbeitsauftrag aufnehmen und vor Freigabe loeschen."


def auswerten(docx_pfad: Path) -> List[Tuple[str, str, str]]:
    """DOCX auswerten: (Fundstelle, Kommentar, Massnahme) je Kommentar-ID."""
    kommentare, document_xml = lese_kommentare(docx_pfad)
    ziele = fundstellen(document_xml)
    return [
        (
            ziele.get(kommentar_id, KEINE_FUNDSTELLE),
            kommentar,
            massnahme_ableiten(kommentar),
        )
        for kommentar_id, kommentar in sorted(
            kommentare.items(), key=lambda item: int(item[0])
        )
    ]


def schreibe_md(
    zeilen: Sequence[Tuple[str, str, str]], quelle: str, out: Path
) -> None:
    lines = [
        "# DOCX-Kommentar-Auswertung",
        "",
        f"Quelle: `{quelle}`",
        "",
        "| Fundstelle | Kommentar | abgeleitete QM-Massnahme |",
        "|---|---|---|",
    ]
    for fundstelle, kommentar, massnahme in zeilen:
        lines.append(f"| {fundstelle} | {kommentar} | {massnahme} |")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
