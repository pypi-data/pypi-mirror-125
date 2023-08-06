
import os
import yaml

from pyrateshield import labels, Logger, Observable

from collections.abc import Sequence
import imageio
import numpy as np

CONSTANTS_FILE = "constants.yml"
LOG_LEVEL = Logger.LEVEL_DEBUG

class Isotopes(Sequence):
    def __init__(self, isotopes):
        self._isotopes = isotopes
    
    @property
    def isotope_names(self):
        return [item.name for item in self]

    def __len__(self):
        return len(self._isotopes)
    
    def __getitem__(self, idx):
        if isinstance(idx, str):
            items = [item for item in self if item.name==idx]
            if len(items) > 1 or len(items) == 0:
                raise IndexError(idx)
            else:
                return self[self.index(items[0])]     
            
        return self._isotopes[idx]
       
class Grid:
    _distance_map = None
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        
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
    def make_grid(cls, shape=None, extent=None, grid_matrix_size=None):
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
        
    @staticmethod
    def make_grid_pyshield(extent=None, grid_matrix_size=None):
        # Ga ik niet meer gebruiken maar laat er nog even in staan. Als ik
        # weer tegen rare problemen aanloop kan ik het nog gebruiken
        
        # onderstaant geeft 1 op 1 hetzelfde grid nu
        
        raise DeprecationWarning()
        def get_spaced_axis(xi_range, gi):
            start, stop = xi_range
            remainder = (stop - start) % grid_matrix_size
            offset = remainder / 2
            offset = 0
            start += 0.5 * gi
            p = np.arange(start+offset, stop, step=gi)
            return p
        
        yi_range = extent[3] - extent[2]
        xi_range = extent[1] - extent[0]
        
        grid_spacing_y = yi_range / grid_matrix_size
        
        
        grid_spacing_x = xi_range / (int(xi_range / grid_spacing_y))

        xi = get_spaced_axis(extent[0:2], grid_spacing_x)

        # why is y inverted ?? (probably because y-axis increases from bottom
        # to top instead of standard top to bottom).
        yi = get_spaced_axis(extent[2:],  grid_spacing_y)[::-1]

        X, Y = np.meshgrid(xi, yi)
        
        return Grid(X, Y)
    
### Base class
class ModelItem(Observable):
    EVENT_UPDATE = 'event_update'
    EVENT_ENABLED_CHANGED = 'event_enabled_changed'
    _attr_dct = {}
    _attr_defaults = {}
    _constants = None
    _enabled = True
    
    def __init__(self, enabled=True, **kwargs):
        Logger.__init__(self, log_level=LOG_LEVEL)
        Observable.__init__(self)
        self.enabled = enabled
        for var in self._attr_dct.keys():
            if var in kwargs.keys():
                value = kwargs[var]
            else:
                value = None
            setattr(self, var, value)   

    @property
    def enabled(self):
        return self._enabled
    
    @enabled.setter
    def enabled(self, enabled):
        if self._enabled != enabled:
            self._enabled = enabled
            self.emit(self.EVENT_ENABLED_CHANGED, self)
        

    @property
    def constants(self):
        if self._constants is None:
            self._constants = Constants()
        return self._constants
            
    def __copy__(self):
        return self.__class__.from_dict(self.to_dict())
            
    def __setattr__(self, attr_name, value):
        if value is None:
            if attr_name in self._attr_dct.keys():
                label = self._attr_dct[attr_name]
                if label in self._attr_defaults.keys():
                    value = self._attr_defaults[label]
                    
        super().__setattr__(attr_name, value)
            
        if attr_name in self._attr_dct.keys():
            self.emit(self.EVENT_UPDATE, event_data=self)
            
    def update_by_dict(self, dct):
        update = False
        for key, value in dct.items():
            attr = self.attr_from_label(key)
            if getattr(self, attr) != value:
                super().__setattr__(attr, value)
                update = True
        if update:
            self.emit(self.EVENT_UPDATE, self)
        
    @classmethod
    def from_dict(cls, dct):
        obj = cls()
        
        setattr(obj, 'enabled', dct.pop(labels.ENABLED, True))
        
        for var, label in obj._attr_dct.items():
            value = dct[label]
            setattr(obj, var, value)
        return obj
    
    def to_dict(self):
        dct = {label: getattr(self, var)\
               for var, label in self._attr_dct.items()}
        dct[labels.ENABLED] = self.enabled
        return dct
    
    def attr_from_label(self, label):
        if label == labels.ENABLED:
            return 'enabled'
        else:
            index = list(self._attr_dct.values()).index(label)
        return list(self._attr_dct.keys())[index]
        
    
    def __str__(self):
        return "\n".join([f"{k}: {v}" for k, v in self.to_dict().items()])
    
    def __repr__(self):
        return self.__str__()
    
    
