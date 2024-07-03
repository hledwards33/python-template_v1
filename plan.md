# Project Plan

## Phase 1
1. **_Done: Create an input/output layer_**
2. **_Done: Create a model wrapper_** 
3. **_Done: Create a model wrapper and config template_**
4. **_Done: Create an example model_**
5. Write descriptive errors for common mistakes 
6. **_Done: Create method of saving parameters to instance variables_**
7. **_Done: Enforce default nan type values for all dtypes_**
8. **_Done: Create a reconciliation capability_**

## Phase 2
1. **_Done: Create automated logs_**
2. **_Done: Create the ability to read in parquet and zip files_**
3. **_Done: Create memory logging_**
4. **_Done: Create a script that can run models on different data with only a change to the config_**
5. **_Done: Create a model meta-data file (.yaml) - i.e. a yaml to run multiple models_**
6. Test various use cases - write pytests for framework
7. **_Done: Create a "create schema" script with datatype inference_**
8. Add zip and parquet capability to the reconciliation codes
9. **_Done: Make file path calls more robust_** 

## Phase 3
1. **_Done: Create a master script that can chain models_**
2. Look into using airflow to schedule model dependencies
3. Add a pyspark model
4. **_Create a way to save model chain logs: work around in Django framework_**
5. Add comments to all code
6. **_Done: Add type casting to all code_**

## Phase 4 
1. **_Create a Django interface for running models_**
2. **_Output the logs to the Django interface_** 
3. **_Show which model is running and status in the Django interface_**
4. **_Done: Define method to save logs_**
5. Add LGD Starling model as example

## Phase 5
1. Develop a way to package the repo
   * Move the Django app outside the repo so, it can install a packaged version
2. Test framework on a Cloud environment
3. Make changes to allow for running & chaining of models on GCP

## Phase 6
1. Write documentation for this library
   * **_Done: Create the read me file_**
   * Complete all 7 documentation files
     * **_Done: docs 1->4_**
     * Need to complete docs 5->7
2. Robustly test the Django framework

## Phase 7
1. Add bespoke errors and error types

# Feedback

