"""Benchmark command: load a generated dataset, load an ingest-style canonical folder, compare."""
from pathlib import Path

import duckdb
import pytest

from synthtool import generate, load_profile
from synthtool.benchmark import load_canonical, load_dataset, run
from synthtool.cli import main as cli

TINY = dict(n_skus=250, ecom_orders_per_day=60, b2b_orders_per_day=3, days=40)


@pytest.fixture(scope="module")
def ds(tmp_path_factory):
    out = tmp_path_factory.mktemp("bench_src")
    generate(load_profile(**TINY), out)
    return out


def _as_ingest_output(ds, folder: Path):
    """Write the dataset the way power-bi-tool's ingest writes its output: canonical names, Parquet."""
    o, r, i, it = load_dataset(ds)
    folder.mkdir()
    o = o.rename(columns={"units": "qty"}).assign(pick_secs=o["hour"] * 3600,
                                                    channel=o["channel"].map({"Ecommerce": "Ecomm", "Store": "Retail"}))
    con = duckdb.connect()
    for name, df in [("orders", o.drop(columns=["hour"])), ("receipts", r), ("inventory", i), ("item_master", it)]:
        con.register("t", df)
        con.execute(f"copy t to '{(folder / (name + '.parquet')).as_posix()}' (format parquet)")
        con.unregister("t")


def test_load_dataset_cleans_like_ingest(ds):
    o, r, i, it = load_dataset(ds)
    assert (o["units"] > 0).all()
    assert not o["sku"].str.contains(r"^\s|\s$|[a-z]").any()
    assert {"order_id", "sku", "order_date", "units", "channel", "hour", "full_case"} <= set(o.columns)
    assert len(r) and len(i) and len(it)


def test_dataset_against_itself_matches(ds, tmp_path):
    _as_ingest_output(ds, tmp_path / "_ingest")
    real = load_canonical(tmp_path / "_ingest", {"Ecomm": "Ecommerce", "Retail": "Store"})[0]
    assert set(real["channel"]) == {"Ecommerce", "Store"}
    t = run(tmp_path / "_ingest", ds, channels={"Ecomm": "Ecommerce", "Retail": "Store"}, out=tmp_path / "out")
    ratio = t.set_index("metric")["synthetic / real"]
    for k in ("ecommerce_single_line_share", "store_lines_per_order", "design_ratio_p95", "top20_sku_line_share",
              "turns_per_year"):
        assert ratio[k] == pytest.approx(1.0), k
    assert (tmp_path / "out" / "comparison.csv").exists() and (tmp_path / "out" / "results.json").exists()


def test_cli_benchmark(ds, tmp_path, capsys):
    _as_ingest_output(ds, tmp_path / "_ingest")
    cli(["benchmark", "--real", str(tmp_path / "_ingest"), "--synthetic", str(ds), "--out", str(tmp_path / "o"),
         "--lines", "order_sku", "--channels", "Ecomm=Ecommerce,Retail=Store"])
    assert "ecommerce_single_line_share" in capsys.readouterr().out
    assert (tmp_path / "o" / "comparison.csv").exists()


def test_missing_real_folder_is_clear(tmp_path, ds):
    with pytest.raises(FileNotFoundError, match="_ingest"):
        run(tmp_path / "nothing", ds)
