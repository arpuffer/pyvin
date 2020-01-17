# PyVIN
A Vehicle Identification Number (VIN) decoder for Python.  This leverages the NHTSA API to decode VINs into collections of vehicle data that can be easily explored (https://vpic.nhtsa.dot.gov/api/)

## Basic Usage:
```
In [0]: from pyvin import VIN

In [1]: vehicle = VIN('JT2AE09W4P0038539')

In [2]: (vehicle.Make, vehicle.Model, vehicle.ModelYear)
Out[2]: ('TOYOTA', 'Corolla', '1993')

In [3]: my_vins = ('JT2AE09W4P0038539', 'KMHD35LH5EU205042')

In [4]: my_vehicles = VIN(*my_vins)

In [5]: for veh in my_vehicles:
   ...:     print(veh.Make, veh.Model, veh.ModelYear)
TOYOTA Corolla 1993
HYUNDAI Elantra 2014
```

## Advanced Usage:
The user can also specify how invalid VINs are handled, be it raising an exception or ignoring them:
```
In [6]: import pyvin
In [7]: new_car = pyvin.VIN('Foo', error_handling=pyvin.RAISE)
Out[7]: VINError: Invalid char "o"the u
```

To simply clean a VIN list, with no decoding involved, the following can be called:
```
In [8]: import pyvin

In [9]: my_vins = ('JT2AE09W4P0038539', 'Foo')

In [10]: cleaned_vins = pyvin.clean_vins(my_vins)

In [11]: cleaned_vins
Out[11]: ['JT2AE09W4P0038539']
```
For simple validation, no calls to the NHTSA API are used, as there is a formula to validate VINs
