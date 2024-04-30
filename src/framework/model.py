import logging
from abc import ABC, abstractmethod

import pandas as pd

logger = logging.getLogger()


class BaseModel(ABC):

    def __init__(self, input_data: dict, parameters: pd.DataFrame()):
        self.model_data: dict = input_data

        if not parameters.empty:
            parameters = self.long_to_wide(parameters)

            self.set_parameters(parameters)

    def set_parameters(self, parameters: dict):
        for key, val in parameters.items():
            setattr(self, str(key), val)
            logger.info(f"Parameter '{key}' has been initiated as an instance variable with value {val} and"
                        f" type '{type(val)}'.")

    @staticmethod
    def long_to_wide(df: pd.DataFrame):

        result = df.T

        headers = result.iloc[0]

        result = result[1:]

        result.columns = headers

        result = result.infer_objects()

        for val in result.columns:

            try:
                result[val] = pd.to_numeric(result[val])

            except ValueError:
                pass

            except TypeError:
                pass

        result = result.to_dict(orient='records')[0]

        return result

    @abstractmethod
    def run(self):
        pass
