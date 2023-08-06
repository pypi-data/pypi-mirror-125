from pyrateshield import model_items
from pyrateshield import labels, Observable
from collections.abc import MutableSequence
import pickle

    
class ModelItems(MutableSequence, Observable):
    
    EVENT_REMOVE_ITEM   = 'event_remove_item'
    EVENT_ADD_ITEM      = 'event_add_item'
    EVENT_UPDATE_ITEM   = 'event_update_item'
    EVENT_NAME_UPDATE   = 'event_name_update'
    
    _selected_item = None

    def __init__(self, items=None, item_class=None):
        if items is None:
            items = []
        self.items = items
        
        MutableSequence.__init__(self)
        Observable.__init__(self)
        
        self.item_class = item_class

        for item in items:
            self.connect_to_item(item)
            

    def __add__(self, other):
        # HACKY
        if isinstance(other, ModelItems):
            other = other.items
            
        return self.items + other
    
    def __radd__(self, other):
        return self.__add__(other)
            
    def __getitem__(self, index):
        return self.items[index]
    
    def __setitem__(self, index, item):
        if item in self:
            raise IndexError()
        
        
        self[index].disconnect(id(self))
        self.items[index] = item
        
        self[index].connect_to_item(self[index])
        
            
    def __delitem__(self, index):
        item = self[index]
        
        item.disconnect(id(self))
        
        del self.items[index]

        self.emit(self.EVENT_REMOVE_ITEM, (index, item))
  
    def emit_update(self, item):
        if not isinstance(item, model_items.ModelItem):
            raise ValueError()
            
        self.emit(self.EVENT_UPDATE_ITEM, event_data=item)
    
    def emit_name_change(self, item):

        self.emit(self.EVENT_NAME_UPDATE, event_data=item)
    

    def connect_to_item(self, item):
        if not isinstance(item, model_items.ModelItem):
            raise ValueError()
            
        item.connect(id(self), item.EVENT_UPDATE, self.emit_update)
        item.connect(id(self), item.EVENT_ENABLED_CHANGED, self.emit_update)
        if isinstance(item, model_items.NamedModelItem):
            item.connect(id(self), item.EVENT_NAME_UPDATE, self.emit_name_change)
            

        
    def insert(self, index, item):
        self.items.insert(index, item)
        self.connect_to_item(item)
        self.emit(self.EVENT_ADD_ITEM, item)
        
    
    def __len__(self):
        return len(self.items)
            
    def get_new_name(self):
        new_name =  self.item_class.default_name + ' 1'
        i = 1
        while new_name in [item.name for item in self]:
            i += 1
            new_name = self.item_class.default_name + ' ' + str(i)
        return new_name     
            
    def force_unique_name(self, model_item):
        for item in self:
            if item is model_item:
                continue
            if model_item.name == item.name:
                model_item.name = self.get_new_name()
    
        return model_item

        
    def add_new_item(self, **kwargs):
        if self.item_class is not model_items.Wall and 'name' not in kwargs.keys():
            kwargs['name'] = self.get_new_name()
        
        new_item = self.item_class(**kwargs)

        self.append(new_item)
        
        return new_item
    
class ShieldingItems(ModelItems):
    def __init__(self, items=None, item_class=model_items.Shielding):
        
        if items is None:
            items = []
            
        items = [item_class(name=labels.EMPTY_SHIELDING)] + items
        super().__init__(items=items, item_class=item_class)
        
    def __delitem__(self, index):
         if index == 0:
             # will not happend
             raise IndexError()
         else:
             super().__delitem__(index)
             
    def get_shielding_by_name(self, shielding_name):
        if len(self) == 0: return None
        if shielding_name is None: return None
        
        shielding = [shielding for shielding in self\
                     if shielding.name == shielding_name]

        if len(shielding) > 1:
            msg = f'Multiple shieldings exists with name: {shielding_name}'
            raise KeyError(msg)
        elif len(shielding) == 0:
            msg = f'No shieldings exists with name: {shielding_name}'
            raise KeyError(msg)
        return shielding[0]



