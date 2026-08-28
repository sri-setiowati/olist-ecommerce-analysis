# Olist E-commerce Data Analysis

Data analysis project using the Olist Brazilian E-commerce Public Dataset (Kaggle), looking at where delivery and pricing issues concentrate across Brazil's states.

## Problem

Olist ships orders across all of Brazil. Two open questions: are delivery delays spread evenly across the country, and does freight cost eat into margin the same way everywhere? If either problem concentrates in specific states, that changes where logistics investment should go first.

## Approach

- Loaded orders, customers, and order items (96,478 delivered orders, 112,650 order items)
- Calculated the gap between actual and estimated delivery date per order, then grouped the late-delivery rate by customer state
- Calculated freight value as a share of item price per order item, then grouped by customer state
- Kept only states with 200+ orders/items so the rates are based on enough volume to be meaningful

Full code: [`analysis.py`](analysis.py)

## Findings

**1. Delivery delays concentrate in a handful of states.** The national late-delivery rate is 6.8%. Five states, Alagoas, Maranhao, Sergipe, Piaui, and Ceara, run two to three times above that average. Alagoas is highest at 21.4%. Orders that do arrive late are 10.6 days behind on average.

**2. Freight costs fall unevenly across states.** Freight runs 16.6% of item price nationally. In Maranhao, Rondonia, and Piaui, that ratio climbs to 24-26%, nearly double the 13.8% seen in Sao Paulo, the largest market with 47,449 items.

Full write-up with tables and formulas: [`olist_business_findings_report.xlsx`](olist_business_findings_report.xlsx)

## Recommendations

- Start logistics and carrier reviews with the five states carrying the highest delay rate, and send customers there a proactive notice when a delivery estimate is at risk
- Look at regional distribution hubs or renegotiated carrier rates for the states with the highest freight burden, so prices stay competitive there without cutting into margin

## Tools

Python (pandas), Excel, Power BI

## Files

- `analysis.py` — full analysis code
- `olist_business_findings_report.xlsx` — findings summary with verifiable Excel formulas
- `case_study_olist.md` — full case study write-up
- `olist-dashboard.pbix` — full Power BI dashboard file
