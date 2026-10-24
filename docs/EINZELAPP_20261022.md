# Einzel-App Cortex QM (2026-10-22)

## Auftrag

Native Tauri-2-Einzelapp für `cortex-qm` auf Zweig `einzelapp-20261022`, Marketplace-Manifest, lauffähiger unsignierter Build, Tests grün.

## Gebaut

| Baustein | Ort | Zweck |
|----------|-----|--------|
| Tauri 2 + Vite/TS | `app/` | Eigenständiges Programm `Cortex QM`, Bundle-ID `de.sanexio.cortex-qm`, Version 0.1.0 |
| `cortex-app-core` | Pfadabhängigkeit in `app/src-tauri/Cargo.toml` | Andock-Manifest, signierte Lizenzprüfung (öffentlicher Schlüssel zur Build-Zeit) |
| UI | `app/src/` | QM-Regelwerk (`rules/`), Phase-B-Vorlagen (`dokumente/`, `arbeitsdateien/` per Manifest), Demo-Checkliste via `cortex_qm` CLI |
| Design | `app/src/themes.css`, `theme.ts` | **Praxis 2025** (Default) und **Cyberpunk** (`cyber-dark`) umschaltbar |
| Marketplace | `marketplace/app.json` + `icon.png` / `icon-qr.png` | Katalog-Metadaten für den Cortex-Marketplace |
| Lizenz-Stub | `app/schluessel/lizenz-oeffentlich.txt` | Ed25519-Öffentlichkeit (wie Nexus Marketplace); keine Zahlung, Freischaltung über signierte `lizenz.json` |
| Updater-Stub | `tauri-plugin-updater` + Platzhalter-Feed in `tauri.conf.json` | Manuelle Prüfung im UI; Artefakt-Signierung aus (Codex/Beglaubigung offen) |

### Funktionsumfang v0.1.0

- Lesender Zugriff auf das **QM-Regelwerk** im Repo (`rules/`, Pfad-Allowlist, keine `*_TENANT.md`).
- Anzeige und Lesen der **Phase-B-Platzhalter** aus `docs/vorlagen-manifest.json` (`dokumente/`, `arbeitsdateien/`).
- **Demo-Werkzeug:** Begehungs-Checkliste über eingebettete Python-Bibliothek (`rules/CATEGORIES_EXAMPLE.md` nur).
- Beim Start: **Andock-Manifest** unter `~/Library/Application Support/Cortex/apps/cortex-qm.json` (macOS).
- **Kein** Zugriff auf private Tenant-Arbeitsordner (`01_Dokumente/` …) oder gitignored Tenant-Listen.

### Build (lokal, unsigniert)

```sh
cd app
npm ci
npm run build
npm exec tauri build
```

Ergebnis (macOS): `app/src-tauri/target/release/bundle/macos/Cortex QM.app`

### Tests

```sh
python3 -m pip install -e '.[test]'      # einmalig: pytest + jsonschema
python3 -m pytest -q                      # Wurzelverzeichnis
cd app && npm test
cd app/src-tauri && cargo test --locked
```

### Was `cargo test` voraussetzt (gemessen 2026-10-24)

`app/src-tauri` hängt über **Pfadabhängigkeiten** an zwei weiteren privaten
Repositories, die **neben** `cortex-qm` liegen müssen — so wie lokal unter
`projects/`:

| Pfad | Repository | Zweig (Stand 24.10.) | Warum |
|------|------------|----------------------|-------|
| `../../../cortex-app-core` | `Sanexio/cortex-app-core` | `p1-cortex-app-core` | `cortex-app-core` **und** `cortex-app-updates`; letzteres gibt es in `main` **nicht** |
| `../../../cortex-app` | `Sanexio/cortex-app` | `p3-cortex-app` | `build.rs` von `cortex-app-updates` liest `config/apple-signierung.json`; in `main` **nicht** vorhanden |

Zusätzlich muss **das Frontend vorher gebaut sein** (`npm ci && npm run build`):
`tauri::generate_context!()` liest `app/dist` zur Compile-Zeit, sonst scheitert
schon das Übersetzen.

## CI (`.github/workflows/ci.yml`)

