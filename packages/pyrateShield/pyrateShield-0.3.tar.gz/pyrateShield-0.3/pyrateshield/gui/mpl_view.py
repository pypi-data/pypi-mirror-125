import os
import math
from pyrateshield import Observable
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg \
    import FigureCanvasQTAgg, NavigationToolbar2QT

from matplotlib.figure import Figure
from matplotlib.backend_bases import MouseButton


from matplotlib.backend_bases import  _Mode
import qtawesome
from pyrateshield import labels



class PointClicker(Observable):
    EVENT_POINT_CLICKED = 'event_point_clicked'

    def __init__(self, mpl_controller=None):
        super().__init__()
        self.mpl_controller = mpl_controller
        mouse = self.mpl_controller.mouse
        mouse.connect(self, mouse.LEFT_CLICK_EVENT, self.get_position)
        self.mpl_controller.pick = False

    def get_position(self, position):
        self.mpl_controller.pick = True
        self.emit(self.EVENT_POINT_CLICKED, position)
        self.mpl_controller.mouse.disconnect(self)

class LineDrawer(Observable):
    EVENT_DRAW_FINISHED = 'event_draw_finisched' 
    line_format = {'color': 'black', 'linewidth': 2, 'linestyle': '--'}
    
    def __init__(self, mpl_controller=None, line=None, wait_for_click=True,
                 hold_button=False):
        super().__init__()
        self.mpl_controller = mpl_controller
        
        self.mouse = self.mpl_controller.mouse
        if wait_for_click:
            self.mouse.connect(self, self.mouse.LEFT_CLICK_EVENT, self.start_draw)
        else:
            self.mouse.connect(self, self.mouse.MOVE_EVENT, self.draw)
            if hold_button:
                self.mouse.connect(self, self.mouse.RELEASE_EVENT, self.finished_draw)
            else:
                self.mouse.connect(self, self.mouse.LEFT_CLICK_EVENT, self.finished_draw)
                self.mouse.connect(self, self.mouse.LEFT_DBLCLICK_EVENT, self.finished_draw_dblclick)
        
       
        
        self._line = line
        self.line.set_visible(True)
        self.mpl_controller.pick = False
        

    @property
    def line(self):
        if self._line is None:
            fm = self.line_format
            self._line = self.mpl_controller.view.canvas.ax.plot(0, 0, **fm)[0]
                                                             
        return self._line
    
    def start_draw(self, position):
        
        newx = [position[0]]*2
        newy = [position[1]]*2
        self.line.set_xdata(newx)
        self.line.set_ydata(newy)
        self.line.set_visible(True)
        self.mpl_controller.draw()
            
        self.mouse.connect(self, self.mouse.MOVE_EVENT, self.draw)
        self.mouse.connect(self, self.mouse.RELEASE_EVENT, self.finished_draw)
        
        
    def draw(self, position):
        newx = [self.line.get_xdata()[0], position[0]]
        
        newy = [self.line.get_ydata()[0], position[1]]
        
        self.vertices = [[newx[0], newy[0]], [newx[1], newy[1]]]
                      
        self.line.set_xdata(newx)
        self.line.set_ydata(newy)
        
        self.mpl_controller.draw()
    
    
    def _finish_draw(self, event_data=None):
        self.mouse.disconnect(self)
        
        newx = self.line.get_xdata()
        newy = self.line.get_ydata()
        
        vertices = [[newx[0], newy[0]], [newx[1], newy[1]]]
        self.mpl_controller.pick = True
        return vertices
    
    def finished_draw_dblclick(self, _=None):
        vertices = self._finish_draw()
        self.emit(self.EVENT_DRAW_FINISHED, (vertices, True))
        
    def finished_draw(self, _=None):
        vertices = self._finish_draw()
        self.emit(self.EVENT_DRAW_FINISHED, (vertices, False))





