import jwt
from jwt import PyJWKClient

class JwtValidator:
    """
    A class for validating JSON Web Tokens (JWTs).

    Args:
        jwks_uri (str): The URI of the JSON Web Key Set (JWKS) endpoint.
        audience (str): The intended audience for the JWT.

    Attributes:
        jwks_uri (str): The validated JWKS URI.
        audience (str): The validated audience.

    Raises:
        ValueError: If the JWKS URI or audience is None or not a string.
        ValueError: If the JWKS URI does not start with 'https'.

    Methods:
        is_token_valid(encoded_token: str) -> bool:
            Validates the given encoded JWT.

    """

    def __init__(self, jwks_uri: str, audience: str):
        self.__jwks_uri = self.__validate_jwks_uri(jwks_uri)
        self.__audience = self.__validate_audience(audience)

    @property
    def jwks_uri(self) -> str:
        return self.__jwks_uri

    @property
    def audience(self) -> str:
        return self.__audience

    def __validate_jwks_uri(self, jwks_uri: str) -> str:
        """
        Validates the JWKS URI.

        Args:
            jwks_uri (str): The JWKS URI to validate.

        Returns:
            str: The validated JWKS URI.

        Raises:
            ValueError: If the JWKS URI is None, not a string, or does not start with 'https'.

        """
        if jwks_uri is None:
            raise ValueError('JWKS URI cannot be None')
        if not isinstance(jwks_uri, str):
            raise ValueError('JWKS URI must be a string')
        if not jwks_uri.startswith('https://'):
            raise ValueError('JWKS URI must start with https')
        return jwks_uri

    def __validate_audience(self, audience: str) -> str:
        """
        Validates the audience.

        Args:
            audience (str): The audience to validate.

        Returns:
            str: The validated audience.

        Raises:
            ValueError: If the audience is None or not a string.

        """
        if audience is None:
            raise ValueError('Audience cannot be None')
        if not isinstance(audience, str):
            raise ValueError('Audience must be a string')
        return audience

    def __fetch_signing_key(self, token: str) -> str:
        """
        Fetches the signing key for the given token.

        Args:
            token (str): The token for which to fetch the signing key.

        Returns:
            str: The signing key.

        """
        jwks_client = PyJWKClient(self.jwks_uri)
        public_key = jwks_client.get_signing_key_from_jwt(token)
        return public_key.key

    def __get_algorithm(self, token: str) -> str:
        """
        Gets the algorithm used in the given token.

        Args:
            token (str): The token for which to get the algorithm.

        Returns:
            str: The algorithm used in the token.

        """
        header = jwt.get_unverified_header(token)
        return header['alg']

    def is_token_valid(self, encoded_token: str) -> bool:
        """
        Validates the given encoded JWT.

        Args:
            encoded_token (str): The encoded JWT to validate.

        Returns:
            bool: True if the token is valid, False otherwise.

        Raises:
            ValueError: If the token is None or not a string.

        """
        if encoded_token is None:
            raise ValueError('Token cannot be None')
        if not isinstance(encoded_token, str):
            raise ValueError('Token must be a string')
        try:
            decoded_token = jwt.decode(jwt=encoded_token, key=self.__fetch_signing_key(encoded_token), audience=self.audience, algorithms=[self.__get_algorithm(encoded_token)])
        except Exception:
            return False
        return decoded_token is not None

    