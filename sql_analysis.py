"""
SQL analysis of delivery delays and freight costs in the Olist e-commerce dataset.
Uses DuckDB to run SQL queries directly against the raw CSV files.

Dataset: Olist Brazilian E-commerce Public Dataset (Kaggle)
https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
Download the CSVs and place them in the same folder as this script before running.
"""

import duckdb

con = duckdb.connect()

# Load all tables directly from the CSVs (must be in the same folder as this script)
con.sql("""
    CREATE VIEW orders AS SELECT * FROM read_csv_auto('olist_orders_dataset.csv');
    CREATE VIEW order_items AS SELECT * FROM read_csv_auto('olist_order_items_dataset.csv');
    CREATE VIEW customers AS SELECT * FROM read_csv_auto('olist_customers_dataset.csv');
    CREATE VIEW sellers AS SELECT * FROM read_csv_auto('olist_sellers_dataset.csv');
    CREATE VIEW products AS SELECT * FROM read_csv_auto('olist_products_dataset.csv');
    CREATE VIEW order_reviews AS SELECT * FROM read_csv_auto('olist_order_reviews_dataset.csv');
    CREATE VIEW category_translation AS SELECT * FROM read_csv_auto('product_category_name_translation.csv');
""")

print("="*60)
print("1. Delay rate per state")
print("="*60)
delay_rate_by_state = con.sql("""
    WITH delivery_status AS (
        SELECT
            o.order_id,
            c.customer_state,
            DATE_DIFF('day', o.order_estimated_delivery_date, o.order_delivered_customer_date) AS delay_days
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        WHERE o.order_delivered_customer_date IS NOT NULL
    )
    SELECT
        customer_state,
        COUNT(*) AS total_orders,
        SUM(CASE WHEN delay_days > 0 THEN 1 ELSE 0 END) AS delayed_orders,
        ROUND(100.0 * SUM(CASE WHEN delay_days > 0 THEN 1 ELSE 0 END) / COUNT(*), 1) AS delay_rate_pct,
        ROUND(AVG(CASE WHEN delay_days > 0 THEN delay_days END), 1) AS avg_delay_days_when_late
    FROM delivery_status
    GROUP BY customer_state
    ORDER BY delay_rate_pct DESC
""").df()
print(delay_rate_by_state)

print("\n" + "="*60)
print("2. Seller ranking by average delay")
print("="*60)
seller_delay_ranking = con.sql("""
    WITH seller_delay AS (
        SELECT
            s.seller_id,
            s.seller_state,
            oi.order_id,
            DATE_DIFF('day', o.order_estimated_delivery_date, o.order_delivered_customer_date) AS delay_days
        FROM order_items oi
        JOIN sellers s ON oi.seller_id = s.seller_id
        JOIN orders o ON oi.order_id = o.order_id
        WHERE o.order_delivered_customer_date IS NOT NULL
    ),
    seller_agg AS (
        SELECT
            seller_id,
            seller_state,
            COUNT(*) AS total_orders,
            ROUND(AVG(delay_days), 1) AS avg_delay_days
        FROM seller_delay
        GROUP BY seller_id, seller_state
        HAVING COUNT(*) >= 10
    )
    SELECT
        *,
        RANK() OVER (ORDER BY avg_delay_days DESC) AS delay_rank
    FROM seller_agg
    ORDER BY delay_rank
    LIMIT 20
""").df()
print(seller_delay_ranking)

print("\n" + "="*60)
print("3. Freight cost as % of price by category")
print("="*60)
freight_pct_by_category = con.sql("""
    WITH cat_agg AS (
        SELECT
            ct.product_category_name_english AS category,
            SUM(oi.price) AS total_price,
            SUM(oi.freight_value) AS total_freight,
            COUNT(*) AS total_items
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        JOIN category_translation ct ON p.product_category_name = ct.product_category_name
        GROUP BY category
    )
    SELECT
        category,
        total_items,
        ROUND(100.0 * total_freight / NULLIF(total_price, 0), 1) AS freight_pct_of_price,
        ROUND(total_price / total_items, 2) AS avg_price,
        ROUND(total_freight / total_items, 2) AS avg_freight
    FROM cat_agg
    WHERE total_items >= 30   -- exclude categories with too small a sample
    ORDER BY freight_pct_of_price DESC
    LIMIT 15
""").df()
print(freight_pct_by_category)

print("\n" + "="*60)
print("4. Review score by delivery status")
print("="*60)
review_score_by_delivery_status = con.sql("""
    WITH delay_review AS (
        SELECT
            o.order_id,
            CASE
                WHEN DATE_DIFF('day', o.order_estimated_delivery_date, o.order_delivered_customer_date) > 0
                THEN 'Delayed'
                ELSE 'On-time'
            END AS delivery_status,
            r.review_score
        FROM orders o
        JOIN order_reviews r ON o.order_id = r.order_id
        WHERE o.order_delivered_customer_date IS NOT NULL
    )
    SELECT
        delivery_status,
        COUNT(*) AS total_orders,
        ROUND(AVG(review_score), 2) AS avg_review_score,
        ROUND(100.0 * SUM(CASE WHEN review_score <= 2 THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_low_review
    FROM delay_review
    GROUP BY delivery_status
""").df()
print(review_score_by_delivery_status)

print("\n" + "="*60)
print("5. Freight cost trend by quarter")
print("="*60)
freight_trend_by_quarter = con.sql("""
    SELECT
        DATE_TRUNC('quarter', o.order_purchase_timestamp) AS quarter,
        ROUND(AVG(oi.freight_value), 2) AS avg_freight
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY quarter
    ORDER BY quarter
""").df()
print(freight_trend_by_quarter)

con.close()
