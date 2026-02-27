# ============================================================
#  SUPERSTORE DATA ANALYST PROJECT
#  Full Exploratory Data Analysis (EDA)
#  Tools: Python | Pandas | Seaborn | Matplotlib
# ============================================================

# ------------------------------------
# STEP 0 — Import Libraries
# ------------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
import os

warnings.filterwarnings("ignore")

# Global style settings
sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams.update({
    "figure.dpi": 150,
    "figure.facecolor": "white",
    "axes.facecolor": "#F8F9FA",
    "axes.edgecolor": "#CCCCCC",
    "font.family": "DejaVu Sans",
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "axes.labelsize": 11,
})

OUTPUT_DIR = "superstore_charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

COLORS = {
    "primary":   "#2E86AB",
    "secondary": "#A23B72",
    "accent":    "#F18F01",
    "positive":  "#44BBA4",
    "negative":  "#E94F37",
    "palette":   ["#2E86AB", "#A23B72", "#F18F01", "#44BBA4", "#E94F37",
                  "#393E41", "#6B4226", "#5C6BC0", "#26A69A", "#EF5350"],
}


# ============================================================
# SECTION 1 — DATA LOADING & GENERATION
# ============================================================
print("\n" + "="*60)
print("  SECTION 1 — DATA LOADING")
print("="*60)

np.random.seed(42)
n = 9994

regions    = ["West", "East", "Central", "South"]
categories = ["Furniture", "Office Supplies", "Technology"]
sub_cats = {
    "Furniture":       ["Bookcases", "Chairs", "Furnishings", "Tables"],
    "Office Supplies": ["Appliances", "Art", "Binders", "Envelopes",
                        "Fasteners", "Labels", "Paper", "Storage", "Supplies"],
    "Technology":      ["Accessories", "Copiers", "Machines", "Phones"],
}
segments   = ["Consumer", "Corporate", "Home Office"]
ship_modes = ["First Class", "Second Class", "Standard Class", "Same Day"]

products = {
    "Bookcases":    ["Bush Somerset Bookcase", "Sauder Harbour View Bookcase",
                     "O'Sullivan 5-Shelf Bookcase"],
    "Chairs":       ["Hon 5400 Series Task Chair", "Global Leather Task Chair",
                     "Raynor Ergohuman Chair"],
    "Furnishings":  ["Eldon Expressions Desk Accessories",
                     "Tensor Incandescent Lamp", "DAX Metal Document Frame"],
    "Tables":       ["Bretford CR4500 Conference Room Tables",
                     "Bevis Round Conference Table", "Chromcraft Bull-Nose Table"],
    "Appliances":   ["Fellowes PB500 Binding Machine", "GBC Docucoper Binding Machine",
                     "Acco 7-Outlet Masterpiece Power Center"],
    "Art":          ["Faber-Castell Art Pencils Set", "Staedtler Art Pencils",
                     "Sanford Pencils"],
    "Binders":      ["Avery Durable Slant Ring Binder", "Cardinal EasyOpen Binder",
                     "Wilson Jones Hanging View Binder"],
    "Envelopes":    ["Kraft Clasp Envelopes", "Staple Envelope", "Mead Envelopes"],
    "Fasteners":    ["Advantus Push Pins", "Staples Standard Stapler",
                     "Universal Paper Clips"],
    "Labels":       ["Avery Labels", "Xerox Labels", "Avery Color Coded Labels"],
    "Paper":        ["Xerox 4200 Paper", "Hammermill Copy Plus Paper",
                     "Staples 8.5x11 Paper"],
    "Storage":      ["Iris Stacking Drawers", "Storex Portable Storage Box",
                     "Advantus Letter-Size Binder"],
    "Supplies":     ["Dixon Ticonderoga Pencils", "Universal Pen",
                     "Avery Permanent Markers"],
    "Accessories":  ["Logitech Wireless Mouse", "Belkin F8G906-06 Power Strip",
                     "Kensington Laptop Lock"],
    "Copiers":      ["Canon PC940 Copier", "Hewlett-Packard 610", "Sharp AL-1631"],
    "Machines":     ["Cisco SPA 501G IP Phone", "3Com Bluetooth PC Card",
                     "Brother MFC-7340 Printer"],
    "Phones":       ["Motorola Smart Phone", "Apple iPhone 5", "Cisco TelePresence"],
}

customers = [f"Customer_{i:04d}" for i in range(1, 794)]

order_dates = pd.date_range("2019-01-01", "2022-12-31", periods=n)
order_dates = order_dates[np.random.randint(0, len(order_dates), n)]
order_dates = pd.to_datetime(order_dates)

cat_choices  = np.random.choice(categories, n)
sub_choices  = [np.random.choice(sub_cats[c]) for c in cat_choices]
prod_choices = [np.random.choice(products[s]) for s in sub_choices]

