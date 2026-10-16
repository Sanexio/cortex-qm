"""Kernlogik: Checklisten-Zeilen und Renderer."""

from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from cortex_qm import CortexQmFehler
from cortex_qm.checkliste import PFLICHT_FALLBACK, checklisten_zeilen, schreibe_html, schreibe_md
from cortex_qm.regelwerk import Kategorie
from cortex_qm.tenant import TenantProfil

KATEGORIE = Kategorie(
    nr="01",
    name="Hygiene_Desinfektion",
    pflicht=("Hygieneplan", "R&D-Plan"),
    anker="IfSG §36",
)
LEER = Kategorie(nr="13", name="Neues_Thema", pflicht=(), anker="")
TENANT = TenantProfil(praxis="Testpraxis", rollen=("Rolle A", "Rolle B"))


class TestChecklistenZeilen(unittest.TestCase):
    def test_ids_und_bereiche(self) -> None:
        zeilen = checklisten_zeilen([KATEGORIE])
        self.assertEqual([z["id"] for z in zeilen], ["CHK-01-01", "CHK-01-02"])
        self.assertEqual(zeilen[0]["bereich"], "01 Hygiene_Desinfektion")
        self.assertEqual(zeilen[0]["anker"], "IfSG §36")

    def test_fallback_bei_leeren_pflicht_inhalten(self) -> None:
        zeilen = checklisten_zeilen([LEER])
        self.assertEqual(len(zeilen), 1)
        self.assertEqual(zeilen[0]["pruefpunkt"], PFLICHT_FALLBACK)


class TestRenderer(unittest.TestCase):
    def test_md_traegt_tenant_kopf(self) -> None:
        with TemporaryDirectory() as tmp:
            out = Path(tmp) / "liste.md"
            schreibe_md(checklisten_zeilen([KATEGORIE]), TENANT, out)
            text = out.read_text(encoding="utf-8")
            self.assertIn("Praxis: Testpraxis", text)
            self.assertIn("Rollen: Rolle A, Rolle B", text)
            self.assertIn("| CHK-01-01 |", text)

    def test_html_escaped_und_traegt_tenant(self) -> None:
        boese = Kategorie(nr="02", name="X<script>", pflicht=("A & B",), anker="<&>")
        with TemporaryDirectory() as tmp:
            out = Path(tmp) / "liste.html"
            schreibe_html(checklisten_zeilen([boese]), TENANT, out)
            text = out.read_text(encoding="utf-8")
            self.assertIn("Testpraxis", text)
            self.assertNotIn("<script>", text)
            self.assertIn("A &amp; B", text)


class TestTenantProfil(unittest.TestCase):
    def test_leerer_praxisname_wird_abgewiesen(self) -> None:
        with self.assertRaises(CortexQmFehler):
            TenantProfil(praxis="   ")

    def test_rollen_werden_getrimmt(self) -> None:
        tenant = TenantProfil(praxis=" P ", rollen=(" A ", "", "B"))
        self.assertEqual(tenant.praxis, "P")
        self.assertEqual(tenant.rollen, ("A", "B"))
        self.assertEqual(tenant.rollen_text, "A, B")


if __name__ == "__main__":
    unittest.main()
