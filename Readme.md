# Swiggy Food Orders Analytics
## Data Visualization & Analytics — DVA Capstone 2

> **Newton School of Technology | Section D | Group 4**
> A 2-week industry simulation capstone using Python, GitHub, and Tableau to convert raw Swiggy food orders data into actionable business intelligence.

---

## Before You Start

1. Clone the repository: `SectionD_G4_swiggy`
2. Add the raw dataset to `data/raw/`
3. Complete the notebooks in order from `01` to `05`
4. Publish the final dashboard and add the public link in `tableau/dashboard_links.md`
5. Export the final report and presentation as PDFs into `reports/`

### Quick Start

If you are working locally:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter notebook
```

If you are working in Google Colab:

- Upload or sync the notebooks from `notebooks/`
- Keep the final `.ipynb` files committed to GitHub
- Export any cleaned datasets into `data/processed/`

---

## Project Overview

| Field | Details |
|---|---|
| **Project Title** | Swiggy Food Orders Analytics |
| **Sector** | Food Tech / Quick Commerce |
| **Team ID** | SectionD — Group 4 |
| **Section** | Section D |
| **Faculty Mentor** | Satyaki Das |
| **GitHub** | [https://github.com/Shreyashgol/SectionD_G4_swiggy](https://github.com/Shreyashgol/SectionD_G4_swiggy) |
| **Tableau Dashboard** | https://public.tableau.com/app/profile/shashwat.sinha3668/viz/Swiggy_Restaurants_Analytics/CustomerSegment |

### Team Members

| Role | Name | GitHub Username |
|---|---|---|
| Statistical & Business Analysis Lead | Shreyash Golhani | `Shreyashgol` |
| Data Engineering Lead | Shivam Dixit | _To be added_ |
| EDA & Visualization Lead | Kavya Mukhija | _To be added_ |
| KPI Building Lead | Saksham Sontakke | _To be added_ |
| Tableau Dashboard Lead | Shashwant Sinha | _To be added_ |
| Report & PPT Lead | Yash | _To be added_ |

---

## Business Problem

India's online food delivery market exceeded ₹500 billion in 2024, with Swiggy serving 500+ cities. Restaurant owners, category managers, and city-level operations heads need data-driven insights to optimise menus, pricing, and service quality. This project analyses 91,788 clean order records spanning 898 restaurants across 28 Indian cities to surface actionable intelligence for platform-level decision-making.

**Core Business Question**

> Which cities, categories, and price segments drive the most orders and highest ratings on Swiggy — and what patterns in time and location reveal unmet demand?

**Decision Supported**

> Enable business stakeholders to identify top-performing restaurants, optimise pricing tiers, and uncover temporal demand patterns to drive revenue growth and operational efficiency.

---

## Dataset

| Attribute | Details |
|---|---|
| **Source Name** | Kaggle |
| **File Name** | swiggy_data_raw.csv |
| **Direct Access Link** | [Kaggle Dataset](https://www.kaggle.com/datasets/nikhilmaurya1324/swiggy-restaurant-data-india) |
| **Raw Row Count** | 1,97,430 rows |
| **Clean Row Count** | 91,788 rows |
| **Column Count** | 10 columns |
| **Time Period Covered** | Jan 2025 – Aug 2025 |
| **Format** | CSV |

**Key Columns Used**

| Column Name | Description | Role in Analysis |
|---|---|---|
| `state` / `city` / `location` | Geographic identifiers | City-level segmentation and filtering |
| `price_inr` → `price_bucket` | Dish price in INR, bucketed into tiers | KPI computation, pricing analysis, scatter plot |
| `rating` / `rating_count` | Customer satisfaction score and volume | Avg Rating KPI, ANOVA, Spearman correlation |
| `category` / `dish_name` | Food category and dish identifier | Category-level EDA, top cuisine analysis |
| `order_date` → `month`, `day_of_week` | Order timestamp, decomposed | Temporal trend analysis, peak day detection |
| `restaurant_name` | Restaurant identifier | Total restaurants KPI, restaurant-level ranking |

For full column definitions, see [`docs/data_dictionary.md`](docs/data_dictionary.md).

---

## KPI Framework

| KPI | Definition | Formula / Computation |
|---|---|---|
| Total Orders | Overall platform activity and dataset coverage | `COUNT(dish_name)` → `03_eda.ipynb` |
| Total Revenue | Cumulative monetary value of all listed dishes | `SUM(price_inr)` → `03_eda.ipynb` |
| Avg Price (INR) | Benchmarks pricing strategy across cities and categories | `AVG(price_inr)` → `04_statistical_analysis.ipynb` |
| Avg Rating | Tracks customer satisfaction across all restaurants | `AVG(rating)` → `04_statistical_analysis.ipynb` |
| Total Restaurants | Scope of restaurant network across 28 cities | `COUNTD(restaurant_name)` → `03_eda.ipynb` |
| Peak Day | Day of week with highest order volume | `MAX(COUNT by day_of_week)` → `05_final_load_prep.ipynb` |

**KPI Summary Values**

| KPI | Value |
|---|---|
| Total Orders | 91,788 |
| Total Revenue | ₹2.30 Cr |
| Avg Price (INR) | ₹250.24 |
| Avg Rating | 4.31 / 5.0 |
| Total Restaurants | 898 |
| Peak Day | Saturday (13,538 orders) |

---

## Tableau Dashboard

| Item | Details |
|---|---|
| **Dashboard URL** | _To be updated after Tableau Public publishing_ |
| **D1 — Overview Analytics** | Executive KPI summary: Orders, Revenue, Rating, Avg Price · Top 5 Cities by Orders (Bar) · Orders by Price Bucket (Pie) |
| **D2 — Restaurants & Price Analytics** | Pricing strategy view: Price vs Rating Scatter · Segment Info Cards · Restaurants Table |
| **D3 — Temporal Patterns & Customer Segments** | Time-based view: Day of Week trend · Monthly trend · Top Categories · Segment Strategy Cards |
| **Common Slicers (all dashboards)** | State · City · Category · Price Bucket · Order Date Range |
| **Dashboard Dimensions** | Fixed 1200×800 · Swiggy Brand Theme |

Store dashboard screenshots in [`tableau/screenshots/`](tableau/screenshots/) and document the public links in [`tableau/dashboard_links.md`](tableau/dashboard_links.md).

---

## Key Insights

1. **Bengaluru Dominates Order Volume** — Bengaluru accounts for 10,385 orders — 1.9× more than Mumbai (5,459), making it the single largest market on the platform.
2. **Mid-Range Pricing Wins the Market** — 59.1% of all dishes are priced ₹150–₹400. Only 11.6% fall in the Premium tier (>₹400), indicating strong price sensitivity among Swiggy users.
3. **Customer Satisfaction is Consistently High** — The average rating across 898 restaurants is 4.31/5.0, with a right-skewed distribution, suggesting most restaurants maintain strong quality standards.
4. **Weekend Demand Peaks on Saturdays** — Saturday drives the highest order volume (13,538 orders), followed by Thursday and Sunday, revealing a clear mid-week and weekend demand surge.
5. **Orders are Stable Across Jan–Aug 2025** — Monthly orders remain consistently between 10,876–11,882, with a slight uptick in Aug 2025, indicating steady platform growth with no seasonal crash.
6. **40% of Raw Data Flagged as Unreliable** — 75,133 rows had Rating Count = 0 and 9,871 rows had missing values — nearly 43% of raw data was filtered before analysis, highlighting significant data quality gaps.
7. **City Location Significantly Affects Ratings** — ANOVA test (F = 62.97, p < 0.0001) confirms city location has a statistically significant effect on restaurant ratings. Bengaluru and Chennai restaurants consistently outperform other cities.
8. **Food Category Influences Customer Satisfaction** — ANOVA test (F = 3.12, p < 0.0001) confirms that food category influences ratings — menu specialisation drives better customer experience.
9. **Price Does NOT Guarantee Higher Ratings** — Spearman correlation (ρ = 0.029, p < 0.0001) shows price and rating are statistically linked but practically unrelated — quality perception is independent of price on Swiggy.
10. **Monday is the Lowest Demand Day** — Monday records the lowest order volume, presenting an opportunity for targeted weekday promotions to reduce operational idle time.

---

## Recommendations

| # | Insight | Recommendation | Expected Impact |
|---|---|---|---|
| R1 | Bengaluru generates 1.9× more orders than any other city | Launch city-specific restaurant partnerships and exclusive Bengaluru deals to deepen market leadership | Estimated 10–15% revenue uplift from top market |
| R2 | 59.1% of orders are Mid-range (₹150–₹400); Premium only 11.6% | Introduce 'Premium Upgrade' nudges at checkout and curate a Premium restaurant collection to shift 5% of Mid-range users to Premium | ~₹11.5L incremental revenue from tier migration |
| R3 | Price and Rating are statistically unrelated (ρ = 0.029) | Market budget restaurants with high ratings more aggressively — value-for-money positioning drives orders independent of price | Higher conversion among price-sensitive users |
| R4 | Saturday & Thursday drive peak demand; Monday is lowest | Launch weekday promotions (Monday–Tuesday discounts) and scale delivery capacity on Saturdays to reduce drop-offs during peak hours | 15–20% reduction in order cancellations on peak days |
| R5 | 43% of raw data had quality issues (nulls + zero ratings) | Implement mandatory restaurant data completion checks before listing — enforce minimum rating count thresholds for visibility | Cleaner data → more reliable recommendations |

---

## Repository Structure

```text
SectionD_G4_swiggy/
|
|-- README.md
|
|-- data/
|   |-- raw/                         # Original dataset (never edited) — swiggy_data_raw.csv
|   `-- processed/                   # Cleaned output from ETL pipeline — 91,788 rows
|
|-- notebooks/
|   |-- 01_extraction.ipynb          # Load & profile raw CSV — shape, nulls, dtypes
|   |-- 02_cleaning.ipynb            # Drop nulls, duplicates, zero-rated rows, IQR outlier flag
|   |-- 03_eda.ipynb                 # EDA — city, category, price, temporal analysis
|   |-- 04_statistical_analysis.ipynb # ANOVA (city, category) + Spearman (price vs rating)
|   `-- 05_final_load_prep.ipynb     # Final dataset prep, KPI computation, export
|
|-- scripts/
|   `-- etl_pipeline.py              # Standalone ETL script
|
|-- tableau/
|   |-- screenshots/                 # Dashboard screenshots
|   `-- dashboard_links.md           # Tableau Public URL
|
|-- reports/
|   |-- README.md
|   |-- project_report_template.md
|   `-- presentation_outline.md
|
|-- docs/
|   `-- data_dictionary.md
|
|-- DVA-oriented-Resume/
`-- DVA-focused-Portfolio/
```

