# Data Cleaning Report

## Project

DecodeLabs Data Analytics Project 1: Data Cleaning and Preparation.

## Goal

Clean a raw order dataset by handling missing values, duplicates, and incorrect data formats.

## Dataset Shape

| Metric | Value |
| --- | ---: |
| Rows before cleaning | 1200 |
| Columns before cleaning | 14 |
| Rows after cleaning | 1200 |
| Columns after cleaning | 14 |

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
| OrderID | 0 |
| Date | 0 |
| CustomerID | 0 |
| Product | 0 |
| Quantity | 0 |
| UnitPrice | 0 |
| ShippingAddress | 0 |
| PaymentMethod | 0 |
| OrderStatus | 0 |
| TrackingNumber | 0 |
| ItemsInCart | 0 |
| CouponCode | 309 |
| ReferralSource | 0 |
| TotalPrice | 0 |

## Missing Values After Cleaning

| Column | Missing Values |
| --- | ---: |
| OrderID | 0 |
| Date | 0 |
| CustomerID | 0 |
| Product | 0 |
| Quantity | 0 |
| UnitPrice | 0 |
| ShippingAddress | 0 |
| PaymentMethod | 0 |
| OrderStatus | 0 |
| TrackingNumber | 0 |
| ItemsInCart | 0 |
| CouponCode | 0 |
| ReferralSource | 0 |
| TotalPrice | 0 |

## Required Quality Proof

| Check | Before | After |
| --- | ---: | ---: |
| Full duplicate rows | 0 | 0 |
| Duplicate OrderID values | 0 | 0 |
| Incorrectly formatted dates | 0 | 0 |
| TotalPrice mismatches corrected | 0 | 0 |

## Final Result

The cleaned dataset passes the required DecodeLabs checks:

- Duplicate OrderID values: 0
- Incorrectly formatted dates: 0
- Missing values remaining: 0
