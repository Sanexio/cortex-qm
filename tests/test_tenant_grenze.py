"""Framework/Tenant-Grenze mechanisch pruefen.

Die Framework-Schicht (``cortex_qm/``) darf keinerlei Demo-Tenant- oder
Praxis-Inhalte tragen: kein Praxisname, keine Demo-Ortsmarke. Der
fiktive Demo-Tenant lebt ausschliesslich unter ``examples/`` (und als
Eingabe-Konstante in den Tests).
"""

from __future__ import annotations

import unittest

from .pfade import REPO

FRAMEWORK = REPO / "cortex_qm"

# Marker des fiktiven Demo-Tenants; bewusst zerlegte Schreibweise,
# damit dieser Test sich nicht selbst findet.
VERBOTENE_MARKER = ("Muster" + "stadt", "Demo-" + "Praxis")


class TestTenantGrenze(unittest.TestCase):
    def test_framework_schicht_ist_tenant_frei(self) -> None:
        funde = []
        for pfad in sorted(FRAMEWORK.rglob("*.py")):
            text = pfad.read_text(encoding="utf-8")
            for marker in VERBOTENE_MARKER:
                if marker in text:
                    funde.append(f"{pfad.name}: {marker}")
        self.assertEqual(
            funde,
            [],
            "Demo-Tenant-Inhalte in der Framework-Schicht gefunden — "
            "sie gehoeren nach examples/: " + "; ".join(funde),
        )

    def test_framework_schicht_existiert(self) -> None:
        self.assertTrue((FRAMEWORK / "__init__.py").is_file())


if __name__ == "__main__":
    unittest.main()
