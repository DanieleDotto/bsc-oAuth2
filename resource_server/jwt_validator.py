import jwt
from jwt import PyJWKClient

class JwtValidator:
    def __init__(self, jwks_uri: str, audiance: str):
        self.__jwks_uri = self.__validate_jwks_uri(jwks_uri)
        self.__audiance = self.__validate_audiance(audiance)
        
    @property
    def jwks_uri(self) -> str:
        return self.__jwks_uri
    
    @property
    def audiance(self) -> str:
        return self.__audiance
    
    def __validate_jwks_uri(self, jwks_uri: str) -> str:
        if jwks_uri is None:
            raise ValueError('JWKS URI cannot be None')
        if not isinstance(jwks_uri, str):
            raise ValueError('JWKS URI must be a string')
        if not jwks_uri.startswith('https://'):
            raise ValueError('JWKS URI must start with https')
        return jwks_uri
    
    def __validate_audiance(self, audiance: str) -> str:
        if audiance is None:
            raise ValueError('Audiance cannot be None')
        if not isinstance(audiance, str):
            raise ValueError('Audiance must be a string')
        return audiance
    
    def __fetch_signing_key(self, token: str) -> str:
        jwks_client = PyJWKClient(self.jwks_uri)
        public_key = jwks_client.get_signing_key_from_jwt(token)
        return public_key.key
    
    def __get_algorithm(self, token: str) -> str:
        header = jwt.get_unverified_header(token)
        return header['alg']
    
    def is_token_valid(self, encoded_token: str) -> bool:
        if encoded_token is None:
            raise ValueError('Token cannot be None')
        if not isinstance(encoded_token, str):
            raise ValueError('Token must be a string')
        try:
            decoded_token = jwt.decode(jwt=encoded_token, key=self.__fetch_signing_key(encoded_token), audience=self.audiance, algorithms=[self.__get_algorithm(encoded_token)])
        except Exception:
            return False
        return decoded_token is not None

    