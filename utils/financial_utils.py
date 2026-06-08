import pandas as pd
import re

df = pd.read_csv("data/sme_sales_data.csv")

# Parse Month column once at load time
df["Month_dt"] = pd.to_datetime(df["Month"], format="%b-%y")
df["Year"] = df["Month_dt"].dt.year
df["Quarter"] = df["Month_dt"].dt.quarter
df["Month_norm"] = df["Month"].str.lower()


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def _fmt(n: float) -> str:
    """Format large numbers as ₹ with Indian comma style."""
    return f"₹{int(n):,}"

def _profit_margin(sales, expenses) -> str:
    if sales == 0:
        return "0.00%"
    return f"{((sales - expenses) / sales) * 100:.2f}%"

def _growth(current, previous) -> str:
    if previous == 0:
        return "N/A"
    pct = ((current - previous) / previous) * 100
    arrow = "▲" if pct >= 0 else "▼"
    return f"{arrow} {abs(pct):.1f}%"

def _filter_by_period(query: str) -> pd.DataFrame:
    """
    Parse a natural language query for year/quarter/month filters
    and return the matching slice of the dataframe.
    """
    query = query.lower()
    data = df.copy()

    year_match = re.search(r"(20\d{2})", query)
    quarter_match = re.search(r"q([1-4])", query)
    month_match = re.search(
        r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*", query
    )

    if year_match:
        year = int(year_match.group(1))
        data = data[data["Year"] == year]

    if quarter_match:
        quarter = int(quarter_match.group(1))
        data = data[data["Quarter"] == quarter]

    if month_match:
        month_str = month_match.group(1)
        data = data[data["Month_norm"].str.startswith(month_str)]

    return data


# ─────────────────────────────────────────────
# TOOL 1 — calculate_profit
# ─────────────────────────────────────────────

def calculate_profit(month: str) -> str:
    """
    Return a detailed profit breakdown for a given month.
    Accepts flexible input: 'Jul-23', 'july 2023', 'jul 23', etc.
    """
    query = month.strip().lower()

    # Try flexible match: short month name + 2 or 4 digit year
    month_pat = re.search(r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)", query)
    year_pat  = re.search(r"(\d{2,4})", query)

    if not month_pat:
        return (
            "Could not parse month. "
            "Please use a format like 'Jul-23', 'July 2023', or 'jul 23'."
        )

    data = df[df["Month_norm"].str.startswith(month_pat.group(1))]

    if year_pat:
        yr = year_pat.group(1)
        yr = int("20" + yr) if len(yr) == 2 else int(yr)
        data = data[data["Year"] == yr]

    if data.empty:
        available = ", ".join(df["Month"].tolist())
        return f"Month not found. Available months: {available}"

    row = data.iloc[0]
    sales      = float(row["Sales"])
    expenses   = float(row["Expenses"])
    inv_cost   = float(row["InventoryCost"])
    mkt_spend  = float(row["MarketingSpend"])
    customers  = int(row["Customers"])

    gross_profit   = sales - expenses
    operating_cost = inv_cost + mkt_spend
    net_profit     = gross_profit - operating_cost
    revenue_per_customer = sales / customers if customers else 0

    return f"""
📅 Month: {row['Month']}
─────────────────────────────
💰 Sales Revenue     : {_fmt(sales)}
📦 Expenses          : {_fmt(expenses)}
🏭 Inventory Cost    : {_fmt(inv_cost)}
📣 Marketing Spend   : {_fmt(mkt_spend)}
─────────────────────────────
📊 Gross Profit      : {_fmt(gross_profit)}  (margin: {_profit_margin(sales, expenses)})
🧾 Operating Costs   : {_fmt(operating_cost)}
✅ Net Profit        : {_fmt(net_profit)}
👥 Customers         : {customers}
💵 Revenue/Customer  : {_fmt(revenue_per_customer)}
""".strip()


# ─────────────────────────────────────────────
# TOOL 2 — business_summary
# ─────────────────────────────────────────────