Drei Jobs auf `ubuntu-latest`: `pytest`, Marketplace-Manifest-Validierung und
`cargo test --locked`. **Nur manuell auslösbar** (`workflow_dispatch`) — dieselbe
Kostenlinie, die `Sanexio/cortex-app` in seinem Bau-Workflow wörtlich festhält.

Der `cargo`-Job braucht Lesetoken für die beiden privaten Nachbar-Repositories
(`CORTEX_APP_CORE_READ_TOKEN`, `CORTEX_APP_READ_TOKEN`); fehlen sie, bricht der
erste Schritt mit klarer Meldung ab, statt unverständlich zu scheitern. Die
Revisionen sind auf geprüfte Commit-IDs festgenagelt und über die
Repository-Variablen `CORTEX_APP_CORE_REF` / `CORTEX_APP_REF` überschreibbar.

Die Manifest-Prüfung arbeitet **ohne Netzzugriff** gegen die angeheftete
Schema-Kopie unter `marketplace/schema/`; ein optionaler Drift-Abgleich geht
ausschließlich gegen GitHub. Warum `app.json` nicht als Ganzes gegen dieses
Schema validiert werden kann, steht in `marketplace/schema/README.md`.

## Noch offen (bewusst nicht in diesem Zweig)

- **Code-Signing / Notarisierung** (macOS) und Windows-Signatur — Auftrag Codex.
- **Minisign-Update-Schlüssel** und echter Update-Feed (aktuell Platzhalter-URL + `REPLACE_WITH_MINISIGN_PUBLIC_KEY`).
- **Tracker- und Kommentar-Werkzeuge** in der UI (CLI vorhanden, noch ohne Datei-Dialog und Tenant-Pfadwahl).
- **Nexus-Brücke** (Cargo-Feature wie App-Template) — nicht aktiviert.
- **CI auf mehreren Betriebssystemen** — angelegt ist der Linux-Weg
  (`.github/workflows/ci.yml`); macOS/Windows folgen der Marketplace-Welle.
  **Noch kein CI-Lauf abgenommen:** GitHub Actions ist im Konto `Sanexio`
  wegen einer Abrechnungssperre gesperrt (Beleg: Lauf `40118358119` in
  `Sanexio/workforce-time`, alle Jobs nach 3 s auf `failure`, 0 ausgeführte
  Schritte). Das ist kontoweit und betrifft diesen Zweig nicht inhaltlich.
- Symbol **Sanexio-QR**: `marketplace/icon-qr.png` ist vorerst dieselbe Rastergrafik wie `icon.png`; dedizierte QR-Markenvariante durch Design/Codex.

## Referenzen

- `Nexus/specs/app-marketplace/00_KONZEPT.md`, `02_CORTEX_APP_DESIGN.md`
- `Nexus/_rules/design-theme.md`
- Vorlage: `projects/cortex-desk/app/` (Einzelapp-Welle 2026-10-22), `projects/cortex-app-core`

## BA2 Release-Härtung

Der Cursor-Zweig bleibt Grundlage. Regelwerk und explizit freigegebene Framework-Vorlagen sind jetzt einkompiliert: kein Laufzeit-Zugriff auf den Quellordner oder Tenant-Dateien. Native Inhaltsbefehle prüfen signierte Lizenz, feste App-Kennung und Klasse. Fehlende Freischaltung zeigt eine nutzbare Statusoberfläche. Echte signierte synthetische Nutzlasten prüfen gültig, fremder Schlüssel, Ablauf, falsche App und nachträgliche Manipulation. QR-Symbol aus der bestehenden Cortex-App; Praxis 2025 bleibt Default, Cyberpunk umschaltbar. Private Update-Adresse je Produkt vorbereitet, kein öffentlicher Release. Keine Update-Schlüssel oder Passwörter ausgelesen.

Apple-Notarisierung ist am 22.10.2026 durch HTTP 403 (fehlende/abgelaufene erforderliche Vereinbarung) gesperrt. Developer-ID-Signatur ist möglich. Ohne Accepted/Ticket/Gatekeeper keine Verteilung. Windows/Linux in dieser BA2-Mac-Welle nicht als gebaut oder gestartet behauptet.
