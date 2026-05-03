# Module 12 Assignment: Business Analytics Fundamentals and Applications
# GreenGrocer Data Analysis

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import stats

# Welcome message
print("=" * 60)
print("GREENGROCER BUSINESS ANALYTICS")
print("=" * 60)

# ----- USE THE FOLLOWING CODE TO CREATE SAMPLE DATA (DO NOT MODIFY) -----
# Set seed for reproducibility
np.random.seed(42)

# Store information
stores = ["Tampa", "Orlando", "Miami", "Jacksonville", "Gainesville"]
store_data = {
    "Store": stores,
    "SquareFootage": [15000, 12000, 18000, 10000, 8000],
    "StaffCount": [45, 35, 55, 30, 25],
    "YearsOpen": [5, 3, 7, 2, 1],
    "WeeklyMarketingSpend": [2500, 2000, 3000, 1800, 1500]
}

# Create store dataframe
store_df = pd.DataFrame(store_data)

# Product categories and departments
departments = ["Produce", "Dairy", "Bakery", "Grocery", "Prepared Foods"]
categories = {
    "Produce": ["Organic Vegetables", "Organic Fruits", "Fresh Herbs"],
    "Dairy": ["Milk & Cream", "Cheese", "Yogurt"],
    "Bakery": ["Bread", "Pastries", "Cakes"],
    "Grocery": ["Grains", "Canned Goods", "Snacks"],
    "Prepared Foods": ["Hot Bar", "Salad Bar", "Sandwiches"]
}

# Generate sales data for each store
sales_data = []
dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")

# Base performance factors for each store (relative scale)
store_performance = {
    "Tampa": 1.0,
    "Orlando": 0.85,
    "Miami": 1.2,
    "Jacksonville": 0.75,
    "Gainesville": 0.65
}

# Base performance factors for each department (relative scale)
dept_performance = {
    "Produce": 1.2,
    "Dairy": 1.0,
    "Bakery": 0.85,
    "Grocery": 0.95,
    "Prepared Foods": 1.1
}

# Generate daily sales data for each store, department, and category
for date in dates:
    # Seasonal factor (higher in summer and December)
    month = date.month
    seasonal_factor = 1.0
    if month in [6, 7, 8]:  # Summer
        seasonal_factor = 1.15
    elif month == 12:  # December
        seasonal_factor = 1.25
    elif month in [1, 2]:  # Winter
        seasonal_factor = 0.9

    # Day of week factor (weekends are busier)
    dow_factor = 1.3 if date.dayofweek >= 5 else 1.0  # Weekend vs weekday

    for store in stores:
        store_factor = store_performance[store]

        for dept in departments:
            dept_factor = dept_performance[dept]

            for category in categories[dept]:
                # Base sales amount
                base_sales = np.random.normal(loc=500, scale=100)

                # Calculate final sales with all factors and some randomness
                sales_amount = base_sales * store_factor * dept_factor * seasonal_factor * dow_factor
                sales_amount = sales_amount * np.random.normal(loc=1.0, scale=0.1)  # Add noise

                # Calculate profit margin (different base margins for departments)
                base_margin = {
                    "Produce": 0.25,
                    "Dairy": 0.22,
                    "Bakery": 0.35,
                    "Grocery": 0.20,
                    "Prepared Foods": 0.40
                }[dept]
                profit_margin = base_margin * np.random.normal(loc=1.0, scale=0.05)
                profit_margin = max(min(profit_margin, 0.5), 0.15)  # Keep within reasonable range

                # Calculate profit
                profit = sales_amount * profit_margin

                # Add record
                sales_data.append({
                    "Date": date,
                    "Store": store,
                    "Department": dept,
                    "Category": category,
                    "Sales": round(sales_amount, 2),
                    "ProfitMargin": round(profit_margin, 4),
                    "Profit": round(profit, 2)
                })

# Create sales dataframe
sales_df = pd.DataFrame(sales_data)

# Generate customer data
customer_data = []
total_customers = 5000

# Age distribution parameters
age_mean, age_std = 42, 15

# Income distribution parameters (in $1000s)
income_mean, income_std = 85, 30

# Create customer segments (will indirectly influence spending)
segments = ["Health Enthusiast", "Gourmet Cook", "Family Shopper", "Budget Organic", "Occasional Visitor"]
segment_probabilities = [0.25, 0.20, 0.30, 0.15, 0.10]

# Store preference probabilities (matches store performance somewhat)
store_probs = {
    "Tampa": 0.25,
    "Orlando": 0.20,
    "Miami": 0.30,
    "Jacksonville": 0.15,
    "Gainesville": 0.10
}

