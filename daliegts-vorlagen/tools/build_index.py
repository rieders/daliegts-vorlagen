#!/usr/bin/env python3
"""Baut index.json aus templates/*.json (Dateien mit „_“ am Anfang werden übersprungen) und prüft jede Vorlage.

Aufruf:  python tools/build_index.py          # prüft und schreibt index.json
         python tools/build_index.py --check  # nur prüfen (für Pull Requests)
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAX_GRID = 50
FIELDS = {"type", "rows", "cols", "row_counts", "merges", "gaps", "naming", "prefix", "count_direction", "bottom_up", "subdivision",
          "subdivision_layout", "subdivision_naming", "light_mode", "width_cm", "height_cm", "group"}


def check(name: str, t: dict) -> list[str]:
    errs = []
    d = t.get("definition")
    if not str(t.get("name", "")).strip():
        errs.append("name fehlt")
    if not isinstance(d, dict):
        return errs + ["definition fehlt"]
    for k in d:
        if k not in FIELDS:
            errs.append(f"unbekanntes Feld „{k}“ in definition (LED-Verkabelung wird nicht geteilt)")
    for k in ("rows", "cols"):
        if not isinstance(d.get(k), int) or not 1 <= d[k] <= MAX_GRID:
            errs.append(f"{k} muss eine ganze Zahl von 1 bis {MAX_GRID} sein")
    for k in ("width_cm", "height_cm"):
        if k in d and not (isinstance(d[k], (int, float)) and 0 < d[k] <= 1000):
            errs.append(f"{k} muss zwischen 0 und 1000 liegen")
    for m in d.get("merges", []):
        if not (isinstance(m, list) and len(m) == 4 and all(isinstance(x, int) and x >= 1 for x in m)):
            errs.append(f"merges: {m} ist nicht [Reihe, Spalte, Reihen, Spalten]")
        elif isinstance(d.get("rows"), int) and isinstance(d.get("cols"), int) and (m[0] + m[2] - 1 > d["rows"] or m[1] + m[3] - 1 > d["cols"]):
            errs.append(f"merges: {m} liegt außerhalb des Rasters")
    if not t.get("notes"):
        errs.append("notes: bitte Quelle der Maße angeben")
    return errs


def main() -> int:
    only_check = "--check" in sys.argv
    out, bad, names = [], False, set()
    for f in sorted((ROOT / "templates").glob("*.json")):
        if f.name.startswith("_"):
            continue
        try:
            t = json.loads(f.read_text(encoding="utf-8"))
        except ValueError as e:
            print(f"✗ {f.name}: kein gültiges JSON ({e})")
            bad = True
            continue
        errs = check(f.name, t)
        if t.get("name") in names:
            errs.append("Name kommt schon in einer anderen Datei vor")
        names.add(t.get("name"))
        if errs:
            bad = True
            print(f"✗ {f.name}: " + "; ".join(errs))
        else:
            out.append({k: t[k] for k in ("name", "kind", "group", "author", "notes", "definition") if k in t})
            print(f"✓ {f.name}")
    if bad:
        return 1
    if not only_check:
        (ROOT / "index.json").write_text(json.dumps({"version": 1, "templates": out}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"index.json: {len(out)} Vorlagen")
    return 0


if __name__ == "__main__":
    sys.exit(main())
