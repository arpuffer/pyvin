import unittest
from typing import List
from pprint import pprint
from pyvin import VIN, VINError, DecodedVIN, RAISE, SKIP, PASS
from .vin_samples import (INVALID,
                          DECODED_TOYOTA_COROLLA,
                          TOYOTA_COROLLA,
                          HYUNDAI_ELANTRA)

class TestPyVin(unittest.TestCase):
    def test_vin_single(self):
        vin = VIN(TOYOTA_COROLLA)
        self.assertIsInstance(vin, DecodedVIN)

    def test_vin_single_invalid(self):
        vins = VIN(INVALID)
        ''' This may test future behavior:
        with self.assertRaises(VINError):
            VIN(INVALID)'''
        self.assertEqual(vins, [])

    def test_vin_multi(self):
        """When multiple vins are input (Iterable or as separate args),
        return a list of decoded vins
        """
        samples = (TOYOTA_COROLLA, HYUNDAI_ELANTRA)
        vins = VIN(*samples)
        self.assertEqual(len(samples), len(vins))
        for vin in vins:
            self.assertIsInstance(vin, DecodedVIN)

    def test_invalid_in_multi(self):
        samples = (INVALID, TOYOTA_COROLLA)
        vins = VIN(*samples)
        self.assertEqual(len([x for x in samples if x is not INVALID]),
                         len(vins))

    def test_invalid_in_multi_raise(self):
        samples = (INVALID, TOYOTA_COROLLA)
        with self.assertRaises(VINError):
            vins = VIN(*samples, error_handling=RAISE)

    def test_invalid_in_multi_pass(self):
        """If invalid vin is present in list, make sure it is handled as specified"""
        samples = (INVALID, TOYOTA_COROLLA)
        vins = VIN(*samples, error_handling=PASS)
        self.assertEqual(len([x for x in samples if x is not INVALID]),
                         len(vins))

    def test_vin_attrs(self):
        vin = VIN(TOYOTA_COROLLA)
        attrs = {k:v for k,v in vin.__dict__.items() if '__' not in k}
        self.assertDictEqual(attrs, DECODED_TOYOTA_COROLLA)
