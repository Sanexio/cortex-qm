# Räumlichkeiten + Hygiene-Zonen — Beispiel-Schablone

> **Demo-Schablone**, nicht echte Praxis-Daten. Tenants kopieren diese
> Datei nach `RAEUMLICHKEITEN_TENANT.md` (gitignored). Konkrete
> Standort-Adressen, Raumpläne und Lieferanten der Praxis bleiben im
> Tenant.

## Struktur eines Raum-Eintrags

```
### <Raum-Kennung>
- **Funktion:** <Empfang / Wartebereich / Sprechzimmer / Behandlung / Labor / Notfall / Sanitär / Lager / Personalraum>
- **Hygiene-Zone:** <1 / 2 / 3 / 4 nach Hygieneplan>
- **Fläche:** <m²>
- **Lüftung:** <natürlich / mechanisch>
- **Wasserzugang:** <Hand-Wasch-Becken Anzahl>
- **R+D-Plan-Bezug:** <Verweis auf den R+D-Plan-Abschnitt>
- **Geräte vor Ort:** <Verweis auf GERAETE_TENANT.md>
- **Besondere Anforderungen:** <z.B. UV-Licht-Sterilisation, Lärmschutz>
```

## Hygiene-Zonen-Definition (generisch, KRINKO-orientiert)

| Zone | Risiko | Beispiel-Räume |
|---|---|---|
| **Zone 1** | sehr niedrig | Empfang, Wartebereich, Personal-Sozialräume |
| **Zone 2** | niedrig | Sprechzimmer ohne invasive Eingriffe, Untersuchung |
| **Zone 3** | mittel | Eingriffsräume mit Hautkontakt, Wundversorgung, Blutentnahme |
| **Zone 4** | hoch | OP-Raum, sterile Aufbereitung |

Die Zonen-Zuordnung steuert das R+D-Niveau (Reinigungs-Frequenz,
Desinfektionsmittel-Auswahl).

## Beispiele

### PSEUDO-EMPFANG
- **Funktion:** Empfang
- **Hygiene-Zone:** 1
- **Fläche:** 20 m²
- **Lüftung:** mechanisch (zentrale Lüftungsanlage)
- **Wasserzugang:** 1 HWB Personal
- **R+D-Plan-Bezug:** Hygieneplan §3.1
- **Geräte vor Ort:** Praxis-Verwaltung-PC (kein Medizinprodukt)
- **Besondere Anforderungen:** Patient-Sicht-Schutz an Tresen
  (DSGVO Themen 06)

### PSEUDO-SPRECHZIMMER-1
- **Funktion:** Sprechzimmer (ärztliche Untersuchung, Anamnese)
- **Hygiene-Zone:** 2
- **Fläche:** 18 m²
- **Lüftung:** natürlich (Fenster)
- **Wasserzugang:** 1 HWB Personal
- **R+D-Plan-Bezug:** Hygieneplan §3.2
- **Geräte vor Ort:** PSEUDO-EKG-01 (siehe `GERAETE_TENANT.md`)
- **Besondere Anforderungen:** schalldichte Tür für Patientengespräch

### PSEUDO-BEHANDLUNG-1
- **Funktion:** Behandlungsraum (Blutentnahme, Impfung,
  Wundversorgung)
- **Hygiene-Zone:** 3
- **Fläche:** 12 m²
- **Lüftung:** mechanisch
- **Wasserzugang:** 1 HWB Personal, 1 separate Spüle für
  Material-Aufbereitung
- **R+D-Plan-Bezug:** Hygieneplan §3.3
- **Geräte vor Ort:** Impfkühlschrank PSEUDO-IMPF-KUEHL,
  POCT-Geräte (siehe `GERAETE_TENANT.md`)
- **Besondere Anforderungen:** Sammelbehälter spitze/scharfe
  Gegenstände, fest installiert (Themen 09)

### PSEUDO-SANITAER-PATIENT
- **Funktion:** Patienten-Sanitärbereich
- **Hygiene-Zone:** 2 (Sanitär)
- **Fläche:** 5 m²
- **Wasserzugang:** WC + HWB
- **R+D-Plan-Bezug:** Hygieneplan §3.5
- **Besondere Anforderungen:** Barrierefreiheit nach DIN 18040-1

### PSEUDO-LAGER-MP
- **Funktion:** Medizinprodukte-Lager
- **Hygiene-Zone:** 1 (kein Patientenkontakt)
- **Fläche:** 6 m²
- **Lüftung:** natürlich
- **Besondere Anforderungen:** Temperatur 15-25 °C, trocken,
  abgeschlossen; Bestandsführung im Medizinproduktebuch (Themen 10)

## Anti-Pattern

❌ Konkrete Adresse (Straße, Hausnummer, PLZ, Ort) der Praxis im
   OSS-Repo — gehört in `RAEUMLICHKEITEN_TENANT.md`.
❌ Raum-Bezeichnungen mit Personennamen (z.B. „Behandlungsraum
   Dr. <Name>") im OSS-Repo.
❌ Patient-Wege-Diagramme mit konkreten Raumplänen einer
   identifizierbaren Praxis.

## Hinweise zur Pflege

- Bei baulichen Änderungen (Umbau, neue Räume, Funktionswechsel):
  Eintrag aktualisieren UND R+D-Plan an die neue Zonierung anpassen
  (Q2-Review nach `WORKFLOW.md`).
- Hygiene-Zone-Wechsel eines Raums (z.B. Behandlung → OP) erfordert
  außerplanmäßigen Hygieneplan-Review und ggf. KRINKO-Konformitäts-
  Prüfung.
- Brandschutz-relevante Räume (Lager mit brennbaren Materialien,
  Sauerstoff-Lagerung) sind zusätzlich in der Brandschutzordnung
  (Themen 09) verankert.
