# Homework: Build Your Own dlt Pipeline

## Question 1: What is the start date and end date of the dataset?

### Answer 1: 
´´´
SELECT
    MIN(trip_pickup_date_time) AS min_pickup_ts,
    MAX(trip_pickup_date_time) AS max_pickup_ts
FROM taxi_pipeline_pipeline_dataset.rides;
```
min_pickup_ts             max_pickup_ts
 2009-06-01 13:33:00+02:00 2009-07-01 01:58:00+02:00

## Question 2: What proportion of trips are paid with credit card?

### Answer 2: 
```
SELECT
    COUNT(*) AS total_trips,
    SUM(CASE WHEN payment_type = 'Credit' THEN 1 ELSE 0 END) AS credit_trips,
    ROUND(
        100.0 * SUM(CASE WHEN payment_type = 'Credit' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS credit_share_pct
FROM taxi_pipeline_pipeline_dataset.rides;
```
total_trips  credit_trips  credit_share_pct
       10000        2666.0             26.66

## Question 3. What is the total amount of money generated in tips?

### Answer 3.

```
SELECT
    ROUND(SUM(tip_amt), 2) AS total_tip_amount
FROM taxi_pipeline_pipeline_dataset.rides;

```
total_tip_amount
          6063.41