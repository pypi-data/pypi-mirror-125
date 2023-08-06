from collections.abc import MutableMapping
import time
from pyrateshield.pyshield.constants import SELF_SHIELDING_WATER
from pyrateshield.pyshield import polygon
from pyrateshield.pyshield import Grid
from pyrateshield.pyshield.physics import isotope, doserates
import math

EMPTY_SHIELDING  = 'None'
EMPTY_MATERIAL = 'None'
EMPTY_KEYS = (EMPTY_SHIELDING, EMPTY_MATERIAL)

from pyrateshield.pyshield.constants import ISOTOPES, ENERGY_keV, ABUNDANCE, DECAY_CONSTANT, BUILDUP_FACTORS, MFP

from pyrateshield.pyshield import PHYSICS


import numpy as np
import scipy.interpolate as si


class BuildupHelper:
    _interpolators = None
    
    def __init__(self):
        self.tables = PHYSICS[BUILDUP_FACTORS]
    
    @staticmethod
    def interpolant(x,y,f):
        # https://stackoverflow.com/questions/47087109/evaluate-the-output-from-scipy-2d-interpolation-along-a-curve
        """ Same interface as interp2d but the returned interpolant will evaluate its inputs as pairs of values.
        """
        x,y = np.asarray(x), np.asarray(y)
        return (si.dfitpack.bispeu(f.tck[0], f.tck[1], f.tck[2], f.tck[3], f.tck[4], x.ravel(), y.ravel())[0]).reshape(x.shape)
        # Wrapping the scipy interp2 function to call out interpolant instead
        #return lambda x,y: interpolant(x,y,si.interp2d(*args,**kwargs))

    
    def _get_interpolator(self, material):
        if self._interpolators is None:
            self._interpolators = {}
        
        if material not in self._interpolators.keys():
            table       = self.tables[material]
            n_mfp       = np.asarray(table[MFP], 'float64')
            table       = table.drop(MFP, axis=1)
            factors     = np.asarray(table, 'float64')
            energies    = np.asarray(table.columns, dtype='float64')
            interpolator = si.interp2d(energies, n_mfp, factors)
            self._interpolators[material] = lambda x, y: self.interpolant(x, y, interpolator)
        return self._interpolators[material]
    
    def calculate(self, material, energy_keV,  thickness):
        # 2DO cutoff at lowest mean free path instead of 0
        interpolator = self._get_interpolator(material)
        
        if isinstance(thickness, np.ndarray):
            index = thickness > 0
            thickness = thickness[index]
        else:
            index = None
        
        
        n_mfpi    = isotope.number_mean_free_path(energy_keV, 
                                                  material, 
                                                  thickness)
        
        if not isinstance(energy_keV, np.ndarray) and index is not None:
            energy_keV = np.ones(len(n_mfpi)) * energy_keV
        
    
        values = interpolator(energy_keV/1000, n_mfpi)
        
        if index is not None:
            buildup = np.ones(len(index))
             
            buildup[index] = values.flatten()
        else:
            buildup = values

        return buildup
    
    

class NumericDict(MutableMapping):
    def __init__(self, items=None):
        items = {} if items is None else items
        self._items=items
        
    def __getitem__(self, key):
        return self._items[key]
    
    def __setitem__(self, key, value):
        if key in self._items.keys() and key not in EMPTY_KEYS:
            raise ValueError('Keys are read only!')
        self._items[key] = value
        
    def __delitem__(self, key):
        del self._items[key]
        
    def __len__(self):
        return len(self._items)
    
    def __iter__(self):
        return self._items.__iter__()
    
    def __mult__(self, other):
        obj = self.copy()
        for key, value in other.keys():
            if key in obj.keys():
                obj._items[key] *= other[key]
            else:
                obj._items[key] = other[key]
        return obj
    
    def __rmult__(self, other):
        return self.__mult__(other)
    
    def __imult__(self, other):
        for key in other.keys():
            if key in self.keys():
                self._items[key] *= other[key]
        return self

    def __neg__(self):
        obj = self.copy()
        for key in obj.keys():
            obj._items[key] = self[key] * -1
        return obj
    
    def __pow__(self, power):
        obj = self.copy()
        for key in obj.keys():
            obj._items[key] = self[key] ** power
        return obj
    
    def __ipow__(self, power):
        for key in self.keys():
            self._items[key] **= power
        return self

    def __add__(self, other):
        obj = self.copy()
        for key, value in other:
            if key in obj.keys():
                obj._items[key] += other[key]
            else:
                obj[key] = other[key]
        return other

    def __radd__(self, other):
        return self.__add__(other)
    
    def __iadd__(self, other):
        for key, value in other.items():
            if key in self.keys():
                self._items[key] += other[key]
            else:
                self._items[key] = other[key]
        return self
    