---

## Analytical Pipeline

The project follows a structured 7-step workflow:

1. **Define** — Food Tech sector selected, problem statement scoped around city/category/price demand patterns, mentor approval obtained.
2. **Extract** — Raw Swiggy dataset (1,97,430 rows × 10 columns) sourced from Kaggle and committed to `data/raw/`; data dictionary drafted.
3. **Clean and Transform** — ETL pipeline in `notebooks/02_cleaning.ipynb`: dropped 9,871 nulls, removed 14 duplicates, filtered 75,133 zero-rated rows, applied IQR outlier flagging (4,180 rows > ₹577).
4. **Analyze** — EDA and statistical analysis performed in notebooks `03` and `04` using pandas, matplotlib, seaborn, and scipy.
5. **Visualize** — 3 interactive Tableau dashboards built and published on Tableau Public (fixed 1200×800, Swiggy brand theme).
6. **Recommend** — 5 data-backed business recommendations delivered with estimated impact values.
7. **Report** — Final project report and presentation deck completed and exported to PDF in `reports/`.

---

## Advanced Statistical Analysis

All statistical testing performed in `04_statistical_analysis.ipynb` using `scipy` library.

| Test | Question | Result | Interpretation |
|---|---|---|---|
| ANOVA (`f_oneway`) | Does Rating differ significantly across Cities? | F = 62.97, p < 0.0001 ✓ Significant | City location has a strong effect on ratings. Bengaluru and Chennai consistently outperform. |
| ANOVA (`f_oneway`) | Does Rating differ significantly across Categories? | F = 3.12, p < 0.0001 ✓ Significant | Food category influences satisfaction — menu specialisation drives better experience. |
| Spearman (`spearmanr`) | Is there a significant correlation between Price & Rating? | ρ = 0.029, p < 0.0001 ✓ Significant but Weak | Price and Rating are statistically linked but practically unrelated — higher price does NOT guarantee higher ratings. |

