import streamlit as st
import pandas as pd

# ---------- CONFIG BÁSICA ----------
st.set_page_config(
    page_title="SQL for Humans: Online Store",
    layout="centered"
)

st.title("SQL for Humans: Online Store")
st.write("""
This mini app shows how basic **SQL ideas** (and a bit of Python)
can answer simple business questions for an online store.
""")

# ---------- DATOS DE EJEMPLO ----------
data = {
    "order_id":    [1, 2, 3, 4, 5, 6, 7, 8],
    "customer_id": [1, 1, 2, 3, 4, 2, 3, 5],
    "country":     ["USA", "Spain", "Germany", "Italy", "USA", "Spain", "Germany", "USA"],
    "order_date":  [
        "2024-01-05", "2024-01-20",
        "2024-01-15", "2024-02-10",
        "2024-02-25", "2024-03-03",
        "2024-03-12", "2024-03-20"
    ],
    "total_amount": [120, 45, 30, 80, 60, 55, 100, 150]
}

orders = pd.DataFrame(data)
orders["order_date"] = pd.to_datetime(orders["order_date"])

# Customers "table" derived from orders (simple demo)
customers = orders[["customer_id", "country"]].drop_duplicates()


# ---------- SECCIÓN 0: MODELO SIMPLE ----------
st.subheader("Our simple data model")

st.markdown("""
We imagine 3 tables in our online store:

- `customers` — one row per customer
- `products` — one row per product
- `orders` — one row per order (customer, date, total_amount)

Here we only simulate **customers** and **orders**.
""")


# ---------- SECCIÓN 1: NÚMERO DE CLIENTES ----------
st.header("1. How many customers do we have?")

st.write("SQL idea: **count rows** in the `customers` table.")

st.code("""
SELECT COUNT(*) AS total_customers
FROM customers;
""", language="sql")

total_customers = customers["customer_id"].nunique()
st.metric("Total customers", total_customers)

st.write("""
In words: we count how many unique customers we have in our store.
""")


# ---------- SECCIÓN 2: PEDIDOS POR MES ----------
st.header("2. How many orders did we receive last month?")

st.write("SQL idea: **filter by date** with `WHERE`, then **count**.")

st.code("""
SELECT COUNT(*) AS orders_last_month
FROM orders
WHERE order_date >= '2024-01-01'
  AND order_date <  '2024-02-01';
""", language="sql")

# Selector de mes interactivo
months = orders["order_date"].dt.to_period("M").astype(str).unique()
selected_month = st.selectbox("Choose a month:", sorted(months))

mask = orders["order_date"].dt.to_period("M").astype(str) == selected_month
orders_in_month = orders[mask]

st.metric(f"Orders in {selected_month}", len(orders_in_month))

st.write("""
In words: we take only the orders in the selected month
and count how many there are.
""")


# ---------- SECCIÓN 3: REVENUE POR PAÍS ----------
st.header("3. Which country brings the most revenue?")

st.write("SQL idea: `GROUP BY country` and `SUM(total_amount)`.")

st.code("""
SELECT country,
       SUM(total_amount) AS revenue
FROM orders
GROUP BY country
ORDER BY revenue DESC;
""", language="sql")

revenue_by_country = (
    orders
    .groupby("country", as_index=False)["total_amount"]
    .sum()
    .rename(columns={"total_amount": "revenue"})
)

st.bar_chart(revenue_by_country, x="country", y="revenue")

st.write("""
In words: we put all orders from the same country together,
add up the money in each group, and compare countries.

These numbers are just **example data**, but the logic
is the same you would use with real sales.
""")


# ---------- RECAP ----------
st.header("4. Recap")

st.write("""
With just three SQL patterns:

- **COUNT** rows
- **WHERE** to filter
- **GROUP BY** + **SUM** to aggregate

we can already answer key questions about customers, orders and revenue
in a simple online store.
""")