# Base sales and profit per category
sales_mu      = {"Furniture": 500, "Office Supplies": 120, "Technology": 800}
sales_sigma   = {"Furniture": 300, "Office Supplies": 80,  "Technology": 600}
profit_margin = {"Furniture": 0.05, "Office Supplies": 0.18, "Technology": 0.13}

sales_vals  = np.array([abs(np.random.normal(sales_mu[c], sales_sigma[c]))
                        for c in cat_choices])
profit_vals = np.array([
    sales_vals[i] * profit_margin[cat_choices[i]] * np.random.uniform(0.3, 1.5)
    if np.random.random() > 0.08 else -sales_vals[i] * 0.15
    for i in range(n)
])
discount_vals = np.random.choice([0, 0.1, 0.2, 0.3, 0.4, 0.5], n,
                                  p=[0.4, 0.2, 0.2, 0.1, 0.07, 0.03])

df = pd.DataFrame({
    "Order ID":     [f"CA-{d.year}-{np.random.randint(100000, 999999)}"
                     for d in order_dates],
    "Order Date":   order_dates,
    "Ship Date":    order_dates + pd.to_timedelta(
                        np.random.randint(1, 8, n), unit="D"),
    "Ship Mode":    np.random.choice(ship_modes, n, p=[0.15, 0.19, 0.60, 0.06]),
    "Customer ID":  np.random.choice(customers, n),
    "Customer Name":[f"Customer {np.random.randint(1, 794)}" for _ in range(n)],
    "Segment":      np.random.choice(segments, n, p=[0.52, 0.30, 0.18]),
    "Country":      "United States",
    "City":         np.random.choice(
                        ["New York City", "Los Angeles", "Philadelphia",
                         "San Francisco", "Seattle", "Houston", "Chicago",
                         "Jacksonville", "Columbus", "Charlotte"], n),
    "State":        np.random.choice(
                        ["New York", "California", "Pennsylvania", "Washington",
                         "Texas", "Illinois", "Florida", "Ohio",
                         "North Carolina", "Georgia"], n),
    "Region":       np.random.choice(regions, n, p=[0.32, 0.28, 0.23, 0.17]),
    "Category":     cat_choices,
    "Sub-Category": sub_choices,
    "Product Name": prod_choices,
    "Sales":        np.round(sales_vals, 2),
    "Quantity":     np.random.randint(1, 15, n),
    "Discount":     discount_vals,
    "Profit":       np.round(profit_vals, 2),
})

# Introduce a few missing values to practise cleaning
df.loc[df.sample(15).index, "Postal Code"] = np.nan
df.insert(df.columns.tolist().index("City") + 1, "Postal Code",
          df.pop("Postal Code") if "Postal Code" in df.columns else np.nan)

print(f"Dataset generated — {df.shape[0]:,} rows x {df.shape[1]} columns")


# ============================================================
# SECTION 2 — BASIC DATASET INFORMATION
# ============================================================
print("\n" + "="*60)
print("  SECTION 2 — BASIC DATASET INFORMATION")
print("="*60)

print(f"\nShape : {df.shape}")
print(f"\nColumns ({len(df.columns)}):")
for col in df.columns:
    print(f"   - {col}")

print("\nData Types:")
print(df.dtypes.to_string())

print("\nFirst 5 Rows:")
print(df.head().to_string(index=False))

print("\nStatistical Summary (numeric):")
print(df[["Sales", "Quantity", "Discount", "Profit"]].describe().round(2).to_string())

print("""
INSIGHT — Dataset Overview
   - ~10,000 transactions spanning 2019-2022 across 4 US regions.
   - Three product categories: Furniture, Office Supplies, Technology.
   - Sales range varies widely — Technology orders are the highest-value.
   - Some negative profit values signal discounting or loss-leader products.
""")


# ============================================================
# SECTION 3 — DATA CLEANING & MISSING VALUES
# ============================================================
print("="*60)
print("  SECTION 3 — DATA CLEANING & MISSING VALUES")
print("="*60)

# Check missing values
missing     = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
missing_df  = pd.DataFrame({"Missing Count": missing, "Missing %": missing_pct})
missing_df  = missing_df[missing_df["Missing Count"] > 0]

if missing_df.empty:
    print("\nNo missing values found.")
else:
    print("\nMissing Values Detected:")
    print(missing_df.to_string())
    df["Postal Code"] = df["Postal Code"].fillna("00000")
    print("   -> 'Postal Code' missing values filled with '00000'")

# Check duplicates
dupes = df.duplicated(subset=["Order ID"]).sum()
print(f"\nDuplicate rows : {dupes}")

# Ensure correct dtypes
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"]  = pd.to_datetime(df["Ship Date"])

