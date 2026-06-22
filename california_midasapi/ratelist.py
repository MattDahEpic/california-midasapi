from datetime import datetime
from .exception import MidasDecodingException
from .internal import MidasInternal
from .types import RateListItem, ValueInfoItem, RateInfo
from typing import Any, Literal
from enum import Enum
import json

class RINFilter(Enum):
        """Filter options for the RIN list."""
        ALL = 0
        TARIFF = 1
        GHG_EMISSION = 2
        FLEX_ALERT = 3

class Midas(MidasInternal):

    async def GetAvailableRates(self, signaltype: RINFilter) -> 'list[RateListItem]':
        """
        Get all the available rates.
        """
        url = 'https://midasapi.energy.ca.gov/api/valuedata?signaltype=' + str(signaltype.value)
        response = await self._request('GET', url)
        parsed = json.loads(response)

        # v2.0 returns {"Rates": [...]}, v1.0 returned bare array
        if isinstance(parsed, dict):
            items = next(iter(parsed.values()))
        else:
            items = parsed

        return [RateListItem(**item) for item in items]
    
    async def GetRateInfo(self, rateID: str, queryType: Literal['alldata', 'realtime'] = 'alldata') -> RateInfo:
        """
        Returns data about a given rate.
        """
            
        # TODO what does queryType=realtime even do? all properties are None
        url = 'https://midasapi.energy.ca.gov/api/valuedata?id=' + rateID + '&querytype=' + queryType
        pricing_response = await self._request('GET', url)

        return self.__parseRateInfoResponse(pricing_response)
    
    async def GetHistoricalRateInfo(self, rateID: str, startDate: datetime, endDate: datetime) -> RateInfo:
        """
        Returns historical data about a given rate during the specified time period.
        """            
        url = 'https://midasapi.energy.ca.gov/api/historicaldata/' + rateID + '?startdate=' + startDate.strftime("%Y-%m-%d") + '&enddate=' + endDate.strftime("%Y-%m-%d")
        pricing_response = await self._request('GET', url)

        return self.__parseRateInfoResponse(pricing_response)
    

    @staticmethod
    def __parseRateInfoResponse(response: str) -> RateInfo:
        """Parse a RateInfo from string."""
        def __rateInfoObjectHook(dict: dict[Any, Any]):
            # this has to handle both the parent object and its children
            if "DateStart" in dict:
                return ValueInfoItem(**dict)
            elif "RateID" in dict:
                return RateInfo(**dict)
            else:
                raise MidasDecodingException("Invalid object type for __rateInfoObjectHook")
        
        return json.loads(response, object_hook=__rateInfoObjectHook)