from pyrateshield import labels
from pyrateshield.logger import Logger
from pyrateshield.gui.controllers import ModelUpdateController
from pyrateshield.gui.mpl_view import LineDrawer
import qtawesome as qta
LOG_LEVEL = Logger.LEVEL_INFO

class EditModelItemControllerBase(Logger, ModelUpdateController):
    def __init__(self, model=None, view=None, mpl_controller=None):
        Logger.__init__(self, log_level=LOG_LEVEL)
        ModelUpdateController.__init__(self)
        
        if mpl_controller is None:
            raise
        
        self.view = view
        self.model = model
        self.mpl_controller = mpl_controller
        
        
        

        self.view.connect(self, self.view.EVENT_VIEW_UPDATE,
                          self.write_to_model)
        
    def connect_model(self):
        super().connect_model()
           
        self.model_items.connect(self, 
                                 self.model_items.EVENT_UPDATE_ITEM,
                                 self.refresh)   
        
        # self.model_items.connect(self, 
        #                           self.model_items.EVENT_REMOVE_ITEM,
        #                           self.delete_callback)
        
        self.model_items.connect(self, 
                                 self.model_items.EVENT_ADD_ITEM,
                                 self.refresh)
        self.model.connect(self, 
                           self.model.EVENT_SELECT_ITEM,
                           self.select_item_callback)
        
        self.refresh()
        
      
            
    
    def select_item_callback(self, item):
        
        if item in self.model_items:
            self.refresh()
            
    # def delete_callback(self, event_data):
    #     index, _ = event_data
    
    #     self.refresh()     
        
    #     if index > 0:
    #         self.model_to_view(self.model_items[index-1])
    #     elif len(self.model_items) > 0:
    #         self.model_to_view(self.model_items[0])
            
        
        
           
    
            
            
    @property
    def model_items(self):
         return self.model.get_model_items_by_label(self.ITEM_LABEL)
     
    def get_item_in_view(self):
         pass
     
    def write_to_model(self, _=None):
        item = self.get_item_in_view()
        if item is not None:
            item.update_by_dict(self.view.to_dict())
        
    def delete(self):
        item = self.get_item_in_view()
        
        if item is not None:
            self.model.delete_item(item)
            
        self.refresh()
            
            
     
    def model_to_view(self, item):
        self.view.disable_connection(self)
        
        if item not in self.model_items:
            return
        
        if item is None:
            raise
            self.view.clear()
        else:
            self.view.from_dict(item.to_dict())
        
        self.view.enable_connection(self)
        
    
    def new(self, **kwargs):
        self.mpl_controller.view.toolbar.deselect()
        new_item = self.model_items.add_new_item(**kwargs)
        self.model.selected_item = new_item
        
    def refresh(self, _=None):
        self.view.disable_connection(self)
       
        
        current_item = self.get_item_in_view()
        self.view.clear()

        if self.model.selected_item in self.model_items:
            self.view.set_enabled(True)
            self.model_to_view(self.model.selected_item)
         
        elif current_item in self.model_items:
            self.view.set_enabled(True)
            self.model_to_view(current_item)
            
        elif len(self.model_items) > 0:
            self.view.set_enabled(True)
            self.model_to_view(self.model_items[0])
            
    
        else:
            self.view.set_enabled(False)
            
        self.view.enable_connection()
        