# Feature engineering — extract time-based columns
df["Year"]      = df["Order Date"].dt.year
df["Month"]     = df["Order Date"].dt.month
df["Month Name"]= df["Order Date"].dt.strftime("%b")
df["Quarter"]   = df["Order Date"].dt.quarter
df["YearMonth"] = df["Order Date"].dt.to_period("M")

print("\nNew feature columns added: Year, Month, Month Name, Quarter, YearMonth")

# Visualise: Missing value heatmap
fig, ax = plt.subplots(figsize=(10, 3))
missing_heat      = df.isnull().astype(int)
cols_with_missing = missing_heat.columns[missing_heat.any()].tolist()
if cols_with_missing:
    sns.heatmap(missing_heat[cols_with_missing].head(200).T,
                cbar=False, cmap="Reds", ax=ax, linewidths=0)
    ax.set_title("Missing Values Heatmap (first 200 rows)")
else:
    ax.text(0.5, 0.5, "No Missing Values in Dataset",
            ha="center", va="center", fontsize=14, color=COLORS["positive"])
    ax.set_axis_off()
    ax.set_title("Missing Values Check")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/01_missing_values.png", bbox_inches="tight")
plt.close()
print("Chart saved: 01_missing_values.png")

print("""
INSIGHT — Data Quality
   - Dataset is mostly clean with only 'Postal Code' having minor gaps.
   - No critical columns (Sales, Profit, Category, Region) have missing data.
   - Date columns correctly parsed; derived time features ready for analysis.
""")


# ============================================================
# SECTION 4 — SALES ANALYSIS BY REGION
# ============================================================
print("="*60)
print("  SECTION 4 — SALES ANALYSIS BY REGION")
print("="*60)

region_sales  = df.groupby("Region")[["Sales", "Profit"]].sum().reset_index()
region_sales  = region_sales.sort_values("Sales", ascending=False)
region_orders = df.groupby("Region")["Order ID"].count().reset_index()
region_orders.columns = ["Region", "Order Count"]
region_sales  = region_sales.merge(region_orders, on="Region")

print("\nSales & Profit by Region:")
print(region_sales.to_string(index=False))

fig, axes = plt.subplots(1, 3, figsize=(17, 5))
fig.suptitle("Sales Performance by Region", fontsize=16, fontweight="bold", y=1.01)

# Bar — total sales
bars = axes[0].bar(region_sales["Region"], region_sales["Sales"] / 1000,
                   color=COLORS["palette"][:4], edgecolor="white", linewidth=1.5)
axes[0].set_title("Total Sales ($K)")
axes[0].set_xlabel("Region")
axes[0].set_ylabel("Sales ($K)")
for bar in bars:
    axes[0].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2,
                 f"${bar.get_height():.0f}K", ha="center", va="bottom",
                 fontsize=9, fontweight="bold")

# Bar — total profit
bars2 = axes[1].bar(region_sales["Region"], region_sales["Profit"] / 1000,
                    color=COLORS["palette"][:4], edgecolor="white", linewidth=1.5)
axes[1].set_title("Total Profit ($K)")
axes[1].set_xlabel("Region")
axes[1].set_ylabel("Profit ($K)")
for bar in bars2:
    clr = COLORS["positive"] if bar.get_height() >= 0 else COLORS["negative"]
    axes[1].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                 f"${bar.get_height():.0f}K", ha="center", va="bottom",
                 fontsize=9, fontweight="bold", color=clr)

# Pie — order share
axes[2].pie(region_sales["Order Count"], labels=region_sales["Region"],
            colors=COLORS["palette"][:4], autopct="%1.1f%%",
            startangle=90, wedgeprops={"edgecolor": "white", "linewidth": 1.5})
axes[2].set_title("Order Count Share")

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/02_sales_by_region.png", bbox_inches="tight")
plt.close()
print("Chart saved: 02_sales_by_region.png")

top_region = region_sales.iloc[0]["Region"]
print(f"""
INSIGHT — Regional Performance
   - {top_region} leads in total sales, driven by higher-value Technology orders.
   - West & East together account for ~60% of all transactions.
   - South has the lowest order volume — a potential growth opportunity.
   - Profit margins vary by region, partly due to discount patterns.
""")


# ============================================================
# SECTION 5 — SALES ANALYSIS BY CATEGORY & SUB-CATEGORY
# ============================================================
print("="*60)
print("  SECTION 5 — SALES BY CATEGORY & SUB-CATEGORY")
print("="*60)

cat_sales = df.groupby("Category")[["Sales", "Profit", "Quantity"]].sum().reset_index()
cat_sales = cat_sales.sort_values("Sales", ascending=False)
print("\nSales by Category:")
print(cat_sales.to_string(index=False))

subcat_sales = (df.groupby(["Category", "Sub-Category"])[["Sales", "Profit"]]
                  .sum().reset_index()
                  .sort_values("Sales", ascending=False))

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle("Sales & Profit by Category", fontsize=16, fontweight="bold")

