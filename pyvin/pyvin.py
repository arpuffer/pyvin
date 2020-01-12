from typing import List, Union
from requests import Session
from .errors import VINError
from .utils import clean_vins, validate_vin

_URL = 'https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValuesBatch/'
_DEFAULT_PARAMS = {'format': 'json'}
_SESSION = Session()
_MAX_BATCH_SIZE = 100

RAISE = 'RAISE'
SKIP = 'SKIP'

class DecodedVIN():
    def __init__(self, data: dict):
        self.__dict__.update(data)

def _decode_vin_values(vins: List[str], error_handling=SKIP):
    if len(vins) > _MAX_BATCH_SIZE:
        raise VINError('VIN count exceeds Max Batch Size of %s' % _MAX_BATCH_SIZE)
    if error_handling == SKIP:
        vin_list = clean_vins(vins)
    elif error_handling == RAISE:
        vin_list = vins
        for vin in vin_list:
            validate_vin(vin_list)
    else:
        raise KeyError('Error handling %s must be %s or %s' % (error_handling, RAISE, SKIP))
    vin_str = ';'.join(vin_list)
    resp = _SESSION.post(url=_URL, params=_DEFAULT_PARAMS, data=vin_str)
    data = resp.json()

def VIN(vins: Union[List[str], str]) -> Union[List[DecodedVIN], DecodedVIN]:
    pass
