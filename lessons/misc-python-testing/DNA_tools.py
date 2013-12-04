import string

def calculate_gc(x):
    """Calculates the GC content of DNA sequence x.
    x: a string composed only of A's, T's, G's, and C's."""
    if x == '':
        return 1
    x = x.upper()
    gc = float(string.count(x, "G") +string.count(x, "C")) / len(x)
    return gc