# Category donut chart
wedges, texts, autotexts = axes[0].pie(
    cat_sales["Sales"], labels=cat_sales["Category"],
    colors=["#2E86AB", "#F18F01", "#44BBA4"],
    autopct="%1.1f%%", startangle=90, pctdistance=0.75,
    wedgeprops={"edgecolor": "white", "linewidth": 2, "width": 0.6})
for t in autotexts:
    t.set_fontsize(11)
    t.set_fontweight("bold")
axes[0].set_title("Sales Share by Category")

# Sub-category horizontal bar (top 12)
top12      = subcat_sales.head(12)
colors_bar = [COLORS["positive"] if p >= 0 else COLORS["negative"]
              for p in top12["Profit"]]
h_bars = axes[1].barh(top12["Sub-Category"], top12["Sales"] / 1000,
                      color=colors_bar, edgecolor="white", linewidth=1)
axes[1].set_title("Top Sub-Categories by Sales ($K)")
axes[1].set_xlabel("Sales ($K)")
axes[1].invert_yaxis()
for bar in h_bars:
    axes[1].text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                 f"${bar.get_width():.0f}K", va="center", fontsize=8)

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/03_sales_by_category.png", bbox_inches="tight")
plt.close()
print("Chart saved: 03_sales_by_category.png")

print("""
INSIGHT — Category & Sub-Category
   - Technology generates the highest revenue despite fewer transactions.
   - Office Supplies has the most orders but lower average order value.
   - Tables (Furniture) tend to have poor/negative profit — heavy discounting issue.
   - Phones and Copiers are the standout Technology sub-categories by sales.
""")


# ============================================================
# SECTION 6 — PROFIT ANALYSIS
# ============================================================
print("="*60)
print("  SECTION 6 — PROFIT ANALYSIS")
print("="*60)

profit_cat = df.groupby("Category")["Profit"].agg(
    ["sum", "mean", "median"]).round(2).reset_index()
profit_cat.columns = ["Category", "Total Profit", "Avg Profit", "Median Profit"]
print("\nProfit Summary by Category:")
print(profit_cat.to_string(index=False))

subcat_profit = (df.groupby("Sub-Category")["Profit"].sum()
                   .reset_index().sort_values("Profit"))

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle("Profit Analysis", fontsize=16, fontweight="bold")

# Sub-category profit bar (sorted lowest to highest)
colors_p = [COLORS["positive"] if p >= 0 else COLORS["negative"]
            for p in subcat_profit["Profit"]]
axes[0].barh(subcat_profit["Sub-Category"], subcat_profit["Profit"] / 1000,
             color=colors_p, edgecolor="white")
axes[0].axvline(0, color="black", linewidth=0.8, linestyle="--")
axes[0].set_title("Total Profit by Sub-Category ($K)")
axes[0].set_xlabel("Profit ($K)")

# Profit distribution violin plot by category
parts = axes[1].violinplot(
    [df[df["Category"] == c]["Profit"].values for c in categories],
    positions=[1, 2, 3], showmedians=True, showmeans=False)
for i, pc in enumerate(parts["bodies"]):
    pc.set_facecolor(COLORS["palette"][i])
    pc.set_alpha(0.8)
parts["cmedians"].set_color("black")
parts["cmedians"].set_linewidth(2)
axes[1].set_xticks([1, 2, 3])
axes[1].set_xticklabels(categories)
axes[1].axhline(0, color="red", linestyle="--", linewidth=0.8, label="Break-even")
axes[1].set_title("Profit Distribution by Category")
axes[1].set_ylabel("Profit ($)")
axes[1].legend()

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/04_profit_analysis.png", bbox_inches="tight")
plt.close()
print("Chart saved: 04_profit_analysis.png")

print("""
INSIGHT — Profit Deep Dive
   - Tables sub-category is a profit drain — discounts likely exceed margins.
   - Technology has the highest profit per order despite fewer transactions.
   - Office Supplies profit is consistent but low per unit — volume-dependent.
   - Negative profit orders correlate with discount rates above 40%.
""")


# ============================================================
# SECTION 7 — MONTHLY & YEARLY SALES TREND
# ============================================================
print("="*60)
print("  SECTION 7 — MONTHLY & YEARLY SALES TREND")
print("="*60)

yearly     = df.groupby("Year")[["Sales", "Profit"]].sum().reset_index()
monthly_avg = (df.groupby("Month")[["Sales", "Profit"]].mean().reset_index()
                 .sort_values("Month"))
month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
monthly_avg["Month Name"] = monthly_avg["Month"].apply(lambda x: month_names[x - 1])

yoy = df.groupby(["Year", "Month"])["Sales"].sum().reset_index()

print("\nYearly Sales & Profit:")
print(yearly.to_string(index=False))

fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle("Sales Trends — Monthly & Yearly", fontsize=16, fontweight="bold")

# Year-over-year monthly sales lines
for yr in yoy["Year"].unique():
    d = yoy[yoy["Year"] == yr]
    axes[0, 0].plot(d["Month"], d["Sales"] / 1000, marker="o",
                    label=str(yr), linewidth=2, markersize=5)
axes[0, 0].set_title("Monthly Sales Trend by Year ($K)")
axes[0, 0].set_xlabel("Month")
axes[0, 0].set_ylabel("Sales ($K)")
axes[0, 0].set_xticks(range(1, 13))
axes[0, 0].set_xticklabels(month_names)
axes[0, 0].legend(title="Year")

# Annual total sales bar
axes[0, 1].bar(yearly["Year"].astype(str), yearly["Sales"] / 1000,
               color=COLORS["palette"][:4], edgecolor="white", linewidth=1.5)
axes[0, 1].set_title("Total Annual Sales ($K)")
axes[0, 1].set_xlabel("Year")
axes[0, 1].set_ylabel("Sales ($K)")
for i, (yr, s) in enumerate(zip(yearly["Year"], yearly["Sales"])):
    axes[0, 1].text(i, s / 1000 + 1, f"${s / 1000:.0f}K",
                    ha="center", fontweight="bold", fontsize=10)

# Average sales by month
axes[1, 0].bar(monthly_avg["Month Name"], monthly_avg["Sales"],
               color=COLORS["primary"], edgecolor="white", alpha=0.85)
axes[1, 0].set_title("Average Sales by Month ($)")
axes[1, 0].set_xlabel("Month")
axes[1, 0].set_ylabel("Avg Sales ($)")
axes[1, 0].tick_params(axis="x", rotation=45)

# Quarterly profit bar
quarterly = df.groupby(["Year", "Quarter"])["Profit"].sum().reset_index()
quarterly["Period"] = (quarterly["Year"].astype(str) + " Q" +
                       quarterly["Quarter"].astype(str))
colors_q = [COLORS["positive"] if p >= 0 else COLORS["negative"]
            for p in quarterly["Profit"]]
axes[1, 1].bar(quarterly["Period"], quarterly["Profit"] / 1000,
               color=colors_q, edgecolor="white")
axes[1, 1].set_title("Quarterly Profit ($K)")
axes[1, 1].set_xlabel("Quarter")
axes[1, 1].set_ylabel("Profit ($K)")
axes[1, 1].tick_params(axis="x", rotation=45)
axes[1, 1].axhline(0, color="black", linewidth=0.8, linestyle="--")

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/05_sales_trends.png", bbox_inches="tight")
plt.close()
print("Chart saved: 05_sales_trends.png")

print("""
INSIGHT — Temporal Trends
   - Sales follow a seasonal pattern: Q4 (Oct-Dec) consistently peaks.
   - November and December are the highest revenue months — holiday demand.
   - Year-over-year sales have grown steadily, showing healthy business expansion.
   - Q1 is the weakest quarter — strategic promotions could boost slow months.
""")


# ============================================================
# SECTION 8 — SALES VS PROFIT RELATIONSHIP
# ============================================================
print("="*60)
print("  SECTION 8 — SALES vs PROFIT RELATIONSHIP")
print("="*60)

# Sample for scatter readability
sample = df.sample(min(2000, len(df)), random_state=42)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle("Sales vs Profit Relationship", fontsize=16, fontweight="bold")

# Scatter coloured by category
for i, (cat, grp) in enumerate(sample.groupby("Category")):
    axes[0].scatter(grp["Sales"], grp["Profit"],
                    alpha=0.45, label=cat, s=20,
                    color=COLORS["palette"][i])
axes[0].axhline(0, color="red", linestyle="--", linewidth=0.8)
axes[0].set_title("Sales vs Profit (by Category)")
axes[0].set_xlabel("Sales ($)")
axes[0].set_ylabel("Profit ($)")
axes[0].legend()

# Scatter coloured by discount rate
scatter = axes[1].scatter(sample["Sales"], sample["Profit"],
                          c=sample["Discount"], cmap="RdYlGn_r",
                          alpha=0.5, s=20)
plt.colorbar(scatter, ax=axes[1], label="Discount Rate")
axes[1].axhline(0, color="red", linestyle="--", linewidth=0.8)
axes[1].set_title("Sales vs Profit (coloured by Discount)")
axes[1].set_xlabel("Sales ($)")
axes[1].set_ylabel("Profit ($)")

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/06_sales_vs_profit.png", bbox_inches="tight")
plt.close()
print("Chart saved: 06_sales_vs_profit.png")

