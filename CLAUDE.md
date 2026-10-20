# synthetic-data-tool

Generates synthetic warehouse clients with a known answer key, for experimenting with
goods-to-person analysis methods. Split out of power-bi-tool (commit `9b70ae7`, where it was
`gtpfit.synth`) because synthetic data was not giving the intended results there. **power-bi-tool no
longer depends on this tool.** Its tests use a frozen sample client that this tool made once
(`profiles/test_fixture.yaml`).

## Ground rules
- **No real client data in the repo.** `data/` is git-ignored. That includes `data/real_benchmark/`
  (profiles calibrated to a real client and their comparison results).
- **Deterministic:** every random draw goes through the profile's seed. Same profile + seed gives
  byte-identical files.
- **Every setting is a `knob()`** in `config.py`, with section, label, help, unit and range; the
  workbench form is built from these.
- Always pass `encoding="utf-8"` when reading/writing text (Windows defaults to cp1252).
- A docstring at the top of each module saying what it does and doesn't do.

## Layout
- `src/synthtool/`
  - `config.py` profile + defect rates + peak basket shape
  - `catalog.py` taxonomy and true item master
  - `demand.py` calendar and orders
  - `inventory.py` (s,Q) simulation, receipts and snapshots
  - `defects.py` planted problems + answer key
  - `generate.py` writer
  - `qa.py` realism report
  - `preview.py` instant calendar preview and size estimate
  - `benchmark.py` shape metrics, real vs synthetic
  - `lines.py` order-line definitions
  - `cli.py` command line
- `src/synthtool/app/` — Streamlit workbench (`synth_page.py`, `synth_form.py`), port 8502
- `profiles/` — `default`, `messy_large`, `playground`, `test_fixture`
- `tests/` — pytest

## Commands
See README.md.
