"""
GPS coordinates can be directly converted to a geohash.
Geohash divides the Earth into "buckets" of different size based on the number of digits
(short Geohash codes create big areas and longer codes for smaller areas).
Geohash is an adjustable precision clustering method.
"""
from geolib import geohash
from sentiance.settings import VISIT_LOC_MIN_LEVEL, VISIT_LOC_MAX_LEVEL


def latlon2gcodes(latitude, longitude):
    gcodes = []
    for level in range(VISIT_LOC_MIN_LEVEL, VISIT_LOC_MAX_LEVEL + 1):
        gcodes.append((geohash.encode(latitude, longitude, level), level))
    return gcodes
