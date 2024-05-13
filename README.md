# Python Template

## Table of Contents
* [Repository Usage](#repository-usage)
  * [Overview of Model Framework](#overview-of-model-framework)
* [Contributing to the repository](#contributing-to-the-repository)
* [Repository Contacts](#repository-contacts)
* [Additional Documentation](#additional-documentation)

## Repository Usage
This repository provides a framework to standardise the scripting on financial 
models in python. Within this framework models can be run in chain, recursively
or individually.

**IMPORTANT:** src folder must be set as the **_content root_** for this repository.
_right click: src > mark directory as > sources root_.

### Overview of Model Framework
1. Input data is loaded from either csv, zip or parquet file format.
2. Data types are enforced from data schemas.
3. Input data processing is applied to standardise all datasets.
4. Input data is passed to the model.
5. Model is run.
6. Model passes output data to model framework.
7. Output data processing is applied to standardise all datasets.
8. Data types are checked against data schemas.
9. Output data is saved to either csv, zip or parquet file format.

## Contributing to the Repository

## Repository Contacts
Please contact Harry Edwards [harry.edwards@uk.ey.com](mailto:harry.edwards@uk.ey.com) 
with any queries regarding the use, behaviour or functionality of this repository.

## Additional Documentation
For additional information on the framework defined in this repository please see the 
[documentation folder](https://github.com/hledwards33/python-template/tree/master/documentation).