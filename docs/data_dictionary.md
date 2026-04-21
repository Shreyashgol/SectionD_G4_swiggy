# Data Dictionary

Use this file to document every important field in the Swiggy dataset. A strong data dictionary makes cleaning decisions, KPI logic, and dashboard filters much easier to review.

---

## Dataset Summary

| Item | Details |
|---|---|
| Dataset name | Swiggy Food Orders Dataset |
| Source | Kaggle |
| Raw file name | `swiggy_data_raw.csv` |
| Last updated | 2025-08-31 (latest Order Date in dataset) |
| Granularity | One row per dish ordered from a restaurant |

---

## Column Definitions

| Column Name | Data Type | Description | Example Value | Used In | Cleaning Notes |
|---|---|---|---|---|---|
| `state` | string | Indian state where the restaurant is located | Karnataka | EDA, Stats, Dashboarding | Nulls dropped |
| `city` | string | City where the restaurant is located | Bengaluru | EDA, Stats, Dashboarding | Nulls dropped |
| `order_date` | date | Date the order was placed | 2025-06-29 | EDA, Time Analysis | Parsed as datetime |
| `restaurant_name` | string | Name of the restaurant | Meghana Foods | EDA, Dashboarding | Nulls dropped |
| `location` | string | Area/locality of the restaurant within the city | Koramangala | EDA, Dashboarding | Nulls dropped |
| `category` | string | Food category of the dish | North Indian Gravy | EDA, Stats, Dashboarding | Nulls dropped |
| `dish_name` | string | Name of the dish ordered | Butter Chicken | EDA | No cleaning needed |
| `price_inr` | float | Price of the dish in Indian Rupees | 133.90 | EDA, Stats, Outlier Flagging | Nulls dropped, IQR outlier flag applied |
| `rating` | float | Customer rating of the restaurant (1.5 to 5.0) | 4.0 | EDA, Stats, ANOVA | Nulls dropped, Rating Count = 0 filtered out |
| `rating_count` | int | Number of ratings received by the restaurant | 25 | EDA, Filtering | Nulls dropped, rows with 0 filtered out. Raw dtype was float64 due to nulls — treat as int after cleaning |
| `month` | string | Month extracted from order_date | 2025-06 | EDA, Time Analysis | Derived from order_date |
| `day_of_week` | string | Day of week extracted from order_date | Sunday | EDA, Time Analysis | Derived from order_date |
| `price_bucket` | string | Price category of the dish | Budget | EDA, Dashboarding | Derived — Budget(<₹150), Mid-range(₹150–₹400), Premium(≥₹400) |

---

## Derived Columns

| Derived Column | Logic | Business Meaning |
|---|---|---|
| `month` | Extracted from `order_date` using `dt.to_period('M')` | Enables monthly trend analysis of orders and revenue |
| `day_of_week` | Extracted from `order_date` using `dt.day_name()` | Identifies which days of the week have highest order volumes |
| `price_bucket` | `pd.cut()` on `price_inr` — Budget(<₹150), Mid-range(₹150–₹400), Premium(≥₹400) | Segments dishes into price tiers for affordability analysis, dashboard filtering, and customer segmentation |

---

## Data Quality Notes

- **Missing data** — 9,871 rows had nulls across `location`, `category`, `price_inr`, `rating`, and `rating_count` simultaneously. All were dropped during cleaning.

- **Duplicate records** — 14 fully duplicate rows were found in the raw dataset and removed.

- **Unrated items** — 75,133 rows had `rating_count = 0`, meaning no customer ratings existed. These were filtered out as they are unreliable for analysis.

- **Price outliers** — Prices ranged from ₹0.95 to ₹8,000 in the raw data. IQR method was applied on the cleaned data (Q1=₹135, Q3=₹312, IQR=₹177), giving bounds of ₹-130.50 (lower) and ₹577.50 (upper). Since the lower bound is negative, all prices above ₹577.50 were flagged as outliers. A total of 4,180 rows were flagged via `is_price_outlier` column, which was later removed in the final dataset.

- **Rating Count dtype** — Raw `rating_count` was stored as `float64` due to nulls. Ideally should be treated as `int` after null removal.

- **Date range** — `order_date` spans Jan 2025 to Aug 2025 only. No data exists outside this window.