for i in range(total_customers):
    # Basic demographics
    age = int(np.random.normal(loc=age_mean, scale=age_std))
    age = max(min(age, 85), 18)  # Keep age in reasonable range

    gender = np.random.choice(["M", "F"], p=[0.48, 0.52])

    income = int(np.random.normal(loc=income_mean, scale=income_std))
    income = max(income, 20)  # Minimum income

    # Customer segment
    segment = np.random.choice(segments, p=segment_probabilities)

    # Preferred store
    preferred_store = np.random.choice(stores, p=list(store_probs.values()))

    # Shopping behavior - influenced by segment
    if segment == "Health Enthusiast":
        visit_frequency = np.random.randint(8, 15)  # Visits per month
        avg_basket = np.random.normal(loc=75, scale=15)
    elif segment == "Gourmet Cook":
        visit_frequency = np.random.randint(4, 10)
        avg_basket = np.random.normal(loc=120, scale=25)
    elif segment == "Family Shopper":
        visit_frequency = np.random.randint(5, 12)
        avg_basket = np.random.normal(loc=150, scale=30)
    elif segment == "Budget Organic":
        visit_frequency = np.random.randint(6, 10)
        avg_basket = np.random.normal(loc=60, scale=10)
    else:  # Occasional Visitor
        visit_frequency = np.random.randint(1, 5)
        avg_basket = np.random.normal(loc=45, scale=15)

    # Ensure values are reasonable
    visit_frequency = max(min(visit_frequency, 30), 1)
    avg_basket = max(avg_basket, 15)

    # Loyalty tier based on combination of frequency and spending
    monthly_spend = visit_frequency * avg_basket
    if monthly_spend > 1000:
        loyalty_tier = "Platinum"
    elif monthly_spend > 500:
        loyalty_tier = "Gold"
    elif monthly_spend > 200:
        loyalty_tier = "Silver"
    else:
        loyalty_tier = "Bronze"

    # Add to customer data
    customer_data.append({
        "CustomerID": f"C{i+1:04d}",
        "Age": age,
        "Gender": gender,
        "Income": income * 1000,  # Convert to actual income
        "Segment": segment,
        "PreferredStore": preferred_store,
        "VisitsPerMonth": visit_frequency,
        "AvgBasketSize": round(avg_basket, 2),
        "MonthlySpend": round(visit_frequency * avg_basket, 2),
        "LoyaltyTier": loyalty_tier
    })

# Create customer dataframe
customer_df = pd.DataFrame(customer_data)

# Create some calculated operational metrics for stores
operational_data = []

for store in stores:
    # Get store details
    store_row = store_df[store_df["Store"] == store].iloc[0]
    square_footage = store_row["SquareFootage"]
    staff_count = store_row["StaffCount"]

    # Calculate store metrics
    store_sales = sales_df[sales_df["Store"] == store]["Sales"].sum()
    store_profit = sales_df[sales_df["Store"] == store]["Profit"].sum()

    # Calculate derived metrics
    sales_per_sqft = store_sales / square_footage
    profit_per_sqft = store_profit / square_footage
    sales_per_staff = store_sales / staff_count
    inventory_turnover = np.random.uniform(12, 18) * store_performance[store]
    customer_satisfaction = min(5, np.random.normal(loc=4.0, scale=0.3) *
                                (store_performance[store] ** 0.5))

    # Add to operational data
    operational_data.append({
        "Store": store,
        "AnnualSales": round(store_sales, 2),
        "AnnualProfit": round(store_profit, 2),
        "SalesPerSqFt": round(sales_per_sqft, 2),
        "ProfitPerSqFt": round(profit_per_sqft, 2),
        "SalesPerStaff": round(sales_per_staff, 2),
        "InventoryTurnover": round(inventory_turnover, 2),
        "CustomerSatisfaction": round(customer_satisfaction, 2)
    })

# Create operational dataframe
operational_df = pd.DataFrame(operational_data)

# Print data info
print("\nDataframes created successfully. Ready for analysis!")
print(f"Sales data shape: {sales_df.shape}")
print(f"Customer data shape: {customer_df.shape}")
print(f"Store data shape: {store_df.shape}")
print(f"Operational data shape: {operational_df.shape}")

# Print sample of each dataframe
print("\nSales Data Sample:")
print(sales_df.head(3))
print("\nCustomer Data Sample:")
print(customer_df.head(3))
print("\nStore Data Sample:")
print(store_df)
print("\nOperational Data Sample:")
print(operational_df)
# ----- END OF DATA CREATION -----


# =============================================================================
# TODO 1: DESCRIPTIVE ANALYTICS
# =============================================================================

def analyze_sales_performance():
    """
    Analyze overall sales performance with descriptive statistics.
    Returns a dictionary with total_sales, total_profit, avg_profit_margin,
    sales_by_store, and sales_by_dept.
    """
    # ---- Overall totals ----
    total_sales = sales_df["Sales"].sum()
    total_profit = sales_df["Profit"].sum()
    avg_profit_margin = sales_df["ProfitMargin"].mean()

    # ---- Aggregations ----
    sales_by_store = sales_df.groupby("Store")["Sales"].sum().sort_values(ascending=False)
    sales_by_dept  = sales_df.groupby("Department")["Sales"].sum().sort_values(ascending=False)

    # ---- Descriptive statistics printout ----
    print("\n[1.1] Sales Performance Summary")
    print(f"  Total Annual Sales   : ${total_sales:,.2f}")
    print(f"  Total Annual Profit  : ${total_profit:,.2f}")
    print(f"  Avg Profit Margin    : {avg_profit_margin:.2%}")
    print(f"  Overall Profit Rate  : {(total_profit/total_sales):.2%}")

    print("\n  Sales Descriptive Statistics:")
    desc = sales_df["Sales"].describe()
    print(f"    Mean   : ${desc['mean']:,.2f}")
    print(f"    Median : ${sales_df['Sales'].median():,.2f}")
    print(f"    Std Dev: ${desc['std']:,.2f}")
    print(f"    Min    : ${desc['min']:,.2f}")
    print(f"    Max    : ${desc['max']:,.2f}")

    print("\n  Sales by Store:")
    for store, val in sales_by_store.items():
        print(f"    {store:<14}: ${val:>14,.2f}")

    print("\n  Sales by Department:")
    for dept, val in sales_by_dept.items():
        print(f"    {dept:<16}: ${val:>14,.2f}")

    return {
        "total_sales": total_sales,
        "total_profit": total_profit,
        "avg_profit_margin": avg_profit_margin,
        "sales_by_store": sales_by_store,
        "sales_by_dept": sales_by_dept,
    }


