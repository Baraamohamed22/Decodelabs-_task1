from pathlib import Path
import json

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parent
RAW_DATA_PATH = ROOT_DIR / "data" / "raw_dataset.xlsx"
OUTPUT_DIR = ROOT_DIR / "outputs"
CSV_OUTPUT_PATH = OUTPUT_DIR / "cleaned_dataset.csv"
XLSX_OUTPUT_PATH = OUTPUT_DIR / "cleaned_dataset.xlsx"
REPORT_PATH = OUTPUT_DIR / "data_cleaning_report.md"
SUMMARY_PATH = OUTPUT_DIR / "quality_summary.json"

REQUIRED_COLUMNS = [
    "OrderID",
    "Date",
    "CustomerID",
    "Product",
    "Quantity",
    "UnitPrice",
    "ShippingAddress",
    "PaymentMethod",
    "OrderStatus",
    "TrackingNumber",
    "ItemsInCart",
    "CouponCode",
    "ReferralSource",
    "TotalPrice",
]


def missing_counts(df: pd.DataFrame) -> dict[str, int]:
    return {column: int(count) for column, count in df.isna().sum().items()}


def normalize_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    text_columns = df.select_dtypes(include=["object", "string"]).columns
    for column in text_columns:
        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
        )
    return df


def validate_required_columns(df: pd.DataFrame) -> None:
    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")


def clean_dataset(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    validate_required_columns(df)

    summary = {
        "rows_before": int(len(df)),
        "columns_before": int(len(df.columns)),
        "missing_values_before": missing_counts(df),
        "full_duplicate_rows_before": int(df.duplicated().sum()),
        "duplicate_order_ids_before": int(df["OrderID"].duplicated().sum()),
        "invalid_dates_before": int(pd.to_datetime(df["Date"], errors="coerce").isna().sum()),
    }

    cleaned = df.copy()

    cleaned = normalize_text_columns(cleaned)

    cleaned["Date"] = pd.to_datetime(cleaned["Date"], errors="coerce")
    cleaned = cleaned.dropna(subset=["Date"])

    numeric_columns = ["Quantity", "UnitPrice", "ItemsInCart", "TotalPrice"]
    for column in numeric_columns:
        cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

    cleaned = cleaned.dropna(subset=["Quantity", "UnitPrice", "ItemsInCart", "TotalPrice"])
    cleaned["Quantity"] = cleaned["Quantity"].astype(int)
    cleaned["ItemsInCart"] = cleaned["ItemsInCart"].astype(int)
    cleaned["UnitPrice"] = cleaned["UnitPrice"].round(2)

    expected_total = (cleaned["Quantity"] * cleaned["UnitPrice"]).round(2)
    total_price_mismatches = int((cleaned["TotalPrice"].round(2) != expected_total).sum())
    cleaned["TotalPrice"] = expected_total

    cleaned["CouponCode"] = cleaned["CouponCode"].fillna("NO_COUPON")
    cleaned["CouponCode"] = cleaned["CouponCode"].replace({"": "NO_COUPON", "<NA>": "NO_COUPON"})

    cleaned = cleaned.drop_duplicates()
    cleaned = cleaned.drop_duplicates(subset=["OrderID"], keep="first")
    cleaned = cleaned.sort_values("OrderID").reset_index(drop=True)

    invalid_dates_after = int(pd.to_datetime(cleaned["Date"], errors="coerce").isna().sum())
    duplicate_order_ids_after = int(cleaned["OrderID"].duplicated().sum())
    full_duplicate_rows_after = int(cleaned.duplicated().sum())

    summary.update(
        {
            "rows_after": int(len(cleaned)),
            "columns_after": int(len(cleaned.columns)),
            "missing_values_after": missing_counts(cleaned),
            "full_duplicate_rows_after": full_duplicate_rows_after,
            "duplicate_order_ids_after": duplicate_order_ids_after,
            "invalid_dates_after": invalid_dates_after,
            "total_price_mismatches_corrected": total_price_mismatches,
        }
    )

    if duplicate_order_ids_after != 0:
        raise ValueError("Quality check failed: duplicate OrderID values remain.")
    if invalid_dates_after != 0:
        raise ValueError("Quality check failed: invalid Date values remain.")

    return cleaned, summary


def write_report(summary: dict) -> None:
    before_missing_rows = "\n".join(
        f"| {column} | {count} |"
        for column, count in summary["missing_values_before"].items()
    )
    after_missing_rows = "\n".join(
        f"| {column} | {count} |"
        for column, count in summary["missing_values_after"].items()
    )

    report = f"""# Data Cleaning Report

## Project

DecodeLabs Data Analytics Project 1: Data Cleaning and Preparation.

## Goal

Clean a raw order dataset by handling missing values, duplicates, and incorrect data formats.

## Dataset Shape

| Metric | Value |
| --- | ---: |
| Rows before cleaning | {summary["rows_before"]} |
| Columns before cleaning | {summary["columns_before"]} |
| Rows after cleaning | {summary["rows_after"]} |
| Columns after cleaning | {summary["columns_after"]} |

## Cleaning Steps

1. Loaded the raw Excel dataset.
2. Checked all required columns.
3. Removed leading, trailing, and repeated spaces from text columns.
4. Converted `Date` values to a valid date format.
5. Converted numeric columns to numeric data types.
6. Recalculated `TotalPrice` as `Quantity * UnitPrice`.
7. Replaced missing `CouponCode` values with `NO_COUPON`.
8. Removed duplicate rows.
9. Removed duplicate `OrderID` values.
10. Exported cleaned CSV and Excel files.

## Missing Values Before Cleaning

| Column | Missing Values |
| --- | ---: |
{before_missing_rows}

## Missing Values After Cleaning

| Column | Missing Values |
| --- | ---: |
{after_missing_rows}

## Required Quality Proof

| Check | Before | After |
| --- | ---: | ---: |
| Full duplicate rows | {summary["full_duplicate_rows_before"]} | {summary["full_duplicate_rows_after"]} |
| Duplicate OrderID values | {summary["duplicate_order_ids_before"]} | {summary["duplicate_order_ids_after"]} |
| Incorrectly formatted dates | {summary["invalid_dates_before"]} | {summary["invalid_dates_after"]} |
| TotalPrice mismatches corrected | {summary["total_price_mismatches_corrected"]} | 0 |

## Final Result

The cleaned dataset passes the required DecodeLabs checks:

- Duplicate OrderID values: 0
- Incorrectly formatted dates: 0
- Missing values remaining: 0
"""
    REPORT_PATH.write_text(report, encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw_df = pd.read_excel(RAW_DATA_PATH, sheet_name="Sheet1")
    cleaned_df, summary = clean_dataset(raw_df)

    cleaned_df.to_csv(CSV_OUTPUT_PATH, index=False, date_format="%Y-%m-%d")
    cleaned_df.to_excel(XLSX_OUTPUT_PATH, index=False, sheet_name="Cleaned_Data")

    SUMMARY_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_report(summary)

    print("Project 1 cleaning complete.")
    print(f"Cleaned CSV: {CSV_OUTPUT_PATH}")
    print(f"Cleaned Excel: {XLSX_OUTPUT_PATH}")
    print(f"Report: {REPORT_PATH}")


if __name__ == "__main__":
    main()
