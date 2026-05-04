from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp

# Spark Session (S3 ready)
spark = SparkSession.builder \
    .appName("Silver Sales Transformation") \
    .getOrCreate()

# Read raw data (keep local OR move later to S3 ingestion)
df = spark.read.csv(
    "s3a://retail-sales-lake-prashant-2026-793477409422-eu-north-1-an/raw/sales_transactions.csv",
    header=True,
    inferSchema=True
)

# Transformations
silver_df = df.dropDuplicates() \
    .filter(col("quantity") > 0) \
    .filter(col("price") > 0) \
    .withColumn("processed_timestamp", current_timestamp())

# Write to S3 (IMPORTANT FIX)
silver_df.write.mode("overwrite").parquet(
    "s3a://retail-sales-lake-prashant-2026-793477409422-eu-north-1-an/silver/sales_transactions/"
)

print("Silver layer completed successfully")

spark.stop()