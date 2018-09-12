from json import JSONEncoder

import pytest

from jsabl import add_protection_to_json_encoder


def test_protection():
    """Tests that the protection method works"""

    class MyInt(int):
        pass

    # create an instance
    i = MyInt(12)

    # 1- default json lib behaviour: the int is encoded :(
    std_lib_encoder = JSONEncoder()
    assert std_lib_encoder.encode(i) == '12'

    # 2- an encoder for which we add the protection, but not the custom object hook
    dummy_encoder = JSONEncoder()
    add_protection_to_json_encoder(dummy_encoder)

    # should raise an error instead of encoding the int
    with pytest.raises(TypeError) as exc_info:
        dummy_encoder.encode(i)

    e = exc_info.value
    assert str(e) == "Object of type 'MyInt' is not JSON serializable"

    # 3- an encoder for which we add the protection AND the custom object hook should encode correctly
    def custom_object_hook(o):
        if isinstance(o, MyInt):
            return o
        else:
            raise TypeError(f'Object of type {o.__class__.__name__} '
                            f'is not JSON serializable')

    encoder = JSONEncoder(default=custom_object_hook)
    add_protection_to_json_encoder(encoder)

    assert encoder.encode(i) == '12'
