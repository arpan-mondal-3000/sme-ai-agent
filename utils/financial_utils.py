import pandas as pd
import re
from core.config import DATA_PATH

df = pd.read_csv(DATA_PATH)

# Parse Month column once at load time
df["Month_dt"] = pd.to_datetime(df["Month"], format="%b-%y")
df["Year"]      = df["Month_dt"].dt.year
df["Quarter"]   = df["Month_dt"].dt.quarter
df["Month_norm"] = df["Month"].str.lower()


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def _fmt(n: float) -> str:
    return f"Rs.{int(n):,}"

def _profit_margin(sales, expenses) -> str:
    if sales == 0:
        return "0.00%"
    return f"{((sales - expenses) / sales) * 100:.2f}%"

def _growth(current, previous) -> str:
    if previous == 0:
        return "N/A"
    pct = ((current - previous) / previous) * 100
    direction = "up" if pct >= 0 else "down"
    return f"{direction} {abs(pct):.1f}%"

def _rank_in_dataset(month: str, metric: str) -> str:
    """Return a human-readable rank string e.g. '3rd highest out of 48 months'."""
    col = metric
    sorted_df = df.sort_values(col, ascending=False).reset_index(drop=True)
    idx = sorted_df[sorted_df["Month"] == month].index
    if idx.empty:
        return ""
    rank = idx[0] + 1
    total = len(df)
    suffix = {1: "st", 2: "nd", 3: "rd"}.get(rank if rank <= 3 else 0, "th")
    return f"{rank}{suffix} highest out of {total} months"

def _filter_by_period(query: str) -> pd.DataFrame:
    query = query.lower()
    data = df.copy()

    year_match    = re.search(r"(20\d{2})", query)
    quarter_match = re.search(r"q([1-4])", query)
    month_match   = re.search(
        r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*", query
    )

    if year_match:
        data = data[data["Year"] == int(year_match.group(1))]
    if quarter_match:
        data = data[data["Quarter"] == int(quarter_match.group(1))]
    if month_match:
        data = data[data["Month_norm"].str.startswith(month_match.group(1))]

    return data


# ─────────────────────────────────────────────
# TOOL 1 — calculate_profit
# ─────────────────────────────────────────────

def calculate_profit(month: str) -> str:
    query     = month.strip().lower()
    month_pat = re.search(r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)", query)
    year_pat  = re.search(r"(\d{2,4})", query)

    if not month_pat:
        return (
            "Could not read the month from your input. "
            "Please use a format like 'Jul-23', 'July 2023', or 'jul 23'."
        )

    data = df[df["Month_norm"].str.startswith(month_pat.group(1))]

    if year_pat:
        yr   = year_pat.group(1)
        yr   = int("20" + yr) if len(yr) == 2 else int(yr)
        data = data[data["Year"] == yr]

    if data.empty:
        available = ", ".join(df["Month"].tolist())
        return f"No data found for that month. Available months are: {available}"

    row      = data.iloc[0]
    sales    = float(row["Sales"])
    expenses = float(row["Expenses"])
    inv      = float(row["InventoryCost"])
    mkt      = float(row["MarketingSpend"])
    customers = int(row["Customers"])

    gross_profit = sales - expenses
    net_profit   = gross_profit - inv - mkt
    rev_per_cust = sales / customers if customers else 0
    is_loss      = net_profit < 0

    performance = (
        "The business ran at a loss this month."
        if is_loss
        else "The business was profitable this month."
    )

    return f"""
{row['Month']} — Profit Breakdown
{'=' * 40}
Revenue
  Sales                  : {_fmt(sales)}
  Customers served       : {customers:,}
  Revenue per customer   : {_fmt(rev_per_cust)}

Costs
  Operating expenses     : {_fmt(expenses)}
  Inventory cost         : {_fmt(inv)}
  Marketing spend        : {_fmt(mkt)}

Results
  Gross profit           : {_fmt(gross_profit)}  (margin: {_profit_margin(sales, expenses)})
  Net profit             : {_fmt(net_profit)}
  Sales rank             : {_rank_in_dataset(row['Month'], 'Sales')}

{performance}
""".strip()


# ─────────────────────────────────────────────
# TOOL 2 — business_summary
# ─────────────────────────────────────────────

