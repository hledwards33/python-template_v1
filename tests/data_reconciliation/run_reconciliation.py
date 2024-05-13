from tests.data_reconciliation.framework.reconciliation_full_analysis import run_full_data_reconciliation

if __name__ == "__main__":
    kwargs = {
        'sys_config_path': r"config/system_config.yml",
        'recon_config_path': r"config/model_config/example_model/example_model_reconciliation_config.yml"
    }

    run_full_data_reconciliation(**kwargs)
