import pytest

from src.domain.config_loader import ConfigLoader


@pytest.fixture
def test_obj():
    loader = ConfigLoader()
    yield loader


def test_config_loads(test_obj):
    objects = test_obj.load_from_yaml_file("/home/grzeslav/Learning/Studia/Praca Magisterska/Implementacja/raspi-clus/tests/data/data_to_load.yaml")
    assert objects
