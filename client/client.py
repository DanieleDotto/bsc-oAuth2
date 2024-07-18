import requests

class Client:
    """
    Represents a client for making OAuth2 requests.
    """

    def __init__(self, client_id: str, client_secret: str, scope: list[str], url: str):
        """
        Initializes a new instance of the Client class.

        Args:
            client_id (str): The client ID.
            client_secret (str): The client secret.
            scope (list[str]): The list of scopes.
            url (str): The URL for obtaining the access token.

        Raises:
            ValueError: If any of the input parameters are invalid.
        """
        self.__client_id = self.__validate_client_id(client_id),
        self.__client_secret = self.__validate_client_secret(client_secret),
        self.__scope = self.__validate_scope(scope),
        self.__url = self.__validate_url(url)
        
    @property
    def client_id(self) -> str:
        """
        Gets the client ID.

        Returns:
            str: The client ID.
        """
        return self.__client_id
    
    @property
    def client_secret(self) -> str:
        """
        Gets the client secret.

        Returns:
            str: The client secret.
        """
        return self.__client_secret
    
    @property
    def scope(self) -> list[str]:
        """
        Gets the list of scopes.

        Returns:
            list[str]: The list of scopes.
        """
        return self.__scope
    
    @property
    def url(self) -> str:
        """
        Gets the URL for obtaining the access token.

        Returns:
            str: The URL for obtaining the access token.
        """
        return self.__url
    
    def __validate_client_id(self, client_id: str) -> str:
        """
        Validates the client ID.

        Args:
            client_id (str): The client ID to validate.

        Returns:
            str: The validated client ID.

        Raises:
            ValueError: If the client ID is invalid.
        """
        if client_id is None:
            raise ValueError('Client ID cannot be None')
        if not isinstance(client_id, str):
            raise ValueError('Client ID must be a string')
        if len(client_id) != 36:
            raise ValueError('Client ID must be 36 characters long')
        return client_id
    
    def __validate_client_secret(self, client_secret: str) -> str:
        """
        Validates the client secret.

        Args:
            client_secret (str): The client secret to validate.

        Returns:
            str: The validated client secret.

        Raises:
            ValueError: If the client secret is invalid.
        """
        if client_secret is None:
            raise ValueError('Client Secret cannot be None')
        if not isinstance(client_secret, str):
            raise ValueError('Client Secret must be a string')
        return client_secret
    
    def __validate_scope(self, scope: list[str]) -> list[str]:
        """
        Validates the list of scopes.

        Args:
            scope (list[str]): The list of scopes to validate.

        Returns:
            list[str]: The validated list of scopes.

        Raises:
            ValueError: If the scope is invalid.
        """
        if scope is None:
            raise ValueError('Scope cannot be None')
        if not isinstance(scope, str) and not all(isinstance(s, str) for s in scope):
            raise ValueError('Scope must be a list of strings')
        return scope
    
    def __validate_url(self, url: str) -> str:
        """
        Validates the URL.

        Args:
            url (str): The URL to validate.

        Returns:
            str: The validated URL.

        Raises:
            ValueError: If the URL is invalid.
        """
        if url is None:
            raise ValueError('URL cannot be None')
        if not isinstance(url, str):
            raise ValueError('URL must be a string')
        if not url.startswith('https://'):
            raise ValueError('URL must start with https')
        return url
    
    def obtain_jwt(self) -> str:
        """
        Obtains a JWT (JSON Web Token) by making a client credentials grant request.

        Returns:
            str: The access token.

        Raises:
            requests.exceptions.RequestException: If there is an error making the request.
        """
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': self.scope
        }
        return requests.post(self.url, data=payload).json().get('access_token')