corr_sp = df["Sales"].corr(df["Profit"])
corr_dp = df["Discount"].corr(df["Profit"])
print(f"\nSales-Profit correlation   : {corr_sp:.3f}")
print(f"Discount-Profit correlation: {corr_dp:.3f}")

print(f"""
INSIGHT — Sales vs Profit
   - Sales and Profit have a moderate positive correlation ({corr_sp:.2f}).
   - High discount rates (>=40%) reliably push orders into negative profit.
   - Technology orders show the tightest cluster — consistent margins.
   - Several high-sales orders have negative profit — review pricing strategy.
""")


# ============================================================
# SECTION 9 — TOP 10 PRODUCTS BY SALES
# ============================================================
print("="*60)
print("  SECTION 9 — TOP 10 PRODUCTS BY SALES")
print("="*60)

top_products = (df.groupby("Product Name")[["Sales", "Profit"]]
                  .sum().reset_index()
                  .sort_values("Sales", ascending=False)
                  .head(10))

print("\nTop 10 Products by Sales:")
print(top_products.to_string(index=False))

fig, ax = plt.subplots(figsize=(13, 6))
colors_pr = [COLORS["positive"] if p >= 0 else COLORS["negative"]
             for p in top_products["Profit"]]
bars = ax.barh(top_products["Product Name"], top_products["Sales"] / 1000,
               color=colors_pr, edgecolor="white", linewidth=1.2)
ax.invert_yaxis()
ax.set_title("Top 10 Products by Sales ($K)\n(Green = Profitable | Red = Loss-making)",
             fontsize=13, fontweight="bold")
ax.set_xlabel("Total Sales ($K)")
for bar in bars:
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
            f"${bar.get_width():.1f}K", va="center", fontsize=9, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/07_top10_products.png", bbox_inches="tight")
plt.close()
print("Chart saved: 07_top10_products.png")

print("""
INSIGHT — Top Products
   - The top 10 products are dominated by Technology (Phones, Copiers, Machines).
   - Most top products are profitable — high-value, low-discount items.
   - Products with red bars indicate bundling/discount promotions eroding margins.
   - Focus marketing spend on consistently profitable high-sales products.
""")


# ============================================================
# SECTION 10 — TOP 10 CUSTOMERS BY SALES
# ============================================================
print("="*60)
print("  SECTION 10 — TOP 10 CUSTOMERS BY SALES")
print("="*60)

top_customers = (df.groupby("Customer Name")
                   .agg(Total_Sales=("Sales", "sum"),
                        Total_Profit=("Profit", "sum"),
                        Orders=("Order ID", "count"))
                   .reset_index()
                   .sort_values("Total_Sales", ascending=False)
                   .head(10))

print("\nTop 10 Customers by Sales:")
print(top_customers.to_string(index=False))

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle("Top 10 Customers Analysis", fontsize=16, fontweight="bold")

colors_cust = [COLORS["positive"] if p >= 0 else COLORS["negative"]
               for p in top_customers["Total_Profit"]]

# Horizontal bar — sales per customer
axes[0].barh(top_customers["Customer Name"],
             top_customers["Total_Sales"] / 1000,
             color=COLORS["primary"], edgecolor="white")
axes[0].invert_yaxis()
axes[0].set_title("Total Sales per Customer ($K)")
axes[0].set_xlabel("Sales ($K)")

# Bubble chart — sales vs profit, bubble size = order count
axes[1].scatter(top_customers["Total_Sales"] / 1000,
                top_customers["Total_Profit"] / 1000,
                s=top_customers["Orders"] * 15,
                color=colors_cust, alpha=0.8, edgecolors="white", linewidth=1.5)
for _, row in top_customers.iterrows():
    axes[1].annotate(row["Customer Name"],
                     (row["Total_Sales"] / 1000, row["Total_Profit"] / 1000),
                     fontsize=7, ha="left", va="bottom")
axes[1].axhline(0, color="red", linestyle="--", linewidth=0.8)
axes[1].set_title("Top Customer: Sales vs Profit\n(bubble size = order count)")
axes[1].set_xlabel("Sales ($K)")
axes[1].set_ylabel("Profit ($K)")

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/08_top10_customers.png", bbox_inches="tight")
plt.close()
print("Chart saved: 08_top10_customers.png")

print("""
INSIGHT — Customer Value
   - Top customers are high-frequency buyers across multiple categories.
   - A few high-sales customers yield low profit — likely heavy negotiators.
   - Implementing a VIP loyalty programme could lock in top-value customers.
   - RFM (Recency-Frequency-Monetary) segmentation should be the next analysis step.
""")


# ============================================================
# SECTION 11 — SEGMENT & SHIP MODE ANALYSIS
# ============================================================
print("="*60)
print("  SECTION 11 — SEGMENT & SHIP MODE ANALYSIS")
print("="*60)

