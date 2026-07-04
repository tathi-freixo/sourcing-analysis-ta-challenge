"""
Sourcing Analysis — Technical Challenge
========================================
Analyzes a mock recruiting dataset to surface conversion insights,
channel performance, recruiter patterns, and AI-powered recommendations.

AI Usage:
  - Claude AI was used to identify insight patterns, generate
    natural-language recommendations, and validate analytical logic.

Requirements:
  pip install pandas openpyxl
"""

import pandas as pd

# ─────────────────────────────────────────
# 1. LOAD DATA
# ─────────────────────────────────────────

df = pd.read_excel("mock_sourcing_dataset.xlsx", sheet_name=0)

# Normalize boolean columns
bool_cols = ["response_received", "screening_pass", "interview1_pass",
             "test_taken", "offer_sent", "hired"]
for col in bool_cols:
    df[col] = df[col].astype(bool)

print(f"Dataset loaded: {len(df)} candidates\n")


# ─────────────────────────────────────────
# 2. FUNNEL OVERVIEW
# ─────────────────────────────────────────

total = len(df)
funnel = {
    "Sourced":        total,
    "Responded":      df["response_received"].sum(),
    "Screen Pass":    df["screening_pass"].sum(),
    "Interview Pass": df["interview1_pass"].sum(),
    "Test Taken":     df["test_taken"].sum(),
    "Offer Sent":     df["offer_sent"].sum(),
    "Hired":          df["hired"].sum(),
}

print("=" * 50)
print("FUNNEL OVERVIEW")
print("=" * 50)
prev = total
for stage, n in funnel.items():
    pct_total = n / total * 100
    pct_prev  = n / prev * 100 if stage != "Sourced" else 100.0
    print(f"  {stage:<20} {n:>4}  ({pct_total:5.1f}% of total | {pct_prev:5.1f}% of prev)")
    prev = n

print("\n⚠  Critical drop: Test → Offer conversion = {:.1f}%".format(
    funnel["Offer Sent"] / funnel["Test Taken"] * 100))


# ─────────────────────────────────────────
# 3. CHANNEL ANALYSIS
# ─────────────────────────────────────────

print("\n" + "=" * 50)
print("CHANNEL PERFORMANCE")
print("=" * 50)

channel_stats = (
    df.groupby("source_channel")
    .agg(
        total=("candidate_id", "count"),
        responded=("response_received", "sum"),
        screen_pass=("screening_pass", "sum"),
        interview_pass=("interview1_pass", "sum"),
        test_taken=("test_taken", "sum"),
        offers=("offer_sent", "sum"),
        hired=("hired", "sum"),
    )
    .assign(
        response_rate=lambda x: x["responded"] / x["total"] * 100,
        hire_rate=lambda x: x["hired"] / x["total"] * 100,
    )
    .sort_values("hire_rate", ascending=False)
)

print(channel_stats[["total", "responded", "response_rate", "hired", "hire_rate"]].to_string())

best_channel  = channel_stats["hire_rate"].idxmax()
worst_channel = channel_stats["hire_rate"].idxmin()
print(f"\n✅ Best channel:  {best_channel} ({channel_stats.loc[best_channel, 'hire_rate']:.1f}%)")
print(f"❌ Worst channel: {worst_channel} ({channel_stats.loc[worst_channel, 'hire_rate']:.1f}%)")


# ─────────────────────────────────────────
# 4. RECRUITER PERFORMANCE
# ─────────────────────────────────────────

print("\n" + "=" * 50)
print("RECRUITER PERFORMANCE")
print("=" * 50)

recruiter_stats = (
    df.groupby("recruiter")
    .agg(
        total=("candidate_id", "count"),
        offers=("offer_sent", "sum"),
        hired=("hired", "sum"),
    )
    .assign(hire_rate=lambda x: x["hired"] / x["total"] * 100)
    .sort_values("hire_rate", ascending=False)
)

print(recruiter_stats.to_string())

top_rec    = recruiter_stats["hire_rate"].idxmax()
bottom_rec = recruiter_stats["hire_rate"].idxmin()
gap = recruiter_stats.loc[top_rec, "hire_rate"] - recruiter_stats.loc[bottom_rec, "hire_rate"]
print(f"\n⚡ Performance gap between {top_rec} and {bottom_rec}: {gap:.1f}pp")


# ─────────────────────────────────────────
# 5. SCORE ANALYSIS — HIRED vs. NOT HIRED
# ─────────────────────────────────────────

print("\n" + "=" * 50)
print("SCORE ANALYSIS: HIRED vs. NOT HIRED")
print("=" * 50)

score_cols = ["technical_test_score", "behavior_score", "manager_score", "years_experience"]
score_compare = df.groupby("hired")[score_cols].mean().rename(
    index={True: "Hired", False: "Not Hired"}
)
print(score_compare.round(1).to_string())

# Score threshold filter
threshold = df[
    (df["technical_test_score"] >= 80) &
    (df["behavior_score"] >= 75) &
    (df["manager_score"] >= 75)
]
print(f"\n🎯 Triple Score Rule (tech≥80, beh≥75, mgr≥75):")
print(f"   Candidates: {len(threshold)}")
print(f"   Hired: {threshold['hired'].sum()} ({threshold['hired'].mean()*100:.1f}% hire rate)")


