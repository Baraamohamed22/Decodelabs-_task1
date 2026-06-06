# DecodeLabs Data Analytics Project 1

## Data Cleaning and Preparation

This project cleans a raw ecommerce order dataset for DecodeLabs Project 1. The goal is to prepare reliable data by checking missing values, removing duplicates, correcting formats, and proving that the final dataset passes the required quality checks.

## Project Requirements

- Identify missing or null values.
- Remove duplicate records.
- Correct data formats for dates, numbers, and text.
- Prove there are zero duplicate IDs.
- Prove there are zero incorrectly formatted dates.

## Dataset

The raw dataset is stored at:

`data/raw_dataset.xlsx`

It contains order-level data with these fields:

- `OrderID`
- `Date`
- `CustomerID`
- `Product`
- `Quantity`
- `UnitPrice`
- `ShippingAddress`
- `PaymentMethod`
- `OrderStatus`
- `TrackingNumber`
- `ItemsInCart`
- `CouponCode`
- `ReferralSource`
- `TotalPrice`

## Tools Used

- Python
- Pandas
- Excel

## Cleaning Process

The cleaning script performs these steps:

1. Loads the raw Excel dataset.
2. Checks that all required columns are present.
3. Checks missing values in every column.
4. Standardizes text by removing extra spaces.
5. Converts the `Date` column to a valid date format.
6. Converts numeric columns to numeric data types.
7. Recalculates `TotalPrice` using `Quantity * UnitPrice`.
8. Replaces missing `CouponCode` values with `NO_COUPON`.
9. Removes duplicate rows.
10. Removes duplicate `OrderID` values.
11. Exports the cleaned dataset.
12. Creates a data cleaning report.

## How to Run

Install the required Python package:

```bash
pip install pandas openpyxl
```

Run the cleaning script:

```bash
python clean_data.py
```

## Output Files

After running the script, the cleaned files are created in the `outputs` folder:

- `outputs/cleaned_dataset.csv`
- `outputs/cleaned_dataset.xlsx`
- `outputs/data_cleaning_report.md`
- `outputs/quality_summary.json`

## Final Quality Checks

The final cleaned dataset must show:

- Duplicate `OrderID` values: `0`
- Incorrectly formatted dates: `0`
- Missing values remaining: `0`

The proof is documented in:

`outputs/data_cleaning_report.md`
