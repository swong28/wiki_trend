# Wiki Trend

Insight Data Engineering</br>
New York 2019B</br>

## Introduction
Wiki Trend is a tool that recommends users other popular and related Wikipedia articles based on the current Wikipedia article they are browsing. For this project, I am using Wikipedia monthly clickstream data which can accurately captures clickstream activities from Wikipedia. I hope users can discover areas of interests and topics based on their current activity through this tool.

## Motivation
I learned about "Six Degrees of Wikipedia" and it has always fascinated me. "Six Degrees of Wikipedia" is an idea that there will always be a path with less than 6 degrees of seperation between two Wikipedia articles. When I was playing around with this idea, I found a lot of information and knowledge. For example, I learned about "1860 Republican National Convention" on my journey from "Chicago" to "Donald Trump". 

Since people read a lot of Wikipedia posts and there are millions of related articles, my main goal for the Insight Data Engineering Project is to build a tool that can help users to decide other interesting topics that they can read. 

## Demo
I created a tool so that people could learn more about related Wikipedia articles based on the current article they are reading. Here is a video recording of the website I built using Flask:
https://youtu.be/_HAo6FFI2vw

## What does my project do?
### Supported Queries
A user can specify the title of a Wikipedia article.

### Data Source
~30 GB Wikipedia monthly aggregated clickstream data with over 3 millions recorded articles, and 400 millions clickstream.

## Pipeline
![Pipeline for Wiki Trends](https://github.com/swong28/wiki_trend/blob/develop/pipeline/pipeline.png)

## Database Design
### Why Neo4j?
Neo4j is a NoSQL 