class EditNamedModelItemController(EditModelItemControllerBase):  
    def __init__(self, model=None, view=None, mpl_controller=None):
        super().__init__(model=model, view=view, mpl_controller=mpl_controller)
        
        self.view.connect(self, self.view.EVENT_LIST_SELECTION, 
                          self.list_selection_callback)
        
        
        
    def connect_model(self):
        
        
        super().connect_model()
        
        self.model_items.connect(self, self.model_items.EVENT_NAME_UPDATE,
                                 self.model_has_new_name)
        
        
        
    def update_list(self):
        self.view.disable_connection(self)
        
        self.view.list.clear()
        
        for item in self.item_names:
            self.view.list.addItem(item)
        

        self.view.enable_connection(self)
        
    def add_model_item(self, _=None):
        super().add_model_item()
        self.update_list()
        
    def remove_model_item(self, _=None):
        super().remove_model_item()
        self.update_list()
        
    def get_item_in_view(self):
        if len(self.model_items) == 0:
            return None
        else:
            name = self.view.list.currentText()
            item = self.get_item_by_name(name)
        return item
    
    @property
    def item_names(self):
        return [item.name for item in self.model_items] 
    
    
    def get_item_by_name(self, name):
        if name not in self.item_names:
            return None
        
        index = self.item_names.index(name) 
    
        return self.model_items[index]
    
    def model_has_new_name(self, item=None):
        self.update_list()
        if item == self.get_item_in_view():
            self.model_to_view(item)
            
    def model_to_view(self, item=None):
        if item not in self.model_items:
            return
        self.view.disable_connection(self)
        self.view.list.setCurrentIndex(self.model_items.index(item))
        super().model_to_view(item)
        
    def refresh(self, _=None):
        self.view.disable_connection(self)
        self.update_list()
        super().refresh()
        
        
        
    def list_selection_callback(self, index=None):
        self.model.selected_item = self.model_items[index]
        
        
    @property
    def list_items(self):
        return [self.view.list.itemText(i)\
                for i in range(self.view.list.count())]


        
            
            

class EditPositionNamedModelItemController(EditNamedModelItemController):
    def new(self, _=None):
        xrange = self.mpl_controller.axes.get_xlim()
        yrange = self.mpl_controller.axes.get_ylim()
        
        position = ((xrange[0] + xrange[1])/2, (yrange[0] + yrange[1]) /2)
        
        super().new(position=position)

class EditSourceCTController(EditPositionNamedModelItemController):
    ITEM_LABEL = labels.SOURCES_CT
    
class EditSourceXrayController(EditPositionNamedModelItemController):
    ITEM_LABEL = labels.SOURCES_XRAY

class EditCriticalPointsController(EditPositionNamedModelItemController):
    ITEM_LABEL = labels.CRITICAL_POINTS
    
class EditSourcesNMController(EditPositionNamedModelItemController):
    ITEM_LABEL = labels.SOURCES_NM

class EditShieldingController(EditNamedModelItemController):
    ITEM_LABEL = labels.SHIELDINGS
    
    def __init__(self, model=None, view=None, mpl_controller=None):
        super().__init__(model=model, view=view, mpl_controller=mpl_controller)
        self.view.delete_button.clicked.connect(self.delete)
        self.view.new_button.clicked.connect(self.new)

    def connect_model(self):
        super().connect_model()
        
        
        self.model.walls.connect(self,
                                 self.model.walls.EVENT_ADD_ITEM,
                                 self.toggle_delete)
        
        self.model.walls.connect(self,
                                 self.model.walls.EVENT_REMOVE_ITEM,
                                 self.toggle_delete)
        
        
      
    @property
    def used_shieldings(self):
        shieldings = [labels.EMPTY_SHIELDING]
        shieldings += [wall.shielding for wall in self.model.walls]
        
        return list(set(shieldings))
    
    
    
    def model_to_view(self, item=None):
        super().model_to_view(item)
        
        
        if self.view.list.currentIndex() == 0:
            self.view.set_enabled(False)
        else:
            self.view.set_enabled(True)
            
        self.toggle_delete()
        
    def toggle_delete(self, _=None):
        item = self.get_item_in_view()

        if item.name in self.used_shieldings:
            self.view.delete_button.setEnabled(False)
        else:
           
            self.view.delete_button.setEnabled(True)     
    
    def select_item_callback(self, item):
        super().select_item_callback(item)
        
        if item in self.model.walls:
            
            shielding = self.model.shieldings.get_shielding_by_name(item.shielding)
            self.model_to_view(shielding)

    def write_to_model(self, _=None):
        item = self.get_item_in_view()
        old_name = item.name
        new_name = self.view.name_input.text()
        
        self.update_wall_shielding_names(old_name, new_name)
        
        super().write_to_model()
    
        if new_name != old_name:
            self.refresh()

    def update_wall_shielding_names(self, old_name, new_name):
        if old_name is None or old_name == new_name:
            return
        
        event_name = self.model.walls.EVENT_UPDATE_ITEM
        
        # dont trigger update for change of name
        self.model.walls.disable_connection(event_name=event_name)
        for wall in self.model.walls:
            if wall.shielding == old_name:
                wall.shielding = new_name
        self.model.walls.enable_connection(event_name=event_name)
    
    def update_list(self):
        self.view.disable_connection(self)
      
        self.view.list.clear()
        
        for item in self.model_items:
            icon = qta.icon('fa5s.circle', color=item.color)
            self.view.list.addItem(icon, item.name)
        
        self.view.enable_connection(self)
        
        
