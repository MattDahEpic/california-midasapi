from aiohttp import ClientSession
import json
import base64

from .exception import MidasRegistrationException
from .internal import Midas as Internal

class Midas(Internal):
    def __init__(self, session: ClientSession, username: str, password: str):
        """
        Create a new API wrapper instance using the given credentials.

        Credentials are required, if you don't have an account use the static `register` method
        """
        self.username = username
        self.password = password
        self.session = session
        self.auth_token: str = None
    
    async def test_credentials(self) -> bool:
        """Test the provided credentials. Throws if invalid or expired."""
        await self.__loginAndStore(self.username, self.password)
    
    @staticmethod
    async def register(session: ClientSession, username: str, password: str, email: str, fullname: str, organization: str = None) -> str:
        """
        Create a new account with the MIDAS server.
        """
        username64 = str(base64.b64encode(username.encode("utf-8")), "utf-8")
        password64 = str(base64.b64encode(password.encode("utf-8")), "utf-8")
        email64 = str(base64.b64encode(email.encode("utf-8")), "utf-8")
        fullname64 = str(base64.b64encode(fullname.encode("utf-8")), "utf-8")

        registration_info = {
            "username":username64,
            "password":password64,
            "emailaddress":email64,
            "fullname":fullname64
        }

        if (organization is not None):
            organization64 = str(base64.b64encode(organization.encode("utf-8")), "utf-8")
            registration_info["organization"] = organization64

        url = 'https://midasapi.energy.ca.gov/api/registration'
        headers =  {"Content-Type":"application/json"}

        response = await session.post(url, data=json.dumps(registration_info), headers=headers)

        if not response.ok:
            raise MidasRegistrationException(response.text)

        return response.text

