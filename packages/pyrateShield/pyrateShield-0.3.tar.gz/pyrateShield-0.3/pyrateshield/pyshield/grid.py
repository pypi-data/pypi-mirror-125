import numpy as np
from pyrateshield.pyshield.line_intersect import intersect_line, angle_between_lines
from pyrateshield.pyshield import polygon
import numpy as np
import math

class Grid:
    _distance_map = None
    _shadow = None
    _X = None
    _Y = None
    _extent = None
    _line_intersect = None
    def __init__(self, extent, shape):
        self.extent = extent
        self.shape = shape
    
    @property
    def XY(self):
        if self._XY is None:
            x0, x1, y0, y1 = self.extent
            xcoords = x0 + (np.arange(self.shape[1])+0.5)*(x1-x0)/self.shape[1]
            ycoords = y1 - (np.arange(self.shape[0])+0.5)*(y1-y0)/self.shape[0]
            self._XY = np.meshgrid(xcoords, ycoords, sparse=False)
        return self._XY
    
    
    @property
    def extent(self):
        return self._extent
    
    
    @extent.setter
    def extent(self, extent):
        self._extent = extent
        
    @property
    def shape(self):
        return self._shape
    
    @shape.setter
    def shape(self, shape):
        self._XY = None
        self._distance_map = None
        self._shadow = None
        self._shape = shape
    
    
    @property
    def X(self):
        return self.XY[0]
    
    @property
    def Y(self):
        return self.XY[1]
    
    def line_intersect(self, vertices1, vertices2):
        def norm(vv):
            return math.sqrt((vv[0][0] - vv[1][0]) **2 + (vv[0][1] - vv[1][1])**2)
    
        if self._line_intersect is None:
            self._line_intersect = {}
        
        vertices1 = self.vertices_to_tuple(vertices1)
        vertices2 = self.vertices_to_tuple(vertices2)
    
        
        if (vertices1, vertices2) in self._line_intersect.keys():
            return self._line_intersect[(vertices1, vertices2)]
        elif (vertices2, vertices1) in self._line_intersect.keys():
            return self._line_intersect[(vertices2, vertices1)]
        else:
            if norm(vertices1) == 0 or norm(vertices2)==0:
                point = (None, None)
                angle = 0
            else:
                point = intersect_line(vertices1, vertices2)
                angle = angle_between_lines(vertices1, vertices2)
            self._line_intersect[(vertices1, vertices2)] = (point, angle)
            return self._line_intersect[(vertices1, vertices2)]
        
        
    def _shadow_map_and_shadow_points(self, point, vertices):
        tpoint = self.point_to_tuple(point)
        tvertices = self.vertices_to_tuple(vertices)
        
        if self._shadow is None:
            self._shadow = {}

        if (tpoint, tvertices) not in self._shadow.keys():
            poly = self._poly(point, vertices)
            points, mask = polygon.grid_points_in_polygon(self, poly)
            self._shadow[(tpoint, tvertices)] = (points, mask)
        return self._shadow[(tpoint, tvertices)]

    def _poly(self, point, vertices):
        point = np.asarray(point)
        line = np.asarray(vertices)
        poly = polygon.get_polygon(point, line, self.extent)
        return poly
    
    @staticmethod
    def point_to_tuple(point):
        return (float(point[0]), float(point[1]))

    @staticmethod
    def vertices_to_tuple(vertices):        
        return ((float(vertices[0][0]), float(vertices[0][1])),
                (float(vertices[1][0]), float(vertices[1][1])))

    def shadow_points(self, points, vertices):
        points, _ = self._shadow_map_and_shadow_points(points, vertices)
        return points

    def shadow_map(self, point, vertices):
        _, shadow_map = self._shadow_map_and_shadow_points(point, vertices)
        return shadow_map
    
        
    def distance_map_meters(self, x=0, y=0):
        x, y = (float(x), float(y))

        if self._distance_map is None:
            # cache results in dict when re-used
            self._distance_map = {}

        if (x, y) not in self._distance_map.keys():
            # no distance map yet calculated for point x, y
            distance_map = np.sqrt( ((self.X-x)/100)**2\
                                   + ((self.Y - y) / 100)**2)
            # add distance map for x, y to cache
            self._distance_map[(x, y)] = distance_map

        # return distance map
        return self._distance_map[(x, y)]
    
    @classmethod
    def make_grid(cls, shape=None, extent=None):
        x0, x1, y0, y1 = extent
        xcoords = x0 + (np.arange(shape[1])+0.5)*(x1-x0)/shape[1]
        ycoords = y1 - (np.arange(shape[0])+0.5)*(y1-y0)/shape[0]
        return cls(*np.meshgrid(xcoords, ycoords, sparse=False))
    
    @staticmethod
    def multiply(*args):
        # used to multiple an iterable of arrays. Can be used safely if
        # iterable has just one element
        if len(args) == 1:
            return args[0]
        else:
            return np.prod(args, axis=0)
        
    
if __name__ == "__main__":
    from pyrateshield.model import Model
    import matplotlib.pyplot as plt
    
    model = Model.load_from_project_file('/Users/marcel/git/pyrateshield/example_projects/SmallProject/project.psp')
    model.match_extent_to_floorplan()
    
    model.dosemap.extent
    model.dosemap.shape
    
    grid = Grid(model.dosemap.extent, model.dosemap.shape)
    
    
    
    