# Module 11 Assignment: Data Visualization with Matplotlib
# SunCoast Retail Visual Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ---------- HELPER FUNCTION ----------
def ensure_data():
    global sales_df, customer_df

    import pandas as pd
    import numpy as np

    if 'sales_df' in globals() and 'customer_df' in globals():
        return

    np.random.seed(42)

    quarters = pd.date_range(start='2022-01-01', periods=8, freq='Q')
    quarter_labels = ['Q1 2022','Q2 2022','Q3 2022','Q4 2022',
                      'Q1 2023','Q2 2023','Q3 2023','Q4 2023']

    locations = ['Tampa','Miami','Orlando','Jacksonville']
    categories = ['Electronics','Clothing','Home Goods','Sporting Goods','Beauty']

    quarterly_data = []

    for quarter_idx, quarter in enumerate(quarters):
        for location in locations:
            for category in categories:
                base_sales = np.random.normal(100000, 20000)

                seasonal = 1.3 if quarter.quarter == 4 else 0.8 if quarter.quarter == 1 else 1.0
                loc_factor = {'Tampa':1.0,'Miami':1.2,'Orlando':0.9,'Jacksonville':0.8}[location]
                cat_factor = {'Electronics':1.5,'Clothing':1.0,'Home Goods':0.8,'Sporting Goods':0.7,'Beauty':0.9}[category]
                growth = (1 + 0.05/4) ** quarter_idx

                sales = base_sales * seasonal * loc_factor * cat_factor * growth
                sales *= np.random.normal(1.0, 0.1)

                ad_spend = (sales ** 0.7) * 0.05 * np.random.normal(1.0, 0.2)

                quarterly_data.append({
                    'Quarter': quarter,
                    'QuarterLabel': quarter_labels[quarter_idx],
                    'Location': location,
                    'Category': category,
                    'Sales': round(sales, 2),
                    'AdSpend': round(ad_spend, 2),
                    'Year': quarter.year
                })

    sales_df = pd.DataFrame(quarterly_data)
    sales_df['Quarter_Num'] = sales_df['Quarter'].dt.quarter
    sales_df['SalesPerDollarSpent'] = sales_df['Sales'] / sales_df['AdSpend']

    customer_df = pd.DataFrame({
        'Age': np.random.randint(18, 80, 500),
        'Location': np.random.choice(locations, 500),
        'PurchaseAmount': np.random.gamma(5, 20, 500),
        'PriceTier': np.random.choice(['Budget','Mid-range','Premium'], 500)
    })


# ---------- TODO 1 ----------
def plot_quarterly_sales_trend():
    ensure_data()
    total = sales_df.groupby('QuarterLabel')['Sales'].sum()

    fig, ax = plt.subplots()
    ax.plot(total.index, total.values, marker='o')
    ax.set_title("Quarterly Sales Trend")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Sales")
    ax.grid()

    return fig


def plot_location_sales_comparison():
    ensure_data()
    data = sales_df.groupby(['QuarterLabel','Location'])['Sales'].sum().unstack()

    fig, ax = plt.subplots()
    for loc in data.columns:
        ax.plot(data.index, data[loc], marker='o', label=loc)

    ax.legend()
    ax.set_title("Sales by Location")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Sales")
    ax.grid()

    return fig


# ---------- TODO 2 ----------
def plot_category_performance_by_location():
    ensure_data()
    latest = sales_df['Quarter'].max()
    df = sales_df[sales_df['Quarter'] == latest]

    pivot = df.pivot_table(index='Category', columns='Location', values='Sales', aggfunc='sum')

    fig, ax = plt.subplots()
    pivot.plot(kind='bar', ax=ax)
    ax.set_title("Category Performance by Location")

    return fig


def plot_sales_composition_by_location():
    ensure_data()
    data = sales_df.groupby(['Location','Category'])['Sales'].sum().unstack()
    pct = data.div(data.sum(axis=1), axis=0)

    fig, ax = plt.subplots()
    pct.plot(kind='bar', stacked=True, ax=ax)
    ax.set_title("Sales Composition by Location")

    return fig


# ---------- TODO 3 ----------
def plot_ad_spend_vs_sales():
    ensure_data()

    fig, ax = plt.subplots()
    x = sales_df['AdSpend']
    y = sales_df['Sales']

    ax.scatter(x, y)

    m, b = np.polyfit(x, y, 1)
    ax.plot(x, m*x + b)

    # ✅ FIXED LABELS
    ax.set_xlabel("Ad Spend")
    ax.set_ylabel("Sales")

    ax.set_title("Ad Spend vs Sales")

    return fig


