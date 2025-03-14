import re
from typing import Any, Union

from aws_lambda_powertools import Logger
from aws_lambda_powertools.logging.formatter import LambdaPowertoolsFormatter

fields_to_mask = ["sensitive", "sensitive_objects", "sensitive_objects2", "sensitive_list", "password", "secret", "token", "cpfs", "cpf"]


class CustomFormatter(LambdaPowertoolsFormatter):
    def mask_data(self, data: Any, mask_all: bool = False) -> Union[dict, list, Any]:
        
        def resolve_list(data: list) -> list:
            return [self.mask_data(item, mask_all) for item in data]
        def resolve_any(data) -> str:
            return re.sub(r'[A-Za-z0-9]', '*', str(data)) if mask_all else data
        def resolve_dict(data: dict) -> dict:
            return {
                key: self.mask_data(
                    data[key],
                    mask_all=True if mask_all or key.lower() in fields_to_mask else False
                )
                for key in data
            }
        
        if isinstance(data, list):
            return resolve_list(data)
        if not isinstance(data, dict):
            return resolve_any(data)
        return resolve_dict(data)

    def serialize(self, log: dict) -> str:
        return self.json_serializer(self.mask_data(log))

    
logger = Logger(logger_formatter=CustomFormatter())