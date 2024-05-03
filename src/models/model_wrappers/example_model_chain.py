from framework.model_chain import ModelChain

if __name__ == "__main__":
    _config_path = "config/model_config/model_chains/example_model_chain.yml"

    model_chain = ModelChain(_config_path)

    model_chain.run_chain()