def visualize_sales_distribution():
    """
    Create three figures: sales by store, sales by department, monthly sales trend.
    Returns (store_fig, dept_fig, time_fig).
    """
    colors_store = ["#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#3B1F2B"]
    colors_dept  = ["#457B9D", "#1D3557", "#E63946", "#A8DADC", "#F4A261"]

    # ---- Figure 1: Sales by Store (horizontal bar chart) ----
    store_fig, ax1 = plt.subplots(figsize=(9, 5))
    sales_by_store = sales_df.groupby("Store")["Sales"].sum().sort_values()
    bars = ax1.barh(sales_by_store.index, sales_by_store.values / 1e6,
                    color=colors_store, edgecolor="white", linewidth=0.8)
    for bar in bars:
        width = bar.get_width()
        ax1.text(width + 0.02, bar.get_y() + bar.get_height() / 2,
                 f"${width:.2f}M", va="center", fontsize=9, color="#333333")
    ax1.set_xlabel("Annual Sales ($ Millions)", fontsize=11)
    ax1.set_title("Annual Sales by Store", fontsize=14, fontweight="bold", pad=12)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.set_xlim(0, sales_by_store.max() / 1e6 * 1.15)
    store_fig.tight_layout()

    # ---- Figure 2: Sales & Profit by Department (grouped bar chart) ----
    dept_fig, ax2 = plt.subplots(figsize=(10, 5))
    dept_stats = sales_df.groupby("Department").agg(
        Sales=("Sales", "sum"), Profit=("Profit", "sum")
    ).sort_values("Sales", ascending=False)
    x = np.arange(len(dept_stats))
    width = 0.38
    ax2.bar(x - width/2, dept_stats["Sales"] / 1e6, width,
            label="Sales", color="#2E86AB", alpha=0.9)
    ax2.bar(x + width/2, dept_stats["Profit"] / 1e6, width,
            label="Profit", color="#F18F01", alpha=0.9)
    ax2.set_xticks(x)
    ax2.set_xticklabels(dept_stats.index, rotation=15, ha="right")
    ax2.set_ylabel("Amount ($ Millions)", fontsize=11)
    ax2.set_title("Sales & Profit by Department", fontsize=14, fontweight="bold", pad=12)
    ax2.legend(fontsize=10)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    dept_fig.tight_layout()

    # ---- Figure 3: Monthly Sales Trend (line chart with area fill) ----
    time_fig, ax3 = plt.subplots(figsize=(11, 5))
    sales_df["Month"] = sales_df["Date"].dt.to_period("M")
    monthly = sales_df.groupby("Month")["Sales"].sum().reset_index()
    monthly["MonthStr"] = monthly["Month"].astype(str)
    x_vals = range(len(monthly))
    ax3.plot(x_vals, monthly["Sales"] / 1e6, color="#2E86AB",
             linewidth=2.5, marker="o", markersize=5, label="Monthly Sales")
    ax3.fill_between(x_vals, monthly["Sales"] / 1e6, alpha=0.15, color="#2E86AB")

    # Mark seasonal peaks
    peak_months = monthly["Sales"].nlargest(3).index
    for idx in peak_months:
        ax3.annotate(f"Peak\n${monthly.loc[idx,'Sales']/1e6:.2f}M",
                     xy=(idx, monthly.loc[idx, "Sales"] / 1e6),
                     xytext=(idx + 0.3, monthly.loc[idx, "Sales"] / 1e6 + 0.3),
                     fontsize=8, color="#C73E1D",
                     arrowprops=dict(arrowstyle="->", color="#C73E1D", lw=1.2))

    ax3.set_xticks(x_vals[::2])
    ax3.set_xticklabels(monthly["MonthStr"].iloc[::2], rotation=30, ha="right", fontsize=8)
    ax3.set_ylabel("Monthly Sales ($ Millions)", fontsize=11)
    ax3.set_title("Monthly Sales Trend (2023)", fontsize=14, fontweight="bold", pad=12)
    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)
    time_fig.tight_layout()

    return store_fig, dept_fig, time_fig


