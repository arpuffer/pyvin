import json
from pathlib import Path
import unittest
from unittest.mock import Mock, patch
from pyvin import VIN, VINError, DecodedVIN, RAISE, SKIP, PASS
from tests.vin_samples import (
    INVALID, INVALID_SHORT, DECODED_TOYOTA_COROLLA,
    TOYOTA_COROLLA, HYUNDAI_ELANTRA, BATCH,
)


class TestDecodedVIN(unittest.TestCase):
    def test_repr(self):
        vin = DecodedVIN(DECODED_TOYOTA_COROLLA)
        self.assertEqual(
            repr(vin),
            "DecodedVIN - JT2AE09W4P0038539 - 1993 - TOYOTA M - Corolla",
        )

    def test_repr_short_or_missing_manufacturer(self):
        for manufacturer, expected in (("Toyota", "Toyota"), (None, "")):
            with self.subTest(manufacturer=manufacturer):
                data = dict(DECODED_TOYOTA_COROLLA)
                if manufacturer is None:
                    data.pop("Manufacturer")
                else:
                    data["Manufacturer"] = manufacturer
                self.assertEqual(
                    repr(DecodedVIN(data)),
                    f"DecodedVIN - JT2AE09W4P0038539 - 1993 - {expected} - Corolla",
                )


class TestPyVin(unittest.TestCase):
    def setUp(self):
        fixture = Path(__file__).with_name("fixtures") / "vpic_responses.json"
        self.responses = json.loads(fixture.read_text())
        patcher = patch("pyvin.pyvin._SESSION.post", side_effect=self.vpic_response)
        self.post = patcher.start()
        self.addCleanup(patcher.stop)

    def vpic_response(self, *, url, data):
        self.assertEqual(
            url, "https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVINValuesBatch/"
        )
        self.assertEqual(data["format"], "json")
        results = [self.responses[vin] for vin in data["data"].split(";")]
        response = Mock()
        response.json.return_value = {
            "Count": len(results),
            "Message": "Results returned successfully",
            "SearchCriteria": None,
            "Results": results,
        }
        return response

    def test_vin_single(self):
        vin = VIN(TOYOTA_COROLLA, error_handling=SKIP)
        self.assertIsInstance(vin, DecodedVIN)

        vin = VIN(TOYOTA_COROLLA, error_handling=RAISE)
        self.assertIsInstance(vin, DecodedVIN)

    def test_unknown_error_handling(self):
        with self.assertRaisesRegex(VINError, "error_handling must be PASS, RAISE, or SKIP"):
            VIN(TOYOTA_COROLLA, error_handling="unknown")
        self.post.assert_not_called()

    def test_vin_batch_at_limit(self):
        samples = (TOYOTA_COROLLA,) * 50
        vins = VIN(*samples)
        self.assertEqual(len(vins), 50)
        self.assertTrue(all(isinstance(vin, DecodedVIN) for vin in vins))
        self.assertEqual([vin.VIN for vin in vins], list(samples))
        self.post.assert_called_once_with(
            url="https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVINValuesBatch/",
            data={"format": "json", "data": ";".join(samples)},
        )

    def test_vin_batch_over_limit(self):
        with self.assertRaisesRegex(VINError, "VIN count exceeds Max Batch Size of 50"):
            VIN(*((TOYOTA_COROLLA,) * 51))
        self.post.assert_not_called()

    def test_vin_single_invalid(self):
        vins = VIN(INVALID, error_handling=SKIP)
        self.assertEqual(vins, [])

        with self.assertRaises(VINError):
            VIN(INVALID, error_handling=RAISE)
        self.post.assert_not_called()

    def test_vin_single_invalid_short(self):
        vin = VIN(INVALID_SHORT, error_handling=SKIP)
        self.assertEqual(vin, [])

        with self.assertRaises(VINError):
            VIN(INVALID_SHORT, error_handling=RAISE)
        self.post.assert_not_called()

    def test_vin_single_invalid_empty(self):
        vin = VIN('', error_handling=SKIP)
        self.assertEqual(vin, [])

        with self.assertRaises(VINError):
            VIN('', error_handling=RAISE)
        self.post.assert_not_called()

    def test_vin_single_invalid_none(self):
        vin = VIN(None, error_handling=SKIP)
        self.assertEqual(vin, [])

        with self.assertRaises(VINError):
            VIN(None, error_handling=RAISE)
        self.post.assert_not_called()

    def test_vin_multi_minimal(self):
        """When multiple vins are input (Iterable or as separate args),
        return a list of decoded vins
        """
        samples = (TOYOTA_COROLLA, HYUNDAI_ELANTRA)
        vins = VIN(*samples)
        self.assertEqual(len(samples), len(vins))
        self.assertEqual([vin.VIN for vin in vins], list(samples))
        self.post.assert_called_once_with(
            url="https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVINValuesBatch/",
            data={"format": "json", "data": ";".join(samples)},
        )
        for vin in vins:
            self.assertIsInstance(vin, DecodedVIN)

    def test_vin_multi_large_batch(self):
        samples = BATCH
        vins = VIN(*samples)
        self.assertEqual(len(samples), len(vins))
        self.assertEqual([vin.VIN for vin in vins], list(samples))
        self.post.assert_called_once_with(
            url="https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVINValuesBatch/",
            data={"format": "json", "data": ";".join(samples)},
        )

    def test_invalid_in_multi(self):
        samples = (INVALID, TOYOTA_COROLLA)
        vins = VIN(*samples)
        self.assertIsInstance(vins, DecodedVIN)
        self.assertEqual(vins.VIN, TOYOTA_COROLLA)
        self.post.assert_called_once_with(
            url="https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVINValuesBatch/",
            data={"format": "json", "data": TOYOTA_COROLLA},
        )

    def test_invalid_in_multi_raise(self):
        samples = (INVALID, TOYOTA_COROLLA)
        with self.assertRaises(VINError):
            VIN(*samples, error_handling=RAISE)
        self.post.assert_not_called()

    def test_invalid_in_multi_pass(self):
        samples = (INVALID, TOYOTA_COROLLA)
        vins = VIN(*samples, error_handling=PASS)
        self.assertEqual(len(samples), len(vins))
        self.assertEqual([vin.VIN for vin in vins], list(samples))
        self.assertEqual(vins[0].ErrorCode, "1")
        self.post.assert_called_once_with(
            url="https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVINValuesBatch/",
            data={"format": "json", "data": ";".join(samples)},
        )

    def test_vin_attrs(self):
        vin = VIN(TOYOTA_COROLLA)
        attrs = {k: v for k, v in vin.__dict__.items() if '__' not in k}
        self.assertDictEqual(attrs, DECODED_TOYOTA_COROLLA)
