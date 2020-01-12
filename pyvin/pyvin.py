from typing import List
from requests import Session
from .errors import VINError
from .utils import validate_vin

URL = 'https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValuesBatch/'
_DEFAULT_PARAMS = {'format': 'json'}
_SESSION = Session()
_MAX_BATCH_SIZE = 100

class DecodedVIN():
    def __init__(self, data: dict):
        self.__dict__.update(data)

def _decode_vin_values(vins: List[str], raise_for_error: bool = True):
    if len(vins) > _MAX_BATCH_SIZE:
        raise VINError('VIN count exceeds Max Batch Size of %s' % _MAX_BATCH_SIZE)
    # If vins are not vali
    for vin in vins:
        validate_vin(vin)
    vin_str = ';'.join(vins)
    resp = _SESSION.post(url=URL, params=_DEFAULT_PARAMS, data=vin_str)
    data = resp.json()

class _Client():
    def __init__(self):
        self._session = Session()

class VIN():
    pass