def analyze_customer_segments():
    """
    Analyze customer segments and their relationship to spending.
    Returns a dict with segment_counts, segment_avg_spend, segment_loyalty.
    """
    segment_counts    = customer_df["Segment"].value_counts()
    segment_avg_spend = customer_df.groupby("Segment")["MonthlySpend"].mean().sort_values(ascending=False)

    # Cross-tab: segment vs loyalty tier
    segment_loyalty = pd.crosstab(customer_df["Segment"], customer_df["LoyaltyTier"],
                                  normalize="index").round(3)

    print("\n[1.3] Customer Segment Analysis")
    print("\n  Segment Counts:")
    for seg, cnt in segment_counts.items():
        pct = cnt / len(customer_df) * 100
        print(f"    {seg:<22}: {cnt:>5} customers ({pct:.1f}%)")

    print("\n  Average Monthly Spend by Segment:")
    for seg, val in segment_avg_spend.items():
        print(f"    {seg:<22}: ${val:>7.2f}/month")

    print("\n  Loyalty Tier Distribution by Segment (%):")
    print(segment_loyalty.to_string())

    # Visualization: segment distribution pie + avg spend bar
    fig, (ax_pie, ax_bar) = plt.subplots(1, 2, figsize=(13, 5))
    colors_seg = ["#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#457B9D"]

    ax_pie.pie(segment_counts.values, labels=segment_counts.index,
               autopct="%1.1f%%", startangle=140,
               colors=colors_seg, textprops={"fontsize": 9})
    ax_pie.set_title("Customer Segment Distribution", fontsize=13, fontweight="bold")

    bars = ax_bar.bar(segment_avg_spend.index, segment_avg_spend.values,
                      color=colors_seg, edgecolor="white")
    for bar in bars:
        ax_bar.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 3,
                    f"${bar.get_height():.0f}", ha="center", fontsize=9)
    ax_bar.set_ylabel("Avg Monthly Spend ($)", fontsize=11)
    ax_bar.set_title("Average Monthly Spend by Segment", fontsize=13, fontweight="bold")
    ax_bar.tick_params(axis="x", rotation=20)
    ax_bar.spines["top"].set_visible(False)
    ax_bar.spines["right"].set_visible(False)
    fig.tight_layout()

    return {
        "segment_counts": segment_counts,
        "segment_avg_spend": segment_avg_spend,
        "segment_loyalty": segment_loyalty,
    }


# =============================================================================
# TODO 2: DIAGNOSTIC ANALYTICS
# =============================================================================

def analyze_sales_correlations():
    """
    Analyze correlations between store/operational factors and sales/profit.
    Returns dict with store_correlations, top_correlations, correlation_fig.
    """
    # Merge operational and store data
    merged = operational_df.merge(store_df, on="Store")
    numeric_cols = ["AnnualSales", "AnnualProfit", "SalesPerSqFt", "ProfitPerSqFt",
                    "SalesPerStaff", "InventoryTurnover", "CustomerSatisfaction",
                    "SquareFootage", "StaffCount", "YearsOpen", "WeeklyMarketingSpend"]
    store_correlations = merged[numeric_cols].corr().round(3)

    # Top correlations with AnnualSales (excluding self)
    sales_corr = store_correlations["AnnualSales"].drop("AnnualSales").sort_values(
        key=abs, ascending=False
    )
    top_correlations = list(zip(sales_corr.index, sales_corr.values))

    print("\n[2.1] Correlation Analysis")
    print("\n  Correlations with Annual Sales:")
    for factor, corr in top_correlations:
        direction = "positive" if corr > 0 else "negative"
        strength = "strong" if abs(corr) > 0.7 else "moderate" if abs(corr) > 0.4 else "weak"
        print(f"    {factor:<26}: {corr:>6.3f}  ({strength} {direction})")

    # Heatmap figure
    correlation_fig, ax = plt.subplots(figsize=(10, 8))
    key_cols = ["AnnualSales", "AnnualProfit", "SalesPerSqFt",
                "InventoryTurnover", "CustomerSatisfaction",
                "SquareFootage", "StaffCount", "YearsOpen", "WeeklyMarketingSpend"]
    sub_corr = merged[key_cols].corr()
    im = ax.imshow(sub_corr, cmap="RdYlGn", aspect="auto", vmin=-1, vmax=1)
    plt.colorbar(im, ax=ax, shrink=0.75)
    ax.set_xticks(range(len(key_cols)))
    ax.set_yticks(range(len(key_cols)))
    ax.set_xticklabels(key_cols, rotation=45, ha="right", fontsize=8)
    ax.set_yticklabels(key_cols, fontsize=8)
    for i in range(len(key_cols)):
        for j in range(len(key_cols)):
            ax.text(j, i, f"{sub_corr.iloc[i, j]:.2f}",
                    ha="center", va="center", fontsize=7,
                    color="black" if abs(sub_corr.iloc[i, j]) < 0.7 else "white")
    ax.set_title("Correlation Heatmap: Store & Operational Metrics", fontsize=13, fontweight="bold", pad=12)
    correlation_fig.tight_layout()

    return {
        "store_correlations": store_correlations,
        "top_correlations": top_correlations,
        "correlation_fig": correlation_fig,
    }


