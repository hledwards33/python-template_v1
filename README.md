# Python Template


## Table of Contents
* [Repository Usage](#repository-usage)
  * [Overview of Model Framework](#overview-of-model-framework)
* [Contributing to the repository](#contributing-to-the-repository)
  * [Large Scale Changes](#large-scale-changes)
  * [Small Changes / Fixes](#small-changes--fixes)
  * [Improving Documentation](#improving-documentation)
  * [Example Use Cases](#example-use-cases)
* [Repository Contacts](#repository-contacts)
* [Additional Documentation](#additional-documentation)

## Repository Usage
This repository provides a framework to standardise the scripting of financial 
models in python. Within this framework, models can be run in sequence recursively
or individually.

**IMPORTANT:** src folder must be set as the **_content root_** for this repository.
_right click: src > mark directory as > sources root_.

### Overview of Model Framework
1. Input data is loaded from either csv, zip or parquet file format.
2. Data types are enforced from data schemas.
3. Input data processing is applied to standardise all datasets.
4. Input data is passed to the model.
5. Model is run.
6. Model passes output data back to the model framework.
7. Output data processing is applied to standardise all datasets.
8. Data types are checked against data schemas and conformance errors are raised.
9. Output data is saved to either csv, zip or parquet file format.

## Contributing to the Repository
Contributions to this repository are welcomed. If you would like to discuss or
assistance with your proposed changes, please contact any of the 
[repository contacts](#repository-contacts).

### Large Scale Changes
To add new functionalities or restructure the framework layout, please:
* Create a fork of this repository.
* Complete and test all changes in the forked repository.
* Create a pull request back to the main repository and tag a repository contact as reviewer.

### Small Changes / Fixes
To fix a bug in the framework or add a small utility, please:
* Contact a repository contact to gain write level access.
* Create a branch to apply and test changes.
* Create a pull request back to the main repository branch and tag a repository contact as reviewer.

### Improving Documentation
To improve the documentation of the repository or to add new documentation, please 
follow the same steps as small changes / fixes.

### Example Use Cases
If you have used this repository, the likelihood is that your work will be useful to others.
To continue to grow and build this repository, please reach out to a repository contact
to tag your repository as an example use case.

## Repository Contacts
Please contact Harry Edwards [harry.edwards@uk.ey.com](mailto:harry.edwards@uk.ey.com) 
with any queries regarding the use, behaviour or functionality of this repository.

## Additional Documentation
For additional information on the framework defined in this repository, please see the 
[documentation folder](https://github.com/hledwards33/python-template/tree/master/documentation). It is suggested to read the additional documentation in the 
following order:
1. model_framework
2. framework_benefits
3. model_chaining
4. model_utils
5. model_creation
6. model_reconciliation
7. model_interface