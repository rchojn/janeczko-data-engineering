# Month 01 Capstone Project Brief: NYC Taxi Data Product

## 1. Executive Summary

Build a local analytical data product in DuckDB using real NYC TLC Yellow Taxi data.

The goal is not to submit a collection of disconnected SQL queries. The goal is to deliver a small but realistic Data Engineering project that turns raw public data into documented, validated, reproducible analytical outputs.

High-level flow:

```text
raw Parquet/CSV
  -> raw views
  -> silver tables and rejected records
  -> dimension and fact tables
  -> gold analytical metrics
  -> validation checks
  -> business summary and technical documentation
```

This project closes Month 01 by combining SQL fundamentals, data modeling, data quality, performance awareness, idempotency, backfill thinking, and operational documentation.

## 2. Business Context

You are building a data product for a hypothetical city operations or mobility analytics team.

The team wants to understand taxi demand and revenue patterns across New York City using Yellow Taxi trip data.

The product should answer questions such as:

```text
Which pickup zones generate the highest revenue?
Which pickup zones have the highest trip volume?
Which hours have the strongest demand?
How do airport trips behave compared with non-airport trips?
Are the published metrics trustworthy and reproducible?
```

The final output should be useful to a business reader and reviewable by a Data Engineering mentor.

## 3. Scope

### In Scope

The project must include:

```text
DuckDB-based local analytics
real NYC TLC Yellow Taxi Parquet files
NYC taxi zone lookup CSV
raw/silver/gold data layers
fact and dimension modeling
SQL validation checks
performance review using EXPLAIN
idempotent SQL patterns
backfill plan
incident runbook
business summary report
reproducible README
```

### Out of Scope

The project does not require:

```text
Airflow or any scheduler
dbt
Spark
cloud storage
production orchestration
Python ingestion code
BI dashboard
```

The focus is Month 01 SQL Data Engineering, not full platform engineering.

## 4. Source Data

### Verified Data Availability

The following sources were verified on 2026-08-16 using HTTP HEAD checks and DuckDB schema/sample queries.

All listed files returned HTTP 200 at the time of verification.

| Dataset | URL | Verified Size |
|---|---|---:|
| `yellow_tripdata_2024-01.parquet` | `https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet` | 49,961,641 B |
| `yellow_tripdata_2024-02.parquet` | `https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-02.parquet` | 50,349,284 B |
| `yellow_tripdata_2024-03.parquet` | `https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-03.parquet` | 60,078,280 B |
| `yellow_tripdata_2024-04.parquet` | `https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-04.parquet` | 59,133,625 B |
| `yellow_tripdata_2024-05.parquet` | `https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-05.parquet` | 62,553,128 B |
| `yellow_tripdata_2024-06.parquet` | `https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-06.parquet` | 59,859,922 B |
| `taxi_zone_lookup.csv` | `https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv` | 12,331 B |

Official source page:

```text
https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
```

### Verified Yellow Taxi Columns

The project instructions assume these columns exist in the Yellow Taxi Parquet files:

```text
VendorID
tpep_pickup_datetime
tpep_dropoff_datetime
passenger_count
trip_distance
RatecodeID
store_and_fwd_flag
PULocationID
DOLocationID
payment_type
fare_amount
extra
mta_tax
tip_amount
tolls_amount
improvement_surcharge
total_amount
congestion_surcharge
Airport_fee
```

### Verified Taxi Zone Lookup Columns

The project assumes these columns exist in `taxi_zone_lookup.csv`:

```text
LocationID
Borough
Zone
service_zone
```

## 5. Data Volume Requirement

Target scope:

```text
January-June 2024, 6 monthly Yellow Taxi Parquet files
```

Minimum acceptable scope:

```text
January-March 2024, 3 monthly Yellow Taxi Parquet files
```

Use the minimum scope only if local hardware, disk space, or network conditions make the target scope impractical. If you reduce the scope, document the reason in `README.md` under `Known Limitations`.

## 6. Required Submission Structure

Submit this directory structure:

