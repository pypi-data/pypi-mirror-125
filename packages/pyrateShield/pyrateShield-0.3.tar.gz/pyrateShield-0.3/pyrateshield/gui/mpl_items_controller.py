from pyrateshield.model_items import (MeasuredGeometry, Shielding, Wall, 
                                      CriticalPoint, SourceNM, SourceCT, 
                                      SourceXray, ModelItem)
from pyrateshield import labels
from pyrateshield.gui import styles
from pyrateshield import Logger

LOG_LEVEL = Logger.LEVEL_INFO


class MplItemsPlotter:
    _model = None
    
    def __init__(self, axes=None, model=None):
        self.plotted_model_items = []
        self.mpl_items = []
        
        self.axes = axes
        self.model = model
       
        
        self.refresh()
        
    @property
    def model_items(self):
        return [*self.model.sources_ct, 
                *self.model.sources_nm,
                *self.model.sources_xray, 
                *self.model.critical_points,
                *self.model.walls]
        
      
    def clear(self):
        # use copy because items will be removed during iteration
        for index, item in enumerate(self.plotted_model_items.copy()):
            self.remove_model_item((index, item))
        
    
    def remove_model_item(self, event_data):
        _, item = event_data
        index = self.plotted_model_items.index(item)

        try:
            # if axes already cleared this wil error
            self.mpl_items[index].remove()
        except:
            pass
        
        self.mpl_items.pop(index)
        
        self.plotted_model_items.remove(item)
        
        self._draw()
        
        
    def add_model_item(self, item):
        if item in self.plotted_model_items:
            raise ValueError()
        mpl_item = self._new_item(item)
        self.plotted_model_items += [item]
        self.mpl_items += [mpl_item]
        self.update_item(item, include_default=True)
        
    def get_mpl_item(self, item):
       
        if item in self.plotted_model_items:
            return self.mpl_items[self.plotted_model_items.index(item)]
        elif item in self.mpl_items or item is None:
            return item
        elif isinstance(item, ModelItem):
            self.add_model_item(item)
            return self.mpl_items[self.plotted_model_items.index(item)]    
        else:
            raise TypeError(f'{type(item)}')
        
    def get_model_item(self, item):
        if item in self.plotted_model_items or item is None:
            return item
        elif item in self.mpl_items:
            return self.plotted_model_items[self.mpl_items.index(item)]
        elif isinstance(item, ModelItem):
            return None
        else:
            return None # mpl item maybe already deleted
    
    def set_visible(self, visible):
        for mpl_item in self.mpl_items:
            mpl_item.set_visible(visible)
            mpl_item.set_picker(visible)
        
        for marker in self.line_markers:
            marker.set_visible(visible)
            marker.set_picker(visible)
            
    @property
    def model(self):
        return self._model
    
    @model.setter
    def model(self, model):
        if model is self.model:
            return
        if self._model is not None:
            self._disconnect_model()
            
        self._model = model
        self.refresh()
        self._connect_model()
        
        
    def refresh(self):
        self.clear()
        
        for item in self.model_items:
            self.add_model_item(item)

    
    def _disconnect_model(self):
        if self.model is None: return
        
        for obj in (self.model.sources_nm, self.model.sources_ct,
                    self.model.sources_xray, self.model.walls,
                    self.model.critical_points, self.model):
            obj.disconnect(self)
        

    def _connect_model(self):
        for obj in (self.model.sources_nm, self.model.sources_ct,
                    self.model.sources_xray, self.model.walls,
                    self.model.critical_points):
            
            obj.connect(self, obj.EVENT_ADD_ITEM,    self.add_model_item)
            obj.connect(self, obj.EVENT_REMOVE_ITEM, self.remove_model_item)
            obj.connect(self, obj.EVENT_UPDATE_ITEM, self.update_item)
            
        self.model.shieldings.connect(self, 
                                      self.model.shieldings.EVENT_UPDATE_ITEM,
                                      self.update_shielding)

    def _draw(self):
        self.axes.figure.canvas.draw_idle()
                
    def _new_item(self, model_item):    
        xlim, ylim = (self.axes.get_xlim(), self.axes.get_ylim())
        center = ((xlim[0] + xlim[1]) / 2, (ylim[0] + ylim[1]) /2)           
        return self.axes.plot(center, picker=True)[0]
    
    def get_formatting(self, item, include_default=False, state=None):
        model_item = self.get_model_item(item)
        item_styles = styles.STYLES[model_item.label]
        
        if isinstance(model_item, Wall):
            shielding = self.model.get_shielding_by_name(model_item.shielding)
            style = styles.STYLES[labels.WALLS][styles.DEFAULT].copy()
            style['color'] = shielding.color
            style['linewidth'] = shielding.linewidth
        else:
            if state is None:
                
                if model_item is self.model.selected_item and model_item.enabled:
                    state = styles.SELECTED
                elif model_item.enabled:
                    state = styles.NORMAL
                elif not model_item.enabled:
                    state = styles.DISABLED
            
            style = item_styles[state].copy()
            
                
        if include_default:
            style = {**item_styles[styles.DEFAULT], **style}
            
        return style

    def update_item(self, model_item, include_default=False):

        if isinstance(model_item, Wall):
            # color of shielding, linewidth, line style and position can change dynamically
            self._update_wall(model_item, include_default=include_default)
        elif isinstance(model_item, (SourceCT, SourceXray, SourceNM, CriticalPoint)):    
            self._update_point(model_item, include_default=include_default)
        elif isinstance(model_item, Shielding):
            self.update_shielding(model_item)
        else:
            raise TypeError(f'{type(model_item)}')
        self._draw()
        
    def update_shielding(self, shielding):
        for wall in self.model.walls:
            if wall.shielding == shielding.name:
                mpl_item = self.get_mpl_item(wall)
                mpl_item.set_color(shielding.color)
                mpl_item.set_linewidth(shielding.linewidth)

        self._draw()
        
    def _update_point(self, item, include_default=False):
        model_item = self.get_model_item(item)
        mpl_item = self.get_mpl_item(item)
        style = self.get_formatting(model_item, include_default=include_default)
        mpl_item.set_data(model_item.position)
        mpl_item.update(style)
        
    def _update_wall(self, model_item, include_default=False):
        mpl_item = self.get_mpl_item(model_item)
        
        fm = self.get_formatting(model_item, include_default=include_default)
    
        fm['xdata'] = (model_item.vertices[0][0], model_item.vertices[1][0])
        fm['ydata'] = (model_item.vertices[0][1], model_item.vertices[1][1])        
        mpl_item.update(fm)
                   
        self._draw()
        

