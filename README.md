# Social Media Political Analysis 🇺🇸

### Springboard Open-ended Capstone

![SM Political Analysis - 4](https://user-images.githubusercontent.com/65197541/131225592-9e8dd0a0-1750-408f-93d8-72ca04e88e1a.png)

## Objectives

### Problems & Questions

_How can we better develop educational materials to meet kids where they are?_

* Is it worth it to spend money to advertise to youth for political campaigns - are they engaging with current events?
* What politics & policies are The Youth™ talking about & why?

### Goals

* to analyze how age/youth impacts political indoctrination and participation
* to track social impacts of political events
* to understand colloquial knowledge of political concepts

### Overview

1. [x] Use NewsAPI to find top news by day
2. [x] Parse news story title & article into individual words/phrases
3. [x] Count most important individual words & phrases
4. [x]  Use top 3 most important words & phrases to search TikTok & Twitter
5. [x]  Count number of tweets & TikToks mentioning key words & phrases

* I used **Snowflake** because of its proficiency as a batch-loading data warehouse
*  

## Installation & Use

`config.ini` should have the following layout and info:

  ```
  [database]
    host = <hostname>
    database = <db name>
    user = <db username>
    password = <db password>
  
  [newsAuth]
    api_key = <NewsAPI.org API key>

  [tiktokAuth]
    s_v_web_id = <s_v_web_id>
    tt_web_id = <tt_web_id>

  [twitterAuth]
    access_token = <access_token>
    access_token_secret = <access_token_secret>
    consumer_key = <consumer_key>
    consumer_secret = <consumer_secret>
  ```

  *Note*: headers and keys/variables in config.ini file don't need to be stored as strings, but when calling them in program, enclose references with quotes

### To scrape the web without getting blocked

Clone the following url into your project directory using Git or checkout with SVN: `https://github.com/tamimibrahim17/List-of-user-agents.git`. These .txt files contain User Agents and are specified by browser (shout out [Timam Ibrahim](https://github.com/tamimibrahim17)!). They will be randomized to avoid detection by web browsers.

![SM Political Analysis - 4 (7)](https://user-images.githubusercontent.com/65197541/131225638-ba49f6d7-a3e1-46bc-8b54-a71b319b8990.png)

### To find your `s_v_web_id` & `tt_web_id` for TikTokAPI access

1. Go to the TikTok website & login
2. If using Google Chrome, open the developer console
3. Go to the 'Application' tab
4. Find & click 'Cookies' in the left-hand panel →
5. On the resulting screen, look for `s_v_web_id` and `tt_web_id` under the 'name' column

Find more information about `.ini` configuration files in Python documentation: `https://docs.python.org/3/library/configparser.html`

![SM Political Analysis - 4 (2)](https://user-images.githubusercontent.com/65197541/131225593-367e0894-08d3-4fea-ab17-36f274e03c64.png)


## Getting Tweets

This project uses Tweepy's tweet search method to search for tweets within the past seven (7) days using the keywords produced from the `.get_all_news()` method. A separate Tweepy Stream Listener subclass catches tweets (statuses) that contain our keywords of interest as they are tweeted. The max stream rate for Twitter's API (upon which Tweepy is based) is 450.

![SM Political Analysis - 4 (8)](https://user-images.githubusercontent.com/65197541/131225639-88301e11-ed3c-4ab0-8b11-2cbd95d0677c.png) ![SM Political Analysis - 4 (9)](https://user-images.githubusercontent.com/65197541/131225641-d1427eb3-439e-4691-9f3d-9eb9b7cbc2b8.png)

## Getting TikToks

This project uses Avilash Kumar's [TikTokAPI](https://github.com/avilash/TikTokAPI-Python). Refer to their GitHub for further information.

### Common TikTok Streaming Issues

* Make sure you use only one installer (pip or conda or whatever) otherwise dependencies may be broken

## API

### Testing