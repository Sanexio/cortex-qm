"""cortex-qm Framework-Bibliothek.

Tenant-neutrale Kernlogik des cortex-qm-Regelwerks:

- ``regelwerk``   — Themen-Kategorien aus dem Regelwerk parsen
- ``checkliste``  — Begehungs-Checkliste aus Kategorien erzeugen
- ``tracker``     — ausgefuellte Checklisten-CSV in Status-Reports ueberfuehren
- ``kommentare``  — Word-Kommentare (DOCX) als Arbeitsanweisungen auswerten
- ``tenant``      — Tenant-Profil als expliziter Injektionspunkt

Die Framework-Schicht enthaelt keine Praxis-Inhalte. Alles
Praxis-Spezifische (Name, Rollen, Bestaende) kommt als ``TenantProfil``
bzw. als Eingabedatei von aussen herein; der fiktive Demo-Tenant lebt
ausschliesslich unter ``examples/``.
"""

from __future__ import annotations

__version__ = "0.1.0"


class CortexQmFehler(Exception):
    """Fachlicher Fehler der cortex-qm-Kernlogik (klare Meldung statt Traceback)."""


from .tenant import TenantProfil  # noqa: E402  (re-export)

__all__ = ["CortexQmFehler", "TenantProfil", "__version__"]