# ─────────────────────────────────────────
# 6. REJECTION ANALYSIS
# ─────────────────────────────────────────

print("\n" + "=" * 50)
print("REJECTION REASONS")
print("=" * 50)

rejection_counts = df["rejection_reason"].value_counts()
print(rejection_counts.to_string())
no_response_pct = rejection_counts.get("No response", 0) / rejection_counts.sum() * 100
print(f"\n📵 'No response' accounts for {no_response_pct:.0f}% of all rejections")


# ─────────────────────────────────────────
# 7. SENIORITY & WORK MODE ANALYSIS
# ─────────────────────────────────────────

print("\n" + "=" * 50)
print("SENIORITY & WORK MODE")
print("=" * 50)

seniority_order = ["Junior", "Pleno", "Senior", "Staff"]
seniority_stats = (
    df.groupby("seniority")
    .agg(total=("candidate_id", "count"), hired=("hired", "sum"))
    .assign(hire_rate=lambda x: x["hired"] / x["total"] * 100)
    .reindex(seniority_order)
)
print("Seniority:\n", seniority_stats.round(1).to_string())

workmode_stats = (
    df.groupby("work_mode")
    .agg(total=("candidate_id", "count"), hired=("hired", "sum"))
    .assign(hire_rate=lambda x: x["hired"] / x["total"] * 100)
    .sort_values("hire_rate", ascending=False)
)
print("\nWork Mode:\n", workmode_stats.round(1).to_string())


# ─────────────────────────────────────────
# 8. ROLE CROSS-ANALYSIS
# ─────────────────────────────────────────

print("\n" + "=" * 50)
print("ROLE × CHANNEL (hire rate %)")
print("=" * 50)

role_channel = (
    df.groupby(["role", "source_channel"])
    .agg(total=("hired", "count"), hired=("hired", "sum"))
    .assign(rate=lambda x: (x["hired"] / x["total"] * 100).round(1))
    ["rate"].unstack()
)
print(role_channel.to_string())
print("\nKey: Github best for An. Recrutamento (26.7%) but 0% for TA Specialist.")
print("     LinkedIn best for TA Specialist (15.0%) but 0% for People BP.")

print("\n" + "=" * 50)
print("ROLE × SENIORITY (hire rate %)")
print("=" * 50)

role_seniority = (
    df.groupby(["role", "seniority"])
    .agg(total=("hired", "count"), hired=("hired", "sum"))
    .assign(rate=lambda x: (x["hired"] / x["total"] * 100).round(1))
    ["rate"].unstack()
    .reindex(columns=["Junior", "Pleno", "Senior", "Staff"])
)
print(role_seniority.to_string())
print("\nKey: Junior An. Recrutamento = 18.5% (above any global seniority avg).")
print("     Junior People BP = 0%. Seniority signal is role-dependent.")

print("\n" + "=" * 50)
print("ROLE × WORK MODE (hire rate %)")
print("=" * 50)

role_workmode = (
    df.groupby(["role", "work_mode"])
    .agg(total=("hired", "count"), hired=("hired", "sum"))
    .assign(rate=lambda x: (x["hired"] / x["total"] * 100).round(1))
    ["rate"].unstack()
)
print(role_workmode.to_string())
print("\nKey: An. Dados Remote = 1.9%, TA Specialist Remote = 2.4% — near zero.")
print("     Remote is consistently worst, but severity varies significantly by role.")


# ─────────────────────────────────────────
# 9. AI-POWERED RECOMMENDATIONS SUMMARY
# ─────────────────────────────────────────

print("\n" + "=" * 50)
print("AI-POWERED RECOMMENDATIONS (via Claude)")
print("=" * 50)

recommendations = [
    ("CRITICAL", "Test→Offer bottleneck",
     f"Only {funnel['Offer Sent']/funnel['Test Taken']*100:.0f}% of testers get an offer. "
     "Audit scoring calibration and alignment between tech reviewers and HMs."),

    ("CHANNEL",  "Double down on Github + Inbound",
     f"Github ({channel_stats.loc['Github','hire_rate']:.1f}%) and "
     f"Inbound ({channel_stats.loc['Inbound','hire_rate']:.1f}%) outperform. "
     "Indicação (referrals) underperforms — audit referral quality at intake."),

    ("SIGNAL",   "Use Triple Score Rule as early filter",
     "Candidates clearing Tech≥80 / Behavior≥75 / Manager≥75 hit 17.9% hire rate. "
     "Flag these profiles for priority follow-up."),

    ("PEOPLE",   "Calibrate recruiters",
     f"Bruno: {recruiter_stats.loc['Bruno','hire_rate']:.1f}% hire rate. "
     f"Fernanda: {recruiter_stats.loc['Fernanda','hire_rate']:.1f}%. "
     "Run a calibration session — share best practices from top performers."),

    ("OUTREACH", "2nd reach-out cadence for no-response",
     f"No response = {no_response_pct:.0f}% of rejections. "
     "A structured 2nd touch (3–5 days after first contact) could recover material pipeline."),
]

for tag, title, body in recommendations:
    print(f"\n[{tag}] {title}")
    print(f"  → {body}")

print("\n✅ Analysis complete.")
