from __future__ import print_function
from pyspark.sql import SparkSession
from pyspark import SparkContext as sc
from pyspark.sql import Row
from pyspark.sql.types import *
import sys


def basic_df_example(spark,emp_nom):
    df = spark.read.json("/opt/lampp/htdocs/battle/statistics/files/fil.json")
    df.show()   
    df.printSchema()    
    df.createOrReplaceTempView("emp_no")
    sqlDF = spark.sql("SELECT * FROM emp_no WHERE emp_no=%s" % emp_nom)
    sqlDF.write.format("com.databricks.spark.csv").option("header", "true").save("file.csv")
    sqlDF.show()
    
    
   

if __name__ == "__main__":
   
    spark = SparkSession \
        .builder \
        .appName("Python Spark SQL basic example") \
        .config("spark.some.config.option", "some-value") \
        .getOrCreate()
    basic_df_example(spark,sys.argv[1])

    
spark.stop()		
