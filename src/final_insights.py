"""Reproduce final statistical comparisons from the raw call center CSV."""
from pathlib import Path
import pandas as pd
from scipy.stats import chi2_contingency, f_oneway
ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "data/raw/call_center.csv")
df["within_sla"] = df["Response Time"].eq("Within SLA")
df["negative"] = df["Sentiment"].isin(["Negative", "Very Negative"])
df["csat_recorded"] = df["Csat Score"].notna()
output = ROOT / "outputs/tables"
output.mkdir(parents=True, exist_ok=True)
rows = []
for dimension in ["Call-Centres City", "Channel", "Reason"]:
    summary = df.groupby(dimension).agg(contacts=("Id", "size"), average_csat=("Csat Score", "mean"), csat_responses=("csat_recorded", "sum"), csat_response_rate=("csat_recorded", "mean"), within_sla_rate=("within_sla", "mean"), negative_sentiment_rate=("negative", "mean"), average_duration=("Call Duration In Minutes", "mean")).reset_index()
    summary.to_csv(output / ("final_" + dimension.lower().replace(" ", "_").replace("-", "_") + ".csv"), index=False)
    groups = [group["Csat Score"].dropna().to_numpy() for _, group in df.groupby(dimension)]
    statistic, p = f_oneway(*groups)
    rows.append((dimension, "CSAT across groups", "one-way ANOVA", statistic, p))
    for outcome in ["within_sla", "negative", "csat_recorded"]:
        statistic, p, _, _ = chi2_contingency(pd.crosstab(df[dimension], df[outcome]))
        rows.append((dimension, outcome, "chi-square", statistic, p))
result = pd.DataFrame(rows, columns=["dimension", "outcome", "test", "statistic", "p_value"])
result.to_csv(output / "statistical_tests.csv", index=False)
print(result.to_string(index=False))