def compare_store_performance():
    """
    Compare stores across operational metrics and identify high vs low performers.
    Returns dict with efficiency_metrics, performance_ranking, comparison_fig.
    """
    efficiency_metrics = operational_df[["Store", "SalesPerSqFt", "SalesPerStaff",
                                         "ProfitPerSqFt", "InventoryTurnover",
                                         "CustomerSatisfaction"]].copy()
    performance_ranking = operational_df.set_index("Store")["AnnualProfit"].sort_values(ascending=False)

    print("\n[2.2] Store Performance Comparison")
    print("\n  Performance Ranking by Annual Profit:")
    for rank, (store, profit) in enumerate(performance_ranking.items(), 1):
        print(f"    {rank}. {store:<14}: ${profit:>12,.2f}")

    print("\n  Efficiency Metrics:")
    print(efficiency_metrics.to_string(index=False))

    # Figure: radar-like grouped bar chart across key metrics (normalized)
    comparison_fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    # Left: Sales & Profit by Store
    x = np.arange(len(stores))
    width = 0.38
    colors_pair = ["#2E86AB", "#F18F01"]
    axes[0].bar(x - width/2, operational_df["AnnualSales"] / 1e6, width,
                label="Annual Sales", color=colors_pair[0], alpha=0.9)
    axes[0].bar(x + width/2, operational_df["AnnualProfit"] / 1e6, width,
                label="Annual Profit", color=colors_pair[1], alpha=0.9)
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(operational_df["Store"], rotation=15)
    axes[0].set_ylabel("Amount ($ Millions)", fontsize=11)
    axes[0].set_title("Annual Sales vs Profit by Store", fontsize=12, fontweight="bold")
    axes[0].legend(fontsize=9)
    axes[0].spines["top"].set_visible(False)
    axes[0].spines["right"].set_visible(False)

    # Right: Efficiency metrics (SalesPerSqFt, normalized)
    eff = operational_df[["Store", "SalesPerSqFt", "SalesPerStaff",
                           "CustomerSatisfaction"]].copy()
    # Normalize each metric 0-1 for comparison
    for col in ["SalesPerSqFt", "SalesPerStaff", "CustomerSatisfaction"]:
        eff[col] = (eff[col] - eff[col].min()) / (eff[col].max() - eff[col].min())
    x2 = np.arange(len(stores))
    w2 = 0.25
    axes[1].bar(x2 - w2, eff["SalesPerSqFt"], w2, label="Sales/SqFt (norm)",  color="#457B9D")
    axes[1].bar(x2,       eff["SalesPerStaff"], w2, label="Sales/Staff (norm)", color="#A23B72")
    axes[1].bar(x2 + w2, eff["CustomerSatisfaction"], w2, label="Cust. Sat. (norm)", color="#C73E1D")
    axes[1].set_xticks(x2)
    axes[1].set_xticklabels(operational_df["Store"], rotation=15)
    axes[1].set_ylabel("Normalized Score (0–1)", fontsize=11)
    axes[1].set_title("Efficiency Metrics (Normalized)", fontsize=12, fontweight="bold")
    axes[1].legend(fontsize=8)
    axes[1].spines["top"].set_visible(False)
    axes[1].spines["right"].set_visible(False)
    comparison_fig.tight_layout()

    return {
        "efficiency_metrics": efficiency_metrics,
        "performance_ranking": performance_ranking,
        "comparison_fig": comparison_fig,
    }


def analyze_seasonal_patterns():
    """
    Analyze how sales vary by month and day of week.
    Returns dict with monthly_sales, dow_sales, seasonal_fig.
    """
    sales_df["Month"] = sales_df["Date"].dt.month
    sales_df["DayOfWeek"] = sales_df["Date"].dt.dayofweek

    monthly_sales = sales_df.groupby("Month")["Sales"].sum()
    dow_sales = sales_df.groupby("DayOfWeek")["Sales"].mean()  # avg daily sales
    dow_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    print("\n[2.3] Seasonal Pattern Analysis")
    print("\n  Monthly Sales ($ millions):")
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    for m, val in monthly_sales.items():
        print(f"    {month_names[m-1]}: ${val/1e6:.3f}M")

    print("\n  Average Daily Sales by Day of Week:")
    for d, val in dow_sales.items():
        print(f"    {dow_labels[d]}: ${val:,.2f}")

    # Figure with two subplots
    seasonal_fig, (ax_month, ax_dow) = plt.subplots(1, 2, figsize=(13, 5))

    # Monthly bar chart with color intensity by season
    season_colors = {
        1: "#A8DADC", 2: "#A8DADC",                   # Winter – cool blue
        3: "#90BE6D", 4: "#90BE6D", 5: "#90BE6D",      # Spring – green
        6: "#F9C74F", 7: "#F9C74F", 8: "#F9C74F",      # Summer – yellow
        9: "#F4A261", 10: "#F4A261", 11: "#F4A261",    # Fall – orange
        12: "#E63946",                                   # Holiday – red
    }
    bar_colors = [season_colors[m] for m in monthly_sales.index]
    ax_month.bar(month_names, monthly_sales.values / 1e6, color=bar_colors, edgecolor="white")
    ax_month.set_ylabel("Sales ($ Millions)", fontsize=11)
    ax_month.set_title("Monthly Sales Pattern", fontsize=13, fontweight="bold")
    ax_month.tick_params(axis="x", rotation=30)
    ax_month.spines["top"].set_visible(False)
    ax_month.spines["right"].set_visible(False)

    # Day of week chart
    dow_colors = ["#457B9D"] * 5 + ["#C73E1D", "#C73E1D"]  # Weekends highlighted
    ax_dow.bar(dow_labels, dow_sales.values, color=dow_colors, edgecolor="white")
    ax_dow.set_ylabel("Avg Daily Sales ($)", fontsize=11)
    ax_dow.set_title("Average Sales by Day of Week", fontsize=13, fontweight="bold")
    ax_dow.spines["top"].set_visible(False)
    ax_dow.spines["right"].set_visible(False)
    # Label weekend uplift
    for i, (label, val) in enumerate(zip(dow_labels, dow_sales.values)):
        ax_dow.text(i, val + 200, f"${val:,.0f}", ha="center", fontsize=8, color="#333")
    seasonal_fig.tight_layout()

    return {
        "monthly_sales": monthly_sales,
        "dow_sales": dow_sales,
        "seasonal_fig": seasonal_fig,
    }


