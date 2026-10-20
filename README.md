# synthetic-data-tool

Makes synthetic warehouse clients (item master, order history, receipts, inventory snapshots) in a
client-style export layout, with an answer key under `_truth/` and a realism report. It's a
standalone tool. Until October 2026 it lived inside power-bi-tool as `gtpfit.synth`.

```
pip install -e .[dev,app]
python -m synthtool --out data/synthetic/default                         # generate + realism report
python -m synthtool --profile profiles/messy_large.yaml --out data/synthetic/messy_large
python -m synthtool.app                                                  # workbench, http://localhost:8502
python -m synthtool benchmark --real ../power-bi-tool/data/<client>/_ingest --synthetic data/synthetic/default \
    --channels Ecomm=Ecommerce,Retail=Store [--lines order_sku]          # compare with a real client
python -m pytest -q
```

`benchmark` compares shape metrics against power-bi-tool's ingest output: the `_ingest` folder of
Parquet files written by its Outputs tab or by `python -m gtpfit.ingest`. The metrics include order
profile, daily and hourly patterns, SKU concentration, inbound and inventory. Generated data and
benchmark results go in `data/`, which git ignores.
