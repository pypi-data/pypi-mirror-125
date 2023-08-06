import time
import numpy as np
import copy
from matplotlib.cm import get_cmap
from matplotlib.colors import LogNorm
from pyrateshield.model import Plotstyle
from pyrateshield.model_items import Wall, Shielding
from pyrateshield.gui.mpl_view import PointClicker, LineDrawer
from pyrateshield.gui.mpl_items_controller import MplItemsPlotter, MplItemsSelector, MplOriginController, MplPixelSizeController
from matplotlib.backend_bases import MouseButton
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
from pyrateshield import labels
DOSEMAP_STYLE = Plotstyle()


from pyrateshield.gui.mpl_view import Mouse

from pyrateshield import Logger, Observable


LOG_LEVEL = Logger.LEVEL_INFO

            
class MplController(Observable):
    # previewLine = None;
    # coordinate = QtCore.pyqtSignal(list)
    # picker = QtCore.pyqtSignal(list)

    _dosemap_image = None
    _contour_lines = None
    _floorplan_image = None
    
    _scale_line = None
    _origin_point = None

    _model = None
    lock_mouse = False
    
    _point_clicker = None
    
    EVENT_PICK_LEFT_CLICK = 'event_pick_left_click'
    EVENT_PICK_RIGHT_CLICK = 'event_pick_right_click'

    def __init__(self, dosemapper=None, view=None, model=None):
        Logger.__init__(self, log_level=LOG_LEVEL)
        Observable.__init__(self)
        self.dosemapper = dosemapper
        self.view = view

        self.mouse = Mouse(self.view.canvas)
        
        
        self.origin = MplOriginController(model=model.floorplan,
                                          axes=self.axes)
        
        self.pixel_size = MplPixelSizeController(model=model.floorplan,
                                                 axes=self.axes)
        
        self.mpl_items = MplItemsPlotter(model=model, axes=self.axes)
        
        
        self.mpl_items_selector = MplItemsSelector(items=self.mpl_items,
                                                   mouse=self.mouse)
        
        self._model = model
    
        self.pick = True
        
        self.set_callbacks()   

        self.connect_model()
        
        self.refresh()
        
        
    def draw(self):        
        self.axes.figure.canvas.draw_idle()
        
    def pick_event(self, event):
        self.lock_mouse = True
        self.logger.debug('Initiate picking!')
        if self.pick is False:
            self.logger.debug('Picking disabled!')
            return
        if self.view.toolbar.zoom_pan_selected:
            self.logger.debug('Zooming/Panning, no picking!')
            return
            
        
        # disable picking while running code. Picking is enabled when mouse
        # button is released. Prevent multiple pick events on overlapping
        # objects at the same time
        
        self._pick = self.pick # store
        self.pick = False # disable picking while running code below
        
    
        self._pick_data = event # debug purpuses
        
        mpl_item = event.artist
        
        if mpl_item not in self.mpl_items_selector.line_markers:
            mouse_position = [event.mouseevent.x, event.mouseevent.y]
            mpl_item = self.override_pick(mpl_item, mouse_position)
    
        if mpl_item in self.mpl_items_selector.line_markers:
            marker = mpl_item
            model_item = self.mpl_items_selector.selected_model_item
        else:
            marker = None
            model_item = self.mpl_items.get_model_item(mpl_item)
            
        if event.mouseevent.button is MouseButton.LEFT:

            if mpl_item in self.mpl_items_selector.line_markers:
               
                self.mpl_items_selector.select_line_marker(mpl_item)
                
            elif mpl_item is self.mpl_items_selector.selected_item:
        
                self.mpl_items_selector.start_move_item(model_item)
     
            else:
               
                self.model.selected_item = model_item
            
           
            self.emit(self.EVENT_PICK_LEFT_CLICK, model_item)
            
        elif event.mouseevent.button is MouseButton.RIGHT:
            if marker is not None:
                position = marker.get_data()
            else:
                position = (event.mouseevent.xdata, event.mouseevent.ydata)
            
            self.emit(self.EVENT_PICK_RIGHT_CLICK, (model_item, position))
        
        self.mouse.connect(self, self.mouse.RELEASE_EVENT, self.mouse_release)
        
                
                
    def override_pick(self, mpl_item, mouse_position):
        self.logger.debug('Start Hack!')
        # HACK INTO the picker system here
        # If a wall already selected and mouse positions smaller than
        # pick radius away from the wall vertices then override the 
        # selected item to the wall marker
        
        if len(self.mpl_items_selector.line_markers) == 0:
            # no markers yet
            return mpl_item
        
        pickradius = self.mpl_items_selector.line_markers[0].get_pickradius()
        
        self.logger.debug('Pickradius: %s', str(pickradius))
        
        # note x, y and pickradius are in points
        x , y = mouse_position
        
        self.logger.debug('Mouse pos: %s', str([x, y]))
        
        distance = []
        for marker in self.mpl_items_selector.line_markers:
            # transform marker position to position in points
            mx, my = self.axes.transData.transform(marker.get_data())
           
            # calculate distance
            d = np.sqrt((x- mx)**2 + (y - my)**2)
    
            if d <= pickradius:
                distance += [d]
            else:
                distance += [float('Inf')]
        
        if min(distance) < pickradius:
            self.logger.debug('Override MPL picked object!')
            index = distance.index(min(distance))
            mpl_item = self.mpl_items_selector.line_markers[index]
            
        return mpl_item
                    
    def mouse_release(self, event_data=None):
        self.lock_mouse = False
        self.pick = self._pick
        
        
    def set_callbacks(self):
        # button callbacks
        button = self.view.buttons[self.view.dosemap_button_pyshield_label]
        button.clicked.connect(self.show_dosemap_pyshield)
        
        button = self.view.buttons[self.view.dosemap_button_radtracer_label]
        button.clicked.connect(self.show_dosemap_radtracer)
        
        button = self.view.buttons[self.view.refresh_button_label]
        button.clicked.connect(self.refresh)
        
        self.axes.figure.canvas.mpl_connect('pick_event', self.pick_event)
        
        event = self.view.toolbar.EVENT_TOOLBUTTON_CLICK
        self.view.toolbar.connect(self, event, self.toolbar_callback)
        


        
    @property
    def dosemap_image(self):
        if self._dosemap_image is None:
            self._dosemap_image = self.axes.imshow(((0,0), (0,0)), interpolation="bilinear")
        return self._dosemap_image
    
    @property
    def floorplan_image(self):
        if self._floorplan_image is None:
            self._floorplan_image = self.axes.imshow(((0,0), (0,0)))
        return self._floorplan_image
        
    @property
    def model(self):
        return self._model
    
    @model.setter
    def model(self, model):
        if self.model is model:
            return
        self.disconnect_model()
        self._model = model
        self.connect_model()
        self.refresh()
        
    def connect_model(self):
        callback = self.select_item_callback
        self.model.connect(self, self.model.EVENT_SELECT_ITEM, callback)
        self.mpl_items.model = self.model
        
        callback = self.mpl_items_selector.update_shielding
        event = self.model.shieldings.EVENT_UPDATE_ITEM
        self.model.shieldings.connect(self, event, callback)
        
        callback = self.mpl_items_selector.wall_deleted
        event = self.model.walls.EVENT_REMOVE_ITEM
        self.model.walls.connect(self, event, callback)
        
    def select_item_callback(self, item):
        self.mpl_items_selector.set_selected_item(item)
        self.toggle_delete()
        
    def toggle_delete(self):
        if self.model.selected_item is not None:
            self.view.toolbar.button_enabled('delete', True)
        else:
            self.view.toolbar.button_enabled('delete', False)
        
            
    def disconnect_model(self):
        if self.model is None: return
        self.model.disconnect(self)
        self.model.shieldings.disconnect(self)
        
    def clear(self):
        self.axes.cla()
        self.toggle_grid(None)

        self._dosemap_image = None
        self._floorplan_image = None
        self.pixel_size.clear()
        self.origin.clear() 
        self.mpl_items_selector.clear()
        self.mpl_items.clear()
        
        
    def toggle_grid(self, major_interval):
        self.axes.xaxis.set_ticks_position('none')
        self.axes.yaxis.set_ticks_position('none')
        self.axes.xaxis.set_ticklabels([])
        self.axes.yaxis.set_ticklabels([])
        
        if not major_interval:
            self.axes.grid(False)
        else:
            self.axes.xaxis.set_major_locator(MultipleLocator(major_interval))
            self.axes.yaxis.set_major_locator(MultipleLocator(major_interval))
            
            self.axes.xaxis.set_minor_locator(AutoMinorLocator(5))
            self.axes.yaxis.set_minor_locator(AutoMinorLocator(5))

            self.axes.grid(which='major', linestyle=":", color="gray", alpha=0.3)
            self.axes.grid(which='minor', linestyle=":", color="gray", alpha=0.1)
    
    @property
    def axes(self):
        return self.view.canvas.ax
        
        
    def refresh(self, _=None):
        self.clear()
        self.plot_floorplan()
        self.mpl_items.refresh()
        self.mpl_items_selector.refresh()
        self.toggle_delete()
        self.draw()

        
    def plot_floorplan(self):
        self.floorplan_image.set_data(self.model.floorplan.image)
        self.floorplan_image.set_extent(self.model.floorplan.extent)
        self.draw()
        
    
    def plot_dosemap(self, dosemap):        
        if self._contour_lines is not None:
            for cline in self._contour_lines.collections:
                try:
                    cline.remove()
                except:
                    pass
                
        extent = self.model.dosemap.extent
        self.dosemap_image.set_data(dosemap)
        self.dosemap_image.set_extent(extent)
        
        clines = list(map(list, zip(*DOSEMAP_STYLE.ContourLines)))
        
        levels, colors, linestyles, linewidths = clines
        CS = self.axes.contour(dosemap, extent=extent, levels=levels, 
                                    colors=colors, linestyles=linestyles,
                                    linewidths=linewidths, origin="upper")
        
        h,_ = CS.legend_elements()
        
        leg = self.axes.legend(h, levels, handlelength=3, 
                                          title="Contours [mSv]", 
                                          framealpha=0.5)
        
        self.axes.add_artist(leg)
        self._contour_lines = CS
        self.draw()
       
        
        
    def style_dosemap(self):
        mpl_im = self.dosemap_image
        
        cmap = copy.copy(get_cmap(DOSEMAP_STYLE.ColorMapName))
        if DOSEMAP_STYLE.ColorMapAlphaGradient:
            alphas = np.linspace(0, 1, cmap.N)
            cmap._init()
            cmap._lut[:len(alphas), -1] = alphas
            
        cmap.set_under(alpha=0)
        
        mpl_im.set_cmap(cmap)
        mpl_im.set_alpha(DOSEMAP_STYLE.ColorMapAlpha)
        mpl_im.set_clim([DOSEMAP_STYLE.ColorMapMin, DOSEMAP_STYLE.ColorMapMax])
        mpl_im.set_norm(LogNorm(vmin=DOSEMAP_STYLE.ColorMapMin, 
                                vmax=DOSEMAP_STYLE.ColorMapMax))
        
        self.draw()
   
    def get_dosemap(self):        
        start = time.time()
        self.model.dosemap.extent = self.axes.get_xlim() + self.axes.get_ylim()
        dosemap = self.dosemapper.get_dosemap(self.model)   
        end = time.time()
        
        exec_time = round(end-start, 2)
        self.logger.info(f'Dosemap calculated in {exec_time}s')
        return dosemap
    
    def show_dosemap_pyshield(self):
        engine = self.model.dosemap.engine
        self.model.dosemap.engine = labels.PYSHIELD
        self.show_dosemap()
        self.model.dosemap.engine = engine
        
    def show_dosemap_radtracer(self):
        engine = self.model.dosemap.engine
        self.model.dosemap.engine = labels.RADTRACER
        self.show_dosemap()
        self.model.dosemap.engine = engine
        
    def show_dosemap(self):
        dosemap = self.get_dosemap()
        if dosemap is not None:
            self.plot_dosemap(dosemap)
            self.style_dosemap()
        else:
            self.refresh()
    
    @property
    def point_clicker(self):
        self.disable_point_clicker()
        self._point_clicker = PointClicker(self)
        return self._point_clicker
        
    def disable_point_clicker(self):
        if self._point_clicker is not None:
            self._point_clicker.disconnect(self)
        
    def add_model_item_by_mouse(self, label, multiple=False, 
                                position=None):
        
        
        if position is None:
            point_clicker = PointClicker(self)
        else:
            point_clicker = None
            
        def click(position):
            #check if right tool is still selected
            if self.view.toolbar.selected_tool == label:
                model_items = self.model.get_model_items_by_label(label)
                new_item = model_items.add_new_item(position=position)
                self.model.selected_item = new_item
                if multiple:
                    self.add_model_item_by_mouse(label, multiple=multiple)
                else:
                    # deselect tool
                    self.view.toolbar.select_checkable_tool(toolname=None)
            else:
                if point_clicker is not None:
                    point_clicker.disconnect(self)
                
            
        if point_clicker is not None:
            
            point_clicker.connect(self, 
                                  self.point_clicker.EVENT_POINT_CLICKED, 
                                  click)     
        else:
            click(position)
                
    def add_wall_by_mouse(self, multiple=False, position=None, hold_button=False):
        
        if position is None:
            point_clicker = PointClicker(self)
        else:
            point_clicker = None
            
        def click(position):
            #check if right tool is still selected
            if self.view.toolbar.selected_tool == labels.WALLS:
                vertices = (position, position)
                if isinstance(self.model.selected_item, Wall):
                    shielding = self.model.selected_item.shielding
                elif isinstance(self.model.selected_item, Shielding):
                    shielding = self.model.selected_item.name
                else:
                    shielding = labels.EMPTY_SHIELDING
                new_item = self.model.walls.add_new_item(vertices=vertices,
                                                         shielding=shielding)
                
                #new_item.disable_connection()
                mpl_item = self.mpl_items.get_mpl_item(new_item)
                
                line_drawer = LineDrawer(self, mpl_item, wait_for_click=False,
                                         hold_button=hold_button)
                
                
                def draw_finished(event_data):
                    vertices, dblclick = event_data
                    new_item.vertices = vertices
                    #new_item.enable_connection()
                    #new_item.emit(new_item.EVENT_UPDATE)
                    self.model.selected_item = new_item
                    self.draw()
                    # continue drawing as long as tool is selected
                    
                    if multiple and not dblclick:
                        self.add_wall_by_mouse(multiple=multiple,
                                               position=vertices[1])
                                               
                    else:
                        # deselect tool
                        self.view.toolbar.select_checkable_tool(toolname=None)

                line_drawer.connect(self, line_drawer.EVENT_DRAW_FINISHED,
                                    draw_finished)
                
                def terminate_draw(key):
                    if key in (' ', 'enter', 'escape'):
                        line_drawer.finished_draw_dblclick()

                        
                
                if multiple:
                    self.mouse.disconnect(self, self.mouse.KEY_PRESS_EVENT)
                    self.mouse.connect(self, self.mouse.KEY_PRESS_EVENT,
                                       terminate_draw)
                    
                    
                
                
            else:
                if point_clicker is not None:
                    
                    point_clicker.disconnect(self)
        
        if position is None:
            point_clicker.connect(self, 
                                  self.point_clicker.EVENT_POINT_CLICKED, 
                                  click)     
            
        else:
            click(position)
        
        
        

    def toolbar_callback(self, event_data):
        toolname, checked = event_data
        
        if toolname == labels.PYSHIELD:
            self.show_dosemap_pyshield()
        elif toolname == labels.RADTRACER:
            self.show_dosemap_radtracer()
        
        elif toolname in (labels.SOURCES_CT, labels.SOURCES_NM, 
                          labels.SOURCES_XRAY, labels.CRITICAL_POINTS):
            
            self.add_model_item_by_mouse(toolname)
            
        elif toolname == labels.WALLS:
            self.add_wall_by_mouse(hold_button=True)
        elif toolname == 'refresh':
            self.refresh()
        elif toolname == 'delete':
            if self.model.selected_item is not None:
                self.model.delete_item(self.model.selected_item)