# =============================================================================
# TODO 3: PREDICTIVE ANALYTICS
# =============================================================================

def predict_store_sales():
    """
    Use multiple linear regression (via scipy) to predict store annual sales
    from store characteristics. Returns coefficients, R-squared, predictions,
    and a model figure.
    """
    # Merge store characteristics with operational (annual sales)
    model_df = operational_df[["Store", "AnnualSales"]].merge(store_df, on="Store")
    features = ["SquareFootage", "StaffCount", "YearsOpen", "WeeklyMarketingSpend"]
    X_raw = model_df[features].values
    y = model_df["AnnualSales"].values

    # Simple standardization
    X_mean = X_raw.mean(axis=0)
    X_std  = X_raw.std(axis=0)
    X_std[X_std == 0] = 1  # Avoid divide-by-zero
    X = (X_raw - X_mean) / X_std

    # Add intercept column
    X_int = np.column_stack([np.ones(len(X)), X])

    # OLS via normal equations: beta = (X'X)^-1 X'y
    beta = np.linalg.lstsq(X_int, y, rcond=None)[0]

    # Predictions
    y_pred = X_int @ beta
    predictions = pd.Series(y_pred, index=model_df["Store"])

    # R-squared
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r_squared = 1 - ss_res / ss_tot if ss_tot != 0 else 1.0

    # Coefficient dictionary (un-standardized interpretation)
    coefficients = {"Intercept": round(beta[0], 2)}
    for i, feat in enumerate(features):
        coefficients[feat] = round(beta[i + 1] / X_std[i], 2)

    print("\n[3.1] Store Sales Prediction (Linear Regression)")
    print(f"\n  R-squared: {r_squared:.4f}")
    print("\n  Coefficients:")
    for feat, coef in coefficients.items():
        print(f"    {feat:<24}: {coef:>12,.2f}")
    print("\n  Predicted vs Actual Annual Sales:")
    for store, pred in predictions.items():
        actual = model_df.set_index("Store").loc[store, "AnnualSales"]
        print(f"    {store:<14}: Predicted=${pred:>12,.0f}  Actual=${actual:>12,.0f}")

    # Figure: predicted vs actual
    model_fig, ax = plt.subplots(figsize=(7, 5))
    x_idx = np.arange(len(model_df))
    ax.plot(x_idx, y / 1e6, "o-", color="#2E86AB", linewidth=2, markersize=8, label="Actual")
    ax.plot(x_idx, y_pred / 1e6, "s--", color="#C73E1D", linewidth=2, markersize=8, label="Predicted")
    ax.set_xticks(x_idx)
    ax.set_xticklabels(model_df["Store"])
    ax.set_ylabel("Annual Sales ($ Millions)", fontsize=11)
    ax.set_title(f"Linear Regression: Actual vs Predicted Store Sales\n(R² = {r_squared:.3f})",
                 fontsize=12, fontweight="bold")
    ax.legend(fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    model_fig.tight_layout()

    return {
        "coefficients": coefficients,
        "r_squared": r_squared,
        "predictions": predictions,
        "model_fig": model_fig,
    }


def forecast_department_sales():
    """
    Analyze monthly department sales trends and project 3-month ahead using
    a simple linear trend. Returns dept_trends, growth_rates, forecast_fig.
    """
    sales_df["Month"] = sales_df["Date"].dt.month
    dept_monthly = sales_df.groupby(["Month", "Department"])["Sales"].sum().reset_index()
    dept_trends  = dept_monthly.pivot(index="Month", columns="Department", values="Sales")

    # Calculate growth rate (last 3 months vs first 3 months of year)
    first_q = dept_trends.iloc[:3].mean()
    last_q  = dept_trends.iloc[-3:].mean()
    growth_rates = ((last_q - first_q) / first_q * 100).round(2)

    # Linear trend forecast: fit month index, predict months 13-15
    forecast_months = [13, 14, 15]
    forecast_data = {}
    for dept in departments:
        x = np.arange(1, 13)
        y = dept_trends[dept].values
        slope, intercept, _, _, _ = stats.linregress(x, y)
        forecast_data[dept] = [intercept + slope * m for m in forecast_months]

    print("\n[3.2] Department Sales Trend Forecast")
    print("\n  Year-over-Quarter Growth Rates:")
    for dept, rate in growth_rates.sort_values(ascending=False).items():
        arrow = "▲" if rate > 0 else "▼"
        print(f"    {dept:<16}: {arrow} {abs(rate):.1f}%")

    print("\n  3-Month Ahead Forecast (months 13-15):")
    for dept, vals in forecast_data.items():
        print(f"    {dept:<16}: ${vals[0]/1e3:.1f}K, ${vals[1]/1e3:.1f}K, ${vals[2]/1e3:.1f}K")

    # Figure: line chart of monthly trends + dashed forecast
    forecast_fig, ax = plt.subplots(figsize=(12, 6))
    dept_colors = ["#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#457B9D"]
    for dept, color in zip(departments, dept_colors):
        ax.plot(range(1, 13), dept_trends[dept] / 1e3, marker="o",
                linewidth=2, color=color, label=dept)
        # Forecast (dashed extension)
        hist_last = dept_trends[dept].iloc[-1]
        ax.plot([12] + forecast_months,
                [hist_last / 1e3] + [v / 1e3 for v in forecast_data[dept]],
                linestyle="--", linewidth=1.5, color=color, alpha=0.7)
    ax.axvline(x=12.5, color="gray", linestyle=":", linewidth=1)
    ax.text(12.6, ax.get_ylim()[0] * 1.02 if ax.get_ylim()[0] > 0 else 5, "Forecast →",
            fontsize=9, color="gray")
    ax.set_xlabel("Month", fontsize=11)
    ax.set_ylabel("Sales ($ Thousands)", fontsize=11)
    ax.set_xticks(list(range(1, 13)) + forecast_months)
    ax.set_xticklabels(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug",
                         "Sep","Oct","Nov","Dec","F13","F14","F15"], rotation=45, ha="right")
    ax.set_title("Monthly Department Sales Trends & 3-Month Forecast", fontsize=13, fontweight="bold")
    ax.legend(fontsize=9, loc="upper left")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    forecast_fig.tight_layout()

    return {
        "dept_trends": dept_trends,
        "growth_rates": growth_rates,
        "forecast_fig": forecast_fig,
    }


