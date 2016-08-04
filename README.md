# Building a scalable Data Science Platform ( Luigi, Apache Spark, Pandas, Flask)
> Fifth Elephant 2016

[[ Proposal ]](https://fifthelephant.talkfunnel.com/2016/64-building-a-scalable-data-science-platform-luigi-ap) [[ Slides] ](https://speakerdeck.com/unnati_xyz/building-scalable-data-science-pipeline)

[How do I run the project after the setup is done?](https://github.com/unnati-xyz/fifthel-2016-workshop/blob/master/app.md)


## Setup

We use Vagrant along with Virtual Box to make our job easier

- To get started you will need Virtual Box. Go download it from
  [here](https://www.virtualbox.org/wiki/Download_Old_Builds_5_0). We highly
  recommend using 5.0 but 5.1 should work just fine as well.
- Once Virtual Box is installed, install Vagrant from
  [here](https://www.vagrantup.com/downloads.html).

By the end of these 2 steps, you should have the `vagrant` executable in your
path.

Once this is done, clone the repository into a location of your choice

```
git clone https://github.com/unnati-xyz/fifthel-2016-workshop.git
```

Then `cd` into the repository directory

```
cd fifthel-2016-workshop
```

From here, you want to bring up the vagrant box. Its quite simple

```
vagrant up
```

This will download the Unnati image and start up the virtual machine. Next
SSH into the machine

```
vagrant ssh
```

Following this, if you see a prompt, then you're good to go :)

## Setup without Vagrant

We **thoroughly** recommend that you use vagrant so that you have everything setup for you. However if you insist on not using it for whatsoever reason (corporate laptop, etc) then the following steps are for you.

The Vagrant box is created with **precisely** the same following steps. We use a Ubuntu 14.04 32 bit Operating System as the base for installation. 

---

Update your `apt`

```
$ sudo apt-get update
```

Install the required packages

```
$ sudo apt-get install build-essential python3-dev python3-pip postgresql-9.3 postgresql-server-dev-9.3 openjdk-7-jdk openjdk-7-jre git-core
```

Install Apache Spark

```
$ cd 
$ wget http://d3kbcqa49mib13.cloudfront.net/spark-1.6.1-bin-hadoop2.6.tgz
$ tar zxvf spark-1.6.1-bin-hadoop2.6.tgz
$ rm spark-1.6.1-bin-hadoop2.6.tgz
```

Next, you need to set a few required environment variables for things to work. This step might change based on your installation

Create a `.exports` file in your home dir to be sourced

```
$ touch ~/.exports
```

Set the `JAVA_HOME` to where the `JDK` is installed

```
$ echo "export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-i386" >> ~/.exports
```

Add `pyspark`'s `bin` directory to `PATH`

```
$ echo "export PATH=/home/vagrant/spark-1.6.1-bin-hadoop2.6/bin:$PATH" >> ~/.exports
```

Set the `SPARK_HOME` variable

```
$ echo "export SPARK_HOME=/home/vagrant/spark-1.6.1-bin-hadoop2.6" >> ~/.exports
```

Set `PYTHONPATH` according to the `SPARK_HOME` variable

```
$ echo "export PYTHONPATH=\$SPARK_HOME/python:\$SPARK_HOME/python/lib/py4j-0.9-src.zip" >> ~/.exports
```

_**Note**: The `\` is for escaping the `$` so that the `$SPARK_HOME` variable isn't evaluated when being added into the file_

You also need to add the repository location into `PYTHONPATH`

```
$ echo "export PYTHONPATH=$PYTHONPATH:/path/to/fifthel-2016-workshop/dir" >> ~/.exports
```

Finally we tell Spark to use Python 3 over 2

```
$ echo "export PYSPARK_PYTHON=/usr/bin/python3" >> ~/.exports
```

We need the `~/.exports` file to be sourced when the shell starts up, so lets do that 

```
$ echo "source ~/.exports" >> ~/.bashrc
```

Next, install all the packages from `requirements.txt` in the repository. **Note**: Since we use vagrant, we install the packages globally. But you might not want to do that if you're installing this on your system. A Virtual environment with `virtualenv` is recommended. Make sure that you create a `virtualenv` with `python3` if you are going down this path.

```
$ cd /path/to/fifthel-2016-workshop/dir
$ sudo pip3 install -r requirements.txt
```

If your PostgreSQL is already configured, then you can skip the following step.

We need to set a password for the `postgres` user and allow login. In order to do this, first login via the `postgres` OS user and set the password using `psql`

```
$ sudo su - postgres
$ psql
postgres=# alter user postgres with password 'postgres';
postgres=# \q
$ logout
```

Back as your regular user, Edit the `pg_hba.conf` 

```
$ sudo vim /etc/postgresql/9.4/main/pg_hba.conf
```

and set change the following line

```
local		all			postgres		peer
```

To

```
local		all			postgres		md5
```

And restart PostgreSQL

```
$ sudo service postgresql restart
```

Now running `psql` should ask you for the password

```
$ psql -U postgres
Password for user postgres:
```

Enter `postgres` at the prompt and you should see the psql prompt.

---

After you've done all this, you should be setup for the workshop :)

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

