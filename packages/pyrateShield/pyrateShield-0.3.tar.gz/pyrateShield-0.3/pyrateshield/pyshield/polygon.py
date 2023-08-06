import numpy as np
from matplotlib.path import Path
# rip from quickmap


def unit_vector(vector):
    return vector / np.linalg.norm(vector)


def get_polygon(point, line, extent):
    p1 = np.asarray(line[0])
    p2 = np.asarray(line[1])

    uv1 = unit_vector(p1-point)
    uv2 = unit_vector(p2-point)

    angle = np.arccos(np.clip(np.dot(uv1, uv2), -1.0, 1.0))

    min_dist = np.sqrt((extent[3] - extent[2]) ** 2\
                      + (extent[1] - extent[0]) **2)


    d = min_dist/np.cos(0.5 * angle)

    p3 = point + d*uv1
    p4 = point + d*uv2

    poly = np.array((p1, p3, p4, p2))
    return poly




def grid_points_in_polygon(grid, poly):

    points = np.asarray([grid.X.flatten(), grid.Y.flatten()]).T

    path = Path(poly)

    inside =  path.contains_points(points)

    mask = inside.reshape(grid.X.shape)

    return points[inside], mask

def get_diagonal_intersection_factor(points, x, y, vertices):
    """ 
    Get diagonal distance factor through wall for every point within polygon (head-on=1, 45deg=sqrt(2))
    """
    r = (points[:, 0] - x, points[:, 1] - y) # Vectors from source to points in polygon
    w = (vertices[1][1]-vertices[0][1], -vertices[1][0]+vertices[0][0]) # Vector orthogonal to wall (vec=v1-v0, w=(vec_y,-vec_x))
    r_in_w = r[0]*w[0] + r[1]*w[1] # Inner product for every vector in r with w
    mag_r_w = np.linalg.norm(r, axis=0) * (w[0]**2 + w[1]**2)**0.5 # Multiplied magnitude of vectors
    return np.abs(mag_r_w / r_in_w) # 1 / Cos(th)     ( cos(th) = u.v / (|u| |v|) )


def get_intersection_map(points, x, y, vertices, mask):
    intersection_thickness = get_diagonal_intersection_factor(points, x, y, vertices)
    intersection_map = np.zeros(mask.shape)
    intersection_map[mask] = intersection_thickness
    return intersection_map
    


if __name__ == "__main__":
    from pyrateshield.model_items import Grid
    import matplotlib.pyplot as plt
    
    
    imshape = (200, 200)
    point = (20, 10)
    vertices = np.asarray(((0, 0), (100, 100)))
    grid_size = 10
    origin = [-50, -50]
    pixel_size = 1
    extent =  (origin[0], imshape[1] * pixel_size + origin[0],
               origin[1], imshape[0] * pixel_size + origin[1])
                  

    image = np.random.rand(*imshape)


    poly = get_polygon(point, vertices, extent)


    grid = Grid.make_grid(imshape, extent, imshape)
    
    points, mask = grid_points_in_polygon(grid, poly)
    
    angles = get_diagonal_intersection_factor(points, point[0], point[1], vertices)
    
    intersection_map = get_intersection_map(points, point[0], point[1], vertices, mask)
    
    intersection_map[mask] = angles
    

    #plt.plot(points[:,0], points[:,1], 'gx')
    plt.imshow(intersection_map, extent=extent, cmap='gray')

    plt.plot(point[0], point[1], 'b*')
    plt.plot(vertices[:,0], vertices[:,1], 'g')

    #plt.imshow(mask, alpha=0.25, extent=extent)



