Module pyvin.pyvin
==================
PyVIN
Interfaces with the NHTSA API to decode Vehicle Identification Numbers (VINs).
Given one or more VINs, validates and returns decoded data with Yeah, Make, Model,
and many other informational fields

Functions
---------

    
`VIN(*vins, error_handling='SKIP')`
:   Decode one or more VINs
    
    Keyword Arguments:
        error_handling {str} -- Select action for invalid VINs (default: {SKIP}):
                                SKIP: Return only the parseable VINs
                                RAISE: Raise exception on the first invalid VIN
                                PASS (Not Implemented): Invalid VINs yield a NoneType
    
    Raises:
        VINError: on any error encountered during VIN parsing
        KeyError: on incorrect error_handling input
    
    Returns:
        Union[List[DecodedVIN], DecodedVIN] -- Decoded VIN result

Classes
-------

`DecodedVIN(data)`
:   VIN decoded by the NHTSA API.  Attributes are generated from the
    API json response