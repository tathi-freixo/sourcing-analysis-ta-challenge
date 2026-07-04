# Sourcing Analysis — Technical Challenge

Funnel and conversion analysis over a mock recruiting dataset (601 candidates), with AI-powered insights and an interactive dashboard.

## Deliverables

| File | Description |
|---|---|
| `sourcing_dashboard.html` | Interactive dashboard — open in any browser |
| `analysis.py` | Python analysis script (all metrics + recommendations) |
| `sourcing_analysis_case.pdf` | Case document: approach, decisions, AI use, key insights |
| `mock_sourcing_dataset.xlsx` | Source dataset |

## How to run

**Dashboard (no setup needed)**
Just open `sourcing_dashboard.html` in a browser. All data is embedded.

**Python script**
```bash
pip install pandas openpyxl
python analysis.py
```

## Key Findings

- **8.2% overall hire rate** (49 hires / 601 sourced)
- **Critical bottleneck**: only 30.8% of candidates who completed the test received an offer
- **Best channels overall**: Github (11.0%), Inbound (10.1%)
- **Worst channel**: Indicação/Referral (4.7%) — underperforms against intuition
- **4x recruiter gap**: Bruno 15.3% vs. Fernanda 3.9%
- **Triple Score Rule**: Tech ≥80 + Behavior ≥75 + Manager ≥75 → 17.9% hire rate (2x average)
- **#1 rejection reason**: No response (58% of all rejections)
- **Channel ROI is role-dependent**: Github is 26.7% for Analista de Recrutamento but 0% for TA Specialist; LinkedIn is 15% for TA Specialist but 0% for People BP
- **Seniority is not universal**: Junior Analista de Recrutamento converts at 18.5% — above any global seniority average; Junior People BP is 0%
- **Remote consistently underperforms**: Analista de Dados Remote at 1.9%, TA Specialist Remote at 2.4%

## AI Usage

Claude AI was used to:
- Generate analytical hypotheses and validate logic
- Surface non-obvious patterns (referral underperformance, recruiter calibration gap)
- Write all natural-language recommendations in the dashboard
- Define the Triple Score Rule prioritization filter

## Stack

- Python · pandas · openpyxl · reportlab
- HTML · Chart.js
- Claude AI (Anthropic)
