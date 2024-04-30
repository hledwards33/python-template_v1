import pandas as pd

from framework.model import BaseModel

import logging

logger = logging.getLogger()


class Model:

    def __init__(self, data_dict: dict, parameters: pd.DataFrame = pd.DataFrame()):
        self.model = ExampleModel(input_data=data_dict, parameters=parameters)

        self.execute = self.execute()

    def execute(self):
        result = self.model.run()

        return result


class ExampleModel(BaseModel):

    def __init__(self, input_data: dict, parameters: pd.DataFrame = pd.DataFrame()):
        super().__init__(input_data, parameters)

    def run(self):

        logger.info("Joining PD and LGD Datasets.")
        ecl_data = pd.merge(self.model_data['pd_data'], self.model_data['lgd_data'],
                            on=['customer_id', 'year', 'period_date'], how='left')

        logger.info("Joining PD and EAD Datasets.")
        ecl_data = pd.merge(ecl_data, self.model_data['ead_data'],
                            on=['customer_id', 'year', 'period_date'], how='left')

        logger.info("Calculating ECL.")
        ecl_data['pit_ecl'] = ecl_data['pit_pd'] * ecl_data['pit_lgd'] * ecl_data['pit_ead']
        ecl_data['avg_ecl'] = ecl_data['avg_pd'] * ecl_data['avg_lgd'] * ecl_data['avg_ead']

        return {'ecl_data': ecl_data}
