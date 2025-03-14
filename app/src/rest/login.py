import functools
import hashlib
import time

import requests

from conf.config import settings


def get_marvel_token():
    public_key = settings.marvel.api_key
    private_key = settings.marvel.private_key
    ts = str(time.time())
    hash_result = hashlib.md5(f"{ts}{private_key}{public_key}".encode('utf-8')).hexdigest()

    params = {
        'ts': ts,
        'apikey': public_key,
        'hash': hash_result,
    }

    url = settings.app.marvel.login_url

    response = requests.get(url, params=params)
    print(response.json())
    

def auth_decorator(func):
    @functools.lru_cache(maxsize=1)
    def get_access_token():
        # auth_url = "https://api.example.com/auth"
        # auth_payload = {"client_id": "seu_id", "client_secret": "seu_segredo"}
        
        # response = requests.post(auth_url, json=auth_payload)
        # data = response.json()

        # expires_in = data.get("expires_in", 3600)
        expiration_time = time.time() + 60

        # return data["access_token"], expiration_time
        return settings.marvel.private_key, expiration_time
        
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        token, expiration = get_access_token()
        if time.time() >= expiration:
            get_access_token.cache_clear()
            token, _ = get_access_token()

        headers = kwargs.get("headers", {})
        headers["Authorization"] = f"Bearer {token}"
        kwargs["headers"] = headers
        print({"args": args, "kwargs": kwargs})
        return func(*args, **kwargs)
    
    return wrapper