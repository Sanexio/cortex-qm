"""Tenant-Profil — der explizite Injektionspunkt der Framework/Tenant-Grenze.

Die Framework-Schicht kennt keine konkrete Praxis. Jede Ausgabe, die einen
Praxisnamen oder Rollen traegt, bekommt diese Werte ueber ein
``TenantProfil`` hereingereicht. Es gibt bewusst keinen Default-Namen:
wer das Framework nutzt, muss seinen Tenant benennen.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple

from . import CortexQmFehler


@dataclass(frozen=True)
class TenantProfil:
    """Minimale Tenant-Identitaet fuer erzeugte QM-Artefakte."""

    praxis: str
    rollen: Tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.praxis or not self.praxis.strip():
            raise CortexQmFehler(
                "TenantProfil: 'praxis' darf nicht leer sein — die "
                "Framework-Schicht hat bewusst keinen Default-Praxisnamen."
            )
        object.__setattr__(self, "praxis", self.praxis.strip())
        object.__setattr__(
            self, "rollen", tuple(r.strip() for r in self.rollen if r.strip())
        )

    @property
    def rollen_text(self) -> str:
        return ", ".join(self.rollen)
