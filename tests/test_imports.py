"""Test that the package imports correctly."""


def test_import_midas():
    """Midas class is importable from the top-level package."""
    from california_midasapi import Midas

    assert Midas is not None


def test_import_types():
    """Core data types are importable."""
    from california_midasapi.types import RateInfo, RateListItem, ValueInfoItem

    assert RateInfo is not None
    assert RateListItem is not None
    assert ValueInfoItem is not None


def test_import_exceptions():
    """Exception classes are importable."""
    from california_midasapi.exception import (
        MidasCommunicationException,
        MidasDecodingException,
        MidasException,
        MidasRegistrationException,
    )

    assert issubclass(MidasCommunicationException, MidasException)
    assert issubclass(MidasDecodingException, MidasException)
    assert issubclass(MidasRegistrationException, MidasException)


def test_import_ratelist_filter():
    """RINFilter enum is importable."""
    from california_midasapi.ratelist import RINFilter

    assert RINFilter.ALL.value == 0
    assert RINFilter.TARIFF.value == 1
    assert RINFilter.GHG_EMISSION.value == 2
    assert RINFilter.FLEX_ALERT.value == 3