class Model(Observable):
    _floorplan = None
    _image_data = 'IMAGE_DATA'
    _selected_item = None
    filename = None
    
    EVENT_SELECT_ITEM = 'event_select_item'
    EVENT_UPDATE_FLOORPLAN = 'event_update_floorplan'    
    
    def __init__(self, floorplan=None, dosemap=None, shieldings=None, 
                 walls=None, critical_points=None, sources_ct=None, 
                 sources_nm=None, sources_xray=None):  
        

        Observable.__init__(self)
        # create empty model possibility for gui
        if floorplan is None:
            floorplan = model_items.Floorplan()
        if dosemap is None:
            dosemap = model_items.Dosemap()
        if shieldings is None:
            shieldings = ShieldingItems(item_class=model_items.Shielding)
            s1 = model_items.Shielding(name='Lead 2mm', color='blue', linewidth=2, 
                                       materials=[['Lead', 0.2]])
            s2 = model_items.Shielding(name='Concrete 10cm', color='black', 
                                       linewidth=2, 
                                       materials=[['Concrete', 10]])
            shieldings += [s1, s2]
           
            
            
        if walls is None:
            walls = ModelItems(item_class=model_items.Wall)
        if critical_points is None:
            critical_points = ModelItems(item_class=model_items.CriticalPoint)
        if sources_ct is None:
            sources_ct = ModelItems(item_class=model_items.SourceCT)
        if sources_nm is None:
            sources_nm = ModelItems(item_class=model_items.SourceNM)
        if sources_xray is None:
            sources_xray = ModelItems(item_class=model_items.SourceXray)

        self.constants = model_items.Constants()
        self.plot_style = Plotstyle()
                
        self.floorplan = floorplan
        self.dosemap = dosemap        
        self.shieldings = shieldings        
        self.walls = walls        
        self.critical_points = critical_points        
        self.sources_nm = sources_nm
        self.sources_ct = sources_ct
        self.sources_xray = sources_xray        
        
        #self.connect_to_containers()
        
    @property
    def floorplan(self):
        if self._floorplan is None:
            self._floorplan = model_items.Floorplan()
        return self._floorplan
    
    @floorplan.setter
    def floorplan(self, floorplan):
        self._floorplan = floorplan
        self.emit(self.EVENT_UPDATE_FLOORPLAN, self.floorplan)
        

    # def connect_to_containers(self):
    #     self.logger.debug('Connecting containers!!!!')
    #     for container in (self.sources_ct, self.sources_nm, self.sources_xray,
    #                       self.critical_points, self.walls):
            
    #         callback = lambda item, container=container: \
    #                 self.receive_selected_item(item, container)
                
    #         container.connect(self, container.EVENT_SELECT_ITEM, callback)

    def shift_cm(self, dx_cm, dy_cm):
         self._shift_walls_cm(dx_cm, dy_cm)
         self._shift_sources_cm(dx_cm, dy_cm)
         
    def _shift_walls_cm(self, shiftx, shifty):
         for wall in self.walls:
             wall.vertices[0][0] += shiftx
             wall.vertices[1][0] += shiftx
             wall.vertices[0][1] += shifty
             wall.vertices[1][1] += shifty
             wall.emit(wall.EVENT_UPDATE, wall)
             
    def _shift_sources_cm(self, shiftx, shifty):
         containers = [self.critical_points, self.sources_nm,
                       self.sources_xray, self.sources_ct]
         
         for container in containers:
             for item in container:
                 item.position[0] += shiftx   
                 item.position[1] += shifty
                 item.emit(item.EVENT_UPDATE, item)
                 
    def get_model_items_by_label(self, label):
        if label == labels.SOURCES_CT:
            return self.sources_ct
        elif label == labels.SOURCES_XRAY:
            return self.sources_xray
        elif label == labels.SOURCES_NM:
            return self.sources_nm
        elif label == labels.CRITICAL_POINTS:
            return self.critical_points
        elif label == labels.SHIELDINGS:
            return self.shieldings
        elif label == labels.WALLS:
            return self.walls
        elif label == labels.FLOORPLAN:
            return self.floorplan
        elif label == labels.DOSEMAP:
            return self.dosemap
        else:
            raise KeyError(label)



    @property
    def selected_item(self):
        return self._selected_item
    
    @selected_item.setter
    def selected_item(self, item):
        self.select_item(item)
        
    def container_for_item(self, item):
        if isinstance(item, model_items.SourceCT):
            container = self.sources_ct
        elif isinstance(item, model_items.SourceXray):
            container = self.sources_xray
        elif isinstance(item, model_items.SourceNM):
            container = self.sources_nm
        elif isinstance(item, model_items.Wall):
            container = self.walls
        elif isinstance(item, model_items.CriticalPoint):
            container = self.critical_points
        elif isinstance(item, model_items.Shielding):
            container = self.shieldings
        else:
            raise TypeError(type(item))
        return container
        
            
    def receive_selected_item(self, item, container=None):
        if self._selected_item is not item:
            self._selected_item = item
            self.emit(self.EVENT_SELECT_ITEM, self.selected_item)
            
        
    def select_item(self, item):
        if item == self._selected_item:
            return
        self._selected_item = item
        self.emit(self.EVENT_SELECT_ITEM, self.selected_item)
  
    def delete_item(self, item):
        container = self.container_for_item(item)

        index = container.index(item)

        
        if item is self.selected_item:
            if index > 0:
                self.selected_item = container[index-1]
            elif len(container) > 1:
                self.selected_item = container[1]
            else:
                self.selected_item = None
            
        self.container_for_item(item).remove(item)

    def add_item(self, item):
        container = self.container_for_item(item)
        if not isinstance(item, model_items.Wall):
            item = container.force_unique_name(item)
        container.append(item)

    def match_extent_to_floorplan(self):
        self.dosemap.extent = self.floorplan.extent
        
        
    def consistency_check(self):
        """Checks if relations between model items are consistent."""
        
        shielding_names = [x.name for x in self.shieldings]
        if len(shielding_names) != len(set(shielding_names)):
            raise ValueError("Shielding name not unique")
        
        for shielding in self.shieldings:
            for material, thickness in shielding.materials:
                try:
                    self.constants.get_material_by_name(material)
                except IndexError:
                    raise ValueError("Undefined material in shielding: "
                                     f"{shielding.name}: {material}")
                try:
                    float(thickness)
                except ValueError:
                    raise ValueError(f"Illegal value for material thickness "
                                     "in shielding: "
                                     f"{shielding.name}: {thickness}")
        
        for wall in self.walls:
            if wall.shielding not in shielding_names:
                raise ValueError("Undefined shielding name in wall: "
                                 f"{wall.shielding}")
        
        shielding_dict = self.shielding_dict
        materials_used = set(mat[0] for wall in self.walls 
                            for mat in shielding_dict[wall.shielding].materials)

        for source in self.sources_ct:
            params = [x for x in self.constants.ct if x.kvp == source.kvp]
            if not len(params):
                raise ValueError(f"CT kVp value not supported:\n{source}")
            for mat in materials_used:
                if mat not in params[0].archer:
                    #TODO @Marcel: even bedenken wat we gaan doen in dit soort 
                    #gevallen. Wel accepteren denk ik, maar conservatief de
                    # transmissie op 1 zetten met een warning erbij?
                    raise ValueError("No CT transmission parameters "
                                     f"available for {source.kvp}kV in {mat}")
                                        

        for source in self.sources_xray:
            params = [x for x in self.constants.xray if x.kvp == source.kvp]
            if not len(params):
                raise ValueError(f"Xray kVp value not supported: {source}")
            for mat in materials_used:
                if mat not in params[0].archer:
                    raise ValueError("No Xray transmission parameters "
                                     f"available for {source.kvp}kV in {mat}")
        
    @property
    def shielding_dict(self):
        return {s.name: s for s in self.shieldings}
        
    def get_shielding_by_name(self, shielding_name):
        if len(self.shieldings) == 0: return None
        if shielding_name is None: return None
        
        shielding = [shielding for shielding in self.shieldings\
                         if shielding.name == shielding_name]
            
        

        if len(shielding) > 1:
            msg = f'Multiple shieldings exists with name: {shielding_name}'
            raise KeyError(msg)
        elif len(shielding) == 0:
            msg = f'No shieldings exists with name: {shielding_name}'
            raise KeyError(msg)
        return shielding[0]
    

    @classmethod
    def from_dict(cls, dct): 
        floorplan = model_items.Floorplan.from_dict( dct[labels.FLOORPLAN])
        # HACK for compatibility for now fix later
        dosemap_dct = dct.get(labels.DOSEMAP, None)
        if dosemap_dct is None:
            dosemap = model_items.Dosemap(grid_matrix_size=100, engine=labels.RADTRACER)
        else:
            dosemap = model_items.Dosemap.from_dict(dosemap_dct)
        
    

        
        shieldings = [model_items.Shielding.from_dict(item)\
                      for item in dct[labels.SHIELDINGS]]
            
        shieldings = ShieldingItems(shieldings, item_class=model_items.Shielding)
            
        walls = [model_items.Wall.from_dict(item)\
                 for item in dct[labels.WALLS]]
            
        walls = ModelItems(walls, item_class=model_items.Wall)
            
        critical_points = [model_items.CriticalPoint.from_dict(item)\
                           for item in dct[labels.CRITICAL_POINTS]]
            
        critical_points = ModelItems(critical_points, 
                                     item_class=model_items.CriticalPoint)
            
        sources_ct = [model_items.SourceCT.from_dict(item)\
                      for item in dct[labels.SOURCES_CT]]
            
        sources_ct = ModelItems(sources_ct, item_class=model_items.SourceCT)
            
        sources_nm = [model_items.SourceNM.from_dict(item)\
                      for item in dct[labels.SOURCES_NM]]
            
        sources_nm = ModelItems(sources_nm, item_class=model_items.SourceNM)
            
        sources_xray = [model_items.SourceXray.from_dict(item)\
                        for item in dct[labels.SOURCES_XRAY]]
            
        sources_xray = ModelItems(sources_xray, item_class=model_items.SourceXray)
            
                
        return cls(floorplan, dosemap, shieldings, walls, critical_points, 
                   sources_ct, sources_nm, sources_xray)
    
    def save_to_project_file(self, file):
        dct = self.to_dict()
        
        dct[self._image_data] = self.floorplan.image
        
        with open(file, 'wb') as handle:
            pickle.dump(dct, handle, protocol=pickle.DEFAULT_PROTOCOL)
 
                
        
        self.filename = file
            
    @classmethod
    def load_from_project_file(cls, file):
        with open(file, 'rb') as handle:
             dct = pickle.load(handle)
             
        image = dct.pop(cls._image_data)
        
        model = cls.from_dict(dct)
        
        model.floorplan.image = image
        
        model.filename = file
        
        return model
        
    def to_dict(self):
        floorplan = self.floorplan.to_dict()
        dosemap = self.dosemap.to_dict()
        
        # first item of shielding is always empty shielding
        shieldings = [shielding.to_dict() for shielding in self.shieldings[1:]]
        walls = [wall.to_dict() for wall in self.walls]        
        critical_points = [critical_point.to_dict()\
                           for critical_point in self.critical_points]
                
        sources_ct      = [source.to_dict() for source in self.sources_ct]
        sources_nm      = [source.to_dict() for source in self.sources_nm]
        sources_xray    = [source.to_dict() for source in self.sources_xray]
            
        return {labels.FLOORPLAN:           floorplan,
                labels.DOSEMAP:             dosemap,
                labels.SHIELDINGS:          shieldings,
                labels.WALLS:               walls,
                labels.SOURCES_NM:          sources_nm,
                labels.SOURCES_XRAY:        sources_xray,
                labels.SOURCES_CT:          sources_ct,
                labels.CRITICAL_POINTS:     critical_points}


class Plotstyle:
    #TODO moet vanuit yaml of gui geinitialiseerd worden. In model_items zetten?
    ColorMapName = "jet"
    ColorMapMin = 0.001
    ColorMapMax = 10
    ColorMapAlpha = 0.5
    ColorMapAlphaGradient = True
    ColorMapAlphaLogScale = True
    ContourLines = [
        [0.1, "black", "dotted", 1.5],
        [0.3, "black", "dashed", 1.5],
        [1.0, "darkred", "solid", 1.5],
        [3.0, "black", "dashdot", 1.5],
    ]
    DisplayUnits = "mSv"
    ColorbarTicks = [0.01, 0.1, 0.2, 0.5, 1, 2, 10, 100]
    Legend = True


if __name__ == "__main__":
    # import yaml
    # with open('test_model_in.yml') as file:
    #     dct = yaml.safe_load(file)
    # model = Model.from_dict(dct)
    
    model = Model.load_from_project_file('/Users/marcel/git/pyrateshield/example_projects/SmallProject/project.psp')
    
