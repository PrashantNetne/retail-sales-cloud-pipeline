from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = SparkSession.builder.appName("Practice Application").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

df= spark.read.csv("practice/datasets/sales.csv",inferSchema=True,header=True)
df.show()
print("Total Rows before:", df.count())
df=df.dropDuplicates()
df.show()
print("Total Rows after:", df.count())
print("pyspark job completed !!")
df.printSchema()
df.filter(col("quantity")>0)
print("After Filter of quantity greater that zero:", df.count())
df=df.filter(col("customer_id").isNotNull())
print("After not null applied:",df.count())
df=df.withColumn("region",trim(upper(col("region"))))
df.select("region").show()
df=df.withColumn("Total_sales",col("quantity")* col("price"))
df.select("Total_sales").show()
spark.stop()