import bz2
import pickle


def pack(value):
    try:
        return pickle.dumps(value)
    except (AttributeError, TypeError):
        # this happens when un-pickleable objects (e.g. functions) are assigned
        # to a parameter. In this case, we don't pickle it but transfer a netref
        # instead
        return value


def unpack(value):
    try:
        return pickle.loads(value)
    except:
        return value