```text
homework/month_01_capstone/
├── sql/
│   ├── 00_bootstrap.sql
│   ├── 01_raw_sources.sql
│   ├── 02_raw_profiling.sql
│   ├── 03_silver_trips.sql
│   ├── 04_dimensions.sql
│   ├── 05_fact_trips.sql
│   ├── 06_gold_daily_zone_metrics.sql
│   ├── 07_gold_hourly_demand.sql
│   ├── 08_gold_airport_metrics.sql
│   ├── 09_validation_checks.sql
│   ├── 10_performance_review.sql
│   └── 11_smoke_test.sql
├── docs/
│   ├── 01_problem_statement.md
│   ├── 02_data_sources.md
│   ├── 03_grain_and_model.md
│   ├── 04_metric_definitions.md
│   ├── 05_data_quality_contract.md
│   ├── 06_pipeline_runs_design.md
│   ├── 07_backfill_plan.md
│   ├── 08_incident_runbook.md
│   ├── 09_query_review.md
│   └── 10_interview_answer.md
├── reports/
│   └── 01_business_summary.md
├── README.md
└── .gitignore
```

Do not submit large raw data files or local database artifacts.

Your `.gitignore` must exclude:

```gitignore
data/raw/*.parquet
data/raw/**/*.parquet
taxi_analytics.duckdb
.cache/
tmp/
```

## 7. Setup Instructions

### 7.1 Create Project Directories

From your repository root:

```bash
mkdir -p homework/month_01_capstone/{sql,docs,reports,data/raw/reference,data/raw/tlc/yellow/year=2024}
cd homework/month_01_capstone
touch README.md .gitignore
```

Create month directories:

```bash
mkdir -p data/raw/tlc/yellow/year=2024/month=01
mkdir -p data/raw/tlc/yellow/year=2024/month=02
mkdir -p data/raw/tlc/yellow/year=2024/month=03
mkdir -p data/raw/tlc/yellow/year=2024/month=04
mkdir -p data/raw/tlc/yellow/year=2024/month=05
mkdir -p data/raw/tlc/yellow/year=2024/month=06
```

### 7.2 Download Data

Download the target 6-month dataset:

```bash
curl -L -o data/raw/tlc/yellow/year=2024/month=01/yellow_tripdata_2024-01.parquet https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet
curl -L -o data/raw/tlc/yellow/year=2024/month=02/yellow_tripdata_2024-02.parquet https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-02.parquet
curl -L -o data/raw/tlc/yellow/year=2024/month=03/yellow_tripdata_2024-03.parquet https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-03.parquet
curl -L -o data/raw/tlc/yellow/year=2024/month=04/yellow_tripdata_2024-04.parquet https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-04.parquet
curl -L -o data/raw/tlc/yellow/year=2024/month=05/yellow_tripdata_2024-05.parquet https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-05.parquet
curl -L -o data/raw/tlc/yellow/year=2024/month=06/yellow_tripdata_2024-06.parquet https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-06.parquet
curl -L -o data/raw/reference/taxi_zone_lookup.csv https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv
```

Verify local files:

```bash
ls -lh data/raw/tlc/yellow/year=2024/month=*/yellow_tripdata_2024-*.parquet
ls -lh data/raw/reference/taxi_zone_lookup.csv
```

### 7.3 Start DuckDB

From `homework/month_01_capstone`:

```bash
duckdb taxi_analytics.duckdb
```

If `duckdb` CLI is not installed, document your local workaround in `README.md`.

## 8. Implementation Plan

### Step 1: Bootstrap Project

File:

```text
sql/00_bootstrap.sql
```

Purpose:

```text
Set up any DuckDB configuration or comments needed to reproduce the project.
```

Keep this file simple. It can include project comments and optional settings.

### Step 2: Create Raw Sources

File:

```text
sql/01_raw_sources.sql
```

Required outputs:

```text
raw_yellow_trips
raw_taxi_zones
```

Expected pattern:

```sql
CREATE OR REPLACE VIEW raw_yellow_trips AS
SELECT *
FROM read_parquet(
  'data/raw/tlc/yellow/year=2024/month=*/yellow_tripdata_2024-*.parquet',
  union_by_name = true
);

CREATE OR REPLACE VIEW raw_taxi_zones AS
SELECT *
FROM read_csv_auto('data/raw/reference/taxi_zone_lookup.csv');
```

### Step 3: Profile Raw Data

Files:

```text
sql/02_raw_profiling.sql
docs/02_data_sources.md
```

Include checks for:

