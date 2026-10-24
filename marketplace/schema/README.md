# Angeheftetes Katalogschema

`manifest.schema.json` ist eine **wortgleiche Kopie** von
`inc/marketplace/schema/manifest.schema.json` aus `Sanexio/praxiszentrum-theme`,
angeheftet an die Revision in `HERKUNFT.json`. Die Kopie liegt hier, damit
`tests/test_marketplace_manifest.py` ohne Netzzugriff prueft; `HERKUNFT.json`
haelt Commit, Blob-Kennung, SHA-256 und Groesse fest, damit die Kopie nicht
stillschweigend von ihrer Quelle abdriftet.

## Zwei verschiedene Dokumentarten — gemessen, nicht vermutet

Das Schema beschreibt den **Katalog des Storefront-Moduls**: ein Dokument mit
`manifest_version`, `store` und einer Liste `apps[]`.

`marketplace/app.json` in diesem Repository ist dagegen das **Manifest einer
einzelnen App** mit eigenen, deutschsprachigen Feldnamen (`kurzbeschreibung`,
`klasse`, `symbol`, `plattformen`, `update_kanal` …). Dieselbe Form liegt in
`Sanexio/cortex-desk` (`marketplace/app.json`, Zweig `ba2-einzelapp-20261022`) —
es ist also eine etablierte Konvention der App-Repositories, kein Ausrutscher
von `cortex-qm`.

Eine Validierung von `app.json` **als Ganzes** gegen dieses Schema kann daher
nicht gruen sein: das Schema setzt `additionalProperties: false` und verlangt
`manifest_version`/`store`/`apps`. Der Test validiert deshalb die
**Katalogprojektion**: aus `app.json` wird der Eintrag gebaut, den das
Storefront-Modul spaeter in `apps[]` aufnimmt, und dieser Eintrag wird gegen
`#/$defs/app` geprueft — mit echtem JSON-Schema-Validator, nicht mit
handgeschriebenen Feldpruefungen.

## Die eine bewusst gelockerte Stelle

`#/$defs/app` verlangt `downloads` (mindestens eine HTTPS-Paket-URL).
`cortex-qm` hat **keinen oeffentlichen Release** (siehe
`docs/EINZELAPP_20261022.md`, Abschnitt „BA2 Release-Haertung"), also gibt es
diese URL nicht. Sie wird **nicht erfunden**. Der Test nimmt `downloads` aus der
Pflichtliste heraus — und prueft zugleich, dass genau dieses eine Feld fehlt.
Kommt ein weiteres Pflichtfeld hinzu oder liefert `app.json` eines Tages
Download-URLs, schlaegt der Test fehl und erzwingt eine Entscheidung, statt die
Luecke stillschweigend groesser werden zu lassen.
