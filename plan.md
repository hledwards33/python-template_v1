# Project Plan

## Phase 1
1. **_Done: Create an input/output layer_**
2. **_Done: Create a model wrapper_** 
3. Create a model wrapper template
4. **_Done: Create an example model_**
5. Write descriptive errors for common mistakes 
6. **_Done: Create method of saving parameters to instance variables_**
7. **_Enforce default nan type values for all dtypes_**
8. **_Done: Create a reconciliation capability_**

## Phase 2
1. _**Done: Create automated logs**_
2. Create the ability to read in parquet and zip files
3. _**Done: Create memory logging**_
4. _**Done: Create a script that can run models on different data with only a change to the config**_
5. Create a model meta-data file (.yaml)
6. Test various use cases

## Phase 3
1. Create a master script that can chain models
2. Define chaining of models within the repo
3. Look into using airflow to schedule model dependencies
4. Add a pyspark model

## Phase 4 
1. Create a Django interface for running models
2. Output the logs to the interface 
3. Show which model is running and status in the interface 
4_**DONE: Define method to save logs**_

## Phase 5
1. Develop a way to package the repo
2. Test framework on Cloud
3. Make changes to allow for running & chaining of models on GCP

## Phase 6
1. Write documentation for this library

## Phase 7
1. Add bespoke errors and error types

# Feedback