class MplItemsSelector(Logger):
    _selected_item = None
    _items = None
    ITEM_LABELS = [*labels.SOURCES, labels.WALLS, labels.CRITICAL_POINTS]
    def __init__(self, items=None, mouse=None):
        super().__init__(log_level=LOG_LEVEL)
        self.mouse = mouse
        self.items = items
        self.line_markers = []
        
        self.items.model.walls.connect(self,
                                       self.items.model.walls.EVENT_UPDATE_ITEM,
                                       self.update_shielding)
        
        self.items.model.shieldings.connect(self,
                                            self.items.model.shieldings.EVENT_UPDATE_ITEM,
                                            self.update_shielding)
        
    def update_shielding(self, item):
        # callback when shielding change, possibly need update of color or
        # linewidth
        if self.selected_item is None: return
        
        if isinstance(self.items.model.selected_item, Wall):
            if item is self.items.model.selected_item:
                self._select_line_item(self.selected_item)
            elif isinstance(item, Shielding)\
                and item.name == self.items.model.selected_item.shielding:
                    self._select_line_item(self.selected_item)
                    
        
       
           
    
        
    def _draw(self):
        self.items._draw()
        
    def clear(self):
        self.line_markers = []
        self.selected_item = None
        
    def refresh(self):
        self.set_selected_item(self.items.model.selected_item)

        
    @property
    def selected_model_item(self):
        return self.items.get_model_item(self.selected_item)
    
    @property
    def selected_item(self):
        return self._selected_item
    
    @selected_item.setter
    def selected_item(self, item):
        self.set_selected_item(item)
        
    
    
    def set_selected_item(self, item):
        model_item = self.items.get_model_item(item)
        if model_item is not None and model_item.label in self.ITEM_LABELS:
            item = self.items.get_mpl_item(item)
            if item is self.selected_item:
                return
            if self.selected_item is not None:
                self._deselect_item(self.selected_item)
            
            self._select_item(item)
            
            self._selected_item = item
        
            if isinstance(model_item, Wall):
                model_item.connect(self, model_item.EVENT_UPDATE, 
                                   self.move_line_markers)
        else:
            self._deselect_item(self.selected_item)
            self._selected_item = None
  
        
        self._draw()
    
    def wall_deleted(self, event_data):
        index, wall = event_data
        if self.selected_model_item is None\
            or self.items.get_model_item(wall) is self.selected_model_item:
            self._deselect_line_item()
        
    def move_line_markers(self, model_item):
        mpl_item = self.items.get_mpl_item(model_item)
        if mpl_item is self.selected_item:
            for index, marker in enumerate(self.line_markers):
                marker.set_data(*model_item.vertices[index])
            self.items._draw() 
            
    def _select_point_item(self, mpl_item):
        model_item = self.items.get_model_item(mpl_item)
        style = self.items.get_formatting(model_item)
        mpl_item.update(style)

    def _deselect_item(self, mpl_item):
        
        if mpl_item not in self.items.mpl_items:
            self._selected_item = None
            return
        
        if mpl_item is None: return

        model_item = self.items.get_model_item(mpl_item)
        
        if isinstance(model_item, Wall):
            self._deselect_line_item(mpl_item)
            model_item.disconnect(self)
         
        if mpl_item is self.selected_item:
            self._selected_item = None
        
        if model_item.enabled:
            style = self.items.get_formatting(model_item, state=styles.NORMAL)
        else:
            style = self.items.get_formatting(model_item, state=styles.DISABLED)

        mpl_item.update(style)
        
        self._draw()

    def _select_item(self, mpl_item):
        model_item = self.items.get_model_item(mpl_item)
    
        if isinstance(model_item, Wall):
            self._select_line_item(mpl_item)
        else:
            if model_item.enabled:
                self._select_point_item(mpl_item)
        
        self._draw()
            
    def _deselect_line_item(self, mpl_item=None):
        if len(self.line_markers) == 0:
            return        
        else:
            for marker in self.line_markers:
                marker.set_visible(False)
                marker.set_picker(False)
                
        if mpl_item is not None:
            mpl_item.set_picker(True)
        
    def _select_line_item(self, mpl_item):
        model_item = self.items.get_model_item(mpl_item)    
        if model_item is None:
            return
        
        if len(self.line_markers) == 0:
            self.logger.debug('Drawing new wall markers!')
            self.line_markers = [self.items.axes.plot((0, 0), picker=True)[0], 
                                 self.items.axes.plot((0, 0), picker=True)[0]]
        
        wall_style = self.items.get_formatting(model_item)        
        style = styles.STYLES[labels.WALLS][styles.SELECTED]
        style['color'] = wall_style['color']
    
        mpl_item.set_picker(False)
        
        for index, marker in enumerate(self.line_markers):
            marker.set_visible(True)
            marker.set_picker(True)
            marker.update(style)
            marker.set_data(*model_item.vertices[index])
            
            
            
    def select_line_marker(self, marker):
        self.logger.debug('Select wall marker')
        index = self.line_markers.index(marker)
        model_item = self.selected_model_item
        callback = lambda event: self.move_wall(model_item, index, event)
        self.mouse.connect(self, self.mouse.MOVE_EVENT, callback)
        self.mouse.connect(self, self.mouse.RELEASE_EVENT, self.mouse_release)
        
    def move_wall(self, model_item, index, position):
        self.logger.debug(f'Moving wall {index}, {position}')
        self.line_markers[index].set_xdata(position[0])
        self.line_markers[index].set_ydata(position[1])
        model_item.set_vertex(index, position)
        
    def mouse_release(self, event_data=None):
        self.logger.debug('Mouse Release')
        self.mouse.disconnect(self)
       
    def start_move_item(self, model_item):
        callback = lambda event: self.move_item(model_item, event)
        self.mouse.connect(self, self.mouse.MOVE_EVENT, callback)
        self.mouse.connect(self, self.mouse.RELEASE_EVENT, self.mouse_release)        
            
    def move_item(self, model_item, position):
        model_item.position = position
        

            

           
           
           
