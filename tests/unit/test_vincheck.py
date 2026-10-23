import unittest
from pyvin import VINError
from pyvin.utils import (clean_vins,
                         validate_vin)
from tests.vin_samples import (INVALID,
                          HYUNDAI_ELANTRA,
                          TOYOTA_COROLLA)


class TestValidateVin(unittest.TestCase):
    def test_validate_vin_forbidden_characters(self):
        for character in "IOQ":
            with self.subTest(character=character):
                vin = character + TOYOTA_COROLLA[1:]
                with self.assertRaisesRegex(VINError, f'Invalid char "{character}"'):
                    validate_vin(vin)

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
