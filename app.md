# How do I get this running?

## Folder structure

```
.
├───data
├───logs
├───luigi_tasks
└───poget
    ├───analytics
    │   ├───data_load
    │   └───ml
    ├───api
    └───utils
```

### data
This folder contains all the csv files required to run the project

### logs
This folder contains the daily logs created by the application

### luigi_tasks
This folder contains the luigi tasks to run. These files internally uses the modules in `poget`

### poget
This is the base application folder which has multiple modules

* `analytics/data_load`

  This module has all the files to load data in csv to postgres db
  
* `analytics/ml`
  
  This module has all the files related to spark machine learning
  
* `api`
  
  This contains the flask application & the endpoints
  
* `utils`

  This contains all the utilities used in the application
  
## Order of execution to see the demo

* Load data from csv to postgres DB

```luigi --module luigi_tasks.load_trip_task LoadTripTask```

* Run the Spark ML model

```luigi --module luigi_tasks.terminal_traffic_task TerminalTrafficTrainTask```

* Run the flask server

```python3 runserver.py```
