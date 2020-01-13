"""PyVIN
Interfaces with the NHTSA API to decode Vehicle Identification Numbers (VINs).
Given one or more VINs, validates and returns decoded data with Yeah, Make, Model,
and many other informational fields
"""

from typing import List, Union
from requests import Session
from .errors import VINError
from .utils import clean_vins, validate_vin

_URL = 'https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValuesBatch/'
_DEFAULT_PARAMS = {'format': 'json'}
_HEADERS = {'Content-type':'application/json', 'Accept':'application/json'}
_SESSION = Session()
_SESSION.headers.update(_HEADERS)
_MAX_BATCH_SIZE = 100
_RESULTS = 'Results'

RAISE = 'RAISE'
SKIP = 'SKIP'
PASS = 'PASS'  # TODO: Not yet implemented

class DecodedVIN():
    """VIN decoded by the NHTSA API.  Attributes are generated from the
    API json response"""
    def __init__(self, data: dict):
        self.__dict__.update(data)

def VIN(*vins: str, error_handling=SKIP) -> Union[List[DecodedVIN], DecodedVIN]:
    """Decode one or more VINs

    Keyword Arguments:
        error_handling {str} -- Select action for invalid VINs (default: {SKIP}):
                                SKIP: Return only the parseable VINs
                                RAISE: Raise exception on the first invalid VIN
                                PASS (Not Implemented): Invalid VINs yield a NoneType

    Raises:
        VINError: on any error encountered during VIN parsing
        KeyError: on incorrect error_handling input

    Returns:
        Union[List[DecodedVIN], DecodedVIN] -- Decoded VIN result
    """
    if len(vins) > _MAX_BATCH_SIZE:
        raise VINError('VIN count exceeds Max Batch Size of %s' % _MAX_BATCH_SIZE)
    if error_handling == SKIP:
        vin_list = clean_vins(vins)
    elif error_handling == RAISE:
        vin_list = vins
        for vin in vin_list:
            validate_vin(vin)
    else:
        raise KeyError('Error handling %s must be %s or %s' % (error_handling, RAISE, SKIP))
    if not vin_list:
        return []
    vin_str = ';'.join(vin_list)
    # resp = _SESSION.post(url=_URL, params=_DEFAULT_PARAMS, data=vin_str)  # TODO: Why didn't this work?
    resp = _SESSION.post(url=_URL + vin_str + '?' , params=_DEFAULT_PARAMS)
    results = resp.json().get(_RESULTS, [])
    if len(vins) == 1:
        return DecodedVIN(results[0])
    return [DecodedVIN(x) for x in results]
