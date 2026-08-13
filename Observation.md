# Medallion Architecture: Observations

## What is Medallion Architecture

It's a way of organizing a data pipeline into three stages: Bronze, Silver and Gold. Each stage has one job and data gets cleaner and more trustworthy as it moves forward.

## Bronze layer

This is the raw data, exactly as it came in.

Nothing gets cleaned or changed here. Duplicates, nulls and messy formatting all stay as is. It works as a backup too, if something breaks downstream you can always reprocess from this original copy.

Files: `bronze/raw_orders.csv` and `bronze/raw_customers.csv`

## Silver layer

This is where the raw data actually becomes usable.

In `2_bronze_to_silver.py` I did the following:

- removed duplicate rows
- fixed inconsistent text casing in city names and order status
- filled missing categories and missing names with placeholder values
- dropped rows where quantity was missing since that field is needed for revenue math
- filled missing unit_price with the median price for that category instead of dropping those rows
- fixed data types for dates and numbers
- joined orders with customers into one table
- kept only orders marked completed, since cancelled or pending orders don't count as real revenue

Output: `silver/orders_clean.parquet` and `silver/customers_clean.parquet`

## Gold layer

This is the final stage, built for reporting and nothing else.

Built in `3_silver_to_gold.py`:

- `revenue_by_category.parquet` shows total revenue, order count and average order value per category
- `monthly_revenue.parquet` shows how revenue changed month to month
- `top_customers.parquet` shows the top 10 customers by total spend

No cleaning happens at this stage, just grouping and summarizing numbers that are already clean.

## Why Parquet instead of CSV

Parquet stores data by column instead of by row, so reading one column doesn't mean reading the whole file like CSV does. It also saves the data types along with the file so you don't need to guess them every time you load it. On top of that it's compressed by default so the file size is much smaller. All of this makes it a better fit for analytical queries where you usually only need a few columns out of many.

## DuckDB vs Pandas

I ran the same group by query, once with pandas and once with DuckDB, directly on the silver parquet file. Both gave the exact same result.

DuckDB was faster even on this small dataset. The reason is that DuckDB reads parquet natively and only pulls in the columns a query actually needs. Pandas loads the whole file into memory first no matter what you ask for. On a small file like this the difference barely matters but on a large dataset it adds up fast since pandas has to hold everything in RAM while DuckDB doesn't.

## How the pipeline flows

raw_orders.csv and raw_customers.csv start in bronze.
`1_generate_bronze_data.py` creates them.
`2_bronze_to_silver.py` cleans and joins them into orders_clean.parquet and customers_clean.parquet in silver.
`3_silver_to_gold.py` aggregates that into revenue_by_category.parquet, monthly_revenue.parquet and top_customers.parquet in gold.
`4_duckdb_vs_pandas.py` queries the silver file and compares performance between the two tools.