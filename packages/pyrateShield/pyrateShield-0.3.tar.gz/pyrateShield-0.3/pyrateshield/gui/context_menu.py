from PyQt5.QtWidgets import QMenu
from PyQt5.QtGui import QCursor
from pyrateshield import labels
from functools import partial
from copy import copy
import math
from pyrateshield.model_items import Wall, ModelItem
from pyrateshield.gui.mpl_view import LineDrawer
import qtawesome as qta
SNAP_RADIUS_POINTS = 100

class ContextMenuController:
    to_copy = None
    
    def __init__(self, model=None, view=None, mpl_controller=None,
                 main_controller=None):
        self.view = view
        self.model = model
        self.main_controller = main_controller
        self.mpl_controller = mpl_controller
        
        self.mpl_controller.connect(self, mpl_controller.EVENT_PICK_RIGHT_CLICK,
                                    self.show_pick_context_menu)
        
        self.mpl_controller.mouse.connect(self, self.mpl_controller.mouse.RIGHT_CLICK_EVENT,
                                          self.show_canvas_context_menu)

    
    def show_canvas_context_menu(self, position=None):
        if self.mpl_controller.lock_mouse:
            return
        if self.mpl_controller.view.toolbar.zoom_pan_selected:
            return
        
        context_menu = QMenu(self.view)
       
        for label in [labels.SOURCES_CT, labels.SOURCES_XRAY,
                      labels.SOURCES_NM, labels.CRITICAL_POINTS]:
            
            title = 'Add ' + label + ' here'
            action = context_menu.addAction(title)
            callback = partial(self.add_item, label, position)
            
            action.triggered.connect(callback)
            
        action = context_menu.addAction('Start wall here')
        callback = partial(self.draw_wall, position)
        action.triggered.connect(callback)
        
            
        action = context_menu.addAction('Paste here')
        callback = partial(self.paste_item, position)
        action.triggered.connect(callback)
        
        
        if self.to_copy is None:
            action.setEnabled(False)
        
        context_menu.exec_(QCursor.pos())
            
    def add_item(self, label, position):
        self.mpl_controller.view.toolbar.button_checked(label, True)
        self.mpl_controller.add_model_item_by_mouse(label, multiple=False,
                                                    position=position)
    
    
    def closest_vertice(self, position, selected_wall):
        closest_vertice = None
        closest_distance = float('Inf')
        closest_wall = None
        for wall in self.model.walls:
            if wall is selected_wall:
                continue
            for index, vertex in enumerate(wall.vertices):
                p1 = self.mpl_controller.axes.transData.transform(position)
                p2 = self.mpl_controller.axes.transData.transform(vertex)
                
                distance = math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
               
                if distance < SNAP_RADIUS_POINTS and distance < closest_distance:
                    closest_vertice = vertex
                    closest_distance = distance
                    closest_wall = wall
        
        if closest_distance == 0:
            # disable snapping
            closest_vertice = None
        
        return closest_vertice, closest_wall
                    
        
        
    def show_pick_context_menu(self, event_data=None):
        item, position = event_data
        context_menu = QMenu(self.view)
        
        if isinstance(item, Wall):
            wall_draw_action = context_menu.addAction("Continue wall here")
            callback = partial(self.draw_wall, position)
            wall_draw_action.triggered.connect(callback)
            
            closest_vertice, closest_wall = self.closest_vertice(position, item)
            
            if closest_vertice is not None:
                disp_vv = str([round(vi) for vi in closest_vertice])
                shielding = self.model.shieldings.get_shielding_by_name(closest_wall.shielding)
                snap_action = context_menu.addAction("Snap to: " + shielding.name + ' at ' + disp_vv)
                callback = partial(self.snap_wall, item, position, closest_vertice)
                snap_action.triggered.connect(callback)
                
                icon = qta.icon('fa5s.circle', color=shielding.color)
                snap_action.setIcon(icon)
                
                

        if isinstance(item, ModelItem):
            delete_action = context_menu.addAction("Delete")
            callback = lambda: self.model.delete_item(item)
            delete_action.triggered.connect(callback)
        
            copy_action = context_menu.addAction("Copy")
            callback = lambda: self.copy_item(item)
            copy_action.triggered.connect(callback)
        
        if not isinstance(item, Wall):
            # cutting / pasting a wall makes no sense
            cut_action = context_menu.addAction("Cut")
            callback = lambda: self.cut_item(item)
            cut_action.triggered.connect(callback)
            
            enabled_action = context_menu.addAction("Enabled")
            enabled_action.setCheckable(True)
            model_item = self.mpl_controller.mpl_items.get_model_item(item)
            enabled_action.setChecked(model_item.enabled)
            callback = lambda: self.set_enabled(model_item, enabled_action)
            enabled_action.triggered.connect(callback)
            
            

            
        context_menu.exec_(QCursor.pos())
        
    def set_enabled(self, model_item, qaction):
        model_item.enabled = qaction.isChecked()
        
    def snap_wall(self, wall, position, closest_vertex):
        vv = wall.vertices
        pp = position
        
        d0 = math.sqrt((vv[0][0] - pp[0])**2 + (vv[0][1] - pp[1])**2)
        d1 = math.sqrt((vv[1][0] - pp[0])**2 + (vv[1][1] - pp[1])**2)
        
        if d0 <= d1:
            wall.set_vertex(0, closest_vertex)
        else:
            wall.set_vertex(1, closest_vertex)
        
        
    def draw_wall(self, position):
        self.mpl_controller.view.toolbar.button_checked(labels.WALLS, True)
        self.mpl_controller.add_wall_by_mouse(position=position)
        
        

    def copy_item(self, item):
        self.to_copy = copy(item)
        self.to_copy.disconnect()
        
    def paste_item(self, pos):
        self.to_copy.position = pos
        self.model.add_item(self.to_copy)
        self.model.selected_item = self.to_copy
        self.to_copy = None
        
    
    def cut_item(self, item):
        self.copy_item(item)
        self.model.delete_item(item)
        
    def delete_item(self, item):
        self.model.delete_item(item)