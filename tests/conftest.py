import pytest


@pytest.mark.tryfirst
def pytest_configure(config) -> None:
    config.option.asyncio_mode = "auto"