---

## Tech Stack

| Tool | Status | Purpose |
|---|---|---|
| Python + Jupyter Notebooks | Mandatory | ETL, cleaning, EDA, statistical analysis, KPI computation |
| Google Colab | Supported | Cloud notebook execution environment |
| Tableau Public | Mandatory | Dashboard design, publishing, and sharing |
| GitHub | Mandatory | Version control, collaboration, contribution audit |
| scipy | Used | ANOVA and Spearman correlation testing |

**Python Libraries Used:** `pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy`

---

## Limitations

- Dataset is synthetic — findings may not reflect real Swiggy platform behaviour.
- 43% of raw data dropped — analysis based on 91,788 of 1,97,430 original rows.
- No customer-level data — cannot analyse repeat orders or churn behaviour.
- No delivery time or complaint data — service quality analysis is incomplete.
- Order date range limited to Jan–Aug 2025 — no seasonal trend beyond 8 months.

---

## Next Steps

1. Build a predictive model for restaurant rating using price, category, and city features (sklearn).
2. Integrate real-time Swiggy API data for live dashboard updates in Tableau.
3. Extend dataset to full year (Jan–Dec) for complete seasonal trend analysis.
4. Add customer segmentation (RFM model) once order-level customer data is available.
5. Deploy ETL pipeline as a scheduled job (Apache Airflow) for automated weekly refresh.

---

