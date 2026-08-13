"""
Generates raw, messy sample data to simulate a Bronze layer ingestion.
Bronze data is intentionally dirty: nulls, duplicates, inconsistent
formatting. This mimics real data coming straight from a source system.
"""

import pandas as pd
import numpy as np
import os

np.random.seed(42)
os.makedirs("bronze", exist_ok=True)

# --- Raw customers ---
customers = pd.DataFrame({
    "customer_id": range(1, 21),
    "customer_name": [
        "Ali Raza", "sana khan", "Bilal Ahmed", None, "Ayesha Malik",
        "hassan sheikh", "Zara Iqbal", "Usman Tariq", "Mahnoor Butt", None,
        "Faisal Qureshi", "hina saeed", "Omar Farooq", "Sadia Yousaf", "Kamran Aziz",
        "nadia hussain", "Tariq Mehmood", "Iqra Siddiqui", "Waleed Anjum", "Rabia Noor"
    ],
    "city": [
        "Lahore", "karachi", "Lahore", "Islamabad", None,
        "Lahore", "Karachi", "islamabad", "Lahore", "Multan",
        "Karachi", "Lahore", None, "Islamabad", "Lahore",
        "multan", "Karachi", "Lahore", "Islamabad", "Lahore"
    ],
    "signup_date": pd.date_range("2023-01-01", periods=20, freq="15D").astype(str)
})

# --- Raw orders (with duplicates and nulls, simulating source system dumps) ---
n_orders = 500
categories = ["Electronics", "Clothing", "Home", "Books", "Sports", None]

orders = pd.DataFrame({
    "order_id": range(1001, 1001 + n_orders),
    "customer_id": np.random.randint(1, 21, size=n_orders),
    "category": np.random.choice(categories, size=n_orders, p=[0.25, 0.2, 0.2, 0.15, 0.15, 0.05]),
    "quantity": np.random.randint(1, 6, size=n_orders),
    "unit_price": np.round(np.random.uniform(5, 500, size=n_orders), 2),
    "order_date": pd.to_datetime("2024-01-01") + pd.to_timedelta(
        np.random.randint(0, 300, size=n_orders), unit="D"
    ),
    "status": np.random.choice(
        ["completed", "COMPLETED", "cancelled", "pending", None],
        size=n_orders, p=[0.55, 0.1, 0.15, 0.15, 0.05]
    )
})

# inject nulls into unit_price and quantity to simulate bad source data
null_idx = np.random.choice(orders.index, size=25, replace=False)
orders.loc[null_idx, "unit_price"] = np.nan

null_idx = np.random.choice(orders.index, size=15, replace=False)
orders.loc[null_idx, "quantity"] = np.nan

# duplicate some rows on purpose, real pipelines get duplicate events often
dupes = orders.sample(20, random_state=1)
orders = pd.concat([orders, dupes], ignore_index=True)

orders["order_date"] = orders["order_date"].astype(str)

customers.to_csv("bronze/raw_customers.csv", index=False)
orders.to_csv("bronze/raw_orders.csv", index=False)

print("bronze layer created")
print("raw_customers.csv  rows:", len(customers))
print("raw_orders.csv     rows:", len(orders))