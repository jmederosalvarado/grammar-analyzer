from functools import lru_cache
from pycmp.parsing import compute_firsts as __compute_firsts
from pycmp.parsing import compute_follows as __compute_follows


@lru_cache
def compute_firsts(grammar):
    return __compute_firsts(grammar)


@lru_cache
def compute_follows(grammar):
    firsts = compute_firsts(grammar)
    return __compute_follows(grammar, firsts)
