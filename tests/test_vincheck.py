import unittest
from pyvin import VINError
from pyvin.utils import (_transliterate,
                         _remainder_sum_weighted,
                         _compare_check_digit,
                         validate_vin)

VALID_VIN = 'JT2AE09W4P0038539'  # 1993 Toyota Corolla LE
INVALID_VIN = 'JT2AE09W5P0038539'  # Same as above with incorrect check digit

class TestValidateVin(unittest.TestCase):
    def test_validate_vin(self):
        self.assertIsNone(validate_vin(VALID_VIN))
        with self.assertRaises(VINError):
            validate_vin(INVALID_VIN)

if __name__ == '__main__':
    unittest.main()