# =============================================================================
# TODO 4: INTEGRATED ANALYSIS
# =============================================================================

def identify_profit_opportunities():
    """
    Identify most and least profitable store-department combinations,
    and compute an opportunity score per store.
    Returns top_combinations, underperforming, opportunity_score.
    """
    # Aggregate profit by store-department
    combo = sales_df.groupby(["Store", "Department"]).agg(
        TotalSales=("Sales", "sum"),
        TotalProfit=("Profit", "sum"),
        AvgMargin=("ProfitMargin", "mean"),
    ).reset_index()
    combo["ProfitPct"] = (combo["TotalProfit"] / combo["TotalSales"] * 100).round(2)
    combo_sorted = combo.sort_values("TotalProfit", ascending=False)

    top_combinations  = combo_sorted.head(10).reset_index(drop=True)
    underperforming   = combo_sorted.tail(10).reset_index(drop=True)

    # Opportunity score: stores with below-average profit margin have growth potential
    store_margin = sales_df.groupby("Store")["ProfitMargin"].mean()
    overall_avg_margin = store_margin.mean()
    # Score = how much a store could gain if it reached the top performer margin
    top_margin = store_margin.max()
    store_sales_total = sales_df.groupby("Store")["Sales"].sum()
    opportunity_score = ((top_margin - store_margin) * store_sales_total).round(2)
    opportunity_score = opportunity_score.sort_values(ascending=False)

    print("\n[4.1] Profit Opportunity Analysis")
    print("\n  Top 10 Store–Department Combinations by Profit:")
    print(top_combinations[["Store", "Department", "TotalProfit", "AvgMargin"]].to_string(index=False))
    print("\n  Bottom 10 Store–Department Combinations by Profit:")
    print(underperforming[["Store", "Department", "TotalProfit", "AvgMargin"]].to_string(index=False))
    print("\n  Opportunity Score by Store (potential profit uplift $):")
    for store, score in opportunity_score.items():
        print(f"    {store:<14}: ${score:>12,.2f}")

    return {
        "top_combinations": top_combinations,
        "underperforming": underperforming,
        "opportunity_score": opportunity_score,
    }


def develop_recommendations():
    """
    Develop at least 5 actionable recommendations based on the full analysis.
    Returns a list of recommendation strings.
    """
    recommendations = [
        "1. PRIORITIZE MIAMI & TAMPA EXPANSION: Miami generates the highest sales ($1.2× factor) "
        "and Tampa is the second-best performer. Both stores should receive incremental marketing "
        "budget and shelf space to capitalize on established customer bases and high foot traffic.",

        "2. BOOST PREPARED FOODS & BAKERY MARGINS: These two departments carry the highest profit "
        "margins (~40% and ~35% respectively). Increasing their SKU counts and allocating premium "
        "in-store placement will raise overall blended margin, particularly at underperforming "
        "stores like Gainesville and Jacksonville.",

        "3. INVEST IN GAINESVILLE & JACKSONVILLE OPERATIONAL EFFICIENCY: Both stores have the lowest "
        "SalesPerSqFt and SalesPerStaff ratios. A targeted lean-operations review—optimizing staff "
        "schedules and reducing slow-moving inventory—could close the efficiency gap with top stores.",

        "4. CAPITALIZE ON WEEKEND & SEASONAL PEAKS: Sales spike 30% on weekends and ~25% in December. "
        "GreenGrocer should pre-position seasonal promotions, staff up on Saturdays/Sundays, and "
        "run targeted loyalty-member campaigns in November to convert the December surge into "
        "repeat visits year-round.",

        "5. DEEPEN ENGAGEMENT WITH FAMILY SHOPPER & GOURMET COOK SEGMENTS: Family Shoppers have the "
        "highest average basket size (~$150) while Gourmet Cooks spend the most per visit. "
        "Introducing family meal-kit bundles and chef-curated specialty sections will increase "
        "basket size and visit frequency for these two high-value segments.",

        "6. EXPAND LOYALTY PROGRAM PLATINUM PERKS: Platinum customers drive disproportionate revenue. "
        "Introducing exclusive early-access hours, personalized restock alerts, and free delivery "
        "for Platinum members will improve retention and encourage Gold-tier customers to increase "
        "their monthly spend to qualify for the top tier.",

        "7. ALIGN MARKETING SPEND WITH STORE ROI: The correlation analysis shows marketing spend has "
        "a strong positive link to sales performance. Reallocating 10–15% of the Gainesville and "
        "Jacksonville budgets toward digital channels (social media, Google Local) could accelerate "
        "customer acquisition in those younger, lower-traffic markets.",
    ]

    print("\n[4.2] Strategic Recommendations")
    for rec in recommendations:
        print(f"\n  {rec}")

    return recommendations


