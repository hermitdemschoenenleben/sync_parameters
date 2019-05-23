import bz2
import pickle


def pack(value):
    return bz2.compress(pickle.dumps(value))


def unpack(value):
    return pickle.loads(bz2.decompress(value))