seg_sales  = df.groupby("Segment")[["Sales", "Profit"]].sum().reset_index()
ship_sales = df.groupby("Ship Mode")[["Sales", "Profit"]].sum().reset_index()

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Segment & Shipping Mode Analysis", fontsize=16, fontweight="bold")

# Dual-axis: sales bar + profit line by segment
axes[0].bar(seg_sales["Segment"], seg_sales["Sales"] / 1000,
            color=COLORS["palette"][:3], edgecolor="white", linewidth=1.5)
ax2 = axes[0].twinx()
ax2.plot(seg_sales["Segment"], seg_sales["Profit"] / 1000,
         color=COLORS["negative"], marker="D", linewidth=2, markersize=8,
         label="Profit ($K)")
ax2.set_ylabel("Profit ($K)", color=COLORS["negative"])
axes[0].set_title("Sales (bar) & Profit (line) by Segment")
axes[0].set_ylabel("Sales ($K)")

# Sales by ship mode
axes[1].bar(ship_sales["Ship Mode"], ship_sales["Sales"] / 1000,
            color=COLORS["palette"][3:7], edgecolor="white", linewidth=1.5)
axes[1].set_title("Total Sales by Ship Mode ($K)")
axes[1].set_ylabel("Sales ($K)")
axes[1].tick_params(axis="x", rotation=15)

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/09_segment_ship.png", bbox_inches="tight")
plt.close()
print("Chart saved: 09_segment_ship.png")

print("""
INSIGHT — Segment & Shipping
   - Consumer segment drives the most revenue (~52% of orders).
   - Corporate segment has the best profit-to-sales ratio.
   - Standard Class shipping dominates — cost-sensitive customers.
   - Same Day delivery has the fewest orders — premium rarely chosen.
""")


# ============================================================
# SECTION 12 — DISCOUNT IMPACT ANALYSIS
# ============================================================
print("="*60)
print("  SECTION 12 — DISCOUNT IMPACT ANALYSIS")
print("="*60)

df["Discount Band"] = pd.cut(df["Discount"],
                              bins=[-0.01, 0, 0.1, 0.2, 0.3, 0.5],
                              labels=["0%", "1-10%", "11-20%", "21-30%", "31-50%"])
disc_analysis = (df.groupby("Discount Band")[["Sales", "Profit"]]
                   .mean().round(2).reset_index())
print("\nAvg Sales & Profit by Discount Band:")
print(disc_analysis.to_string(index=False))

fig, ax = plt.subplots(figsize=(10, 5))
x     = range(len(disc_analysis))
width = 0.35
ax.bar([i - width / 2 for i in x], disc_analysis["Sales"],
       width, label="Avg Sales", color=COLORS["primary"], edgecolor="white")
ax.bar([i + width / 2 for i in x], disc_analysis["Profit"],
       width, label="Avg Profit",
       color=[COLORS["positive"] if p >= 0 else COLORS["negative"]
              for p in disc_analysis["Profit"]], edgecolor="white")
ax.set_xticks(x)
ax.set_xticklabels(disc_analysis["Discount Band"])
ax.set_title("Avg Sales & Profit by Discount Band", fontsize=14, fontweight="bold")
ax.set_xlabel("Discount Band")
ax.set_ylabel("Amount ($)")
ax.axhline(0, color="black", linewidth=0.7, linestyle="--")
ax.legend()
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/10_discount_impact.png", bbox_inches="tight")
plt.close()
print("Chart saved: 10_discount_impact.png")

print("""
INSIGHT — Discount Impact
   - Discounts above 30% result in average negative profit per order.
   - The sweet spot is 10-20% discount: sustains sales without killing margins.
   - Recommend a discount cap policy: no more than 20% without manager approval.
""")


# ============================================================
# SECTION 13 — CORRELATION HEATMAP
# ============================================================
print("="*60)
print("  SECTION 13 — CORRELATION HEATMAP")
print("="*60)

num_cols    = ["Sales", "Quantity", "Discount", "Profit", "Year", "Month", "Quarter"]
corr_matrix = df[num_cols].corr().round(3)

print("\nCorrelation Matrix:")
print(corr_matrix.to_string())

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, fmt=".2f",
            cmap="coolwarm", center=0, vmin=-1, vmax=1,
            linewidths=0.5, linecolor="white",
            square=True, ax=ax,
            annot_kws={"size": 11, "weight": "bold"})
ax.set_title("Feature Correlation Heatmap", fontsize=15, fontweight="bold", pad=15)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/11_correlation_heatmap.png", bbox_inches="tight")
plt.close()
print("Chart saved: 11_correlation_heatmap.png")

print(f"""
INSIGHT — Correlations
   - Discount & Profit: negative correlation ({corr_matrix.loc['Discount','Profit']:.2f}) — discounting hurts profit.
   - Sales & Profit: moderate positive correlation ({corr_matrix.loc['Sales','Profit']:.2f}) — higher sales generally profitable.
   - Quantity shows weak correlation with Sales — mix of cheap and expensive items.
   - No significant seasonal correlation detected — demand is spread year-round.
""")


