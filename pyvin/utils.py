"""PyVIN utilities.
Contains all actions that do not interact with the NHTSA API:
- VIN validation
- Removal of invalid VINs from a list
"""

import logging
from typing import List
from .errors import VINError

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

_CHECK_DIGIT_INDEX = 8
_SUM_WEIGHTED_DIVIDEBY = 11
_VIN_LENGTH = 17

#transliteration lookup table
_TRANS_LOOKUP = {'A': 1,
                 'B': 2,
                 'C': 3,
                 'D': 4,
                 'E': 5,
                 'F': 6,
                 'G': 7,
                 'H': 8,
                 'J': 1,
                 'K': 2,
                 'L': 3,
                 'M': 4,
                 'N': 5,
                 'P': 7,
                 'R': 9,
                 'S': 2,
                 'T': 3,
                 'U': 4,
                 'V': 5,
                 'W': 6,
                 'X': 7,
                 'Y': 8,
                 'Z': 9}

# Positional weighting factors - by index of VIN string
_WEIGHTING_FACTORS = (8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2)

def _transliterate(vin: str) -> List[int]:
    """Uses transliteration table to convert letters into int values

    Arguments:
        vin {str}

    Raises:
        VINError: if character cannot be transliterated

    Returns:
        List[int] -- transliterated VIN
    """
    try:
        return [int(x) if x.isdigit() else _TRANS_LOOKUP[x] for x in vin]
    except KeyError as e:
        raise VINError('Invalid char "%s"' % e.args)
    
def _remainder_sum_weighted(trans_vin: List[int]) -> int:
    """Compute the remainder of the sum of weighted VIN character values.
    Transliterated VIN's weighted values (from _WEIGHTING_FACTORS table) are
    summed, and then divided by _SUM_WEIGHTED_DIVIDEBY.

    Args:
        trans_vin (List[int]): transliterated VIN

    Returns:
        int: remainder
    """
    sum_weighted = sum([x * y for x, y in zip(trans_vin, _WEIGHTING_FACTORS)])
    return sum_weighted % _SUM_WEIGHTED_DIVIDEBY

def _compare_check_digit(vin: str, remainder: int):
    """Compares check digit against remainder value

    Args:
        vin (str)
        remainder (int): remainder of the sum of weighted, transliterated VIN values

    Raises:
        VINError: on failed check
    """
    check_digit = vin[_CHECK_DIGIT_INDEX]
    if remainder == 10:
        rem_val = 'X'
    else:
        rem_val = str(remainder)
    if check_digit != rem_val:
        raise VINError('Invalid check digit! %s does not match computed val %s' % (check_digit, rem_val))
    logger.debug("%s check [OK]")

def validate_vin(vin:str):
    """Used to verify VIN independently of the NHTSA API.

    Args:
        vin (str)
    """
    trans_vin = _transliterate(vin=vin)
    rem = _remainder_sum_weighted(trans_vin=trans_vin)
    _compare_check_digit(vin=vin, remainder=rem)

def clean_vins(vins: List[str]) -> list:
    """Removes invalid VINs from a list of VINs
    
    Arguments:
        vins {List[str]}
    
    Returns:
        list
    """
    remove = []
    for vin in vins:
        try:
            validate_vin(vin=vin)
        except VINError:
            remove.append(vin)
    return [x for x in vins if x not in remove]
