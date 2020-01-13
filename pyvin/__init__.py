from .pyvin import (VIN,
                    DecodedVIN,
                    RAISE,
                    SKIP,
                    PASS)
from .errors import VINError
from .utils import clean_vins, validate_vin

_VERSION = '0.0.1'

def get_version():
    return _VERSION