class Mouse(Observable):
    LEFT_CLICK_EVENT = 'left_click_event'
    RIGHT_CLICK_EVENT = 'right_click_event'
    LEFT_DBLCLICK_EVENT = 'left_dblclick_event'
    KEY_PRESS_EVENT = 'key_press_event'
    
    
    MOVE_EVENT = 'move_event'
    RELEASE_EVENT = 'release_event'
    _last_x = None
    _last_y = None
    
    delta = 10
   
    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas
        
        self.canvas.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.canvas.setFocus()

        #self.toolbar = toolbar
        self.inaxes = False
        self.infigure = False
        self.canvas.mpl_connect('button_press_event', self.mouse_click)
        self.canvas.mpl_connect('button_release_event', self.mouse_release)
        self.canvas.mpl_connect('motion_notify_event', self.mouse_move)
        self.canvas.mpl_connect('axes_enter_event', self.enter_axes)
        self.canvas.mpl_connect('axes_leave_event', self.leave_axes)
        self.canvas.mpl_connect('figure_enter_event', self.enter_figure)
        self.canvas.mpl_connect('figure_leave_event', self.leave_figure)
        self.canvas.mpl_connect('key_press_event', self.keypress)
        self.canvas.mpl_connect('key_release_event', self.keyrelease)
        
        self.shift_pressed = False
    
        
    def keypress(self, event):
        if event.key in ('shift',):
            self.shift_pressed = True
        self.emit(self.KEY_PRESS_EVENT, event.key)
        
    def keyrelease(self, event):
        if event.key in ('shift',):
            self.shift_pressed = False
        
        
    def enter_figure(self, event_data=None):
        self.infigure = True
        
    def leave_figure(self, event_data=None):
        self.infigure = False
        self.inaxes = False
        
    def enter_axes(self, event_data=None):
        self.inaxes = True
        self.infigure = True
        
    def leave_axes(self, event_data=None):
        self.inaxes = False
    
    def mouse_click(self, event):
        # if self.toolbar.mode in ('pan/zoom', 'zoom rect'):
        #     return
        
        if not event.inaxes: return
        x = event.xdata
        y = event.ydata

        self.click_position = (x, y)
        
        if event.button is MouseButton.LEFT:
            if event.dblclick:
                self.emit(self.LEFT_DBLCLICK_EVENT, [x, y])
            else:
                self.emit(self.LEFT_CLICK_EVENT, [x, y])
        if event.button is MouseButton.RIGHT:
            self.emit(self.RIGHT_CLICK_EVENT, [x, y])
            
    def mouse_move(self, event):
        if not event.inaxes: return
        
        x = event.xdata
        y = event.ydata
        
        
        if self.shift_pressed:
            if abs(y-self.click_position[1]) > abs(x-self.click_position[0]):
                x = self.click_position[0]
            else:
                y = self.click_position[1]
        
        
        if self._last_x is not None and self._last_y is not None:
            dx = (x - self._last_x)
            dy = (y - self._last_y)
            
            if math.sqrt(dx**2 + dy**2) < self.delta:
                return
            
        
                
            
        self._last_x = x
        self._lasy_y = y
        
        self.emit(self.MOVE_EVENT, [x, y])

    def mouse_release(self, event):
        x = event.xdata
        y = event.ydata
        self.emit(self.MOVE_EVENT, [x, y])
        self.emit(self.RELEASE_EVENT)
        self._last_x = None
        self._last_y = None
        