class NamedModelItem(ModelItem):
    EVENT_NAME_UPDATE = 'event_name_update'
    _name = None
    default_name = 'default_item_name'
    
    @property
    def name(self):
        if self._name is None:
            self._name = self.default_name
        return self._name

    @name.setter
    def name(self, name):
        if self._name != name:
            self._name = name
            self.emit(self.EVENT_NAME_UPDATE, self)
        return self
    

class Material(NamedModelItem):
    default_name = 'Lead'
    
    _attr_dct = {
        "name": labels.NAME,
        "density": labels.DENSITY,
    }
    
    _attr_defaults = {labels.DENSITY: 11.35 }
    
    
class Isotope(NamedModelItem):
    default_name = 'F-18'
    
   
    _attr_dct = {
        "name": labels.NAME,
        "half_life": labels.HALF_LIFE,
        "self_shielding_options": labels.SELF_SHIELDING_OPTIONS,
    }
    
    _attr_defaults = {
                      labels.HALF_LIFE: 1.8295,
                      labels.SELF_SHIELDING_OPTIONS: ['Body', 'None']}
                      

class ArcherParams(ModelItem):
    _attr_dct = {
        "kvp": labels.KVP,
        "archer": labels.ARCHER,
        "dcc": labels.DCC,
    }

class Dosemap(ModelItem):
    _grid = None
    _extent = None
    _grid_matrix_size = None
    _attr_dct = {
       "grid_matrix_size": labels.GRID_MATRIX_SIZE,
       "extent": labels.EXTENT,
       "engine": labels.ENGINE,
    }
    
    _attr_defaults = {labels.GRID_MATRIX_SIZE: 100,
                      labels.EXTENT: [None],
                      labels.ENGINE: labels.RADTRACER} 
    
    @classmethod
    def from_dict(cls, dct):
        # HACK to be compatible with old files for now
        # engine is defined in dosemap and in Modlel ! FIX 
        dct[labels.ENGINE] = dct.pop(labels.ENGINE, labels.PYSHIELD)
        return super().from_dict(dct)
                  
    def to_grid_coords(self, coords_cm):
        shape = self.shape
        x, y = coords_cm
        x0, x1, y0, y1 = self.extent
        j = (y1-y)/(y1-y0) * shape[0] - 0.5
        i = (x-x0)/(x1-x0) * shape[1] - 0.5
        return np.array((j, i))
        
    @property
    def extent(self):
        # convert np and tuple to list for clean yaml output
        if self._extent is None:
            self._extent =  [0 , self.grid_matrix_size, 0, self.grid_matrix_size]
        elif isinstance(self._extent, tuple):
            self._extent = list(self._extent)
        elif isinstance(self._extent, np.ndarray):
            self._extent = [float(ei) for ei in self._extent]
        return self._extent
    
    @extent.setter
    def extent(self, extent):
        self._extent = extent
        self._grid = None
        self._shape = None
        
    @property
    def grid_matrix_size(self):
        if self._grid_matrix_size is None:
            self._grid_matrix_size = self._attr_defaults["grid_matrix_size"]
        return self._grid_matrix_size
    
    @grid_matrix_size.setter
    def grid_matrix_size(self, grid_matrix_size):
        self._grid_matrix_size = grid_matrix_size
        self._shape = None
        self._grid = None
        
    @property
    def grid(self):  
        if self._grid is None:
            grid = Grid.make_grid(shape=self.shape, 
                                  extent=self.extent,
                                  grid_matrix_size=self.grid_matrix_size)
            self._grid = grid
        return self._grid
    
    @property
    def shape(self):
        if self._shape is None:
            x0, x1, y0, y1 = self.extent
            y_size = self.grid_matrix_size
            self._shape = (int(y_size), int(y_size * (x1-x0)/(y1-y0)))
        return self._shape
    
