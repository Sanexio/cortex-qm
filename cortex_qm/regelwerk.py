"""Themen-Kategorien aus dem Markdown-Regelwerk parsen.

Normative Quelle des Formats: ``rules/CATEGORIES_EXAMPLE.md`` bzw. die
Tenant-eigene Kategorien-Datei gleichen Aufbaus. Ein Themen-Eintrag ist
eine ``## NN Name``-Ueberschrift mit den Labeln ``**Pflicht-Inhalte:**``
und ``**Regulatorische Anker:**``.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

from . import CortexQmFehler

_KATEGORIE_RE = re.compile(r"^## (\d{2}) ([^\n]+)$", flags=re.MULTILINE)


@dataclass(frozen=True)
class Kategorie:
    """Eine Themen-Kategorie (z.B. ``01 Hygiene_Desinfektion``)."""

    nr: str
    name: str
    pflicht: Tuple[str, ...]
    anker: str


def parse_kategorien(text: str) -> List[Kategorie]:
    """Alle ``## NN Name``-Themenbloecke eines Regelwerk-Textes parsen."""
    matches = list(_KATEGORIE_RE.finditer(text))
    kategorien: List[Kategorie] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[start:end]
        kategorien.append(
            Kategorie(
                nr=match.group(1),
                name=match.group(2).strip(),
                pflicht=tuple(parse_bullets_nach_label(block, "Pflicht-Inhalte")),
                anker=parse_inline_wert(block, "Regulatorische Anker"),
            )
        )
    return kategorien


def lade_kategorien(pfad: Path) -> List[Kategorie]:
    """Kategorien aus einer Datei laden; leeres Ergebnis ist ein Fehler."""
    if not pfad.is_file():
        raise CortexQmFehler(f"Kategorien-Datei nicht gefunden: {pfad}")
    kategorien = parse_kategorien(pfad.read_text(encoding="utf-8"))
    if not kategorien:
        raise CortexQmFehler(
            f"Keine Themen-Kategorien in {pfad} gefunden — erwartet werden "
            "'## NN Name'-Ueberschriften nach rules/SCHEMA.md."
        )
    return kategorien


def parse_bullets_nach_label(block: str, label: str) -> List[str]:
    """Bullet-Liste unter einem ``**Label:**`` einsammeln (mit Umbruch-Fortsetzung)."""
    label_match = re.search(
        rf"^\*\*{re.escape(label)}(?: [^*]+)?:\*\*$", block, flags=re.MULTILINE
    )
    if not label_match:
        return []
    section = block[label_match.end():]
    next_label = re.search(r"^\*\*[^*]+:\*\*", section, flags=re.MULTILINE)
    if next_label:
        section = section[: next_label.start()]
    bullets: List[str] = []
    current: List[str] = []
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


def parse_inline_wert(block: str, label: str) -> str:
    """Mehrzeiligen Inline-Wert hinter ``**Label:**`` einsammeln."""
    marker = f"**{label}:**"
    if marker not in block:
        return ""
    section = block.split(marker, 1)[1].strip()
    lines: List[str] = []
    for line in section.splitlines():
        if not line.strip() or line.startswith("**"):
            break
        lines.append(line.strip())
    return " ".join(lines)
