"""PyVIN
Interfaces with the NHTSA API to decode Vehicle Identification Numbers (VINs).
Given one or more VINs, validates and returns decoded data with Yeah, Make, Model,
and many other informational fields
"""

from json.decoder import JSONDecodeError
from typing import List, Union
from requests import Session
from retry import retry
from .errors import VINError
from .utils import clean_vins, validate_vin

_URL = 'https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVINValuesBatch/'
_SESSION = Session()
_MAX_BATCH_SIZE = 50
_RESULTS = 'Results'

RAISE = 'RAISE'
SKIP = 'SKIP'
PASS = 'PASS'


class DecodedVIN:  # pylint:disable=too-few-public-methods
    """VIN decoded by the NHTSA API.  Attributes are generated from the
    API json response"""

    def __init__(self, data: dict):
        self.__dict__.update(data)


@retry(exceptions=JSONDecodeError,
       tries=10,
       delay=10)
def VIN(*vins: str, error_handling=SKIP) -> Union[List[DecodedVIN], DecodedVIN]:  # pylint:disable=invalid-name
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
    if error_handling == SKIP:
        vins = clean_vins(vins)
    elif error_handling == RAISE:
        validate_vin(*vins)
    elif error_handling == PASS:
        pass
    else:
        raise VINError('error_handling must be PASS, RAISE, or SKIP')

    if not vins:
        return []

    count = len(vins)
    if count > _MAX_BATCH_SIZE:
        raise VINError('VIN count exceeds Max Batch Size of %s' % _MAX_BATCH_SIZE)

    vin_str = ';'.join(vins)
    post_fields = {'format': 'json',
                   'data': vin_str}
    resp = _SESSION.post(url=_URL, data=post_fields)
    results = resp.json().get(_RESULTS, [])
    if count == 1:
        return DecodedVIN(results[0])
    return [DecodedVIN(x) for x in results]