class Geometry(ModelItem):
    _origin_cm = None
    _pixel_size_cm = None
    _attr_dct = {
        "pixel_size_cm":     labels.PIXEL_SIZE_CM,
        "origin_cm":         labels.ORIGIN_CM,
        'locked':            labels.LOCKED}
    
    _attr_defaults = {
        labels.PIXEL_SIZE_CM: 1,
        labels.ORIGIN_CM: [0, 0],
        labels.LOCKED: False}

    
    def get_extent(self, image):
        if image is None or self.pixel_size_cm is None\
            or self.origin_cm is None:
                return (0, 1, 0, 1)
        else:
            extent = (-self.origin_cm[0],
                      image.shape[1] * self.pixel_size_cm - self.origin_cm[0],
                      -self.origin_cm[1],
                      image.shape[0] * self.pixel_size_cm - self.origin_cm[1])
        return extent
    
    def pixels_to_cm(self, point):
        oo = self.origin_cm
        pp = self.pixel_size_cm
        return [point[0] * pp - oo[0], point[1] * pp - oo[1]]

    def cm_to_pixels(self, point):
        oo = self.origin_cm
        pp = self.pixel_size_cm
        return [(point[0] + oo[0])/ pp, (point[1] + oo[1]) / pp]
        


class MeasuredGeometry(Geometry):
    _distance_cm = None
    
    _attr_dct = {
        "origin_cm":         labels.ORIGIN_CM,
        "vertices_pixels":   labels.VERTICES_PIXELS,
        "distance_cm":       labels.REAL_WORLD_DISTANCE_CM,
        'locked':            False}
    
    _attr_defaults = {
        labels.REAL_WORLD_DISTANCE_CM: 1,
        labels.ORIGIN_CM: [0, 0],
        labels.VERTICES_PIXELS: [[0, 0], [1, 0]]}
    

    
    @property
    def vertices_cm(self):
        vv = self.vertices_pixels
        return [self.pixels_to_cm(vv[0]), self.pixels_to_cm(vv[1])]
    

    
    @property
    def distance_pixels(self):
        vvp = self.vertices_pixels
        dpixels = np.sqrt((vvp[0][0]-vvp[1][0])**2\
                          + (vvp[0][1] - vvp[1][1])**2)

        dpixels =  float(dpixels) if dpixels > 0 else 1
        return dpixels
    
    @property
    def pixel_size_cm(self):
        return self.distance_cm / self.distance_pixels
    
    def to_fixed_geometry(self):
        return Geometry(pixel_size_cm=self.pixel_size_cm,
                        origin_cm=self.origin_cm)
        
        
    
class Floorplan(ModelItem):
    EVENT_UPDATE_IMAGE     = 'event_update_image'
    EVENT_UPDATE_GEOMETRY  = 'event_geometry_update'
   
    _attr_dct = {
        "filename": labels.FILENAME,
        "geometry": labels.GEOMETRY}
        
    _filename = None
    _image = None    

    def __init__(self, *args, **kwargs):
        ModelItem.__init__(self, *args, **kwargs)
        
        
        

    @property
    def extent(self):
        return self.geometry.get_extent(self.image)

    @property
    def geometry(self):
        if self._geometry is None:
            self._geometry = Geometry()
        return self._geometry
    
    @geometry.setter
    def geometry(self, geometry):
        self._geometry = geometry
        self._connect_geometry()
        self.emit(self.EVENT_UPDATE_GEOMETRY, self.geometry)
        
    def _connect_geometry(self):
        callback = lambda _: self.emit(self.EVENT_UPDATE_GEOMETRY, 
                                       self.geometry)
        
        self.geometry.connect(self, self.geometry.EVENT_UPDATE, callback)
        
    def get_empty_image(self):
        return np.ones((100, 100, 3))
    
    @property
    def image(self):
        if self._image is None:
            if self.filename is None:
                self._image = self.get_empty_image()
            elif self.filename is not None and os.path.exists(self.filename):
                self._image = imageio.imread(self.filename)
            else:
                self._image = self.get_empty_image()
        return self._image
    
    @image.setter
    def image(self, image):
        if image is self._image: return
        
        if not isinstance(image, np.ndarray):
            raise TypeError()
            
        if image.ndim == 2 and image.shape[0] > 1 and image.shape[1] > 1:
            image = np.stack([image]*3, axis=2) # convert to RGB
            
        if image.ndim == 3 and image.shape[0] > 1\
            and image.shape[1] > 1 and image.shape[2] in (3, 4):
            self._image = image
        else:
            raise ValueError('Type or shape of image is invalid!')
            
        self.emit(self.EVENT_UPDATE_IMAGE, self.image)
    
    def load_image_from_file(self, file):
        if file is None: return
        if not os.path.exists(file):
            file = os.path.join(os.path.dirname(__file__), file)
            if not os.path.exists(file):
                return
            
        try:
            image = imageio.imread(file)
        except:
            return
        
        self.image = image
        self._filename = file
        self.geometry.locked = False
    
    @property
    def filename(self):
        return self._filename
    
    @filename.setter
    def filename(self, filename):
        self.load_image_from_file(filename)

        
    @classmethod
    def from_dict(cls, dct):
        obj = cls()
        for var, label in obj._attr_dct.items():
            value = dct[label]
            if label == labels.GEOMETRY:
                if 'distance_cm' in value.keys():
                    value = MeasuredGeometry.from_dict(value)
                else:
                    value = Geometry.from_dict(value)
            setattr(obj, var, value)
        return obj
    
    def to_dict(self):
        dct = {label: getattr(self, var)\
               for var, label in self._attr_dct.items()}
        dct[labels.GEOMETRY] = dct[labels.GEOMETRY].to_dict()
        return dct
    

    


