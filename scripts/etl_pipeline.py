"""
ETL Pipeline — Swiggy Dataset
Run: python scripts/etl_pipeline.py
"""

import matplotlib
matplotlib.use('Agg')

from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy import stats


# ── Paths ────────────────────────────────────────────────────────────────────

PROJECT_ROOT   = Path(__file__).resolve().parent.parent
RAW_PATH       = PROJECT_ROOT / 'data/raw/swiggy_data_raw.csv'
CLEANED_PATH   = PROJECT_ROOT / 'data/processed/swiggy_cleaned.csv'
FINAL_PATH     = PROJECT_ROOT / 'data/processed/swiggy_final_cleaned.csv'
FIGURES_PATH   = PROJECT_ROOT / 'reports/figures'
STATS_PATH     = PROJECT_ROOT / 'reports/stats'

FIGURES_PATH.mkdir(parents=True, exist_ok=True)
STATS_PATH.mkdir(parents=True, exist_ok=True)
(PROJECT_ROOT / 'data/processed').mkdir(parents=True, exist_ok=True)

ALPHA    = 0.05
FIG_SIZE = (12, 5)
sns.set_theme(style='whitegrid')


# ── Logger ───────────────────────────────────────────────────────────────────

def log(message: str) -> None:
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{timestamp}] {message}')


# ── Step 1 — Extraction ──────────────────────────────────────────────────────

def step_extract() -> pd.DataFrame:
    df = pd.read_csv(RAW_PATH, parse_dates=['Order Date'])
    log(f'✓ Step 1 — Extraction complete   ({len(df):,} rows loaded)')
    return df


# ── Step 2 — Cleaning ────────────────────────────────────────────────────────