class GammaRayOnGrid:
    _h10 = None
    _distance_map = None
    _dose_map = None
    def __init__(self, position, keV=0, abundance=0, grid=None):
        self.x, self.y = float(position[0]), float(position[1])
        self.keV = keV
        self.abundance = abundance
        self.grid = grid
            
    @property
    def h10(self):
        # uSv/ h per MBq / m2
        if self._h10 is None:
            self._h10 = doserates.H10(self.keV, abundance=self.abundance)
        return self._h10 

    def dose_at_point(self, point):
        # mSv
        x, y = point
        distance = np.sqrt((x-self.x)**2 + (y-self.y)**2) / 100 # cm --> m
        if distance == 0:
            return float('Inf')
        else:
            dose = self.h10 / (distance**2) / 1000 #uSv --> mSv
        return dose

    @property
    def dosemap(self):
        return self.get_dosemap()

    def get_dosemap(self):
        # mSv / h per MBq / m2
        distance_map = self.grid.distance_map_meters(self.x, self.y)
        return self.h10 /  distance_map**2 / 1000 # uSv --> mSv
    
    

class IsotopeOnGrid:
    _gammarays = None
    def __init__(self, grid=None, position=None, isotope=None):

        isotope_data = PHYSICS[ISOTOPES][isotope.name]
        
        self.position = position
        self.grid = grid
        self.keVs = isotope_data[ENERGY_keV]
        self.abundance = isotope_data[ABUNDANCE]
        self.decay_constant = isotope_data[DECAY_CONSTANT]
        
    
        
    @property
    def gammarays(self):
        if self._gammarays is None:
            self._gammarays = {}
            for ei, ai in zip(self.keVs, self.abundance):
                ray = GammaRayOnGrid(grid=self.grid, keV=ei, abundance=ai, 
                                     position=self.position)
                self._gammarays[ei] = ray
                                                   
        return self._gammarays

    
class SourceWallMap():
    _intersection_map = None
    _material_map = None
    _intersection_time = 0
    _counter = 0
    def __init__(self, source=None, wall=None, grid=None, shielding=None):
        self.source = source
        self.wall = wall
        self.shielding = shielding
        self.grid = grid 
        

    @property
    def intersection_map(self):
        start = time.time()
        if self._intersection_map is None:
            x, y = self.source.position
            vertices = self.wall.vertices
            mask = self.grid.shadow_map((x,y), vertices)
            points = self.grid.shadow_points((x,y), vertices)
            intersection_map = polygon.get_intersection_map(points, x, y, 
                                              vertices, mask)
            self._intersection_map = intersection_map
        stop = time.time()
        self._intersection_time += (stop-start)
        return self._intersection_map
    
    @property
    def material_map(self):
        if self._material_map is None:
            material_map = NumericDict()
            for material, thickness in self.shielding.materials:
    
                material_map[material] = (thickness * self.intersection_map)
             
            self._material_map = material_map
            
            
            
        return self._material_map
    
    def line_intersect(self, point):
        vertices1 = self.wall.vertices
        vertices2 = (self.source.position, point)
        point, angle = self.grid.line_intersect(vertices1, vertices2)
        SourceWallMap._counter += 1
        return point, angle
    

            