class Shielding(NamedModelItem):
    default_name = 'Shielding'
    label = labels.SHIELDINGS

    _constants = None

    _materials = None

    _attr_dct = {
        "name": labels.NAME,
        "color": labels.COLOR,
        "linewidth": labels.LINEWIDTH,
        "materials": labels.MATERIALS,
    }
    
    _attr_defaults = {labels.COLOR: 'red',
                      labels.LINEWIDTH: 1,
                      labels.NAME: 'shielding'}
    
    @property
    def available_materials(self):
        return list(set([item.name for item in self.constants.materials]))
    
    @property
    def materials(self):
        if self._materials is None:
            self._materials = [[labels.EMPTY_MATERIAL, 0], 
                               [labels.EMPTY_MATERIAL, 0]]
        return self._materials
    
    @materials.setter
    def materials(self, materials):
        self._materials = materials
        

class Wall(ModelItem):
    default_name = 'Wall'
    label = labels.WALLS
    _vertices = None
    _shielding = None
    
    _attr_dct = {
        "vertices": labels.VERTICES, 
        "shielding": labels.SHIELDING,
    }
    
    _attr_defaults = {
        labels.VERTICES: [[0, 0], [1, 1]],
        labels.SHIELDING: labels.EMPTY_SHIELDING
    }
        
    def set_vertex(self, index, vertice):
        # needed by gui
        self.vertices[index] = vertice
        self.emit(self.EVENT_UPDATE, event_data=self)
        

        
        
   

class CriticalPoint(NamedModelItem):
    default_name = 'Critical Point'
    label = labels.CRITICAL_POINTS

    _attr_dct = {
        "name": labels.NAME,
        "position": labels.POSITION, 
        "occupancy_factor": labels.OCCUPANCY_FACTOR,
    }
    
    _attr_defaults = {
        labels.NAME: 'critical_point',
        labels.POSITION: [0, 0],
        labels.OCCUPANCY_FACTOR: 1
    }
    