```text
row count
schema / DESCRIBE
minimum and maximum pickup timestamp
minimum and maximum total_amount
minimum and maximum trip_distance
sample records
```

The documentation must summarize what you learned from the raw data.

### Step 4: Define Grain and Model

File:

```text
docs/03_grain_and_model.md
```

Document the grain for every important table:

```text
raw_yellow_trips
silver_taxi_trips
rejected_taxi_trips
dim_taxi_zone
fact_taxi_trips
gold_daily_zone_metrics
gold_hourly_demand
gold_airport_metrics
```

Use this format:

```text
Table: fact_taxi_trips
Grain: one row = one accepted Yellow Taxi trip after quality filters
Primary use: source for business aggregations
```

### Step 5: Build Silver and Rejected Tables

File:

```text
sql/03_silver_trips.sql
```

Required outputs:

```text
silver_taxi_trips
rejected_taxi_trips
```

Minimum silver filters:

```text
pickup and dropoff timestamps are not null
pickup timestamp is earlier than dropoff timestamp
trip_distance > 0
total_amount >= 0
```

`rejected_taxi_trips` must include a `reject_reason` column.

Example reject reasons:

```text
missing_pickup_at
missing_dropoff_at
invalid_trip_time
invalid_distance
negative_total_amount
```

### Step 6: Build Dimension and Fact Tables

Files:

```text
sql/04_dimensions.sql
sql/05_fact_trips.sql
```

Required outputs:

```text
dim_taxi_zone
fact_taxi_trips
```

`dim_taxi_zone` should expose:

```text
location_id
borough
zone
service_zone
```

`fact_taxi_trips` should expose trip-level fields required for downstream aggregations, including:

```text
pickup_at
dropoff_at
service_date
pickup_hour
pickup_location_id
dropoff_location_id
passenger_count
trip_distance
fare_amount
tip_amount
total_amount
payment_type
```

### Step 7: Build Gold Metrics

Files:

```text
sql/06_gold_daily_zone_metrics.sql
sql/07_gold_hourly_demand.sql
sql/08_gold_airport_metrics.sql
```

Required outputs:

```text
gold_daily_zone_metrics
gold_hourly_demand
gold_airport_metrics
```

Minimum metrics for `gold_daily_zone_metrics`:

```text
service_date
pickup_borough
pickup_zone
trip_count
total_revenue
avg_trip_distance
avg_fare_amount
avg_tip_amount
tip_rate
avg_revenue_per_trip
```

`gold_hourly_demand` must include a window function, for example daily demand rank by hour.

`gold_airport_metrics` must isolate airport pickup zones using a documented rule such as:

```text
pickup zone contains 'Airport'
```

### Step 8: Implement Validation Checks

File:

```text
sql/09_validation_checks.sql
```

Required checks:

```text
silver_taxi_trips has rows
rejected_taxi_trips has reject_reason populated
silver_taxi_trips has no negative total_amount
silver_taxi_trips has no trip_distance <= 0
gold_daily_zone_metrics has unique grain
fact_taxi_trips joins to dim_taxi_zone without unexpected missing zones
```

For checks that should return no problems, write the expected outcome in a SQL comment.

Example:

```sql
-- Expected result: 0 rows
SELECT service_date, pickup_borough, pickup_zone, COUNT(*) AS row_count
FROM gold_daily_zone_metrics
GROUP BY 1, 2, 3
HAVING COUNT(*) > 1;
```

### Step 9: Review Performance

Files:

```text
sql/10_performance_review.sql
docs/09_query_review.md
```

Use `EXPLAIN` on one meaningful aggregation query.

In `docs/09_query_review.md`, answer:

```text
Which query is the most expensive?
Does the project filter records before gold aggregations?
Does the query read only necessary columns?
What would you change if the dataset were 100x larger?
```

### Step 10: Add Smoke Test

File:

```text
sql/11_smoke_test.sql
```

The smoke test must return row counts for:

```text
fact_taxi_trips
gold_daily_zone_metrics
gold_hourly_demand
gold_airport_metrics
```

Purpose:

```text
Quickly confirm that the main tables exist and contain data.
```

### Step 11: Write Technical Documentation

Required files:

```text
docs/01_problem_statement.md
docs/04_metric_definitions.md
docs/05_data_quality_contract.md
docs/06_pipeline_runs_design.md
docs/07_backfill_plan.md
docs/08_incident_runbook.md
docs/10_interview_answer.md
```