def business_summary(query: str) -> str:
    """
    Summarise business performance for a period detected from the query.
    Handles: full dataset, by year, by quarter, by year+quarter.
    Also detects improvement/advice queries and appends recommendations.
    """
    data = _filter_by_period(query)

    if data.empty:
        return "No data found for the requested period. Try specifying a valid year (2021–2024) or quarter."

    total_sales    = data["Sales"].sum()
    total_expenses = data["Expenses"].sum()
    total_inv      = data["InventoryCost"].sum()
    total_mkt      = data["MarketingSpend"].sum()
    net_profit     = total_sales - total_expenses - total_inv - total_mkt
    avg_customers  = data["Customers"].mean()
    total_customers = data["Customers"].sum()
    best_month     = data.loc[data["Sales"].idxmax(), "Month"]
    worst_month    = data.loc[data["Sales"].idxmin(), "Month"]
    avg_mkt_roi    = (total_sales / total_mkt) if total_mkt else 0

    # Month-over-month growth (first vs last in period)
    if len(data) >= 2:
        first_sales = data.iloc[0]["Sales"]
        last_sales  = data.iloc[-1]["Sales"]
        growth_str  = _growth(last_sales, first_sales)
    else:
        growth_str = "N/A (single month)"

    summary = f"""
📊 Business Performance Summary
Period: {data.iloc[0]['Month']} → {data.iloc[-1]['Month']}  ({len(data)} months)
─────────────────────────────────────────
💰 Total Sales          : {_fmt(total_sales)}
📦 Total Expenses       : {_fmt(total_expenses)}
🏭 Total Inventory Cost : {_fmt(total_inv)}
📣 Total Marketing Spend: {_fmt(total_mkt)}
─────────────────────────────────────────
✅ Net Profit           : {_fmt(net_profit)}
📈 Profit Margin        : {_profit_margin(total_sales, total_expenses)}
📉 Sales Growth         : {growth_str}
👥 Total Customers      : {total_customers:,}
👤 Avg Customers/Month  : {int(avg_customers)}
📣 Marketing ROI        : {avg_mkt_roi:.1f}x  (₹{avg_mkt_roi:.1f} sales per ₹1 spent)
🏆 Best Month           : {best_month}
⚠️  Weakest Month        : {worst_month}
""".strip()

    # Append advice if query is improvement-oriented
    advice_triggers = ["improve", "advice", "suggest", "how", "increase", "grow", "better"]
    if any(word in query.lower() for word in advice_triggers):
        low_margin_months = data[
            (data["Sales"] - data["Expenses"]) / data["Sales"] < 0.30
        ]["Month"].tolist()

        recommendations = "\n\n💡 Recommendations:\n"
        recommendations += f"  • Best month was {best_month} — analyse what drove that and replicate it.\n"
        recommendations += f"  • Weakest month was {worst_month} — consider targeted promotions during that period.\n"

        if avg_mkt_roi < 10:
            recommendations += "  • Marketing ROI is low — review channel effectiveness and reallocate budget.\n"
        else:
            recommendations += f"  • Marketing ROI is strong at {avg_mkt_roi:.1f}x — consider increasing spend in peak months.\n"

        if low_margin_months:
            recommendations += f"  • Low profit margin months: {', '.join(low_margin_months)} — audit expenses here.\n"

        if avg_customers < 200:
            recommendations += "  • Customer acquisition is below 200/month — invest in lead generation.\n"
        else:
            recommendations += "  • Customer base is healthy — focus on retention and upselling.\n"

        summary += recommendations

    return summary


# ─────────────────────────────────────────────
# TOOL 3 — compare_periods
# ─────────────────────────────────────────────

def compare_periods(period1: str, period2: str) -> str:
    """
    Compare two periods (years or year+quarter) side by side.
    Example inputs: '2022', '2023'  or  'Q1 2022', 'Q1 2023'
    """
    d1 = _filter_by_period(period1)
    d2 = _filter_by_period(period2)

    if d1.empty:
        return f"No data found for period: '{period1}'"
    if d2.empty:
        return f"No data found for period: '{period2}'"

    def _agg(data):
        return {
            "sales":     data["Sales"].sum(),
            "expenses":  data["Expenses"].sum(),
            "inv":       data["InventoryCost"].sum(),
            "mkt":       data["MarketingSpend"].sum(),
            "customers": data["Customers"].sum(),
            "label":     f"{data.iloc[0]['Month']} → {data.iloc[-1]['Month']}",
        }

    a, b = _agg(d1), _agg(d2)

    a["profit"] = a["sales"] - a["expenses"] - a["inv"] - a["mkt"]
    b["profit"] = b["sales"] - b["expenses"] - b["inv"] - b["mkt"]

    return f"""
📊 Period Comparison
─────────────────────────────────────────────────────
Metric              {a['label']:<20} {b['label']:<20} Change
─────────────────────────────────────────────────────
💰 Sales          {_fmt(a['sales']):<22} {_fmt(b['sales']):<22} {_growth(b['sales'], a['sales'])}
📦 Expenses       {_fmt(a['expenses']):<22} {_fmt(b['expenses']):<22} {_growth(b['expenses'], a['expenses'])}
✅ Net Profit     {_fmt(a['profit']):<22} {_fmt(b['profit']):<22} {_growth(b['profit'], a['profit'])}
👥 Customers      {a['customers']:<22,} {b['customers']:<22,} {_growth(b['customers'], a['customers'])}
📣 Mkt Spend      {_fmt(a['mkt']):<22} {_fmt(b['mkt']):<22} {_growth(b['mkt'], a['mkt'])}
""".strip()


# ─────────────────────────────────────────────
# TOOL 4 — top_months
# ─────────────────────────────────────────────

def top_months(metric: str = "Sales", n: int = 5) -> str:
    """
    Return the top N months for a given metric.
    Valid metrics: Sales, Expenses, Customers, InventoryCost, MarketingSpend
    """
    valid_metrics = ["Sales", "Expenses", "Customers", "InventoryCost", "MarketingSpend"]
    metric = next((m for m in valid_metrics if m.lower() == metric.lower()), "Sales")

    top = df.nlargest(n, metric)[["Month", metric]]

    lines = [f"🏆 Top {n} months by {metric}:", "─" * 35]
    for i, (_, row) in enumerate(top.iterrows(), 1):
        val = _fmt(row[metric]) if metric != "Customers" else f"{int(row[metric]):,}"
        lines.append(f"  {i}. {row['Month']:<10} {val}")

    return "\n".join(lines)