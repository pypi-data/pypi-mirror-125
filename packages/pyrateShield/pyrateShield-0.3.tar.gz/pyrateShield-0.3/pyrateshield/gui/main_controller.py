from pyrateshield.gui.main_view import MainView
from pyrateshield.model import Model
from PyQt5.QtWidgets import QApplication
from pyrateshield.gui.mpl_controller import MplController
from pyrateshield.model_items import MeasuredGeometry
from pyrateshield.gui.context_menu import ContextMenuController
from pyrateshield.gui.critical_point_controller import CriticalPointReportController

from pyrateshield.gui.controllers import (EditOriginController, 
                                          EditPixelSizeController, 
                                          EditFloorplanController,
                                          LoadSaveController,
                                          NewProjectController)
                                          
from pyrateshield.gui.item_controllers import (EditSourceXrayController, 
                                               EditSourceCTController, 
                                               EditWallsController, 
                                               EditCriticalPointsController, 
                                               EditSourcesNMController, 
                                               EditShieldingController)
                                               
                                              

from pyrateshield import labels


    
class MainController():
    _critical_points_controller = None
    def __init__(self, dosemapper=None, model=None, view=None):
        
        if model is None:
            model = Model()
    
            
        if view is None:
            view = MainView()
        
        self.dosemapper = dosemapper
        
        self.view = view
            
        self._model = model
        
        self.controllers = self.create_controllers()
        
        self.set_callbacks()
        
        # display model
        self.controllers[labels.CANVAS].plot_floorplan()
        
        
        self.context_menu_controller = ContextMenuController(view=self.view,
                             mpl_controller=self.controllers[labels.CANVAS],
                             model=model,
                             main_controller=self)
        
        self.load_model()
        
        self.controllers[labels.SHIELDINGS].view.setEnabled(True)
        
    @property
    def mpl_controller(self):
        return self.controllers[labels.CANVAS]
        
    @property
    def model(self):
        if self._model is None:
            self._model = Model()
        return self._model
    
    @model.setter
    def model(self, model):
        if model is self.model:
            return
        self._model = model
        self.load_model()
        
    def load_model(self):
        self.model.match_extent_to_floorplan()
     
        for key, controller in self.controllers.items():
            controller.model = self.model
            


        self.controllers[labels.CANVAS].plot_floorplan()

        self.context_menu_controller.model = self.model

        event = self.model.floorplan.EVENT_UPDATE_GEOMETRY
        self.model.floorplan.connect(self, event, self.refresh)
        
        event = self.model.floorplan.EVENT_UPDATE_IMAGE
        self.model.floorplan.connect(self, event, self.refresh)
        
        event = self.model.EVENT_UPDATE_FLOORPLAN
        self.model.connect(self, event, self.new_floorplan)

        self.model.connect(self, self.model.EVENT_SELECT_ITEM, 
                           self.set_selected_item)
        

        self.refresh()

    
    @property
    def controller_types(self):
        return {labels.CANVAS:                      MplController,
                labels.SOURCES_CT:                  EditSourceCTController,
                labels.SOURCES_XRAY:                EditSourceXrayController,
                labels.SOURCES_NM:                  EditSourcesNMController,
                labels.WALLS:                       EditWallsController,
                labels.SHIELDINGS:                  EditShieldingController,
                labels.CRITICAL_POINTS:             EditCriticalPointsController,
                labels.FLOORPLAN:                   EditFloorplanController,
                labels.PIXEL_SIZE_CM:               EditPixelSizeController,
                labels.ORIGIN_CM:                   EditOriginController,
                labels.LOAD_SAVE:                   LoadSaveController,
                #labels.PREFERENCES:                 PreferenceController,
                
                labels.CRITICAL_POINT_REPORT_VIEW:  CriticalPointReportController,
                labels.NEW_PROJECT:                 NewProjectController}

    
        
    def create_controllers(self):
        controllers = {}
        
        # shieldings = self.model.shieldings
        # walls = self.model.walls
        mpl_controller_type = self.controller_types[labels.CANVAS]
        
        mpl_controller = mpl_controller_type(dosemapper=self.dosemapper,
                                             view=self.view.views[labels.CANVAS],
                                             model=self.model)
        
        
        for key, contr_type in self.controller_types.items():
            view = self.view.views[key]
            
            if key == labels.CANVAS:
                controllers[labels.CANVAS] = mpl_controller
            
            elif key in (labels.SOURCES_NM, labels.SOURCES_CT, 
                       labels.SOURCES_XRAY, labels.WALLS, 
                       labels.CRITICAL_POINTS, labels.ORIGIN_CM, 
                       labels.PIXEL_SIZE_CM, labels.SHIELDINGS):

                controllers[key] = contr_type(model=self.model, 
                                              view = view,
                                              mpl_controller=mpl_controller)
            
            
            elif key in (labels.CRITICAL_POINT_REPORT_VIEW):
                controllers[key] = contr_type(model=self.model, 
                                              view = view,
                                              dosemapper=self.dosemapper)
                
            elif key in (labels.NEW_PROJECT, labels.LOAD_SAVE, labels.FLOORPLAN):
                controllers[key] = contr_type(model=self.model,
                                              view=view,
                                              main_controller=self)
           
                
            else:
                raise KeyError()
                

        
        return controllers


        
        
    def set_callbacks(self):

        
        
        for label, tab in self.view.toolbox_tabs.items():
            callback = lambda index, label=label: self.tab_selected(index, label)
            tab.currentChanged.connect(callback)
            
        self.view.toolbox.currentChanged.connect(self.toolbox_selected)

        
        # {develop}
        mouse = self.controllers[labels.CANVAS].mouse
        mouse.connect(self, mouse.MOVE_EVENT, self.view.set_status_text)
        
        toolbar = self.view.views[labels.CANVAS].toolbar
        toolbar.connect(self, toolbar.EVENT_TOOLBUTTON_CLICK, self.toolbar_callback)
    
    def toolbar_callback(self, event_data):
        toolname, checked = event_data
        
        if toolname == 'side_panel':
            self.view.toolbox.setVisible(checked)
        elif toolname == 'save_project_as':
            self.controllers[labels.LOAD_SAVE].save_as()
        elif toolname == 'load_project':
            self.controllers[labels.LOAD_SAVE].load()
        elif toolname == 'save_project':
            self.controllers[labels.LOAD_SAVE].save()
            
            
        
        
    def new_floorplan(self, floorplan):
        model = Model(floorplan=floorplan)
        self.model = model
        
        
    def refresh(self, _=None):
        self.mpl_controller.refresh()
        tooltext = self.view.toolbox.itemText(self.view.toolbox.currentIndex())
        
        if tooltext == labels.FLOORPLAN:
            tab = self.view.toolbox_tabs[labels.FLOORPLAN]
            tabtext = tab.tabText(tab.currentIndex())
            if tabtext == labels.PIXEL_SIZE_CM:
                self.mpl_controller.pixel_size.set_visible(True)
            elif tabtext == labels.ORIGIN_CM:
                self.mpl_controller.origin.set_visible(True)
                
        if self.model.floorplan.geometry.locked:
            self.view.set_tab_enabled(labels.PIXEL_SIZE_CM, False)
            self.view.set_tab_enabled(labels.ORIGIN_CM, False)
            
        else:
            self.view.set_tab_enabled(labels.PIXEL_SIZE_CM, True)      
            self.view.set_tab_enabled(labels.ORIGIN_CM, True)
            
        if self.model.filename is None:
            self.mpl_controller.view.toolbar.button_enabled('save_project', False)
        else:
            self.mpl_controller.view.toolbar.button_enabled('save_project', True)
        
        
    def toolbox_selected(self, index):
        text = self.view.toolbox.itemText(index)
        tab_index = self.view.toolbox_tabs[text].currentIndex()
        self.tab_selected(tab_index, text)           
        
    def tab_selected(self, index, label):
        text = self.view.toolbox_tabs[label].tabText(index)
        
        if text in [labels.SHIELDINGS]:
            wall = self.controllers[labels.WALLS].get_item_in_view()
            if wall is not None:
                shielding = self.model.shieldings.get_shielding_by_name(wall.shielding)
                self.controllers[text].model_to_view(shielding)
            
        if text == labels.PIXEL_SIZE_CM:
            self.mpl_controller.pixel_size.update()
            if isinstance(self.model.floorplan.geometry, MeasuredGeometry):
                self.mpl_controller.pixel_size.set_visible(True)

            self.mpl_controller.origin.set_visible(False)
            self.controllers[text].refresh()
            
        elif text == labels.ORIGIN_CM:
            self.mpl_controller.pixel_size.set_visible(False)
            self.mpl_controller.origin.set_visible(True)
            self.controllers[text].refresh()
        else:
            self.mpl_controller.pixel_size.set_visible(False)
            self.mpl_controller.origin.set_visible(False)
        
        
        
    def set_selected_item(self, item):
        # set edit menu to focus when an item is picked in the plot
        
        if item is not None:
            self.view.set_focus(item.label)
            self.controllers[item.label].refresh()

       
def main(model=None, controller=None, dm=None):
        app = QApplication([])
        
        controller = MainController(model=model, dosemapper=dm)
        window = controller.view
        window.show()    
        app.exec_()
    
if __name__ == "__main__":  
    from pyrateshield.dosemapper import Dosemapper

    project = '../../example_projects/Lu-177.psp'
    #project = '/Users/marcel/git/pyrateshield/example_projects/SmallProject/project.psp'
    #project = '../../example_projects/LargeProject/project2.psp'
    model = Model.load_from_project_file(project)
    
    app = QApplication([])
    
    with Dosemapper() as dm:
        controller = MainController(model=model, dosemapper=dm)
        window = controller.view
        window.show()    
        app.exec_()
        

