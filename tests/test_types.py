"""Test data types handle v2.0 API responses."""

from california_midasapi.types import RateInfo, RateListItem, ValueInfoItem


def test_value_info_item_accepts_int_day():
    """v2.0 API returns DayStart/DayEnd as integers, not strings."""
    item = ValueInfoItem(
        ValueName="Off Peak",
        DateStart="2026-06-22",
        DateEnd="2026-06-22",
        DayStart=1,
        DayEnd=1,
        TimeStart="00:00:00",
        TimeEnd="15:59:59",
        Value=0.25,
        Unit="$/kWh",
    )
    assert item.DayStart == 1
    assert item.DayEnd == 1


def test_value_info_item_accepts_str_day():
    """v1.0 API returned DayStart/DayEnd as strings."""
    item = ValueInfoItem(
        ValueName="Off Peak",
        DateStart="2026-06-22",
        DateEnd="2026-06-22",
        DayStart="1",
        DayEnd="1",
        TimeStart="00:00:00",
        TimeEnd="15:59:59",
        Value=0.25,
        Unit="$/kWh",
    )
    assert item.DayStart == "1"
    assert item.DayEnd == "1"


def test_rate_info_has_signal_type_and_description():
    """v2.0 added SignalType and Description to RateInfo."""
    info = RateInfo(
        RateID="USCA-ELEC-IOUS-SCE1",
        SystemTime_UTC="2026-06-22T12:00:00Z",
        RateName="TOU-D-4-9PM",
        RateType="TOU",
        Sector="Residential",
        API_Url=None,
        RatePlan_Url="https://example.com",
        EndUse="All",
        AltRateName1="",
        AltRateName2=None,
        SignalType="Electricity Rates",
        Description="Time of use rate",
        SignupCloseDate=None,
    )
    assert info.SignalType == "Electricity Rates"
    assert info.Description == "Time of use rate"


def test_rate_list_item_has_signal_type_and_description():
    """v2.0 added SignalType and Description to rate list items."""
    item = RateListItem(
        RateID="USCA-ELEC-IOUS-SCE1",
        SignalType="Electricity Rates",
        Description="SCE TOU-D 4-9PM",
    )
    assert item.SignalType == "Electricity Rates"
    assert item.Description == "SCE TOU-D 4-9PM"
    assert item.LastUpdated is None
