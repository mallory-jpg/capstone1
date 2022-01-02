# Architectural Decision Record
Social Media Political Analysis (SMPA) Pipeline 

## Background

### Exploratory Data Analysis

![SM Political Analysis - 4 (4)](https://user-images.githubusercontent.com/65197541/131225599-038ec36c-d644-4f60-a8f2-0bd43ade94df.png)

This step was guided by my anticipation that the data will be used for trend graphing, sentiment analysis, age inference, and correlation between user characteristics and extent of participation in responding to political events. With this in mind, I plan to optimize query speed via limiting storage by geographic location of both users and events to the US (though this categorization may be loose at times because of US involvement on the world stage). My PostgreSQL database will also be sharded by datetime, as the analytical window references 3 days before and 3 days after the political event of interest.

The article text in the news table will serve as data sources from which to extract our top 3 keywords (per article) using Term Frequency-Inverse Document Frequency (TF-IDF) calculations. These keywords will be applied to our searches for related TikToks and tweets. For some resources on this, check out
[TF-IDF in the real world](https://towardsdatascience.com/tf-idf-for-document-ranking-from-scratch-in-python-on-real-world-dataset-796d339a4089) and [a step-by-step guide by Prachi Prakash](https://www.analyticsvidhya.com/blog/2020/11/words-that-matter-a-simple-guide-to-keyword-extraction-in-python/).

![SM Political Analysis - 4 (10)](https://user-images.githubusercontent.com/65197541/131225642-20b9ca15-5777-474a-a13d-0693c7b74db3.png)

![SM Political Analysis - 4 (11)](https://user-images.githubusercontent.com/65197541/131225643-0ff23457-eada-4b2a-98d0-256e8ecd5df7.png)

With data from social media adding a pop-cultural context to political news, we inch closer to an understanding of TikTok and Twitter as novel forms of youth political engagement!

![SM Political Analysis - 4 (12)](https://user-images.githubusercontent.com/65197541/131225654-089ce37f-7f7d-42b9-8972-5dba199252f8.png)

### Summary

The ETL pipeline code will call multiple APIs (NewsAPI, Tweepy, & TikTok), transform the data in Python, and load that data into Postgres. Because this is pretty niche data, there is a small enough amount of data ingested to justify an ETL approach.

1. NewsAPI finds top news by day
2. Parse news story titles and their article text into individual words and phrases
3. Determine 3 most important individual words and phrases
4. Use key words as filters for TikTok and Twitter data 
5. Count the number of tweets and TikToks mentioning key words and phrases

### ??

### ???


# Solution

## Summary

PgAdmin UI
Postgres as DW


### Architecture Diagram

<//>

## Data Lifecycle & <?>

Data is batch-ingested into ...

## API

Data is served through a Flask API

### Technology

* GraphQL: more efficient than REST due to compound requests pulling data in one lump sum

### Security 

* Rate-limiting factors
* Firewall
* TLS encryption

### Performance

* Caching

### Testing

* Testing in isolation for funtionality, reliability, latency, performance, security, etc.
* Testing with JSON payloads over HTTP, HTTPS, JMS, & MQ
* Unit testing: individual operations of API in logical unit divisions to ID imperfections in early stages
* Functional testing: testing all functions in codebase, using unit tests as building blocks
* Load testing: validating functionality and performance under load to ensure it will work as expected with multiple concurrent users
* Runtime error detection: monitoring API by running it in its entirety to check for errors, exceptions, and prevent resource leaks
* Security testing: checking for external threats, validation, access control, and data encryption
* Penetration testing: to find vulnerabilities in system or codebase that could be exploited by attackers, testing vulnerability of functions and security assets
* Fuzz testing: utilizes random input data (aka fuzz) to rest reliability and ensure reliability in worst-case

## Rejected Solutions

### Kafka streaming

* no need to stream updates

### Transforming with dbt

* don't need dbt with pyspark sql transformations