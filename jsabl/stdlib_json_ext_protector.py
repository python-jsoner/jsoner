from collections import OrderedDict
from json import JSONEncoder


STDLIB_JSON_TYPES = (dict, list, tuple, str, int, float, bool)
""" Reference list for the types for which json.dumps does not call the encoder """


def _protect_against_primitive_subclasses(inst):
    """
    Internal method to wrap objects inheriting from primitives, so that the underlying stdlib json
    stack does not handle them automatically as primitives but as objects.

    This way there is no automatic behaviour for non-primitive data - everything is managed in the object hooks.

    The initial idea was to protect at least against the case of classes inheriting both from JSONAble and a primitive,
    but it was extended to a more conservative behaviour - both because it makes sense, and also because it works for
    custom JSONCodecs too, not only JSONAble.

    Note: this method is recursive across the various container types.

    :param inst:
    :return:
    """
    # Recursive for all primitive containers
    if type(inst) is OrderedDict:
        return OrderedDict([(_protect_against_primitive_subclasses(k),
                             _protect_against_primitive_subclasses(v))
                            for k, v in inst.items()])

    elif type(inst) is dict:
        return {_protect_against_primitive_subclasses(k): _protect_against_primitive_subclasses(v)
                for k, v in inst.items()}

    elif type(inst) is list:
        return [_protect_against_primitive_subclasses(v) for v in inst]

    elif type(inst) is tuple:
        return tuple(_protect_against_primitive_subclasses(v) for v in inst)

    elif type(inst) in STDLIB_JSON_TYPES:  # Fast test using equality, not isinstance
        # this is a pure primitive, not a tricky class.
        return inst

    else:
        # Subclass of a primitive: this *can* be a tricky class
        if isinstance(inst, STDLIB_JSON_TYPES):
            # note: if there are perf issues we could also remove the isinstance and always return a protected object
            return _Protector(inst)
        else:
            return inst


class _Protector:
    """
    A class used only internally in order to wrap objects both inheriting from a primitive and from something else
    (JSONAble for example). This way, the underlying json stack will not handle them as primitives but as objects, so
    it will call all our registered codecs. Without this, a custom class subclassing both JSONAble and dict for example,
    will never reach the JSONAble codec. This is true for any class subclassing a python primitive.
    """

    __slots__ = 'wrapped'

    def __init__(self, wrapped):
        if isinstance(wrapped, _Protector):  # should not happen but just in case...
            wrapped = wrapped.wrapped

        if wrapped is None:
            raise ValueError("Trying to protect <None> ?!!")

        self.wrapped = wrapped


def add_protection_to_json_encoder(json_encoder  # type: JSONEncoder
                                   ):
    # type: (...) -> None
    """
    Modifies the encoding and decoding methods in the provided `JSONEncoder`, so that objects that are primitive
    subclasses are not automatically encoded but sent to the object hook.

    For example if o = [1, Foo()] and Foo is a class that extends both JSONAble and int:
     - first o will be converted to [1, _Protector(Foo())]
     - then the usual encoding function will be executed. Since _Protector is not a primitive, the custom object
    hook of the JSONEncoder will be called to resolve it.
     - but the custom object hook (self.default) is also modified so that the _Protector is removed before execution.

    :param json_encoder:
    :return:
    """

    old_encode = json_encoder.encode

    def protected_encode(o, *args, **kwargs):
        """
        First replaces all items in o by a _Protector(i) when they need protection against primitive encoding.
        Then executes self.encode.

        :param o:
        :param args:
        :param kwargs:
        :return:
        """
        # Handle the case of an object inheriting both from a primitive and a type for which a codec is registered
        o = _protect_against_primitive_subclasses(o)

        # Then execute the encode method as usual
        return old_encode(o, *args, **kwargs)

    # replace the encoding method in the encoder class, with the protected one
    json_encoder.encode = protected_encode

    old_iterencode = json_encoder.iterencode

    def protected_iterencode(o, *args, **kwargs):
        """
        First replaces all items in o by a _Protector(i) when they need protection against primitive encoding.
        Then executes self.iterencode.

        :param o:
        :param args:
        :param kwargs:
        :return:
        """
        # Handle the case of an object inheriting both from a primitive and a type for which a codec is registered
        o = _protect_against_primitive_subclasses(o)

        # Then execute the iterencode method as usual
        return old_iterencode(o, *args, **kwargs)

    # replace the iterative encoding method in the encoder class, with the protected one
    json_encoder.iterencode = protected_iterencode

    old_default = json_encoder.default

    def protector_aware_default(o):
        """

        :param o:
        :return:
        """
        # Un-protect if needed (type equality is probably faster than isinstance here)
        if type(o) is _Protector:
            o = o.wrapped

        # Then execute the default method as usual
        return old_default(o)

    # replace the default hook to decode unknown objects, with the protector-aware one
    json_encoder.default = protector_aware_default