class SourceNM(NamedModelItem):
    default_name = 'Source NM'
    label = labels.SOURCES_NM
    _attr_dct = {
        "name": labels.NAME,
        "position": labels.POSITION,  
        "number_of_exams": labels.NUMBER_OF_EXAMS,
        "isotope": labels.ISOTOPE,
        "self_shielding": labels.SELF_SHIELDING,
        "activity": labels.ACTIVITY,
        "duration": labels.DURATION,
        "apply_decay_correction": labels.APPLY_DECAY_CORRECTION, 
        "apply_biological_decay": labels.APPLY_BIOLOGICAL_DECAY,
        "biological_halflife_hours": labels.BIOLOGICAL_HALFLIFE,
    }
    
    
    _attr_defaults = {
        labels.POSITION: [0, 0],
        labels.NUMBER_OF_EXAMS: 1,
        labels.ISOTOPE: 'F-18',
        labels.SHIELDING: 'None',
        labels.ACTIVITY: 1,
        labels.DURATION: 1,
        labels.APPLY_DECAY_CORRECTION: True,
        labels.APPLY_BIOLOGICAL_DECAY: False,
        labels.BIOLOGICAL_HALFLIFE: 0}
    
    
   
        
    @property
    def available_isotopes(self):
        return self.constants.isotopes.isotope_names
        
    @property
    def isotope(self):
        return self._isotope
    
    @isotope.setter
    def isotope(self, isotope):
        # @Rob hier gelijk het isotope object toekennen vanuit de constants
        if isinstance(isotope, str):
            isotope = self.constants.get_isotope_by_name(isotope)
        self._isotope = isotope
        
    def to_dict(self):
        dct = super().to_dict()
        dct[labels.ISOTOPE] = self.isotope.name 
        return dct
        
    @property
    def time_integrated_activity_coefficient_mbqh(self):
        activity = self.activity * self.number_of_exams 
        
        if self.apply_decay_correction:
            decay_constant = np.log(2) / self.isotope.half_life
            
            if self.apply_biological_decay:
                decay_constant += np.log(2) / self.biological_halflife_hours
                
            tiac = activity / decay_constant * \
                (1 - np.exp(-decay_constant * self.duration))
        else:
            tiac = activity * self.duration
        return tiac
    
    @property
    def tiac(self):
        return self.time_integrated_activity_coefficient_mbqh

class SourceXray(NamedModelItem):
    default_name = 'Source Xray'
    label = labels.SOURCES_XRAY
    _kvp = None
    _attr_dct = {
        "name": labels.NAME,
        "position": labels.POSITION, 
        "number_of_exams": labels.NUMBER_OF_EXAMS,
        "kvp": labels.KVP,
        "dap": labels.DAP,
    }
    
    _attr_defaults = {
        labels.POSITION: [0,  0],
        labels.DAP: 1,
        labels.NUMBER_OF_EXAMS: 1
        }

        
    @property 
    def kvp(self):
        if self._kvp is None:
            self._kvp = self.available_kvp[0]
        return self._kvp
    
    @kvp.setter
    def kvp(self, kvp):
        self._kvp = kvp
            
    @property
    def available_kvp(self):
        return list(set([item.kvp for item in self.constants.xray]))
    
        



class SourceCT(NamedModelItem):
    default_name = 'Source CT'
    label = labels.SOURCES_CT
    _attr_dct = {
        "name": labels.NAME,
        "position": labels.POSITION, 
        "number_of_exams": labels.NUMBER_OF_EXAMS,
        "body_part": labels.BODY_PART,
        "kvp": labels.KVP,
        "dlp": labels.DLP,
    }
    
    
    _attr_defaults = {
        labels.POSITION: [0,  0],
        labels.DLP: 1,
        labels.NUMBER_OF_EXAMS: 1,
        labels.BODY_PART: 'Body'
        }

        
    @property 
    def kvp(self):
        if self._kvp is None:
            self._kvp = self.available_kvp[0]
        return self._kvp
    
    
    @kvp.setter
    def kvp(self, kvp):
        self._kvp = kvp
        
    @property
    def available_kvp(self):
        return list(set([item.kvp for item in self.constants.ct]))
    
           
class Constants:
    def __init__(self):
        try:
            wdir = os.path.split(__file__)[0] 
        except:
            wdir = os.getcwd()
            
        with open(os.path.join(wdir, CONSTANTS_FILE)) as f:
            constants = yaml.safe_load(f)

        self.materials = [Material.from_dict(item)\
                          for item in constants[labels.MATERIALS]]
            
        self.isotopes = Isotopes([Isotope.from_dict(item)\
                         for item in constants[labels.ISOTOPES]])
            
        self.ct = [ArcherParams.from_dict(item)\
                   for item in constants[labels.CT_PARAMETERS]]
            
        self.xray = [ArcherParams.from_dict(item)\
                     for item in constants[labels.XRAY_PARAMETERS]]
        
        # Voor nu neem ik aan dat de self shielding options niet per isotoop 
        # verschillen. Eventueel later als feature toevoegen?
        self.self_shielding_options = constants[labels.SELF_SHIELDING_OPTIONS]
        
        self.body_part_options = constants[labels.BODY_PART_OPTIONS]

    def get_isotope_by_name(self, name):
        return [x for x in self.isotopes if x.name == name][0]
    
    def get_material_by_name(self, name):
        return [x for x in self.materials if x.name == name][0]
    

