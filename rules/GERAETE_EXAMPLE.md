# Geräte-Liste — Beispiel-Schablone

> **Demo-Schablone**, nicht echte Praxis-Daten. Tenants kopieren diese
> Datei nach `GERAETE_TENANT.md` (gitignored). Konkrete Serien- und
> Inventarnummern, Hersteller-Kennungen und individuelle STK-Termine
> bleiben im Tenant.

## Struktur eines Geräte-Eintrags

```
### <Geräte-Kennung>
- **Typ:** <Gerätetyp>
- **Hersteller:** <Hersteller>  (im OSS-Repo: PSEUDO-Hersteller)
- **Modell:** <Modell>
- **Inventar-Nr:** <intern vergeben>
- **Serien-Nr:** <Hersteller-Serien-Nr>
- **Standort:** <Raum/Funktionszone>
- **Inbetriebnahme:** <YYYY-MM-DD>
- **MP-Klasse:** <I / IIa / IIb / III nach EU-MDR>
- **STK-Intervall:** <Monate, gemäß MPBetreibV §11>
- **Letzte STK:** <YYYY-MM-DD>
- **Nächste STK:** <YYYY-MM-DD>
- **Eingewiesene MFAs:** <Liste mit Einweisungs-Datum>
- **Gebrauchsanweisung:** <Pfad zur Hersteller-PDF>
- **Wartungsvertrag:** <Vertragspartner / Vertragsnummer>
```

## Beispiele

### PSEUDO-DEFI-01
- **Typ:** Defibrillator (AED)
- **Hersteller:** PSEUDO-Hersteller AG
- **Modell:** Pseudo-AED-100
- **Inventar-Nr:** <Tenant>
- **Serien-Nr:** <Tenant>
- **Standort:** Notfall-Wagen, Empfang
- **Inbetriebnahme:** 2020-03-15
- **MP-Klasse:** IIb
- **STK-Intervall:** 12 Monate
- **Letzte STK:** 2026-03-10
- **Nächste STK:** 2027-03-10
- **Eingewiesene MFAs:** alle aktiven (siehe `PERSONAL_TENANT.md`),
  Letzteinweisung 2026-Q1
- **Gebrauchsanweisung:** `02_Vorlagen_und_Anlagen/10/PSEUDO-AED-100_Gebrauchsanweisung.pdf`
- **Wartungsvertrag:** PSEUDO-Hersteller-Service

### PSEUDO-EKG-01
- **Typ:** Ruhe-EKG
- **Hersteller:** PSEUDO-Hersteller GmbH
- **Modell:** Pseudo-EKG-12L
- **Inventar-Nr:** <Tenant>
- **Serien-Nr:** <Tenant>
- **Standort:** Sprechzimmer 1
- **Inbetriebnahme:** 2021-09-01
- **MP-Klasse:** IIa
- **STK-Intervall:** 24 Monate
- **Letzte STK:** 2025-08-20
- **Nächste STK:** 2027-08-20
- **Eingewiesene MFAs:** <Liste>
- **Gebrauchsanweisung:** `02_Vorlagen_und_Anlagen/10/PSEUDO-EKG-12L_Gebrauchsanweisung.pdf`
- **Wartungsvertrag:** kein laufender Vertrag, Service ad-hoc

### PSEUDO-POCT-HBA1C
- **Typ:** Point-of-Care HbA1c-Analyzer
- **Hersteller:** PSEUDO-Lab AG
- **Modell:** Pseudo-HbA1c-Reader
- **MP-Klasse:** IIa
- **STK-Intervall:** 12 Monate
- **Eingewiesene MFAs:** <Liste>
- **QC-Protokoll:** wöchentliche externe Kontrolle (RILI-BÄK B 2),
  Eintrag in `02_Vorlagen_und_Anlagen/04/QC_Protokoll_POCT.docx`

### PSEUDO-IMPF-KUEHL
- **Typ:** Impfstoff-Kühlschrank
- **Standort:** Behandlungsraum
- **Temperatur-Sollbereich:** +2 °C bis +8 °C
- **Tagesprotokoll:** `03_Arbeitsdateien/<aktuelle-Iteration>/`
- **Stromausfall-Verfahren:** siehe Verfahrensanweisung
  `02_Vorlagen_und_Anlagen/01/Kuehlkettenunterbrechung_Verfahrensanweisung.docx`

## Anti-Pattern

❌ Geräte-Hersteller einer einzelnen Praxis namentlich im OSS-Repo —
   gehört in `GERAETE_TENANT.md`.
❌ Konkrete Serien-Nummern im OSS-Repo (Inventar-Eindeutigkeit).
❌ Patient-bezogene QC-Protokolle (Patient-Probennummer, Patient-
   Kennung) im QM-System — DSGVO. QC-Protokolle führen NUR
   anonymisierte/aggregierte Werte.

## Hinweise zur Pflege

- Jeder Geräte-Eintrag wird bei Inbetriebnahme erstellt und bei
  Außerbetriebnahme mit Außerbetriebnahme-Datum + „**außer Betrieb**"-
  Markierung versehen (nicht löschen — Audit-Spur über
  Aufbewahrungsfrist hinaus).
- STK-Termine sind die Grundlage für Q3-Review (siehe `WORKFLOW.md`
  Workflow 3).
- Bei Hersteller-Sicherheitshinweisen (FSCA — Field Safety Corrective
  Action) wird der entsprechende Eintrag mit FSCA-ID und Datum
  ergänzt.
