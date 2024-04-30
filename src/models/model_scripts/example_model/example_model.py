import pandas as pd

from framework.model import BaseModel


class Model:

    def __int__(self, data_dict: dict):
        self.model = ExampleModel(input_data=data_dict, parameters={})

        self.execute = self.execute()

    def execute(self):
        result = self.model.run()

        return result


class ExampleModel(BaseModel):

    def __init__(self, input_data: dict, parameters: dict = {}):
        super().__init__(input_data, parameters)

    def run(self):
        ecl_data = pd.merge(self.model_data['pd_data'], self.model_data['lgd_data'],
                            on=['customer_id', 'year', 'period_date'], how='left')

        ecl_data = pd.merge(ecl_data, self.model_data['ead_data'],
                            on=['customer_id', 'year', 'period_date'], how='left')

        ecl_data['pit_ecl'] = ecl_data['pit_pd'] * ecl_data['pit_lgd'] * ecl_data['pit_ead']
        ecl_data['avg_ecl'] = ecl_data['avg_pd'] * ecl_data['avg_lgd'] * ecl_data['avg_ead']

        return {'ecl_data': ecl_data}
