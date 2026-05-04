from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, count, col

# Spark Session
spark = SparkSession.builder \
    .appName("Gold KPI Aggregation") \
    .getOrCreate()

# Read Silver from S3
df = spark.read.parquet(
    "s3a://retail-sales-lake-prashant-2026-793477409422-eu-north-1-an/silver/sales_transactions/"
)

# Create total_sales (IMPORTANT FIX: cast to DOUBLE for Athena)
df = df.withColumn(
    "total_sales",
    (col("quantity") * col("price")).cast("double")
)

# KPI Aggregation
gold_df = df.groupBy("region").agg(
    sum("total_sales").alias("region_total_sales"),
    count("transaction_id").alias("total_transactions")
)

# Write Gold to S3
gold_df.write.mode("overwrite").parquet(
    "s3a://retail-sales-lake-prashant-2026-793477409422-eu-north-1-an/gold/region_sales_kpi/"
)

print("Gold KPI layer completed successfully")

spark.stop()