class MplOriginController():
    _mpl_item = None
    def __init__(self, model=None, axes=None):
        self.model = model
        self.axes = axes
       
        self.model.connect(self, 
                           self.model.EVENT_UPDATE_GEOMETRY,
                           self.update)
        
    @property
    def mpl_item(self):
        if self._mpl_item is None:
            self._mpl_item = self._get_mpl_item()
        return self._mpl_item
    
    def _get_mpl_item(self):
        fm = styles.STYLES[labels.ORIGIN_CM][styles.DEFAULT]
        mpl_item  = self.axes.plot(0, 0, **fm)[0]
        return mpl_item
    
    def update(self, event_data=None, mpl_item=None):
        if mpl_item is None:
            mpl_item = self.mpl_item
        mpl_item.set_data((0, 0))
        
    def clear(self):
        self._mpl_item = None
        
    def get_visible(self):
        return self.mpl_item.get_visible()
        
    def _draw(self):
        self.axes.figure.canvas.draw_idle()
    
        
    def set_visible(self, visible=True):
        # origin always at 0, 0
        if visible != self.get_visible(): 
            self.mpl_item.set_visible(visible)
            self._draw()
            
  
class MplPixelSizeController(MplOriginController):
    def __init__(self, model=None, axes=None):
        super().__init__(model=model, axes=axes)
        self.update()
        
    def _get_mpl_item(self):
        fm = styles.STYLES[labels.PIXEL_SIZE_CM][styles.DEFAULT]
 
        mpl_item = self.axes.plot((0, 0), (0, 0), **fm)[0]
        self.update(mpl_item=mpl_item)
        return mpl_item
    
    def update(self, event_data=None, mpl_item=None):
        if mpl_item is None:
            mpl_item = self.mpl_item
        if isinstance(self.model.geometry, MeasuredGeometry):
            vv = self.model.geometry.vertices_cm

            mpl_item.set_xdata([vv[0][0], vv[1][0]])
            mpl_item.set_ydata([vv[0][1], vv[1][1]])
            self._draw()
        else:
            mpl_item.set_visible(False)
    



    
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from pyrateshield.model import Model
    axes = plt.axes()
    project = '/Users/marcel/git/pyrateshield/example_projects/SmallProject/project.psp'
    model = Model.load_from_project_file(project)
    
    items = MplItemsPlotter(model=model, axes=axes)
    
    
       
                
   
                       
   
            
            
   

    
    
    
       
            
    
    
            
        
        

        

