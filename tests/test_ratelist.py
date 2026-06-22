"""Test rate list parsing handles v2.0 API responses."""

import json
from unittest.mock import AsyncMock, patch

import pytest
from california_midasapi import Midas
from california_midasapi.ratelist import RINFilter
from california_midasapi.types import RateListItem


@pytest.fixture
def midas():
    """Create a Midas instance with a mock session."""
    session = AsyncMock()
    return Midas(session)


@pytest.mark.asyncio
async def test_get_available_rates_v2_dict_response(midas):
    """v2.0 wraps the rate list in {"Rates": [...]}."""
    v2_response = json.dumps({
        "Rates": [
            {"RateID": "USCA-ELEC-IOUS-SCE1", "SignalType": "Electricity Rates", "Description": "SCE rate"},
            {"RateID": "USCA-SGIP-MOER-SCE", "SignalType": "GHG Emissions", "Description": "GHG rate"},
        ]
    })

    with patch.object(midas, "_request", new_callable=AsyncMock, return_value=v2_response):
        rates = await midas.GetAvailableRates(RINFilter.ALL)

    assert len(rates) == 2
    assert isinstance(rates[0], RateListItem)
    assert rates[0].RateID == "USCA-ELEC-IOUS-SCE1"
    assert rates[1].RateID == "USCA-SGIP-MOER-SCE"


@pytest.mark.asyncio
async def test_get_available_rates_v1_list_response(midas):
    """v1.0 returned a bare JSON array."""
    v1_response = json.dumps([
        {"RateID": "USCA-ELEC-IOUS-SCE1", "SignalType": "Electricity Rates", "Description": "SCE rate"},
    ])

    with patch.object(midas, "_request", new_callable=AsyncMock, return_value=v1_response):
        rates = await midas.GetAvailableRates(RINFilter.TARIFF)

    assert len(rates) == 1
    assert isinstance(rates[0], RateListItem)


@pytest.mark.asyncio
async def test_get_rate_info_parses_v2_response(midas):
    """GetRateInfo parses a v2.0 response with Value (capital V) and int DayStart/DayEnd."""
    v2_response = json.dumps({
        "RateID": "USCA-ELEC-IOUS-SCE1",
        "SystemTime_UTC": "2026-06-22T12:00:00Z",
        "RateName": "TOU-D-4-9PM",
        "RateType": "TOU",
        "Sector": "Residential",
        "API_Url": None,
        "RatePlan_Url": "https://example.com",
        "EndUse": "All",
        "AltRateName1": "",
        "AltRateName2": None,
        "SignalType": "Electricity Rates",
        "Description": "SCE TOU rate",
        "SignupCloseDate": None,
        "ValueInformation": [
            {
                "ValueName": "Off Peak",
                "DateStart": "2026-06-22",
                "DateEnd": "2026-06-22",
                "DayStart": 1,
                "DayEnd": 1,
                "TimeStart": "00:00:00",
                "TimeEnd": "15:59:59",
                "Value": 0.25,
                "Unit": "$/kWh",
            }
        ],
    })

    with patch.object(midas, "_request", new_callable=AsyncMock, return_value=v2_response):
        info = await midas.GetRateInfo("USCA-ELEC-IOUS-SCE1")

    assert info.RateID == "USCA-ELEC-IOUS-SCE1"
    assert info.SignalType == "Electricity Rates"
    assert len(info.ValueInformation) == 1
    assert info.ValueInformation[0].Value == 0.25
    assert info.ValueInformation[0].DayStart == 1
