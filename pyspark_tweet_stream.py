import pyspark
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.functions import col, split
import logging

spark = SparkSession.builder.appName("Tweet Stream").getOrCreate()

blobname = ''
containername = ''

# spark._jsc.hadoopConfiguration().set("fs.azure.account.keyprovider.{blobname}.blob.core.windows.net","org.apache.hadoop.fs.azure.SimpleKeyProvider")
# spark._jsc.hadoopConfiguration().set("fs.azure.account.key.{blobname}.blob.core.windows.net","{storagekey == }")
# spark.read.csv("wasb://{containername}@{blobname}.blob.core.windows.net/students/students.csv").show()

# setup Spark with Kafka
tweet_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "host1:port1,host2:port2") \
    .option("subscribe", "politics") \
    .load()

# Type cast the key and column value
tweet_df_string = tweet_df.selectExpr(
    "CAST(key AS STRING)", "CAST(value AS STRING)")

# split words based on space, filter out hashtags
tweets_tab = tweet_df_string.withColumn('word', explode(split(col('value'), ' '))) \
    .groupBy('word') \
    .count() \
    .sort('count', ascending=False). \
    filter(col('word').contains('#'))

# write data into memory
writeTweet = tweets_tab.writeStream. \
    outputMode("complete"). \
    format("memory"). \
    queryName("tweetquery"). \
    trigger(processingTime='2 seconds'). \
    start()

print("----- streaming is running -------")

# show data
spark.sql("select * from tweetquery").show()

# Stop the query
writeTweet.stop()
# check status
writeTweet.status
writeTweet.isActive
