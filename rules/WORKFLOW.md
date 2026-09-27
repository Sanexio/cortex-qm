# Workflow — von der Bearbeitung zur Freigabe

Drei generische Workflows, die jede Praxis adaptieren kann:

1. **QM-Dokument bearbeiten** (Iteration auf bestehendem Dokument)
2. **Neue SOP erstellen** (Standard Operating Procedure von Grund auf)
3. **Jährliche QM-Überprüfung** (vier Quartals-Reviews nach R-007)

---

## Workflow 1: QM-Dokument bearbeiten

### Vorbereitung

- [ ] Aktuelle Version des Dokuments aus `01_Dokumente/` laden
- [ ] Prüfen, ob offene Word-Kommentare (Autor „QM-System", R-002)
      vorhanden sind
- [ ] Relevante Vorlagen aus `02_Vorlagen_und_Anlagen/01..12/` sichten
- [ ] Datums-Subfolder `03_Arbeitsdateien/YYMMDD/` anlegen (Datum =
      Bearbeitungs-Beginn)
- [ ] Original-Dokument in den Subfolder kopieren, Suffix `_BEARBEITET`
      anhängen (z.B. `Hygieneplan_BEARBEITET.docx`)

### Bearbeitung

- [ ] Word-Kommentare (R-002) als Arbeitsanweisungen abarbeiten
- [ ] Praxis-spezifische Informationen eintragen — Quelle: jeweiliges
      Tenant-File (`PERSONAL_TENANT.md`, `GERAETE_TENANT.md`,
      `RAEUMLICHKEITEN_TENANT.md`)
- [ ] Bei Unsicherheiten: Rücksprache mit Praxisinhaber dokumentieren
      (Mini-Notiz im Subfolder, NICHT im offiziellen Dokument)
- [ ] Erledigte Kommentare in Word löschen (nicht „resolved" setzen —
      R-002 Begründung)
- [ ] Versionsnummer im Kopfteil erhöhen (R-001)

### Qualitätssicherung

- [ ] Versionsnummer hochzählen (Major bei strukturellem Change,
      Minor bei inhaltlichem Update)
- [ ] Datum aktualisieren (Erstelldatum bleibt; Freigabedatum wird
      mit der Freigabe gesetzt)
- [ ] Freigabe durch Praxisinhaber einholen (Unterschrift im
      Kopfteil + Datum)
- [ ] Original-Dokument in `01_Dokumente/` ersetzen; alte Version
      nach `01_Dokumente/_archiv/<original-stand>_YYMMDD.docx`
      verschieben
- [ ] `_BEARBEITET`-Kopie im Subfolder belassen als Audit-Spur

### Nachbereitung

- [ ] Änderungen im Team kommunizieren (Team-Sitzung, Mail-Versand,
      Schwarzes Brett — je nach Praxis)
- [ ] Schulungsbedarf prüfen (bei inhaltlichen Änderungen mit Wirkung
      auf Mitarbeiter-Handeln)
- [ ] Nächsten Review-Termin im Kalender eintragen (gemäß R-007)
- [ ] Eintrag im Fehlerprotokoll, falls Bearbeitung durch einen
      Fehler-Befund ausgelöst war

---

## Workflow 2: Neue SOP erstellen

### Vorbereitung

- [ ] SOP-Vorlage aus passendem Themen-Ordner kopieren
      (siehe `SCHEMA.md` Themen 01..12)
- [ ] Hardware-/Software-/Vorgangs-Daten erfassen (Typenschild bei
      Medizinprodukten, Hersteller-Gebrauchsanweisung, einschlägige
      Norm/Richtlinie)
- [ ] Verantwortliche festlegen (durchführende MFA, Aufsicht durch
      Praxisinhaber)

### Erstellung (SOP-Format, 7 Abschnitte)

- [ ] 1. **Ziel & Geltungsbereich**
- [ ] 2. **Verantwortliche**
- [ ] 3. **Schritt-für-Schritt-Anleitung** (mit Abbildungen, wenn
      sinnvoll — Hände-/Material-Position)
- [ ] 4. **Sicherheitsmaßnahmen & Notfallverfahren**
- [ ] 5. **Dokumentation & Nachweise**
- [ ] 6. **Gültigkeitsdatum & Unterschrift** (Praxisinhaber)
- [ ] 7. **Änderungshistorie**

### Freigabe

- [ ] Review durch erfahrene MFA (Plausibilität der Schritte im
      Praxis-Alltag)
- [ ] Review durch Praxisinhaber (medizinisch-fachliche Prüfung,
      Haftungs-Aspekte)
- [ ] Freigabe-Datum und Unterschrift eintragen
- [ ] SOP in `01_Dokumente/` ablegen (Dateinamen-Konvention
      `SOP_<Prozessname>_<YYYY-MM-DD>.docx` aus R-005)
- [ ] Bei SOP für ein Medizinprodukt: zusätzlich Eintrag im
      Medizinproduktebuch (Themen-Ordner 10)
- [ ] Team-Schulung planen + durchführen + Schulungsnachweis in
      `03_Arbeitsdateien/<schulungsdatum>/` ablegen

---

## Workflow 3: Jährliche QM-Überprüfung

Die vier Quartals-Reviews aus R-007 als Checkliste:

### Q1 — Januar

- [ ] QM-Handbuch auf Aktualität prüfen (regulatorische Änderungen
      seit Vorjahr eingearbeitet?)
- [ ] Qualitätsziele des Vorjahres auswerten (erreicht / verfehlt /
      teilweise)
- [ ] Neue Qualitätsziele definieren (3-5 Ziele, messbar, mit
      Zeit-Bezug)
- [ ] Mitarbeitergespräche planen (mind. 1 pro Mitarbeiter/Jahr)
- [ ] Managementbewertung schreiben (G-BA-konform, Themen 07)

### Q2 — April

- [ ] Hygieneplan überprüfen und aktualisieren (KRINKO/RKI-Updates?)
- [ ] R&D-Plan (Reinigungs- und Desinfektionsplan) aktualisieren
      (neue Produkte? neue Konzentrationen? Bauliche Änderungen?)
- [ ] Hygieneschulung durchführen und dokumentieren
- [ ] Hautschutz- und Handschuhplan auf Aktualität prüfen

### Q3 — Juli

- [ ] Medizinproduktebuch aktualisieren (Bestand abgleichen,
      Außerbetriebnahmen eintragen)
- [ ] STK-Termine prüfen und planen (welche Geräte sind in den
      nächsten 12 Monaten fällig?)
- [ ] Bestandsverzeichnis Medizinprodukte abgleichen
      (`02_Vorlagen_und_Anlagen/10/`)
- [ ] Geräteeinweisungen überprüfen (alle aktiven MFAs für alle
      eingesetzten Geräte eingewiesen?)
- [ ] Impfkühlschrank-Temperatur-Tagesprotokoll auf Lückenlosigkeit
      prüfen

### Q4 — Oktober

- [ ] Alle SOPs auf Aktualität prüfen (klinische Standards aktuell?
      Personalwechsel berücksichtigt?)
- [ ] Schulungsnachweise vervollständigen (alle erforderlichen
      Schulungen des Jahres dokumentiert?)
- [ ] Fortbildungsplan für Folgejahr erstellen
- [ ] Vorbereitung auf mögliche Begehung durch Gesundheitsamt
      (`02_Vorlagen_und_Anlagen/07/Praxisbegehungs-Checkliste`)

### Audit-Dokumentation

- [ ] Audit-Bericht in `03_Arbeitsdateien/<audit-datum>/` ablegen
- [ ] Abweichungen in `FEHLERPROTOKOLL_TENANT.md` eintragen
- [ ] Maßnahmen + Fristen im Aktionsplan dokumentieren
- [ ] Nachverfolgung der Maßnahmen-Erledigung im nächsten Quartal

---

## Empfohlene Frequenz für ad-hoc-Arbeit

- **Tägliche Mini-Vorgänge** (Eintrag im Medizinproduktebuch beim
  Geräte-Einsatz, Schulungsnachweis-Unterschrift): von der MFA
  unmittelbar erledigt, kein eigener Workflow.
- **Wöchentliche Pflege** (Impfkühlschrank-Tagesprotokoll-Plausibilität,
  R&D-Plan-Abgleich): ein definiertes MFA-Zeitfenster pro Woche.
- **Monatlicher Quick-Scan** (STK-Termine in den nächsten 90 Tagen,
  ausstehende Word-Kommentare): von der QM-verantwortlichen Person
  durchgeführt.

## Notfall: behördliche Begehung kommt überraschend

Wenn das Gesundheitsamt oder die Aufsichtsbehörde unangekündigt eine
Begehung durchführt:

1. **NICHT in Panik Dokumente nachträglich anpassen.** Begehungen
   prüfen Original-Versionsstand; nachträgliche Änderungen wären
   manipulativ und strafrelevant.
2. Sicherstellen, dass `01_Dokumente/` die aktuelle freigegebene
   Version enthält (gemäß letztem Review-Stand R-007).
3. Bei einem Mangel-Befund: Eintrag im Fehlerprotokoll, Maßnahme
   im Aktionsplan, **außerplanmäßiger Review** für das betroffene
   Dokument auslösen.
4. Wenn Bearbeitungs-Versionen in `03_Arbeitsdateien/` offen sind:
   das ist legitim und üblich — die Begehung bewertet den Stand in
   `01_Dokumente/`, nicht die laufende Arbeit.
