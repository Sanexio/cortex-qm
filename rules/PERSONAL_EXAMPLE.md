# Personal-Liste — Beispiel-Schablone

> **Demo-Schablone**, nicht echte Praxis-Daten. Tenants kopieren diese
> Datei nach `PERSONAL_TENANT.md` (gitignored) und tragen dort ihr
> echtes Team ein. `PERSONAL_TENANT.md` wird NIE committed — sie
> enthält personenbezogene Daten und bricht ohne Tenant-Trennung die
> DSGVO.

## Struktur eines Personal-Eintrags

```
### <Kürzel>
- **Vollname:** <Vorname Nachname>
- **Rolle:** <Praxisinhaber / Ärztliche Leitung / MFA / VERAH / …>
- **Eintritt:** <YYYY-MM-DD>
- **Delegations-Stufen:** <welche delegierten Tätigkeiten zugelassen>
- **Geräte-Einweisungen:** <Liste der Medizinprodukte mit Einweisungs-Datum>
- **Schulungs-Stand:** <Hygiene / IfSG / Datenschutz / Brandschutz / PEP — jeweils Datum>
- **Notfall-Kontakt:** <private Nummer, falls im Notfall erreichbar>
```

## Beispiele

### PSEUDO-AS
- **Vollname:** Pseudo Adams (Demo)
- **Rolle:** Praxisinhaber, ärztliche Leitung
- **Eintritt:** 2020-01-01
- **Delegations-Stufen:** alle ärztlich vorbehaltenen Tätigkeiten
- **Geräte-Einweisungen:** Defibrillator (2024-01-15), EKG (2024-01-15),
  Spirometer (2024-01-15)
- **Schulungs-Stand:** Hygiene 2026-Q2, IfSG 2026-Q2, Datenschutz 2026-Q1,
  Brandschutz 2026-Q1
- **Notfall-Kontakt:** <Tenant-File>

### PSEUDO-MM
- **Vollname:** Pseudo Müller (Demo-MFA)
- **Rolle:** MFA mit VERAH-Qualifikation
- **Eintritt:** 2022-04-01
- **Delegations-Stufen:** Blutentnahme, Impfung, EKG selbständig;
  Wundversorgung unter Aufsicht; keine Verschreibungen
- **Geräte-Einweisungen:** Defibrillator (2022-04-15), EKG (2022-04-15),
  Spirometer (2024-06-01), POCT-HbA1c (2024-06-01)
- **Schulungs-Stand:** Hygiene 2026-Q2, IfSG 2026-Q2, Datenschutz 2026-Q1,
  Brandschutz 2026-Q1, PEP 2025-Q4
- **Notfall-Kontakt:** <Tenant-File>

## Anti-Pattern

❌ Privatadressen, Geburtsdaten, Kontodaten — nicht ins QM-System.
❌ Krankheits- oder Schwangerschafts-Hinweise — DSGVO.
❌ Performance-Bewertungen / Disziplinar-Vermerke — gehören in eine
   getrennte Personalakte, nicht ins QM-System (auch nicht im Tenant).
❌ Kürzel, die mit echten Initialen identisch sind, aber andere
   Personen meinen → Verwechslungs-Gefahr in Schulungsnachweisen.

## Hinweise zur Pflege

- Jeder Personen-Eintrag wird beim Eintritt erstellt und beim
  Austritt mit Austritts-Datum + „**inaktiv**"-Markierung versehen
  (nicht löschen — Audit-Spur).
- Geräte-Einweisungen mit Datum sind die Grundlage für STK-/MP-Buch-
  Audit (Themen 10).
- Delegations-Stufen sind die Grundlage für die Aufgabenmatrix
  (Themen 08).