class NavigationToolbar(NavigationToolbar2QT, Observable):
    
    # only display the buttons we need
    EVENT_TOOLBUTTON_CLICK = 'event_toolbutton_click'
    
    
    pyrateshield_dict = {'source_nm': labels.SOURCES_NM,
                         'source_ct': labels.SOURCES_CT,
                         'source_xray': labels.SOURCES_XRAY,
                         'critical_point': labels.CRITICAL_POINTS,
                         'wall': labels.WALLS}
    
    toolitems = (
        
        #('Back', 'Back to previous view', 'back', 'back'), 
        #('Forward', 'Forward to next view', 'forward', 'forward'), 
        #(None, None, None, None), 
        (labels.PYSHIELD, 'Pyshield dosemap', 'icon', 'pyshield'),
        (labels.RADTRACER, 'Radtracer dosemap', 'icon', 'radtracer'),
        
        ('Floorplan', 'Show floorplan whithout dosemap', 'mdi.floor-plan', 'refresh'),
        (None, None, None, None), 
        ('Reset', 'Reset zoom/pan', 'mdi.arrow-expand', 'home'), 
        ('Pan', 'Left button pans, Right button zooms\nx/y fixes axis, CTRL fixes aspect', 'mdi.arrow-all', 'pan'), 
        ('Zoom', 'Zoom to rectangle\nx/y fixes axis, CTRL fixes aspect', 'mdi.magnify-scan', 'zoom'), 
        #(None, None, None, None), 
        #('Subplots', 'Configure subplots', 'subplots', 'configure_subplots'), 
        #(None, None, None, None), 
        
        
        (None, None, None, None), 
        ('Source NM', 'Add NM source by mouse click', 'mdi.radioactive', 'source_nm'),
        ('Source CT', 'Add CT source by mouse click', 'mdi.radiology-box-outline', 'source_ct'),
        ('Source Xray', 'Add Xray source by mouse click', 'mdi.radiology-box-outline', 'source_xray'),
        ('Wall', 'Draw new wall with mouse', 'mdi.wall', 'wall'),
        ('Critical Point', 'Add critical point by mouse click', 'mdi.map-marker-alert-outline', 'critical_point'),
        
        
        ('Delete', 'Delete selected item', 'mdi.trash-can-outline', 'delete'),
        (None, None, None, None), 
        
        #('Side Panel', 'Show/hide side panel', 'mdi.file-document-outline', 'side_panel'),
        
        
        (None, None, None, None), 
        
        ('Snapshot', 'Save current view as image', 'mdi.camera-outline', 'save_figure'),
        ('Load', 'Load project from disk', 'mdi.folder-open-outline', 'load_project'),
        ('Save', 'Save project', 'mdi.content-save-outline', 'save_project'),
        ('Save As', 'Save project as ...', 'mdi.content-save-edit-outline', 'save_project_as')
       
    )
    
    def __init__(self, *args, mpl_controller=None, **kwargs):
        NavigationToolbar2QT.__init__(self, *args, coordinates=False, **kwargs)
        Observable.__init__(self)
        self.setStyleSheet("border-bottom: 0px; border-top: 0px;")
        
        self.mpl_controller = mpl_controller
        
        
        for name, action in self._actions.items():
            widget = self.widgetForAction(action)
            
            if name in ('source_nm', 'source_ct', 'source_xray',
                        'critical_point', 'wall', 'zoom', 'pan', 'side_panel'):
           
                action.setCheckable(True)
                if name == 'side_panel':
                    action.setChecked(True)
                if name == 'save_project':
                    action.setEnabled(False)
                
                style = 'QToolButton:checked { background-color: darkgray }'
            else:
                style = 'QToolButton:pressed { background-color: darkgray }'
            widget.setStyleSheet(style)
            
            #if name in ('pyshield', 'radtracer', 'source_nm', 'source_ct', 'source_xray'):
            
            widget.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon);
            
        
    def _icon(self, name):
        if name == 'icon.png':
            folder = os.path.split(__file__)[0]
            icon = QIcon(os.path.join(folder, 'icon.png'))
        else:
            try:
                # .png is added remove last 4 characters
                icon = qtawesome.icon(name[:-4])
            except:
                icon = NavigationToolbar2QT._icon(self, name)
        return icon
    
    def button_enabled(self, label, enabled):
        if label in self.pyrateshield_dict.values():
            label = dict([(value, key)\
                          for key, value in self.pyrateshield_dict.items()])[label]
        
        self._actions[label].setEnabled(enabled)
    
    
    def button_checked(self, label, enabled):
        if label in self.pyrateshield_dict.values():
            label = dict([(value, key)\
                          for key, value in self.pyrateshield_dict.items()])[label]
        
        self._actions[label].setChecked(enabled)
    
        
    
    def delete(self):
        self.emit(self.EVENT_TOOLBUTTON_CLICK, ('delete', False))
    
    def refresh(self):
        self.emit(self.EVENT_TOOLBUTTON_CLICK, ('refresh', False))
        
        
    def load_project(self):
        self.emit(self.EVENT_TOOLBUTTON_CLICK, ('load_project', False))
        
    def save_project_as(self):
        self.emit(self.EVENT_TOOLBUTTON_CLICK, ('save_project_as', False))
        
    def save_project(self):
        self.emit(self.EVENT_TOOLBUTTON_CLICK, ('save_project', False))
        
    def radtracer(self):
        self.emit(self.EVENT_TOOLBUTTON_CLICK, (labels.RADTRACER, False))
        
    def pyshield(self):
        self.emit(self.EVENT_TOOLBUTTON_CLICK,  (labels.PYSHIELD, False))
    
    @property
    def selected_tool(self):
        selected_item = None
        for name, action in self._actions.items():
            if name == 'side_panel':
                continue
            
            if action.isChecked():
                if selected_item is not None:
                    raise RuntimeError() # debug purpuses
                elif name in ('zoom', 'pan'):
                    return name
                else:
                    selected_item = self.pyrateshield_dict[name]
        return selected_item
    
    def tool_selected(self, toolname):
        checked = self._actions[toolname].isChecked()
        self.deselect_zoom_pan()
        if checked:
            self.select_checkable_tool(toolname)
        label = self.pyrateshield_dict[toolname]
        self.emit(self.EVENT_TOOLBUTTON_CLICK, (label, checked))
        
    def source_nm(self):
        self.tool_selected('source_nm')
        
    def source_ct(self):
        self.tool_selected('source_ct')
        
    def source_xray(self):
        self.tool_selected('source_xray')
        
    def wall(self):
        self.tool_selected('wall')
        
    def critical_point(self):
        self.tool_selected('critical_point')
        
    def side_panel(self):
        checked = self._actions['side_panel'].isChecked()
        self.emit(self.EVENT_TOOLBUTTON_CLICK, ('side_panel', checked))
        
    def zoom(self):
        NavigationToolbar2QT.zoom(self)
        if self.mode == _Mode.ZOOM:
            self.deselect_model_items()
        
    def pan(self):
        NavigationToolbar2QT.pan(self)
        if self.mode == _Mode.PAN:
            self.deselect_model_items()
        
        
    def select_checkable_tool(self, toolname=None):
        for name in ('source_nm', 'source_ct', 'source_xray',
                     'wall', 'critical_point'):
            if toolname != name:
                self._actions[name].setChecked(False)
    
    @property
    def zoom_pan_selected(self):
        return self.mode in (_Mode.PAN, _Mode.ZOOM)
    
    def deselect_zoom_pan(self):
        if self.mode == _Mode.PAN:
            self.pan()
        elif self.mode == _Mode.ZOOM:
            self.zoom()
    
    def deselect_model_items(self):
        for action in ('source_ct', 'source_xray', 'source_nm',
                       'critical_point', 'wall'):
            self._actions[action].setChecked(False)
            
            
    def deselect(self):
        self.deselect_zoom_pan()
        self.deselect_model_items()
        
    

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self):
        self.fig = Figure()
        self.fig.set_facecolor('0.8') #Gray background around axes
        self.ax = self.fig.add_axes([0, 0, 1, 1])

        FigureCanvasQTAgg.__init__(self, self.fig)

        FigureCanvasQTAgg.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)

        FigureCanvasQTAgg.updateGeometry(self)

    