class SourceWallsMap():
    _gammarays = None
    _material_map = None
    _attenuation_map = None
    _buildup_map = None
    _isotope = None
    _line_intersect_thickness = None
    def __init__(self, grid=None, source=None, walls=None, shieldings=None, 
                 buildup_helper=None):
        
        self.source = source
        self.walls = walls
        self.shieldings = shieldings 
        self._items = []
        self.grid = grid
        self.buildup_helper = buildup_helper
    
        
        for wall in walls:
            shielding = shieldings.get_shielding_by_name(wall.shielding)
            sw_map = SourceWallMap(source=source, wall=wall, grid=grid,
                                   shielding=shielding)
            self._items += [sw_map]
            

            
    def line_intersect(self, point):
        return list([item.line_intersect(point) for item in self._items])
    
    def line_thickness(self, point):
        materials = NumericDict()
        for (point, angle), wall in zip(self.line_intersect(point), self.walls):
            if point == (None, None):
                continue
            
            shielding = self.shieldings.get_shielding_by_name(wall.shielding)
            for material, thickness in shielding.materials:
                materials += {material: thickness / math.sin(angle)}
                
        return materials
    
    def dose_at_point(self, point):
        materials = self.line_thickness(point)
        sumdose = 0
        
        for gammaray in self.isotope.gammarays.values():
            dose = gammaray.dose_at_point(point)

            for material, thickness in materials.items():
                if material == EMPTY_MATERIAL: continue
                attenuation = isotope.attenuation(gammaray.keV, 
                                                  material, thickness)
                
                buildup = self.buildup_helper.calculate(material,gammaray.keV, 
                                                        thickness)

                dose = dose * attenuation * buildup
                
            if self.source.self_shielding == 'Body':
                attenuation = isotope.attenuation(gammaray.keV, 
                                                  'Water', SELF_SHIELDING_WATER)
                buildup = self.buildup_helper.calculate('Water',gammaray.keV, 
                                                        SELF_SHIELDING_WATER)
                dose = dose * attenuation * buildup
                
            sumdose += dose
            
        sumdose *= self.source.tiac
        return sumdose
     
        
    @property
    def isotope(self):
        if self._isotope is None:
            self._isotope = IsotopeOnGrid(grid=self.grid,
                                          position=self.source.position,
                                          isotope=self.source.isotope)
        return self._isotope
    
    @property
    def dosemap(self):
        dosemap = np.zeros(self.grid.X.shape)
        for keV, gammaray in self.isotope.gammarays.items():
            time1 = time.time()
            dosemap_keV = gammaray.dosemap
            time2 = time.time()
            dosemap_keV *= self.attenuation_map(gammaray.keV)
            time3 = time.time()
            dosemap_keV *= self.buildup_map(gammaray.keV)
            time4 = time.time()
            dosemap += dosemap_keV
            time5 = time.time()
            
            #print(time2-time1, time3-time2, time4-time3, time5-time4)
        
        dosemap *= self.source.tiac
        return dosemap
            
   
    @property
    def material_map(self):
        if self._material_map is None:
            material_map = NumericDict()
            for item in self._items:
                material_map += item.material_map
            self._material_map = material_map
            
            if self.source.self_shielding == 'Body':
            
                water_map = np.ones(self.grid.X.shape) * SELF_SHIELDING_WATER
                self._material_map += {'Water': water_map}
        
            
        return self._material_map
    
    def attenuation_map(self, keV):
        return math.prod([self.material_attenuation_map(material, keV)\
                          for material in self.material_map.keys()])
            
    def buildup_map(self, keV):
        return math.prod([self.material_buildup_map(material, keV)\
                          for material in self.material_map.keys()])
            
            
    
    def material_attenuation_map(self, material, keV):
        keV = float(keV)
        if self._attenuation_map is None:
            self._attenuation_map = NumericDict()
        
        if (material, keV) not in self._attenuation_map.keys():
            attenuation_map = self.get_material_attenuation_map(material, keV)
            self._attenuation_map[(material, keV)] = attenuation_map
            
        return self._attenuation_map[(material, keV)]
            
    def get_material_attenuation_map(self, material, keV):
        if material == EMPTY_SHIELDING:
            attenuation = np.ones(self.grid.X.shape)
        else:
            thickness_map = self.material_map[material]
            attenuation = isotope.attenuation(keV, 
                                              material, 
                                              thickness_map)
            
        return attenuation
    
    def material_buildup_map(self, material, keV):
        time1 = time.time()
        keV = float(keV)
        if self._buildup_map is None:
            self._buildup_map = {}
        
        if (material, keV) not in self._buildup_map.keys():
            buildup_map = self.get_material_buildup_map(material, keV)
            self._buildup_map[(material, keV)] = buildup_map
        time2 = time.time()
        #print(time2 - time1)
        return self._buildup_map[(material, keV)]
    
    
    def get_material_buildup_map(self, material, keV):
    
        if material == EMPTY_SHIELDING:
            buildup = np.ones(self.grid.X.shape)
        else:
            thickness = self.material_map[material].flatten()
            if any(thickness>0):
                #buildup = isotope.buildup(keV, material, thickness)
                #buildup = buildup.reshape(self.grid.X.shape)
                    # stop1 = time.time()
                buildup = self.buildup_helper.calculate(material, keV, thickness)
                    # stop2 = time.time()
                    
                    # print(stop1-start1, stop2-stop1)
                # except:
                #     import pickle
                #     import os
                #     file = os.path.join(os.path.split(__file__)[0], 'dump.pickle')
                #     pickle.dump((keV, material, thickness_map), open(file, 'wb'))
                #     raise
                buildup = buildup.reshape(self.grid.X.shape)
            else:
                buildup = np.ones(self.grid.X.shape)
    
        return buildup

    
    
