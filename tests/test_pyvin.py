import pytest
from pyvin import VIN, VINError, DecodedVIN, RAISE, SKIP, PASS
from pyvin.pyvin import _URL, _SESSION
from .vin_samples import (INVALID,
                          INVALID_SHORT,
                          DECODED_TOYOTA_COROLLA,
                          TOYOTA_COROLLA,
                          HYUNDAI_ELANTRA,
                          BATCH)

def test_vin_single():
    vin = VIN(TOYOTA_COROLLA, error_handling=SKIP)
    assert isinstance(vin, DecodedVIN)

    vin = VIN(TOYOTA_COROLLA, error_handling=RAISE)
    assert isinstance(vin, DecodedVIN)

def test_vin_single_invalid():
    vins = VIN(INVALID, error_handling=SKIP)
    assert vins == []

    with pytest.raises(VINError):
        VIN(INVALID, error_handling=RAISE)

def test_vin_single_invalid_short():
    vin = VIN(INVALID_SHORT, error_handling=SKIP)
    assert vin == []

    with pytest.raises(VINError):
        VIN(INVALID_SHORT, error_handling=RAISE)

def test_vin_single_invalid_empty():
    vin = VIN('', error_handling=SKIP)
    assert vin == []

    with pytest.raises(VINError):
        VIN('', error_handling=RAISE)

def test_vin_single_invalid_none():
    vin = VIN(None, error_handling=SKIP)
    assert vin == []

    with pytest.raises(VINError):
        VIN(None, error_handling=RAISE)

def test_vin_multi_minimal():
    """When multiple vins are input (Iterable or as separate args),
    return a list of decoded vins
    """
    samples = (TOYOTA_COROLLA, HYUNDAI_ELANTRA)
    vins = VIN(*samples)
    assert len(samples) == len(vins)
    for vin in vins:
        assert isinstance(vin, DecodedVIN)

def test_vin_multi_large_batch():
    samples = BATCH
    vins = VIN(*samples)
    assert len(samples) == len(vins)

def test_invalid_in_multi():
    samples = (INVALID, TOYOTA_COROLLA)
    vins = VIN(*samples)
    assert isinstance(vins, DecodedVIN)
    assert len([x for x in samples if x is not INVALID]) == 1

def test_invalid_in_multi_raise():
    samples = (INVALID, TOYOTA_COROLLA)
    with pytest.raises(VINError):
        VIN(*samples, error_handling=RAISE)

def test_invalid_in_multi_pass():
    samples = (INVALID, TOYOTA_COROLLA)
    vins = VIN(*samples, error_handling=PASS)
    assert len(samples) == len(vins)

def test_vin_attrs():
    vin = VIN(TOYOTA_COROLLA)
    attrs = {k: v for k, v in vin.__dict__.items() if '__' not in k}
    assert attrs == DECODED_TOYOTA_COROLLA
