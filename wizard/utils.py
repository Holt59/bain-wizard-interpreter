# -*- encoding: utf-8 -*-

from typing import Callable, List, Union

from .expr import Value, VariableType, Void


class optional:
    t: type

    def __init__(self, t: type):
        self.t = t


def wrap_function(
    name: str,
    method,
    *args: Union[optional, type],
    varargs: bool = False,
    rawargs: bool = False,
) -> Callable[[List[Value]], Value]:

    """
    Wrap the given function to be usable by the Wizard expression visitor.

    Args:
        name: The name of the function, for logging purpose (warning / errors).
        method: The function to wrap.
        *args: The type of arguments expected by the method.
        varargs: True if the method accept any number of arguments.
        rawargs: True if the method accept Value(), False to extract the underlying
            object.
    """

    def fn(vs: List[Value]) -> Value:

        # List of Python arguments:
        pargs: List = []

        if not varargs and len(vs) > len(args):
            raise TypeError(f"{name}: too many arguments.")

        for iarg, arg in enumerate(args):
            if iarg >= len(vs) and not isinstance(arg, optional):
                raise TypeError(f"{name}: missing required positional argument(s).")

            tp: type
            if isinstance(arg, optional):
                tp = arg.t
            else:
                tp = arg

            if not isinstance(vs[iarg].value, tp):
                raise TypeError(
                    f"Argument at position {iarg} has incorrect type for"
                    f" {name}, expected {VariableType.from_pytype(tp)} got"
                    f" {vs[iarg].type}."
                )

            if rawargs:
                pargs.append(vs[iarg])
            else:
                pargs.append(vs[iarg].value)

        ret: Value = method(*pargs)
        if ret is None:
            ret = Void()

        if not rawargs:
            ret = Value(ret)  # type: ignore

        return ret

    return fn