def plot_ad_efficiency_over_time():
    ensure_data()
    data = sales_df.groupby('QuarterLabel')['SalesPerDollarSpent'].mean()

    fig, ax = plt.subplots()
    ax.plot(data.index, data.values, marker='o')
    ax.set_title("Ad Efficiency Over Time")

    return fig


# ---------- TODO 4 ----------
def plot_customer_age_distribution():
    ensure_data()

    fig, axs = plt.subplots(2, 2)
    axs = axs.flatten()

    for i, loc in enumerate(customer_df['Location'].unique()):
        ages = customer_df[customer_df['Location'] == loc]['Age']
        axs[i].hist(ages, bins=20)
        axs[i].axvline(ages.mean())
        axs[i].axvline(ages.median())
        axs[i].set_title(loc)

    return fig


def plot_purchase_by_age_group():
    ensure_data()

    bins = [18,30,45,60,80]
    labels = ['18-30','31-45','46-60','61+']
    customer_df['AgeGroup'] = pd.cut(customer_df['Age'], bins=bins, labels=labels)

    data = [customer_df[customer_df['AgeGroup']==g]['PurchaseAmount'] for g in labels]

    fig, ax = plt.subplots()
    ax.boxplot(data, labels=labels)
    ax.set_title("Purchase by Age Group")

    return fig


# ---------- TODO 5 ----------
def plot_purchase_amount_distribution():
    ensure_data()

    fig, ax = plt.subplots()
    ax.hist(customer_df['PurchaseAmount'], bins=30)
    ax.set_title("Purchase Distribution")

    return fig


def plot_sales_by_price_tier():
    ensure_data()

    data = customer_df.groupby('PriceTier')['PurchaseAmount'].sum()
    explode = [0.1 if v == data.max() else 0 for v in data]

    fig, ax = plt.subplots()
    ax.pie(data, labels=data.index, autopct='%1.1f%%', explode=explode)
    ax.set_title("Price Tier Breakdown")

    return fig


# ---------- TODO 6 ----------
def plot_category_market_share():
    ensure_data()

    data = sales_df.groupby('Category')['Sales'].sum()
    explode = [0.1 if v == data.max() else 0 for v in data]

    fig, ax = plt.subplots()
    ax.pie(data, labels=data.index, autopct='%1.1f%%', explode=explode)

    return fig


def plot_location_sales_distribution():
    ensure_data()

    data = sales_df.groupby('Location')['Sales'].sum()

    fig, ax = plt.subplots()
    ax.pie(data, labels=data.index, autopct='%1.1f%%')

    return fig


# ---------- TODO 7 ----------
def create_business_dashboard():
    ensure_data()

    fig, axs = plt.subplots(2,2, figsize=(10,8))

    total = sales_df.groupby('QuarterLabel')['Sales'].sum()
    axs[0,0].plot(total.index, total.values)
    axs[0,0].set_title("Sales Trend")

    loc = sales_df.groupby(['QuarterLabel','Location'])['Sales'].sum().unstack()
    loc.plot(ax=axs[0,1])
    axs[0,1].set_title("Location Comparison")

    axs[1,0].scatter(sales_df['AdSpend'], sales_df['Sales'])
    axs[1,0].set_title("Ad vs Sales")

    cat = sales_df.groupby('Category')['Sales'].sum()
    axs[1,1].pie(cat, labels=cat.index, autopct='%1.1f%%')

    fig.suptitle("Business Dashboard")

    return fig


# ---------- MAIN ----------
def main():
    fig1 = plot_quarterly_sales_trend()
    fig2 = plot_location_sales_comparison()
    fig3 = plot_category_performance_by_location()
    fig4 = plot_sales_composition_by_location()
    fig5 = plot_ad_spend_vs_sales()
    fig6 = plot_ad_efficiency_over_time()
    fig7 = plot_customer_age_distribution()
    fig8 = plot_purchase_by_age_group()
    fig9 = plot_purchase_amount_distribution()
    fig10 = plot_sales_by_price_tier()
    fig11 = plot_category_market_share()
    fig12 = plot_location_sales_distribution()
    fig13 = create_business_dashboard()

    print("\nKEY BUSINESS INSIGHTS:")
    print("""
    - Sales increase over time, with strong Q4 spikes.
    - Miami leads in sales performance.
    - Electronics dominates category sales.
    - Advertising positively impacts sales.
    - Mid-range pricing drives most revenue.
    """)

    plt.show()


if __name__ == "__main__":
    main()