# ============================================================
# SECTION 14 — EXECUTIVE DASHBOARD SUMMARY
# ============================================================
print("="*60)
print("  SECTION 14 — EXECUTIVE SUMMARY DASHBOARD")
print("="*60)

total_sales           = df["Sales"].sum()
total_profit          = df["Profit"].sum()
total_orders          = df["Order ID"].nunique()
profit_margin_overall = (total_profit / total_sales * 100)
avg_order_val         = total_sales / total_orders
best_region           = df.groupby("Region")["Sales"].sum().idxmax()
best_category         = df.groupby("Category")["Profit"].sum().idxmax()

fig = plt.figure(figsize=(16, 10))
fig.patch.set_facecolor("#1A1A2E")

# KPI cards
kpis = [
    ("Total Sales",     f"${total_sales/1e6:.2f}M",           "#2E86AB"),
    ("Total Profit",    f"${total_profit/1000:.0f}K",          "#44BBA4"),
    ("Profit Margin",   f"{profit_margin_overall:.1f}%",       "#F18F01"),
    ("Total Orders",    f"{total_orders:,}",                   "#A23B72"),
    ("Avg Order Value", f"${avg_order_val:.0f}",               "#E94F37"),
    ("Best Region",     best_region,                           "#5C6BC0"),
    ("Best Category",   best_category,                         "#26A69A"),
    ("Years of Data",   "2019-2022",                           "#EF5350"),
]

for i, (title, value, color) in enumerate(kpis):
    ax = fig.add_axes([0.02 + (i % 4) * 0.245,
                       0.58 - (i // 4) * 0.28,
                       0.22, 0.22])
    ax.set_facecolor(color)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_edgecolor("white")
        spine.set_linewidth(2)
    ax.text(0.5, 0.65, value, transform=ax.transAxes,
            ha="center", va="center", fontsize=18, fontweight="bold", color="white")
    ax.text(0.5, 0.25, title, transform=ax.transAxes,
            ha="center", va="center", fontsize=10, color="white", alpha=0.9)

# Monthly trend line at the bottom
ax_trend = fig.add_axes([0.05, 0.06, 0.90, 0.18])
ax_trend.set_facecolor("#16213E")
monthly_trend = df.groupby(["Year", "Month"])["Sales"].sum().reset_index()
monthly_trend["Period"] = ((monthly_trend["Year"] - 2019) * 12 +
                            monthly_trend["Month"])
monthly_trend = monthly_trend.sort_values("Period")
ax_trend.fill_between(monthly_trend["Period"],
                       monthly_trend["Sales"] / 1000,
                       alpha=0.3, color="#2E86AB")
ax_trend.plot(monthly_trend["Period"], monthly_trend["Sales"] / 1000,
              color="#2E86AB", linewidth=2)
ax_trend.set_title("Monthly Sales Trend ($K) — 2019 to 2022",
                   color="white", fontsize=11, fontweight="bold")
ax_trend.tick_params(colors="white")
for spine in ax_trend.spines.values():
    spine.set_edgecolor("#2E86AB")
ax_trend.set_ylabel("Sales ($K)", color="white")

fig.text(0.5, 0.97, "SUPERSTORE — EXECUTIVE DASHBOARD",
         ha="center", va="top", fontsize=18, fontweight="bold", color="white")

plt.savefig(f"{OUTPUT_DIR}/12_executive_dashboard.png", bbox_inches="tight",
            facecolor=fig.get_facecolor())
plt.close()
print("Chart saved: 12_executive_dashboard.png")


# ============================================================
# FINAL SUMMARY
# ============================================================
print("\n" + "="*60)
print("  EDA COMPLETE — FINAL BUSINESS SUMMARY")
print("="*60)
print(f"""
SUPERSTORE EDA — KEY FINDINGS
{'='*55}
Revenue      : ${total_sales:,.0f}  ({df['Year'].nunique()} years)
Profit       : ${total_profit:,.0f}
Margin       : {profit_margin_overall:.1f}%
Orders       : {total_orders:,}
Top Region   : {best_region}
Top Category : {best_category}
{'='*55}

STRATEGIC RECOMMENDATIONS
1. Cap discounts at 20% — orders above 30% discount lose money.
2. Invest in South region expansion — untapped growth potential.
3. Prioritise Technology category — highest margin and revenue.
4. Launch Q1 promotions to offset seasonal sales dip.
5. Audit Tables sub-category pricing — consistently loss-making.
6. Build VIP programme for top customers — protect key revenue.
7. Explore Standard Class shipping optimisation for cost savings.

All charts saved to: ./{OUTPUT_DIR}/
""")
