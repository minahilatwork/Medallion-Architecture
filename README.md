# Medallion Architecture Data Pipeline

A simple Data Engineering project demonstrating the Medallion Architecture using Python, Pandas, Parquet, and DuckDB.

## Overview

This project implements a basic data pipeline based on the Medallion Architecture:

**Bronze → Silver → Gold**

Each layer has a different purpose:

- **Bronze:** Stores the raw data with minimal changes.
- **Silver:** Cleans, filters, and transforms the data.
- **Gold:** Produces processed and aggregated data ready for analysis.

## Data Flow

```text
Raw Data
   ↓
Bronze Layer
   ↓
Cleaning & Transformation
   ↓
Silver Layer
   ↓
Aggregation & Analysis
   ↓
Gold Layer
   ↓
Parquet + DuckDB
Project Structure
Medallion-Architecture/
│
├── bronze/
│   └── Raw data files
│
├── silver/
│   └── Cleaned and transformed data
│
├── gold/
│   └── Aggregated and analysis-ready data
│
├── Bronze.py
├── Bronze_to_Silver/
├── Silver_to_Gold/
├── duckdb_vs_pandas/
├── Observation.md
└── README.md
Technologies Used
Python
Pandas
Parquet
DuckDB
Git & GitHub
Pandas Data Manipulation

The project practices common data manipulation techniques including:

Filtering data
Handling missing/null values
Data transformations
Joining datasets
Grouping data
Aggregations
Data type conversions
Parquet

Processed datasets are stored in Parquet format.

Parquet is useful in Data Engineering because it is:

Column-oriented
Compressed
Efficient for analytical workloads
Faster to read for selected columns
Generally more storage-efficient than CSV
DuckDB

DuckDB is used to query the Parquet files using SQL.

This project also compares querying and processing data using:

Pandas vs DuckDB

The comparison focuses on processing approach, performance, and memory usage.

Medallion Layers
Bronze Layer

Contains the original/raw data.

The goal is to preserve the source data before major transformations are applied.

Silver Layer

Contains cleaned and transformed data.

Typical operations include:

Removing or handling null values
Filtering records
Converting data types
Cleaning values
Joining datasets
Applying transformations
Gold Layer

Contains final, analysis-ready data.

This layer can contain:

Aggregated results
Grouped data
Calculated metrics
Summaries for reporting and analysis
Key Learning

This project demonstrates how raw data can move through different stages of a modern Data Engineering pipeline:

Raw → Clean → Transform → Aggregate → Analyze

It also demonstrates how Pandas can be used for data manipulation, Parquet can be used for efficient storage, and DuckDB can be used to query analytical data using SQL.