from tests.vin_samples import TOYOTA_COROLLA, HYUNDAI_ELANTRA
from pyvin.pyvin import VIN

vins = VIN(TOYOTA_COROLLA, HYUNDAI_ELANTRA)
print(vins)
