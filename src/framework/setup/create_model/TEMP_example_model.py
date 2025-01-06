import logging

import pandas as pd

from framework.setup.create_model.model import IModel

logger = logging.getLogger()


class ExampleModel(IModel):

    def __init__(self, input_data: dict, parameters: dict):
        super().__init__(input_data, parameters)

    def run(self):
        logger.info("Joining PD and LGD Datasets.")
        ecl_data = pd.merge(self.data['pd_data'], self.data['lgd_data'],
                            on=['customer_id', 'year', 'period_date'], how='left')

        logger.info("Joining PD and EAD Datasets.")
        ecl_data = pd.merge(ecl_data, self.data['ead_data'],
                            on=['customer_id', 'year', 'period_date'], how='left')

        logger.info("Calculating ECL.")
        ecl_data['pit_ecl'] = ecl_data['pit_pd'] * ecl_data['pit_lgd'] * ecl_data['pit_ead']
        ecl_data['avg_ecl'] = ecl_data['avg_pd'] * ecl_data['avg_lgd'] * ecl_data['avg_ead']

        return {'ecl_data': ecl_data}