Minimum expectations:

```text
problem_statement: business user, decision context, scope, non-goals
metric_definitions: exact SQL meaning of each business metric
data_quality_contract: freshness, grain, quality gates, owner, consumer
pipeline_runs_design: fields you would store for each pipeline run
backfill_plan: how to reprocess one old month safely
incident_runbook: how to debug a revenue spike
interview_answer: 10-15 sentence explanation of your design
```

### Step 12: Write Business Summary

File:

```text
reports/01_business_summary.md
```

The report must include 5-8 business insights.

Suggested sections:

```text
Top 5 pickup zones by revenue
Top 5 pickup zones by trip count
Strongest demand hours
Airport revenue share
Month with highest revenue
Data quality observation
Metric interpretation risk
```

This file is for the data consumer, not only for the engineer.

### Step 13: Write Reproducible README

File:

```text
README.md
```

The README must include:

```text
project goal
source data and links
how to download data
how to start DuckDB
SQL execution order
tables/views created by the project
grain and metric summary
validation checks
known limitations
links to docs and business report
```

A reviewer should be able to reproduce your project using only the README and submitted files.

## 9. Final Technical Output

After running the SQL files, the DuckDB database should contain:

```text
raw_yellow_trips
raw_taxi_zones
silver_taxi_trips
rejected_taxi_trips
dim_taxi_zone
fact_taxi_trips
gold_daily_zone_metrics
gold_hourly_demand
gold_airport_metrics
```

## 10. Final Business Output

The business-facing deliverable is:

```text
reports/01_business_summary.md
```

It must clearly explain:

```text
what the most important findings are
which zones, hours, or months stand out
whether the metrics passed validation
what the main data limitations are
how the results should and should not be interpreted
```

## 11. Acceptance Criteria

The project is accepted if all criteria below are met.

### Data and Reproducibility

```text
[ ] Source data can be downloaded from documented URLs.
[ ] README explains how to reproduce the project from scratch.
[ ] Raw data and local DuckDB database are excluded from version control.
[ ] SQL execution order is documented.
```

### SQL and Modeling

```text
[ ] Raw views read Parquet and CSV sources correctly.
[ ] Silver table applies documented quality filters.
[ ] Rejected table stores rejected records with reject reasons.
[ ] Dimension and fact tables are created.
[ ] At least three gold tables are created.
[ ] The project uses JOIN, GROUP BY, CTE, CASE WHEN, and a window function.
[ ] Every major table has documented grain.
```

### Reliability and Operations

```text
[ ] Validation checks are implemented in SQL.
[ ] Unique grain check exists for at least one gold table.
[ ] Join quality check exists for fact-to-dimension relationship.
[ ] Performance review uses EXPLAIN.
[ ] SQL is idempotent, preferably using CREATE OR REPLACE.
[ ] Backfill plan explains how to reprocess one old month.
[ ] Incident runbook explains how to investigate a revenue spike.
[ ] Data quality contract defines freshness, owner, consumer, and quality gates.
```

### Product Quality

```text
[ ] Business summary contains 5-8 clear insights.
[ ] Metric definitions are explicit and reproducible.
[ ] Known limitations are documented.
[ ] Interview answer explains design decisions in plain language.
[ ] Project structure is clean and reviewable.
```

## 12. Recommended Work Plan

Use this order to avoid getting stuck:

```text
Day 1: create folders, download data, create raw views, run profiling
Day 2: build silver and rejected tables, document grain
Day 3: build dimension and fact tables
Day 4: build three gold metric tables
Day 5: add validation checks, smoke test, and EXPLAIN review
Day 6: write metric definitions, data quality contract, README
Day 7: write backfill plan, incident runbook, business summary, interview answer
```

Do not write all documentation at the end from memory. Update docs as you build the project.

## 13. Review Notes for the Student

A strong submission should make the reviewer think:

```text
I can reproduce this project.
I understand the data sources.
I know the grain of every important table.
I can see how bad records are handled.
I can trust the gold metrics because checks exist.
I know how the student would rerun, backfill, and debug the pipeline.
I can explain the business value of the final report.
```

That is the bar for a professional Month 01 capstone.