class EditWallsController(EditModelItemControllerBase):
    ITEM_LABEL = labels.WALLS
    def __init__(self, model=None, view=None, mpl_controller=None):
        super().__init__(model=model, view=view, mpl_controller=mpl_controller)

       
        
        #self.view.draw_new_button.clicked.connect(lambda _: self.draw())
        

        self.view.connect(self, self.view.EVENT_SCROLL, self.update_by_scroll)
       
        
    def get_item_in_view(self):
        if len(self.model_items) == 0:
            return None
        else:
            index = self.view.scroll_widget.value()
            if index < (len(self.model_items)):
                return self.model_items[index]
            else:
                return None
        

    def connect_model(self):
        super().connect_model()
        
        self.model.shieldings.connect(self, 
                                      self.model.shieldings.EVENT_ADD_ITEM,
                                      self.refresh)
        
        self.model.shieldings.connect(self, 
                                      self.model.shieldings.EVENT_REMOVE_ITEM,
                                      self.refresh)
        
        self.model.shieldings.connect(self,
                                      self.model.shieldings.EVENT_NAME_UPDATE,
                                      self.refresh)
        
    def refresh(self, _=None):
        self.update_shieldings()
        
        
        super().refresh()
        
        self.update_scroll_length()
        

        
        
    def update_by_scroll(self, index):
        if index < len(self.model_items):
            self.model.selected_item = self.model_items[index]
        
  
    def update_scroll_length(self):
        
        self.view.scroll_widget.setMaximum(max(0, len(self.model_items)-1))
    
    def model_to_view(self, model=None):
        if model not in self.model_items:
            return
        
        self.view.disable_connection(self)
        
        index = self.model_items.index(model)
        self.view.set_index(index) 
        
    
        shielding = self.model.shieldings.get_shielding_by_name(model.shielding)
        index = self.model.shieldings.index(shielding)
        self.view.shielding_list.setCurrentIndex(index)
        
        super().model_to_view(model)
        
    def update_shieldings(self, event_data=None):
        self.view.disable_connection(self)
        
        self.view.shielding_list.clear()
        
        for item in self.model.shieldings:
            icon = qta.icon('fa5s.circle', color=item.color)
            self.view.shielding_list.addItem(icon, item.name)

        self.view.enable_connection(self, self.view.EVENT_VIEW_UPDATE)
           
    def draw(self, event_data=None):
        # deselect zoom pan if selected
        self.mpl_controller.view.toolbar.deselect()
        
        item = self.model_items.add_new_item()
        
        
        # takes few ms for mpl to plot and be able to return line item

        line = self.mpl_controller.mpl_items.get_mpl_item(item)

        self.drawer = LineDrawer(mpl_controller=self.mpl_controller,
                                 line=line)
                            
        
        def draw_finished(vertices):
        
            item.vertices = vertices
            
            self.model.selected_item = item

        self.drawer.connect(self, self.drawer.EVENT_DRAW_FINISHED, 
                            draw_finished)
        
   
      
        
        