class Engine:
    _source_dose_map = None
    _sources = None
    def __init__(self, grid=None, walls=None, shieldings=None,
                 sources=None):
       
       
        self.grid = grid
        self.buildup_helper = BuildupHelper()
        self.walls = walls
        self.shieldings = shieldings
        
    
    def dose_at_point(self, point, sources=None):
        
        dose = 0
        self.sources = sources
        for item in self._items:
            dose += item.dose_at_point(point)
        return dose
    
    @property
    def sources(self):
        if self._sources is None:
            self._sources = []
        return self._sources
    
    @sources.setter
    def sources(self, sources):
        self._items = []
        self._sources = sources
        for source in self.sources:
            if not source.enabled: continue
            item = SourceWallsMap(grid=self.grid,
                                  source=source,
                                  walls=self.walls,
                                  shieldings=self.shieldings,
                                  buildup_helper=self.buildup_helper)
            
            self._items += [item]
            
    def source_dosemap(self, source):
        self.sources = [source]
        # item = [item for item in self._items if item.source is source][0]
        return self._items[0].dosemap
        
    
    @classmethod
    def from_pyrateshield(cls, model, sources=None):
        grid = Grid(model.dosemap.extent, model.dosemap.shape)
        return cls(grid=grid, sources=sources, walls=model.walls,
                   shieldings=model.shieldings)
    

        
        
    
    
    
if __name__ == "__main__":
    from pyrateshield.model import Model
    import matplotlib.pyplot as plt
    
    model = Model.load_from_project_file('/Users/marcel/git/pyrateshield/example_projects/SmallProject/project.psp')
    model.match_extent_to_floorplan()
    
    engine = Engine.from_pyrateshield(model, sources=model.sources_nm)#[model.sources_nm[0]])
    
    start = time.time()
    
    #     for subitem in item._items:
    #         subitem.material_map
            
    stop = time.time()
        
    
    
        
        