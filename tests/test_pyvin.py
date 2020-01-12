import unittest
from typing import List
from pyvin import VIN, VINError, DecodedVIN
from .vin_samples import (INVALID,
                          DECODED_TOYOTA_COROLLA,
                          TOYOTA_COROLLA,
                          HYUNDAI_ELANTRA)

class TestPyVin(unittest.TestCase):
    def test_vin_invalid(self):
        with self.assertRaises(VINError):
            vin = VIN(INVALID)

    def test_vin_single(self):
        vin = VIN(TOYOTA_COROLLA)
        self.assertIsInstance(vin, DecodedVIN)

    def test_vin_multi(self):
        """When multiple vins are input (Iterable or as separate args),
        return a list of decoded vins
        """
        samples = (TOYOTA_COROLLA, HYUNDAI_ELANTRA)
        vins = VIN(*samples)
        self.assertIsInstance(vins, List[DecodedVIN])
        vins = VIN(samples)
        self.assertIsInstance(vins, List[DecodedVIN])

    def test_invalid_in_multi(self):
        """If invalid vin is present in list, make sure it is handled as specified"""
        samples = (INVALID, TOYOTA_COROLLA)
        vins = VIN(*samples, raise_on_error=False)
        self.assertCountEqual(samples, vins)
        vins = VIN(*samples, skip_on_error=True)
        self.assertCountEqual([x for x in samples if x is not INVALID],
                              vins)
        with self.assertRaises(VINError):
            vins = VIN(*samples, raise_on_error=True)

    def test_vin_attrs(self):
        vin = VIN(TOYOTA_COROLLA)
        self.assertEqual(vin.__dict__,
                         DECODED_TOYOTA_COROLLA)
