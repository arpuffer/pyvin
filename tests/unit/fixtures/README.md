# vPIC mock responses

The Toyota record reuses the existing `DECODED_TOYOTA_COROLLA` fixture.
Other records are minimal simulated vPIC results, not live API captures.
The unit test mock wraps these records in the batch endpoint response envelope.
Only the fields relevant to each test are included.
