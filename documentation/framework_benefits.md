# Model Framework Benefits

## Table of Contents
1. [Benefits of a Standardised Framework](#benefits-of-a-standardised-framework)
2. [Prebuilt Capabilities](#prebuilt-capabilities)
3. [Future Updates](#future-updates)

## Benefits of a Standardised Framework
There are a number of benefits to  using a standardised framework, 
the benefits relevant to this framework are listed below.

* **Trust**: This framework has been tested and improved upon. You do not need to 
reinvent the wheel
* **Re-usability**: This framework is designed around the principles of object-oriented programming,
the design will reduce the amount of new code needed to be written.
* **Support**: With better adoption of the framework comes better support available within
the team.
* **No Key-Person Dependency**: The more people who understand how to use this framework the easier 
resourcing becomes.
* **Less Training Needed**: Once a resource has worked with the framework once they will be able to 
switch to other projects using this framework without the need for onboarding.
* **EY Enhancements**: The README file of this framework prescribes methods for making enhancements as the
framework follows well-defined patterns enhancements can be brought back from client work and re-used.
* **Utilities**: Each time a repetitive task (i.e. schema creation) is required a utilities method is defined, these methods
are collated within the utilities directory and available to all users of the repository.

## Prebuilt Capabilities
This framework has a number of in-built capabilities designed to save the modeller time and effort.
This also reduces the chances of mistakes as we are using the same tested code over and over again.

* **Logging Framework**: 
  * The framework configures and creates a logging framework to monitor and document model 
  processes
  * The framework also allows customisation of the = log file names enable a tracked model history to be created. 
    * Ability to include date for model logs
    * Ability to include date and data for reconciliation logs
  * Model logs are pre-formatted for readability and automatically written to a file and console.
  * All Models memory usage and run-time are also logged by default.
* **Read/Write**: The framework provides standardised and tested read/write functions for .yaml, .sv and .zip file extensions.
* **Model Chaining**: The framework is designed to allow the chaining of models so that regular model patters can be predefined
for ease of use. This also help guard against errors in the model run order.
* **Model Code Protection**: The framework is designed so that the end user need not see the model code or have access to model data,
this allows processes to be access by more individuals.

* **Web Application**:
  * This framework comes with a ready to go django web application
  * This web application allows the execution of any model configuration stored within the repo,
  along with the execution of any model chain run configuration.
  * The web application automatically presents the model to the user's inspection upon 
  execution.
  * The web application does not require any extra installations the database running in the 
  back-end come inbuilt with python.

## Future Updates
As we continuously improve the framework some upcoming features you can expect to see are:
* **Pyspark**: Ability to run models within a spark context built into the framework.
* **Releases**: Ability to package and release the repo so that it can be imported into other projects.
* **Cloud Compatibility**: Ability to run models defined within the framework in a cloud environment.
