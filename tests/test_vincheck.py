import pytest
from pyvin import VINError
from pyvin.utils import (clean_vins,
                         validate_vin)
from .vin_samples import (INVALID,
                          HYUNDAI_ELANTRA,
                          TOYOTA_COROLLA)


def test_validate_vin():
    assert validate_vin(TOYOTA_COROLLA) is None
    assert validate_vin(TOYOTA_COROLLA, HYUNDAI_ELANTRA) is None
    with pytest.raises(VINError):
        validate_vin(INVALID)

def test_clean_vins():
    vins = (INVALID, TOYOTA_COROLLA)
    results = clean_vins(vins)
    assert tuple(x for x in vins if x is not INVALID) == results
