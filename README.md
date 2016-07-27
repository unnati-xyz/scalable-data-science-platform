# Building a scalable Data Science Platform ( Luigi, Apache Spark, Pandas, Flask)
> Fifth Elephant 2016

[Link](https://fifthelephant.talkfunnel.com/2016/64-building-a-scalable-data-science-platform-luigi-ap)

## Abstract

"In theory, there is no difference between theory and practice. But in
practice, there is." - Yogi Berra

Once the task of prototyping a data science solution has been accomplished on a
local machine, the real challenge begins in how to make it work in production.
To ensure that the plumbing of the data pipeline will work in production at
scale is both an art and a science. The science involves understanding the
different tools and technologies needed to make the data pipeline connect,
while the art involves making the trade-offs needed to tune the data pipeline
  so that it flows.

In this workshop, you will learn how to build a scalable data science platform
with set up and conduct data engineering using Pandas and Luigi, build a
machine learning model with Apache Spark and deploy it as predictive api with
Flask

## Outline

The biggest challenge in building a data science platform is to glue all the
moving pieces together. Typically, a data science platform consists of:

- Data engineering - involves a lot of ETL and feature engineering.
- Machine learning - involves writing a bunch of machine learning models and
  persistence of the model
- API - involves exposing end points to the outside world to invoke the
  predictive capabilities of the model

Over time the amount of data stored that needs to be processed increases and it
necessitates the need to run the Data Science process frequently. But different
technologies/stack solve different parts of the Data Science problem. Leaving
it to respective teams introduces lag into the system. What is needed is an
automated pipeline process - one that can be invoked based on business logic
(real time, near-real-time etc) and a guarantee that it will maintain data
integrity.  Details of the workshop

### Data Engineering

We all know that 80% of the effort is spent on data engineering while the rest
is spent in building the actual machine learning models. Data engineering
starts with identifying the right data sources. Data sources can be databases,
third party APIs, HTML documents which needs to be scrapped and so on.
Acquiring data from databases is a straight forward job, while acquiring data
from third party APIs and scrapping may come with its own complexities like
page visit limits, API rate limiting etc. Once we manage to acquire data from
all these sources, the next job is to clean the data.

We will be covering the following topics for data engineering:

- Identifying and working with 2 data sources.
- Writing ETL (Extraction, Transformation and Loading) with Pandas
- Building dependency management with Luigi
- Logging the process
- Adding notifications on success and failure

### Machine Learning

Building a robust and scalable machine learning platform is a hard job. As the
data size increases, the need for more computational capabilities increase. So
how do you build a system that can scale by just adding more hardware and not
worrying about changing the code too much every time? The answer to that is to
use Apache Spark ML. Apache Spark lets us build machine learning platforms by
providing distributed computing capabilities out of the box.

We will be covering the following topics for Machine Learning:

- Feature Engineering
- Hypothesis to solve
- Configuration of environment variables for Apache Pyspark
- Build the Machine Learning code with Apache Spark
- Persisting the model

### API

It ain’t over until the fat lady sings. Making a system API driven is very
essential as it ensures the usage of the built machine learning model , thereby
helping other systems integrate the capabilities with ease.

We will be covering the following topics for API:

- Building REST API with Flask
- Based on the input parameters, build respective methods to extract features to be fed into the model
- Send responses as a JSON

### Pre-Requisites:

- Python - Knowledge of writing classes
- Knowledge of data science:
  - What is data science?
  - Practical use cases for data science?
- Knowledge of machine learning:
  - Expect to know Linear regression and logistic regression
- Knowledge of software engineering:
  - Understanding scalability and high available systems

