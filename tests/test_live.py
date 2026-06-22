"""Integration tests against the live MIDAS v2.0 API.

These hit the real API (no auth required) and are skipped in CI
unless explicitly opted in with: pytest -m live
"""

import aiohttp
import pytest
import pytest_asyncio
from california_midasapi import Midas
from california_midasapi.ratelist import RINFilter
from california_midasapi.types import RateInfo, RateListItem, ValueInfoItem

pytestmark = pytest.mark.live


@pytest_asyncio.fixture
async def midas():
    async with aiohttp.ClientSession() as session:
        yield Midas(session)


@pytest.mark.asyncio
async def test_get_available_rates(midas):
    """GetAvailableRates returns a list of RateListItem objects."""
    rates = await midas.GetAvailableRates(RINFilter.ALL)
    assert len(rates) > 0
    assert isinstance(rates[0], RateListItem)
    assert rates[0].RateID
    assert rates[0].SignalType
    assert rates[0].Description


@pytest.mark.asyncio
async def test_get_available_rates_tariff_filter(midas):
    """Filtering by TARIFF returns only electricity rate RINs."""
    rates = await midas.GetAvailableRates(RINFilter.TARIFF)
    assert len(rates) > 0
    assert all(r.SignalType == "Electricity Rates" for r in rates)


@pytest.mark.asyncio
async def test_get_available_rates_ghg_filter(midas):
    """Filtering by GHG_EMISSION returns only GHG RINs."""
    rates = await midas.GetAvailableRates(RINFilter.GHG_EMISSION)
    assert len(rates) > 0
    assert all("GHG" in r.SignalType or "Emission" in r.SignalType for r in rates)


@pytest.mark.asyncio
async def test_get_rate_info(midas):
    """GetRateInfo returns a RateInfo with tariffs."""
    rates = await midas.GetAvailableRates(RINFilter.TARIFF)
    rin = rates[0].RateID

    info = await midas.GetRateInfo(rin)
    assert isinstance(info, RateInfo)
    assert info.RateID == rin
    assert info.RateName
    assert info.SignalType
    assert isinstance(info.ValueInformation, list)


@pytest.mark.asyncio
async def test_rate_info_tariffs_are_typed(midas):
    """ValueInformation entries are ValueInfoItem with correct field types."""
    rates = await midas.GetAvailableRates(RINFilter.TARIFF)
    info = await midas.GetRateInfo(rates[0].RateID)

    if len(info.ValueInformation) > 0:
        t = info.ValueInformation[0]
        assert isinstance(t, ValueInfoItem)
        assert isinstance(t.Value, (int, float))
        assert isinstance(t.DayStart, (str, int))
        assert isinstance(t.Unit, str)
