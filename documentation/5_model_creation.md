# Model Creation Procedure

## Table of Contents
1. [Repository Layout](#repository-layout)
2. [Model Templates](#model-templates)
   * [Model Config Templates](#model-config-templates)
     * [Model Config Template](#model-config-template)
     * [Model Chain Config Template](#model-chain-config-template)
     * [Model Chain Config Template](#model-chain-config-template)
   * [Model Script Templates](#model-script-templates)
     * [Model Template](#model-template)
     * [Model Chain Template](#model-chain-template)
     * [Model Wrapper Template](#model-wrapper-template)

## Repository Layout
* python-template/
  * config/
    * model_config/...
      * model_chains/...
      * model_metadata/...
      * **_model_chain_config_template.yml**
      * **_model_config_template.yml**
      * **_model_reconciliation_template.yml**
  * data/...
  * documentation/...
    * resources/...
  * interface/
    * interface/...
    * run_chain/...
    * run_model/...
  * model_logs/...
  * src/
    * framework/...
      * setup/...
    * models/
      * model_schemas/...
      * model_scripts/...
        * **_model_template.py**
      * model_wrappers/...
        * **_model_chain_template.py**
        * **_model_wrapper_template.py**
    * utils/...
  * tests/
    * data_reconciliation/
      * framework/...
    * pytests/...
  * venv/...


Within the repository framework there are various templates to help
with the creation of new models. These templates are highlighted in bold
above, note all templates have a leading "_" this is so they stay out of the way, at the top of the directory.

## Model Templates
There are 6 templates in this repository:
1. _model_chain_config_template.yml
2. _model_chain_config_template.yml
3. _model_chain_config_template.yml
4. _model_template.py
5. _model_chain_template.py
6. _model_wrapper_template.py

### Model Config Templates
First we will focus on the model config templates _model_chain_config_template.yml, 
_model_chain_config_template.yml, _model_chain_config_template.yml. 

Note all these templates are .yml files - if you do not have  a yml extension installed in your IDE it would be 
helpful to download one when working with these templates.

#### Model Config Template

#### Model Chain Config Template

#### Model Reconciliation Config Template

### Model Script Templates
Now we will focus on the model script templates _model_template.py, _model_chain_template.py, 
_model_wrapper_template.py.

All these templates are python files so pay special attention to the import statements
is you are going to move your scripts to different directories.

#### Model Template

#### Model Chain Template

#### Model Wrapper Template