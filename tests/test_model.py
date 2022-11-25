import pytest

from src.domain.models import RaspberryPi


@pytest.fixture()
def test_obj():
    yield RaspberryPi()


class TestRaspberryPi:

    def test_ok(self, test_obj):
        assert test_obj is not None