def business_summary(query: str) -> str:
    data = _filter_by_period(query)

    if data.empty:
        return (
            "No data found for that period. "
            "Please specify a valid year (2021 to 2024) or quarter."
        )

    total_sales     = data["Sales"].sum()
    total_expenses  = data["Expenses"].sum()
    total_inv       = data["InventoryCost"].sum()
    total_mkt       = data["MarketingSpend"].sum()
    net_profit      = total_sales - total_expenses - total_inv - total_mkt
    avg_customers   = data["Customers"].mean()
    total_customers = data["Customers"].sum()
    best_month      = data.loc[data["Sales"].idxmax(), "Month"]
    worst_month     = data.loc[data["Sales"].idxmin(), "Month"]
    avg_mkt_roi     = (total_sales / total_mkt) if total_mkt else 0
    is_profitable   = net_profit >= 0

    if len(data) >= 2:
        growth_str = _growth(data.iloc[-1]["Sales"], data.iloc[0]["Sales"])
    else:
        growth_str = "only one month in range"

    overall = (
        f"The business was {'profitable' if is_profitable else 'running at a loss'} "
        f"over this period with a net {'profit' if is_profitable else 'loss'} of {_fmt(abs(net_profit))}."
    )

    summary = f"""
Business Performance Summary
Period  : {data.iloc[0]['Month']} to {data.iloc[-1]['Month']}  ({len(data)} months)
{'=' * 50}
Revenue and Costs
  Total sales            : {_fmt(total_sales)}
  Total expenses         : {_fmt(total_expenses)}
  Total inventory cost   : {_fmt(total_inv)}
  Total marketing spend  : {_fmt(total_mkt)}

Key Results
  Net profit             : {_fmt(net_profit)}
  Profit margin          : {_profit_margin(total_sales, total_expenses)}
  Sales trend            : {growth_str}
  Total customers        : {total_customers:,}
  Average customers/month: {int(avg_customers)}
  Marketing ROI          : {avg_mkt_roi:.1f}x  ({_fmt(avg_mkt_roi)} sales per Rs.1 spent)

Highlights
  Strongest month        : {best_month}
  Weakest month          : {worst_month}

{overall}"""

    advice_triggers = ["improve", "advice", "suggest", "how", "increase", "grow", "better"]
    if any(word in query.lower() for word in advice_triggers):
        low_margin_months = data[
            (data["Sales"] - data["Expenses"]) / data["Sales"] < 0.30
        ]["Month"].tolist()

        recs = "\n\nRecommendations\n" + "-" * 40 + "\n"
        recs += f"  - {best_month} was your strongest month. Identify what drove that performance and plan to replicate it.\n"
        recs += f"  - {worst_month} was your weakest month. A targeted promotion or cost review during that period could help.\n"

        if avg_mkt_roi < 10:
            recs += "  - Marketing ROI is below 10x. Review which channels are underperforming and reallocate budget.\n"
        else:
            recs += f"  - Marketing ROI is strong at {avg_mkt_roi:.1f}x. Consider increasing spend during peak months to amplify returns.\n"

        if low_margin_months:
            recs += f"  - These months had thin profit margins (below 30%): {', '.join(low_margin_months)}. Audit fixed costs here.\n"

        if avg_customers < 200:
            recs += "  - Average monthly customers is below 200. Focus on customer acquisition — referral programmes or local campaigns could help.\n"
        else:
            recs += "  - Your customer base is healthy. Prioritise retention and upselling to existing customers to grow revenue without extra acquisition cost.\n"

        summary += recs

    return summary.strip()


# ─────────────────────────────────────────────
# TOOL 3 — compare_periods
# ─────────────────────────────────────────────

def compare_periods(period1: str, period2: str) -> str:
    d1 = _filter_by_period(period1)
    d2 = _filter_by_period(period2)

    if d1.empty:
        return f"No data found for '{period1}'. Please check the period and try again."
    if d2.empty:
        return f"No data found for '{period2}'. Please check the period and try again."

    def _agg(data):
        return {
            "sales"    : data["Sales"].sum(),
            "expenses" : data["Expenses"].sum(),
            "inv"      : data["InventoryCost"].sum(),
            "mkt"      : data["MarketingSpend"].sum(),
            "customers": data["Customers"].sum(),
            "label"    : f"{data.iloc[0]['Month']} to {data.iloc[-1]['Month']}",
        }

    a, b   = _agg(d1), _agg(d2)
    a["profit"] = a["sales"] - a["expenses"] - a["inv"] - a["mkt"]
    b["profit"] = b["sales"] - b["expenses"] - b["inv"] - b["mkt"]

    winner = (
        "Both periods broke even."
        if a["profit"] == b["profit"]
        else (
            f"{b['label']} was more profitable by {_fmt(abs(b['profit'] - a['profit']))}."
            if b["profit"] > a["profit"]
            else f"{a['label']} was more profitable by {_fmt(abs(a['profit'] - b['profit']))}."
        )
    )

    col_a = f"{a['label']}"
    col_b = f"{b['label']}"
    w = 26

    return f"""
Period Comparison
{'=' * 70}
{"Metric":<22} {col_a:<{w}} {col_b:<{w}} {"Change":<12}
{'-' * 70}
{"Sales":<22} {_fmt(a['sales']):<{w}} {_fmt(b['sales']):<{w}} {_growth(b['sales'], a['sales'])}
{"Expenses":<22} {_fmt(a['expenses']):<{w}} {_fmt(b['expenses']):<{w}} {_growth(b['expenses'], a['expenses'])}
{"Net Profit":<22} {_fmt(a['profit']):<{w}} {_fmt(b['profit']):<{w}} {_growth(b['profit'], a['profit'])}
{"Customers":<22} {a['customers']:<{w},} {b['customers']:<{w},} {_growth(b['customers'], a['customers'])}
{"Marketing Spend":<22} {_fmt(a['mkt']):<{w}} {_fmt(b['mkt']):<{w}} {_growth(b['mkt'], a['mkt'])}
{'=' * 70}
Verdict: {winner}
""".strip()


# ─────────────────────────────────────────────
# TOOL 4 — top_months
# ─────────────────────────────────────────────

def top_months(metric: str = "Sales", n: int = 5) -> str:
    valid_metrics = ["Sales", "Expenses", "Customers", "InventoryCost", "MarketingSpend"]
    metric = next((m for m in valid_metrics if m.lower() == metric.lower()), "Sales")

    top     = df.nlargest(n, metric)[["Month", metric, "Year"]]
    bottom  = df.nsmallest(1, metric)[["Month", metric]].iloc[0]

    lines = [
        f"Top {n} months by {metric}",
        "=" * 35,
    ]
    for i, (_, row) in enumerate(top.iterrows(), 1):
        val = f"{int(row[metric]):,}" if metric == "Customers" else _fmt(row[metric])
        lines.append(f"  {i}.  {row['Month']:<10}  {val}")

    low_val = f"{int(bottom[metric]):,}" if metric == "Customers" else _fmt(bottom[metric])
    lines.append("")
    lines.append(f"Lowest month  :  {bottom['Month']:<10}  {low_val}")

    return "\n".join(lines)