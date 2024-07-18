import requests

class Client:
    def __init__(self, client_id: str, client_secret: str, scope: list[str], url: str):
        self.__client_id = self.__validate_client_id(client_id),
        self.__client_secret = self.__validate_client_secret(client_secret),
        self.__scope = self.__validate_scope(scope),
        self.__url = self.__validate_url(url)
        
    @property
    def client_id(self) -> str:
        return self.__client_id
    
    @property
    def client_secret(self) -> str:
        return self.__client_secret
    
    @property
    def scope(self) -> list[str]:
        return self.__scope
    
    @property
    def url(self) -> str:
        return self.__url
    
    def __validate_client_id(self, client_id: str) -> str:
        if client_id is None:
            raise ValueError('Client ID cannot be None')
        if not isinstance(client_id, str):
            raise ValueError('Client ID must be a string')
        if len(client_id) != 36:
            raise ValueError('Client ID must be 36 characters long')
        return client_id
    
    def __validate_client_secret(self, client_secret: str) -> str:
        if client_secret is None:
            raise ValueError('Client Secret cannot be None')
        if not isinstance(client_secret, str):
            raise ValueError('Client Secret must be a string')
        return client_secret
    
    def __validate_scope(self, scope: list[str]) -> list[str]:
        if scope is None:
            raise ValueError('Scope cannot be None')
        if not isinstance(scope, str) and not all(isinstance(s, str) for s in scope):
            raise ValueError('Scope must be a list of strings')
        return scope
    
    def __validate_url(self, url: str) -> str:
        if url is None:
            raise ValueError('URL cannot be None')
        if not isinstance(url, str):
            raise ValueError('URL must be a string')
        if not url.startswith('https://'):
            raise ValueError('URL must start with https')
        return url
    
    def obtain_jwt(self) -> str:
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': self.scope
        }
        return requests.post(self.url, data=payload).json().get('access_token')