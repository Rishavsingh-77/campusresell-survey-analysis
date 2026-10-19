"""CampusResell survey analysis (pilot, n=20).
Run: python analysis.py  (needs pandas, matplotlib)
Note: Q7 (fair-price difficulty) was set up as multiple choice with broken
labels in the form, so it is excluded from the analysis.
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv("survey_responses.csv")
df.columns = ["timestamp", "residence", "year", "bought", "bought_what", "sold_or_discarded",
              "how_find", "q7_unusable", "would_use", "max_fee", "trust"]
n = len(df)

def pct(series):
    return (series.value_counts() / n * 100).round(0).astype(int)

summary = {
    "responses": n,
    "residence": df.residence.value_counts().to_dict(),
    "year": df.year.value_counts().to_dict(),
    "bought_secondhand_pct": round((df.bought == "Yes").mean() * 100),
    "sold_or_discarded_pct": round((df.sold_or_discarded == "Yes").mean() * 100),
    "would_use": pct(df.would_use).to_dict(),
    "how_find": pct(df.how_find).to_dict(),
    "max_fee": pct(df.max_fee).to_dict(),
    "trust": pct(df.trust).to_dict(),
}
for k, v in summary.items():
    print(k, v)

def bar(series, title, fname, color="#c8201f"):
    counts = series.value_counts().sort_values()
    fig, ax = plt.subplots(figsize=(7, 3.4))
    ax.barh(counts.index, counts.values, color=color)
    for i, v in enumerate(counts.values):
        ax.text(v + 0.2, i, f"{v} ({round(v / n * 100)}%)", va="center", fontsize=9)
    ax.set_title(title, loc="left", fontsize=12, fontweight="bold")
    ax.set_xlim(0, counts.max() * 1.25)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_xlabel(f"Respondents (n={n})")
    fig.tight_layout()
    fig.savefig(fname, dpi=160)
    plt.close(fig)

bar(df.would_use, "Would you use a student-only resale platform?", "chart_interest.png")
bar(df.max_fee, "Most a student would pay per sale", "chart_fee.png")
bar(df.trust, "What would make students trust it?", "chart_trust.png")
