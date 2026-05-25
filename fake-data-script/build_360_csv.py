#!/usr/bin/env python3
"""Build data/360.csv from generated fake raw CSV files."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import duckdb


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
SQL_PATH = SCRIPT_DIR / "sql" / "ads_unified.sql"
DEFAULT_OUTPUT_PATH = PROJECT_ROOT / "data" / "360.csv"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def build_360_csv(sql_text: str, output_path: Path) -> int:
    sql_without_trailing_semicolon = sql_text.rstrip().rstrip(";")
    escaped_output = str(output_path).replace("'", "''")
    copy_sql = f"""
        COPY (
            {sql_without_trailing_semicolon}
        )
        TO '{escaped_output}'
        (HEADER, DELIMITER ',')
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with duckdb.connect() as connection:
        connection.execute(copy_sql)
        row_count = connection.execute(
            f"SELECT COUNT(*) FROM read_csv_auto('{escaped_output}', header = true)"
        ).fetchone()[0]

    return int(row_count)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build data/360.csv from fake raw marketing CSV files.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT_PATH), help="Output CSV path.")
    args = parser.parse_args()

    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = PROJECT_ROOT / output_path

    os.chdir(PROJECT_ROOT)
    row_count = build_360_csv(read_text(SQL_PATH), output_path)
    print(f"Built {output_path} with {row_count} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
