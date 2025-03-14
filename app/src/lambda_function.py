import json

import requests

from observability.logger import logger
from rest.login import auth_decorator


@logger.inject_lambda_context
def lambda_handler(event, context):
    @auth_decorator
    def get_pokemon(url, **kwargs):
        requests.get(url, **kwargs)
    
    logger.info("Hello from Lambda!", extra={"event": event})
        
    response = get_pokemon("https://pokeapi.co/api/v2/pokemon/pikachu")
    
    print(response.json())
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
    
if __name__ == "__main__":
    class Context:
        def __init__(self):
            self.function_name = "test"
            self.function_version = "1"
            self.memory_limit_in_mb = 1024
            self.invoked_function_arn = "arn:aws:lambda:us-east-1:123456789012:function:test"
            self.aws_request_id = "test"
    event = {
        "payload": {
            "password": "supersecret",
            "username": "admin",
            "something": {
                "secret": "donttell"
            },
            "test": "test",
            "sensitive": {
                "idade": 36,
                "trabalha"  : True,
                "nome": "Anderson",
                "endereco": "Rua 1",
                "cpf": "123.456.789-00"              
            }
        },
        "sensitive_objects": [
            {
                "cpf": "123.456.789-00",
                "access_token": "sometoken"
            },
            {
                "cpf": "987.654.321-00",
                "refresh_token": "sometoken"
            }
        ],
        "sensitive_list": [
           ["123.456.789-00", "987.654.321-00"],
           ["123.456.789-00", "987.654.321-00"]
        ],
        "sensitive_objects2": [
            {
                "list": ["123.456.789-00","987.654.321-00"]
            }
        ],
        "test": "test",
        "token": "sometoken",
        "cpfs": ["123.456.789-00", "987.654.321-00"],
        "normal": ["A", "B"]
    }
    
    lambda_handler(event, Context())