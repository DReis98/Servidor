import math

"""
Transforms 3 coordinates into a dict
"""
def coordinate_3(lat, lon, alt):
    d = {}
    d["lon"] = lon
    d["lat"] = lat
    d["alt"] = alt

    return d

"""
Transforms 2 coordinates into a dict
"""
def coordinate_2(lat, lon):
    d = {}
    d["lon"] = lon
    d["lat"] = lat
    d["alt"] = 0.0

    return d

def calculate_XYZ(d):
    lon = d["lon"]
    lat = d["lat"]
    alt = d["alt"]

    degree_to_rad = math.pi / 180

    lon_rad = lon * degree_to_rad
    lat_rad = lat * degree_to_rad

    a = 6378137
    f = 1/298.257223563
 

    r_n = a / math.sqrt(1 - (f * (2-f) * math.sin(lat_rad) * math.sin(lat_rad)))

    x = (r_n + alt) * math.cos(lat_rad) * math.cos(lon_rad)
    y = (r_n + alt) * math.cos(lat_rad) * math.sin(lon_rad)
    z = ( (1-f)*(1-f)*r_n + alt) * math.sin(lat_rad)

    ret = {}
    ret["x"] = x
    ret["y"] = y
    ret["z"] = z

    return ret

"""
def calculate_XYZ2(d):
    lon = d["lon"]
    lat = d["lat"]
    alt = d["alt"]

    degree_to_rad = math.pi / 180

    lon_rad = lon * degree_to_rad
    lat_rad = lat * degree_to_rad

    a = 6378137
    b = 6356752.314245
    a_sqr = a * a
    b_sqr = b * b
    e_sqr = 1 - (b_sqr / a_sqr)

    n_phi = a / math.sqrt(1 - (e_sqr * math.sin(lat_rad) * math.sin(lat_rad)))

    x = (n_phi + alt) * math.cos(lat_rad) * math.cos(lon_rad)
    y = (n_phi + alt) * math.cos(lat_rad) * math.sin(lon_rad)
    z = ( ((b_sqr/a_sqr) * n_phi) + alt) * math.sin(lat_rad)

    ret = {}
    ret["x"] = x
    ret["y"] = y
    ret["z"] = z

    return ret

"""

def calculate_distance(p1, p2):
    x1 = p1["x"]
    y1 = p1["y"]
    z1 = p1["z"]

    x2 = p2["x"]
    y2 = p2["y"]
    z2 = p2["z"]

    dif_x = x2 - x1
    dif_y = y2 - y1
    dif_z = z2 - z1

    dist = math.sqrt((dif_x * dif_x) + (dif_y * dif_y) + (dif_z * dif_z))
    
    return dist

def distance(lat1, lon1, alt1, lat2, lon2, alt2):

    p1 = coordinate_3(lat1, lon1, alt1)
    p2 = coordinate_3(lat2, lon2, alt2)

    p1 = calculate_XYZ(p1)
    p2 = calculate_XYZ(p2)

    dist = calculate_distance(p1, p2)
    return dist