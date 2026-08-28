"""
Olist E-commerce Data Analysis
Business question: where should logistics and pricing attention be prioritized
across Brazil's states?

Data source: Olist Brazilian E-commerce Public Dataset (Kaggle)
Files used: olist_orders_dataset.csv, olist_customers_dataset.csv,
            olist_order_items_dataset.csv
"""

import pandas as pd

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
orders = pd.read_csv("olist_orders_dataset.csv")
items = pd.read_csv("olist_order_items_dataset.csv")
customers = pd.read_csv("olist_customers_dataset.csv")

date_cols = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]
for col in date_cols:
    orders[col] = pd.to_datetime(orders[col], errors="coerce")

# ---------------------------------------------------------------------------
# Finding 1: delivery delay rate by state
# ---------------------------------------------------------------------------
delivered = orders[orders["order_status"] == "delivered"].copy()
delivered["delay_days"] = (
    delivered["order_delivered_customer_date"]
    - delivered["order_estimated_delivery_date"]
).dt.days
delivered["is_late"] = delivered["delay_days"] > 0

national_late_rate = delivered["is_late"].mean() * 100
avg_delay_when_late = delivered.loc[delivered["is_late"], "delay_days"].mean()

delivered = delivered.merge(
    customers[["customer_id", "customer_state"]], on="customer_id", how="left"
)
delay_by_state = (
    delivered.groupby("customer_state")
    .agg(total_orders=("order_id", "count"), late_orders=("is_late", "sum"))
    .reset_index()
)
delay_by_state["late_rate_pct"] = (
    delay_by_state["late_orders"] / delay_by_state["total_orders"] * 100
).round(2)
# Only keep states with enough volume for the rate to be meaningful
delay_by_state = delay_by_state[delay_by_state["total_orders"] >= 200].sort_values(
    "late_rate_pct", ascending=False
)

print(f"National late-delivery rate: {national_late_rate:.1f}%")
print(f"Average delay for late orders: {avg_delay_when_late:.1f} days")
print("\nTop states by late-delivery rate (200+ orders):")
print(delay_by_state.head(6).to_string(index=False))

# ---------------------------------------------------------------------------
# Finding 2: freight cost as a share of item price, by state
# ---------------------------------------------------------------------------
items_with_state = items.merge(
    orders[["order_id", "customer_id"]], on="order_id", how="left"
).merge(customers[["customer_id", "customer_state"]], on="customer_id", how="left")

national_freight_pct = (
    items["freight_value"].sum() / items["price"].sum() * 100
)

freight_by_state = (
    items_with_state.groupby("customer_state")
    .agg(
        n_items=("order_id", "count"),
        total_price=("price", "sum"),
        total_freight=("freight_value", "sum"),
    )
    .reset_index()
)
freight_by_state["freight_pct_of_price"] = (
    freight_by_state["total_freight"] / freight_by_state["total_price"] * 100
).round(2)
freight_by_state = freight_by_state[freight_by_state["n_items"] >= 200].sort_values(
    "freight_pct_of_price", ascending=False
)

print(f"\nNational freight cost as % of item price: {national_freight_pct:.1f}%")
print("\nTop states by freight burden (200+ items):")
print(freight_by_state.head(6).to_string(index=False))
print("\nLowest-burden state for comparison:")
print(freight_by_state.tail(1).to_string(index=False))
