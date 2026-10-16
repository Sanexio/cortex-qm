"""Kernlogik: Kategorien-Parser des Regelwerks."""

from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from cortex_qm import CortexQmFehler
from cortex_qm.regelwerk import (
    lade_kategorien,
    parse_bullets_nach_label,
    parse_inline_wert,
    parse_kategorien,
)

from .pfade import KATEGORIEN_BEISPIEL


class TestParseKategorienBeispiel(unittest.TestCase):
    """Gegen das mitgelieferte Beispiel-Regelwerk (nur lesend)."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.kategorien = lade_kategorien(KATEGORIEN_BEISPIEL)

    def test_zwoelf_kategorien_mit_laufenden_nummern(self) -> None:
        self.assertEqual([k.nr for k in self.kategorien], [f"{i:02d}" for i in range(1, 13)])

    def test_jede_kategorie_hat_pflicht_und_anker(self) -> None:
        for kategorie in self.kategorien:
            with self.subTest(nr=kategorie.nr):
                self.assertTrue(kategorie.pflicht, "Pflicht-Inhalte fehlen")
                self.assertTrue(kategorie.anker, "Regulatorische Anker fehlen")

    def test_strukturueberschriften_sind_keine_kategorien(self) -> None:
        namen = [k.name for k in self.kategorien]
        self.assertNotIn("Struktur eines Themen-Eintrags", namen)

    def test_bekannter_eintrag_hygiene(self) -> None:
        hygiene = self.kategorien[0]
        self.assertEqual(hygiene.name, "Hygiene_Desinfektion")
        self.assertIn("Hygieneplan (Standort-spezifisch)", hygiene.pflicht)
        self.assertIn("IfSG", hygiene.anker)


class TestParserDetails(unittest.TestCase):
    def test_bullets_mit_umbruch_fortsetzung(self) -> None:
        block = (
            "\n**Pflicht-Inhalte:**\n"
            "- Erster Punkt,\n"
            "  der umgebrochen weitergeht\n"
            "- Zweiter Punkt\n"
            "\n**Optionale Inhalte:**\n- Nicht mitnehmen\n"
        )
        self.assertEqual(
            parse_bullets_nach_label(block, "Pflicht-Inhalte"),
            ["Erster Punkt, der umgebrochen weitergeht", "Zweiter Punkt"],
        )

    def test_bullets_fehlendes_label_ergibt_leere_liste(self) -> None:
        self.assertEqual(parse_bullets_nach_label("kein Label", "Pflicht-Inhalte"), [])

    def test_inline_wert_mehrzeilig(self) -> None:
        block = "**Regulatorische Anker:** IfSG §6 + §7,\nKRINKO-Empfehlung\n\n**Weiter:**"
        self.assertEqual(
            parse_inline_wert(block, "Regulatorische Anker"),
            "IfSG §6 + §7, KRINKO-Empfehlung",
        )

    def test_inline_wert_fehlend(self) -> None:
        self.assertEqual(parse_inline_wert("nix", "Regulatorische Anker"), "")

    def test_parse_kategorien_leerer_text(self) -> None:
        self.assertEqual(parse_kategorien("# nur Prosa\n"), [])


class TestLadeKategorienFehler(unittest.TestCase):
    def test_fehlende_datei(self) -> None:
        with self.assertRaises(CortexQmFehler):
            lade_kategorien(Path("/nirgendwo/KATEGORIEN.md"))

    def test_datei_ohne_kategorien(self) -> None:
        with TemporaryDirectory() as tmp:
            pfad = Path(tmp) / "leer.md"
            pfad.write_text("# Ueberschrift ohne Themenbloecke\n", encoding="utf-8")
            with self.assertRaises(CortexQmFehler):
                lade_kategorien(pfad)


if __name__ == "__main__":
    unittest.main()
