import numpy as np
import shapely
from shapely.geometry import LineString, Polygon


def flatten_geometry(obj):
    """ Takes a 3D geometry and returns a 2D geometry discarding the third coordinate
    Parameters
    ----------
    obj : shapely.geometry
        A 3D geometry
    Returns
    -------
    shapely.geometry
        A 2D geometry
    """
    return shapely.wkb.loads(shapely.wkb.dumps(obj, output_dimension=2))


def lift(obj, elevation=0.):
    """ Takes a geometry and turns it in a 3D geometry with given constant elevation
    Parameters
    ----------
    obj : shapely.geometry
        A geometry
    elevation : float
        elevation to which obj will be raised
    Returns
    -------
    shapely.geometry
        A 3D geometry
    """
    for idx, row in obj.iterrows():
        g = row['geometry']
        if g.geom_type == 'LineString' or g.geom_type == 'Point':
            coords = [(i[0], i[1], elevation) for i in row['geometry'].coords]
            obj.loc[idx, 'geometry'] = LineString(coords)
        elif g.geom_type == 'Polygon':
            # exterior ring
            exterior = [(i[0], i[1], elevation) for i in g.exterior.coords]
            # interior rings (a.k.a. holes)
            interiors = [[(j[0], j[1], elevation) for j in i.coords] for i in g.interiors]
            obj.loc[idx, 'geometry'] = Polygon(exterior, interiors)
    # return obj  # not needed as operation is done inplace


def rotate_around_vector(vector, angle, degrees=False, affine_4x4=False):
    """Returns the matrix associated to a rotation by a given angle around a given vector using Rodrigues formula
    Parameters
    ----------
    vector : numpy.array
        vector around which the rotation matrix will be computed
    angle : float
        amplitude of rotation given following the right-hand-side rule
    degrees : bool, default: False
        set to True if angle is given in degrees rather than in radians
    affine_4x4 : bool, default: False
        set to True to return a 4x4 affine transform matrix
    Returns
    -------
    numpy.array
        transform matrix
    Example
    -------
    This example shows how to use this function to rotate by 90° a given vector a around vector v.
    >>> import numpy as np
    >>> import geometron.geometries.transforms as ggt
    >>> a = np.array([0., 0., 1.])
    >>> v = np.array([3., 0., 0.])
    >>> angle = np.pi/2
    >>> r = ggt.rotate_around_vector(v, angle)
    >>> np.dot(r, a)
    array([ 0.00000000e+00, -1.00000000e+00,  1.11022302e-16])
    For more info. see https://en.wikipedia.org/wiki/Rodrigues'_rotation_formula#Matrix_notation"""

    vector = np.array(vector)  # convert array-like (list, tuple) into a numpy array
    vector = vector/np.linalg.norm(vector)  # normalize the vector
    if degrees:
        # convert degrees to radians
        angle = angle * np.pi / 180.
    c = np.array([[0., -vector[2], vector[1]], [vector[2], 0., -vector[0]], [-vector[1], vector[0], 0.]])
    r = np.eye(3) + c * np.sin(angle) + np.matmul(c, c) * (1 - np.cos(angle))
    if affine_4x4:
        r = np.vstack([r, np.array([0., 0., 0.])])
        r = np.hstack([r, np.array([[0., 0., 0., 1.]]).T])
    return r

# def transform_matrix_2d(from_obj, to_obj, shapely_format=False):
#     # TODO: deal with more than two points in from_points and to_points using best fit ?
#     # TODO: introduce skew?
#     # TODO: deprecate and reuse what was done for the 4x4 vtk matrix?
#     if type(from_obj) is not tuple:
#         f = (*from_obj.coords[0], *from_obj.coords[-1])
#         f_length = from_obj.length
#     else:
#         f = from_obj
#         f_length = np.sqrt((f[2] - f[0]) ** 2 + (f[1] - f[1]) ** 2)
#     if type(to_obj) is not tuple:
#         t = (*to_obj.coords[0], *to_obj.coords[-1])
#         t_length = to_obj.length
#     else:
#         t = to_obj
#         t_length = np.sqrt((t[2] - t[0]) ** 2 + (t[3] - t[1]) ** 2)
#     print(f, t)
#     theta = np.arctan2(t[3] - t[1], t[2] - t[0]) - np.arctan2(f[3] - f[1], f[2] - f[0])
#     ct = np.cos(theta)
#     st = np.sin(theta)
#     sf = (t_length / f_length)
#     t1x = -f[0]
#     t1y = -f[1]
#     t2x = t[0]
#     t2y = t[1]
#
#     a = sf * ct
#     b = -sf * st
#     c = 0.
#     # noinspection SpellCheckingInspection
#     xoff = t1x * sf * ct - t1y * sf * st + t2x
#     d = sf * st
#     e = sf * ct
#     f = 0.
#     # noinspection SpellCheckingInspection
#     yoff = t1x * sf * st + t1y * sf * ct + t2y
#     g = 0.
#     h = 0.
#     i = 1.
#     # noinspection SpellCheckingInspection
#     zoff = 0.
#
#     if shapely_format:
#         return [a, b, c, d, e, f, g, h, i, xoff, yoff, zoff]
#     else:
#         return np.array([[a, b, c, xoff], [d, e, f, yoff], [g, h, i, zoff], [0., 0., 0., 1.]])
