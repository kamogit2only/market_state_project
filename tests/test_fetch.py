from pathlib import Path

from data_fetch import fetch


def test_csv_exists():
    out = fetch()
    assert Path(out).exists()
