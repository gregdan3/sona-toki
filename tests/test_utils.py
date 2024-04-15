# STL
import itertools


def overlapping_pairs(iterable: str):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    _ = next(b, None)
    return zip(a, b)
