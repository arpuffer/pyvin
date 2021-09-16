import unittest
from pyvin import VIN, VINError, DecodedVIN, RAISE, SKIP, PASS
from .vin_samples import (INVALID,
                          INVALID_SHORT,
                          DECODED_TOYOTA_COROLLA,
                          TOYOTA_COROLLA,
                          HYUNDAI_ELANTRA,
                          BATCH)


class TestPyVin(unittest.TestCase):
    def test_vin_single(self):
        vin = VIN(TOYOTA_COROLLA, error_handling=SKIP)
        self.assertIsInstance(vin, DecodedVIN)

        vin = VIN(TOYOTA_COROLLA, error_handling=RAISE)
        self.assertIsInstance(vin, DecodedVIN)

    def test_vin_single_invalid(self):
        vins = VIN(INVALID, error_handling=SKIP)
        self.assertEqual(vins, [])

        with self.assertRaises(VINError):
            VIN(INVALID, error_handling=RAISE)

    def test_vin_single_invalid_short(self):
        vin = VIN(INVALID_SHORT, error_handling=SKIP)
        self.assertEqual(vin, [])

        with self.assertRaises(VINError):
            VIN(INVALID_SHORT, error_handling=RAISE)

    def test_vin_single_invalid_empty(self):
        vin = VIN('', error_handling=SKIP)
        self.assertEqual(vin, [])

        with self.assertRaises(VINError):
            VIN('', error_handling=RAISE)

    def test_vin_single_invalid_none(self):
        vin = VIN(None, error_handling=SKIP)
        self.assertEqual(vin, [])

        with self.assertRaises(VINError):
            VIN(None, error_handling=RAISE)

    def test_vin_multi_minimal(self):
        """When multiple vins are input (Iterable or as separate args),
        return a list of decoded vins
        """
        samples = (TOYOTA_COROLLA, HYUNDAI_ELANTRA)
        vins = VIN(*samples)
        self.assertEqual(len(samples), len(vins))
        for vin in vins:
            self.assertIsInstance(vin, DecodedVIN)

    def test_vin_multi_large_batch(self):
        samples = BATCH
        vins = VIN(*samples)
        self.assertEqual(len(samples), len(vins))

    def test_invalid_in_multi(self):
        samples = (INVALID, TOYOTA_COROLLA)
        vins = VIN(*samples)
        self.assertIsInstance(vins, DecodedVIN)
        self.assertEqual(len([x for x in samples if x is not INVALID]), 1)

    def test_invalid_in_multi_raise(self):
        samples = (INVALID, TOYOTA_COROLLA)
        with self.assertRaises(VINError):
            VIN(*samples, error_handling=RAISE)

    def test_invalid_in_multi_pass(self):
        samples = (INVALID, TOYOTA_COROLLA)
        vins = VIN(*samples, error_handling=PASS)
        self.assertEqual(len(samples),
                         len(vins))

    def test_vin_attrs(self):
        vin = VIN(TOYOTA_COROLLA)
        attrs = {k: v for k, v in vin.__dict__.items() if '__' not in k}
        self.assertDictEqual(attrs, DECODED_TOYOTA_COROLLA)
