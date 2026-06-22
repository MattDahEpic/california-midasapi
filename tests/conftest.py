import pytest


def pytest_addoption(parser):
    parser.addoption("--no-live", action="store_true", default=False, help="skip live API tests")


def pytest_collection_modifyitems(config, items):
    if not config.getoption("--no-live"):
        return
    skip = pytest.mark.skip(reason="--no-live flag set")
    for item in items:
        if "live" in item.keywords:
            item.add_marker(skip)
