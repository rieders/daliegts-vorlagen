# Vorlage beitragen

## Was gehört in eine Vorlage?

Eine Vorlage beschreibt **Gehäusemaße und Fachraster** eines Möbels – keine Daten aus deiner Installation. Das Format ist das des JSON-Exports
in DaLiegt’s:

```json
{
  "name": "Parkside Kleinteilemagazin 33 Schubladen (30,5×41,5 cm)",
  "kind": "magazin",
  "group": "Sortimentskästen",
  "author": "dein Name",
  "notes": "Gehäuse 30,5 × 41,5 × 13,5 cm. Quelle: Lidl-Datenblatt, Raster am eigenen Exemplar geprüft.",
  "definition": { "type": "magazin", "rows": 11, "cols": 3, "width_cm": 30.5, "height_cm": 41.5 }
}
```

* `name`: Hersteller zuerst, dann Modell, Fächerzahl und Maße in Klammern. Der Name ist eindeutig.
* `group`: Rubrik in der Vorlagen-Liste. Für Sortimentskästen und Kleinteilemagazine **„Sortimentskästen“**, für Regale z. B. „Regale“.
* `notes`: **Pflicht** – woher stammen die Maße (Herstellerangabe, Händler, selbst gemessen)? Ist das Raster nur abgeleitet, schreibe das hinein.
* `definition`: `rows` und `cols` (je 1–50), `width_cm` und `height_cm` (Außenmaße), optional `merges` (zusammengefasste Fächer als
  `[Reihe, Spalte, Reihen, Spalten]`, 1-basiert), `gaps` (leere Plätze), `row_counts` (unterschiedlich viele Schubladen je Reihe).
  LED-Verkabelung wird **nicht** geteilt.

## Regeln

* Nur Maße und Raster, keine Fotos oder Produkttexte der Hersteller.
* Nur Dinge eintragen, die du am Produkt oder im Datenblatt geprüft hast. Im Zweifel in `notes` „Raster abgeleitet“ schreiben.
* Eine Datei pro Vorlage in `templates/`. Dateien, die mit `_` beginnen, werden ignoriert.

## Prüfen

Lokal: `python tools/build_index.py --check`. Im Pull Request läuft dieselbe Prüfung automatisch.
