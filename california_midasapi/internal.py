from typing import Literal
from aiohttp import ClientError, ClientSession

from .exception import MidasCommunicationException, MidasException, MidasNotFoundException

class MidasInternal():
    """Internal Methods and State used by MIDAS functionality"""
    __session: ClientSession

    def __init__(self, session: ClientSession):
        """
        Create a new API wrapper instance.
        """
        self.__session = session

    async def _request(self, method: Literal['GET', 'POST'], url: str):
        """Preform a request and return the body."""
        try:
            response = await self.__session.request(method, url)
            #TODO retry on 401 before fully throwing
            if response.status == 404:
                raise MidasNotFoundException(f"Requested data not found: {response.status} {await response.text()}")
            if (not response.status == 200):
                raise MidasException(f"Error preforming request: {response.status} {await response.text()}")
            return await response.text()
        except ClientError as exception:
            raise MidasCommunicationException("Connection error occurred while attempting to reach the MIDAS server.") from exception