# Öffentlicher Lieferumfang — cortex-qm

Stand: 2026-09-26. Regelwerk, ausführbare Demos und generische
Strukturvorlagen sind vorhanden. Die Veröffentlichung erfolgt separat
nach Prüfung und Freigabe des auszuliefernden Baums.

## Enthaltene Bausteine

- `rules/`: Kernregeln, Themen- und Ordnerschema, Workflows sowie
  generische Beispiele für Personal, Geräte und Räume.
- `dokumente/`: Strukturvorlagen für Hygieneplan, QM-Handbuch,
  Medizinproduktebuch, Aktionsplan und SOP.
- `arbeitsdateien/`: Kommentarübersicht, Reviewprotokoll und Schulungsnachweis.
- `examples/`: eigenständig ausführbare Demos zur DOCX-Kommentarauswertung
  und zur Audit-Checklisten-Erstellung mit fiktiven Daten.
- [Vorlagenumfang](docs/PHASE_B_VORLAGEN.md) und
  [Vorlagenmanifest](docs/vorlagen-manifest.json): vollständige Vorlagenliste.
- [Tooling-Integration](docs/ENGINE_INTEGRATION.md): öffentliche
  Fähigkeiten und Schnittstellen für eigene oder optionale Engines.

## Private Arbeitskopien und optionales Tooling

Die Vorlagen enthalten leere Eingabefelder. Ausgefüllte Dokumente,
Personallisten, Raum- und Gerätebestände sowie Schulungsbestätigungen
bleiben im privaten Arbeitsbereich der jeweiligen Praxis.
Produktive proprietäre Engines werden separat bereitgestellt und sind
weder Voraussetzung für das Lesen des Regelwerks noch für die Demos.

Vorhandene öffentliche Vorlagen bestätigen keine Migration privater
Bestände und keine fachliche Freigabe ausgefüllter Praxisdokumente.

## Nutzung und Veröffentlichung

1. Den [Quickstart](README.md) und die Nutzungshinweise der Vorlagen lesen.
2. `bash examples/run-demo.sh` für die mitgelieferten Demos ausführen.
3. Gewünschte Vorlagen privat kopieren, ausarbeiten und fachlich freigeben.
4. Vor einer Veröffentlichung den vollständigen Lieferbaum einschließlich
   Beispielen und Dokumentmetadaten prüfen und separat freigeben.

Regelwerk, Vorlagen und Demos stehen unter Apache 2.0; siehe
[LICENSE](LICENSE) und [NOTICE](NOTICE).