def step_clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna()
    df = df.drop_duplicates()
    df = df[df['Rating Count'] != 0]

    Q1  = df['Price (INR)'].quantile(0.25)
    Q3  = df['Price (INR)'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df['is_price_outlier'] = ~df['Price (INR)'].between(lower_bound, upper_bound)

    df.to_csv(CLEANED_PATH, index=False)
    log(f'✓ Step 2 — Cleaning complete     ({len(df):,} rows remaining)')
    return df


# ── Step 3 — EDA ─────────────────────────────────────────────────────────────

def step_eda(df: pd.DataFrame) -> None:
    df_clean_price = df[df['is_price_outlier'] == False]

    # 01 Price distribution
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    sns.histplot(df_clean_price['Price (INR)'], bins=50, kde=True, ax=ax)
    ax.set_title('Price Distribution (Excluding Outliers)')
    ax.set_xlabel('Price (INR)')
    ax.set_ylabel('Count')
    plt.tight_layout()
    fig.savefig(FIGURES_PATH / '01_price_distribution.png', dpi=150)
    plt.close(fig)

    # 02 Rating distribution
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    sns.histplot(df['Rating'], bins=30, kde=True, ax=ax)
    ax.set_title('Rating Distribution')
    ax.set_xlabel('Rating')
    ax.set_ylabel('Count')
    plt.tight_layout()
    fig.savefig(FIGURES_PATH / '02_rating_distribution.png', dpi=150)
    plt.close(fig)

    # 03 Rating Count distribution
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    sns.histplot(df['Rating Count'], bins=50, kde=True, ax=ax)
    ax.set_title('Rating Count Distribution')
    ax.set_xlabel('Rating Count')
    ax.set_ylabel('Count')
    plt.tight_layout()
    fig.savefig(FIGURES_PATH / '03_rating_count_distribution.png', dpi=150)
    plt.close(fig)

    # 04 Top 10 Categories
    top_categories = df['Category'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    sns.barplot(x=top_categories.values, y=top_categories.index, ax=ax)
    ax.set_title('Top 10 Categories by Order Count')
    ax.set_xlabel('Order Count')
    ax.set_ylabel('Category')
    plt.tight_layout()
    fig.savefig(FIGURES_PATH / '04_top10_categories.png', dpi=150)
    plt.close(fig)

    # 05 Top 10 Restaurants
    top_restaurants = df['Restaurant Name'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    sns.barplot(x=top_restaurants.values, y=top_restaurants.index, ax=ax)
    ax.set_title('Top 10 Restaurants by Order Count')
    ax.set_xlabel('Order Count')
    ax.set_ylabel('Restaurant Name')
    plt.tight_layout()
    fig.savefig(FIGURES_PATH / '05_top10_restaurants.png', dpi=150)
    plt.close(fig)

    # 06 Orders by State
    orders_by_state = df['State'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    sns.barplot(x=orders_by_state.values, y=orders_by_state.index, ax=ax)
    ax.set_title('Top 10 States by Order Count')
    ax.set_xlabel('Order Count')
    ax.set_ylabel('State')
    plt.tight_layout()
    fig.savefig(FIGURES_PATH / '06_orders_by_state.png', dpi=150)
    plt.close(fig)

    # 07 Orders by City
    orders_by_city = df['City'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    sns.barplot(x=orders_by_city.values, y=orders_by_city.index, ax=ax)
    ax.set_title('Top 10 Cities by Order Count')
    ax.set_xlabel('Order Count')
    ax.set_ylabel('City')
    plt.tight_layout()
    fig.savefig(FIGURES_PATH / '07_orders_by_city.png', dpi=150)
    plt.close(fig)

    # 08 Orders by Month
    df['Month'] = df['Order Date'].dt.to_period('M').astype(str)
    orders_by_month = df.groupby('Month').size().reset_index(name='Order Count')
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    sns.lineplot(data=orders_by_month, x='Month', y='Order Count', marker='o', ax=ax)
    ax.set_title('Orders Trend by Month')
    ax.set_xlabel('Month')
    ax.set_ylabel('Order Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    fig.savefig(FIGURES_PATH / '08_orders_by_month.png', dpi=150)
    plt.close(fig)

    # 09 Orders by Day of Week
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df['Day of Week'] = pd.Categorical(df['Order Date'].dt.day_name(), categories=day_order, ordered=True)
    orders_by_day = df.groupby('Day of Week', observed=True).size().reset_index(name='Order Count')
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    sns.barplot(data=orders_by_day, x='Day of Week', y='Order Count', ax=ax)
    ax.set_title('Orders by Day of Week')
    ax.set_xlabel('Day of Week')
    ax.set_ylabel('Order Count')
    plt.tight_layout()
    fig.savefig(FIGURES_PATH / '09_orders_by_dayofweek.png', dpi=150)
    plt.close(fig)

    # 10 Correlation Heatmap
    corr_cols   = ['Price (INR)', 'Rating', 'Rating Count']
    corr_matrix = df[corr_cols].corr()
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', ax=ax)
    ax.set_title('Correlation Heatmap — Price, Rating, Rating Count')
    plt.tight_layout()
    fig.savefig(FIGURES_PATH / '10_correlation_heatmap.png', dpi=150)
    plt.close(fig)

    log('✓ Step 3 — EDA complete          (10 plots saved to reports/figures/)')


# ── Step 4 — Statistical Analysis ────────────────────────────────────────────

def step_stats(df: pd.DataFrame) -> None:
    # Grouped stats by City
    grouped_city = (
        df.groupby('City')[['Price (INR)', 'Rating', 'Rating Count']]
        .agg(['mean', 'median', 'std', 'min', 'max'])
        .round(2)
    )
    grouped_city.columns = ['_'.join(col) for col in grouped_city.columns]
    grouped_city.reset_index().to_csv(STATS_PATH / 'grouped_stats_by_city.csv', index=False)

    # Grouped stats by Category
    grouped_category = (
        df.groupby('Category')[['Price (INR)', 'Rating', 'Rating Count']]
        .agg(['mean', 'median', 'std', 'min', 'max'])
        .round(2)
    )
    grouped_category.columns = ['_'.join(col) for col in grouped_category.columns]
    grouped_category.reset_index().to_csv(STATS_PATH / 'grouped_stats_by_category.csv', index=False)

    # Avg Price by Category
    (
        df.groupby('Category')['Price (INR)']
        .mean().round(2).reset_index()
        .rename(columns={'Price (INR)': 'Avg Price (INR)'})
        .sort_values('Avg Price (INR)', ascending=False)
        .to_csv(STATS_PATH / 'avg_price_by_category.csv', index=False)
    )

    # Avg Price by City
    (
        df.groupby('City')['Price (INR)']
        .mean().round(2).reset_index()
        .rename(columns={'Price (INR)': 'Avg Price (INR)'})
        .sort_values('Avg Price (INR)', ascending=False)
        .to_csv(STATS_PATH / 'avg_price_by_city.csv', index=False)
    )

    # ANOVA — Rating by City
    city_groups     = [g['Rating'].dropna().values for _, g in df.groupby('City')]
    f_city, p_city  = stats.f_oneway(*city_groups)

    # ANOVA — Rating by Category
    cat_groups      = [g['Rating'].dropna().values for _, g in df.groupby('Category')]
    f_cat, p_cat    = stats.f_oneway(*cat_groups)

    # Spearman — Price vs Rating
    corr_data           = df[['Price (INR)', 'Rating']].dropna()
    spearman_r, spearman_p = stats.spearmanr(corr_data['Price (INR)'], corr_data['Rating'])

    # Save hypothesis results
    pd.DataFrame([
        {'Test': 'ANOVA',                'Description': 'Rating by City',    'F-Statistic': round(f_city, 4),     'p-value': round(p_city, 4),     'Significant': p_city < ALPHA},
        {'Test': 'ANOVA',                'Description': 'Rating by Category', 'F-Statistic': round(f_cat, 4),      'p-value': round(p_cat, 4),      'Significant': p_cat < ALPHA},
        {'Test': 'Spearman Correlation', 'Description': 'Price vs Rating',    'F-Statistic': round(spearman_r, 4), 'p-value': round(spearman_p, 4), 'Significant': spearman_p < ALPHA},
    ]).to_csv(STATS_PATH / 'hypothesis_test_results.csv', index=False)

    log('✓ Step 4 — Stats complete        (5 CSVs saved to reports/stats/)')


# ── Step 5 — Final Load Prep ─────────────────────────────────────────────────

def step_final_load(df: pd.DataFrame) -> None:
    df['Month']        = df['Order Date'].dt.to_period('M').astype(str)
    df['Day of Week']  = df['Order Date'].dt.day_name()
    df['Price Bucket'] = pd.cut(
        df['Price (INR)'],
        bins=[0, 150, 400, float('inf')],
        labels=['Budget', 'Mid-range', 'Premium'],
        right=False
    )
    df = df.drop(columns=['is_price_outlier'])
    df = df.rename(columns={
        'State'           : 'state',
        'City'            : 'city',
        'Order Date'      : 'order_date',
        'Restaurant Name' : 'restaurant_name',
        'Location'        : 'location',
        'Category'        : 'category',
        'Dish Name'       : 'dish_name',
        'Price (INR)'     : 'price_inr',
        'Rating'          : 'rating',
        'Rating Count'    : 'rating_count',
        'Month'           : 'month',
        'Day of Week'     : 'day_of_week',
        'Price Bucket'    : 'price_bucket'
    })

    # Validation
    assert df.isnull().sum().sum() == 0, 'Nulls found in final dataset'
    assert df.duplicated().sum()   == 0, 'Duplicates found in final dataset'

    df.to_csv(FINAL_PATH, index=False)
    log(f'✓ Step 5 — Final Load complete   ({len(df):,} rows saved to data/processed/swiggy_final.csv)')


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    log('═══ Swiggy ETL Pipeline Started ═══')
    try:
        df = step_extract()
    except Exception as e:
        log(f'✗ Step 1 — Extraction failed: {e}')
        return

    try:
        df = step_clean(df)
    except Exception as e:
        log(f'✗ Step 2 — Cleaning failed: {e}')
        return

    try:
        step_eda(df)
    except Exception as e:
        log(f'✗ Step 3 — EDA failed: {e}')
        return

    try:
        step_stats(df)
    except Exception as e:
        log(f'✗ Step 4 — Statistical Analysis failed: {e}')
        return

    try:
        step_final_load(df)
    except Exception as e:
        log(f'✗ Step 5 — Final Load failed: {e}')
        return

    log('═══ Swiggy ETL Pipeline Completed Successfully ═══')


if __name__ == '__main__':
    main()
