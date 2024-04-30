# Project Plan

## Phase 1
1. Create an input/output layer
2. Create a model wrapper 
3. Create a model wrapper template
4. Create an example model
5. Write descriptive errors for common mistakes

## Phase 2
1. Create automated logs
2. Create the ability to read in parquet and zip files
3. Create memory logging
4. Create a script that can run models on different data with only a change to the config
5. Create a model meta-data file (.yaml)

## Phase 3
1. Create a master script that can chain models
2. Define chaining of models within the repo
3. Look into using airflow to schedule model dependencies
4. Look into adding a pyspark model

## Phase 4 
1. Create a Django interface for running models
2. Output the logs to the interface 
3. Show which model is running and status in the interface
