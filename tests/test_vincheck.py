import unittest
from pyvin import VINError
from pyvin.utils import (clean_vins,
                         validate_vin)
from .vin_samples import (INVALID,
                          HYUNDAI_ELANTRA,
                          TOYOTA_COROLLA)


class TestValidateVin(unittest.TestCase):
    def test_validate_vin(self):
        self.assertIsNone(validate_vin(TOYOTA_COROLLA))
        self.assertIsNone(validate_vin(TOYOTA_COROLLA, HYUNDAI_ELANTRA))
        with self.assertRaises(VINError):
            validate_vin(INVALID)

    def test_clean_vins(self):
        vins = (INVALID, TOYOTA_COROLLA)
        results = clean_vins(vins)
        self.assertTupleEqual(tuple(x for x in vins if x is not INVALID),
                              results)


if __name__ == '__main__':
    unittest.main()