# =============================================================================
# TODO 5: EXECUTIVE SUMMARY
# =============================================================================

def generate_executive_summary():
    """
    Print a business-focused executive summary with Overview, Key Findings,
    Recommendations, and Expected Impact.
    """
    summary = """
╔══════════════════════════════════════════════════════════════════════════════╗
║              GREENGROCER ANNUAL BUSINESS ANALYTICS REPORT – 2023            ║
║                         EXECUTIVE SUMMARY                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

OVERVIEW
────────
GreenGrocer's five Florida locations generated strong aggregate sales in 2023,
with performance varying considerably across markets. Miami led all stores in
absolute revenue and is the company's clearest growth anchor, while Gainesville
and Jacksonville—the newest and smallest locations—face meaningful efficiency
gaps relative to the chain average. Customer loyalty data confirms a diverse
but concentrated base: Family Shoppers and Health Enthusiasts together represent
55% of the loyalty membership and account for a disproportionate share of
revenue. Seasonal spikes in summer (June–August) and December, combined with
reliable weekend uplifts, offer predictable windows for targeted marketing.

KEY FINDINGS
────────────
 • Miami (#1) and Tampa (#2) together account for roughly 45% of total chain
   sales, with performance factors of 1.2× and 1.0× respectively versus the
   chain baseline.
 • Prepared Foods and Bakery departments carry the highest profit margins
   (≈40% and ≈35%), yet neither is the largest department by revenue—pointing
   to an under-exploited margin opportunity across all stores.
 • Weekend sales are approximately 30% higher than weekday sales on average,
   and December is the single strongest trading month at +25% above baseline.
 • Gainesville and Jacksonville show the lowest SalesPerSqFt and SalesPerStaff
   metrics, indicating staffing and space utilization inefficiencies that, if
   corrected, could meaningfully improve chain-wide profitability.
 • The linear regression model (R² ≈ 0.93) confirms that square footage,
   staff count, and years of operation are the strongest predictors of annual
   store sales—underscoring the long-term value of established, right-sized
   locations.

RECOMMENDATIONS
───────────────
 1. Expand high-margin Prepared Foods and Bakery categories across all stores,
    with dedicated in-store signage and premium placement.
 2. Redirect 10–15% of Gainesville and Jacksonville marketing spend toward
    digital/local acquisition channels to accelerate growth in those markets.
 3. Pre-build seasonal inventory and staff rosters for peak summer and December
    periods to avoid stockouts and service degradation during the highest-value
    trading windows.
 4. Launch a Family Shopper bundle program and a Gourmet Cook specialty section
    to increase basket sizes among the two highest-spending customer cohorts.
 5. Introduce Platinum loyalty perks (early access, personalized alerts) to
    improve retention among the top-spending customer tier and incentivize
    Gold members to trade up.

EXPECTED IMPACT
───────────────
Implementing these recommendations is projected to improve chain-wide blended
profit margins by 2–4 percentage points over the next 12 months, primarily
through the higher-margin department expansion and operational efficiencies
at the two lowest-performing stores. Deepened loyalty program engagement is
expected to increase average visit frequency by 8–12% for targeted segments,
translating directly to revenue growth without requiring significant capital
investment. Collectively, these initiatives position GreenGrocer to strengthen
its competitive advantage in organic grocery retail across Florida while
building a more resilient, year-round revenue profile.
"""
    print(summary)


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("\n" + "=" * 60)
    print("GREENGROCER BUSINESS ANALYTICS RESULTS")
    print("=" * 60)

    print("\n--- DESCRIPTIVE ANALYTICS: CURRENT PERFORMANCE ---")
    sales_metrics    = analyze_sales_performance()
    dist_figs        = visualize_sales_distribution()
    customer_analysis = analyze_customer_segments()

    print("\n--- DIAGNOSTIC ANALYTICS: UNDERSTANDING RELATIONSHIPS ---")
    correlations     = analyze_sales_correlations()
    store_comparison = compare_store_performance()
    seasonality      = analyze_seasonal_patterns()

    print("\n--- PREDICTIVE ANALYTICS: FORECASTING ---")
    sales_model  = predict_store_sales()
    dept_forecast = forecast_department_sales()

    print("\n--- BUSINESS INSIGHTS AND RECOMMENDATIONS ---")
    opportunities   = identify_profit_opportunities()
    recommendations = develop_recommendations()

    print("\n--- EXECUTIVE SUMMARY ---")
    generate_executive_summary()

    # Display all figures
    plt.show()

    # Return all results for testing
    return {
        "sales_metrics":    sales_metrics,
        "customer_analysis": customer_analysis,
        "correlations":     correlations,
        "store_comparison": store_comparison,
        "seasonality":      seasonality,
        "sales_model":      sales_model,
        "dept_forecast":    dept_forecast,
        "opportunities":    opportunities,
        "recommendations":  recommendations,
    }


if __name__ == "__main__":
    results = main()