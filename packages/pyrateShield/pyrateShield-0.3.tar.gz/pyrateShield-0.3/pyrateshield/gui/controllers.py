from PyQt5.QtWidgets  import QFileDialog
from pyrateshield import labels, Logger, Observable
from pyrateshield.gui.mpl_view import LineDrawer, PointClicker
from pyrateshield.model_items import Floorplan, Geometry, MeasuredGeometry
from pyrateshield.model_items import Constants
from pyrateshield.model import Model

import numpy as np
import math
import os
import yaml

CONSTANTS = Constants()

LOG_LEVEL = Logger.LEVEL_INFO

def ask_existing_file(title, extensions, directory=None):
    filedialog = QFileDialog(directory=directory)
    filedialog.setFileMode(QFileDialog.ExistingFile)
    file = str(QFileDialog.getOpenFileName(filedialog, title, "",
                                           extensions)[0])
    
    return file

def ask_new_file(title, extensions, directory=None):
    filedialog = QFileDialog(directory=directory)
    filedialog.setFileMode(QFileDialog.AnyFile)
    file = str(QFileDialog.getSaveFileName(filedialog, title, "",
                                           extensions)[0])
    
    return file
    
class ModelUpdateController:
    _model = None
    
    @property
    def model(self):
        return self._model
    
    @model.setter
    def model(self, model):
        if model is self.model:
            return
        
        if isinstance(self.model, Observable):
            self.model.disconnect(self)

        self._model = model
        
        self.connect_model()
        
    def model_to_view(self, item=None):
        pass
    
    def connect_model(self):
        pass
    
# class PreferenceController(ModelUpdateController):
#     def __init__(self, model=None, view=None):
        
#         self.view = view
#         self.model = model
#         self.view.connect(self, self.view.EVENT_VIEW_UPDATE, 
#                           self.write_model)
        
#     def connect_model(self):
#         self.model.dosemap.connect(self, self.model.dosemap.EVENT_UPDATE,
#                            self.model_to_view)

#     def model_to_view(self, _=None):
#         if self.model.dosemap.engine == labels.PYSHIELD:
#             self.view.pyshield_button.setChecked(True)
#         elif self.model.dosemap.engine == labels.RADTRACER:
#             self.view.radtracer_button.setChecked(True)
#         else:
#             raise ValueError(self.model.dosemap.engine)
            
#     def write_model(self, _=None):        
#         if self.view.pyshield_button.isChecked():
#             self.model.dosemap.engine  = labels.PYSHIELD
#         elif self.view.radtracer_button.isChecked():
#             self.model.dosemap.engine  = labels.RADTRACER
        


class LoadSaveController(ModelUpdateController):
    def __init__(self, model=None, view=None, main_controller=None):
        self.view = view
        self.main_controller = main_controller
        self.model = model
        
        
        self.view.load_project_button.clicked.connect(self.load)
        self.view.save_project_button.clicked.connect(self.save_as)
        
        
        self.view.save_yaml_button.clicked.connect(self.save_yaml)
        self.view.load_yaml_button.clicked.connect(self.load_yaml)
        
    def load(self):
        if self.model.filename is not None:
            folder = os.path.split(self.model.filename)[0]
            if not os.path.exists(folder):
                folder = None
        else:
            folder = None
            
        file = ask_existing_file("Select Project File", 
                                 "PyrateShield Projects (*.psp)",
                                 directory=folder)
        
        if isinstance(file, str) and file != '' and os.path.exists(file):
            new_model = Model.load_from_project_file(file)
            
            self.main_controller.model = new_model
        
    def save_as(self): 
        
        if self.model.filename is not None:
            folder = os.path.split(self.model.filename)[0]
            if not os.path.exists(folder):
                folder = None
        else:
            folder = None
            
        file = ask_new_file("Select Project File", 
                            "PyrateShield Projects (*.psp)",
                            directory=folder)
        
        
        
        if isinstance(file, str) and file != '':
            self.main_controller.model.save_to_project_file(file)
            
            
    def save(self):
        try:
            self.main_controller.model.save_to_project_file(self.model.filename)
        except:
            self.save_as()
            
    
    def load_yaml(self):
        filename = ask_existing_file("Select Yaml File", 
                                     "yaml (*.yml)")
        if isinstance(filename, str) and filename != '':
            with open(filename, 'r') as file:
                contents = yaml.safe_load(file)
            
            new_model = Model.from_dict(contents)
            
            if new_model.floorplan.image is None:
                new_model.floorplan = self.model.floorplan
            
            self.main_controller.model = new_model
        
    def save_yaml(self):
        filename = ask_new_file("Select Yaml File", 
                                 "yaml (*.yml)")
        
        if isinstance(filename, str) and filename != '':
            with open(filename, 'w') as file:
                yaml.dump(self.main_controller.model.to_dict(), file)
        
            
    
class NewProjectController(ModelUpdateController):
    _default_empty_size_y = 1E2 # empty canvas number of pixels in y
    _default_empty_size_cm = (1E4, 1E4) # default new size in cm
    
    _image_file = None
    _keep_geometry = None
    
    def __init__(self, view=None, model=None, main_controller=None):
        ModelUpdateController.__init__(self)
        self.view = view
        self.model = model
        self.main_controller = main_controller
        
        self.view.confirm_button.clicked.connect(self.confirm)
        self.view.image_button.clicked.connect(self.select_image)  
        self.model_to_view()

    def select_image(self):
        file = self.ask_image_file("Select bitmap image")
        
        if isinstance(file, str) and file != '' and os.path.exists(file):
            self.view.image_label.setText(file)
            self.load_image()
        
    def model_to_view(self, _=None):
        self.view.x.setValue(self._default_empty_size_cm[0])
        self.view.y.setValue(self._default_empty_size_cm[1])
        
    def load_image(self):
        file = self.view.image_label.text()
        
        if isinstance(file, str) and file != '' and os.path.exists(file):
            floorplan = Floorplan()
            floorplan.filename = file
            model = Model(floorplan=floorplan)
            self.main_controller.model = model
            self.main_controller.view.set_focus(labels.PIXEL_SIZE_CM)

    def load_empty(self):
        
       
        shape_cm = (int(self.view.x.value()), int(self.view.y.value()))
        
        
        pixel_size = shape_cm[1] / self._default_empty_size_y
        
        
        
        origin = (0, 0)
        
        
        # rounds pixels in x down, should not matter for large arrays
        shape_pixels = (int(shape_cm[0] / pixel_size), 
                        int(shape_cm[1] / pixel_size))


        empty_canvas = np.ones(shape_pixels)
        
        geometry = Geometry(origin_cm=origin, 
                            pixel_size_cm=pixel_size,
                            locked=True)
    
        floorplan_model = Floorplan(image=empty_canvas, geometry=geometry)
                                    
        
        model = Model(floorplan=floorplan_model)
  
        
        self.main_controller.model = model
        
    def confirm(self):
     
        if self.view.choose_image.isChecked():
            self.load_image()
        elif self.view.choose_empty.isChecked():
            self.load_empty()
        
        
    def ask_image_file(self, title):
        extensions = "Image Files (*.png *.jpg *.jpeg, *.tiff, *.bmp)"
        return ask_existing_file(title, extensions)
          
class EditFloorplanController(ModelUpdateController):
    def __init__(self, view=None, model=None, main_controller=None):
        ModelUpdateController.__init__(self)
        
        self.model = model
        self.view = view
        self.main_controller = main_controller
        self.view.image_button.clicked.connect(self.select_image)  
        self.model_to_view()
    
    def connect_model(self):
        self.refresh()
        
    def refresh(self):
        self.model_to_view()
    
    def model_to_view(self, _=None):
        if self.model.floorplan.filename is not None:
            self.view.image_label.setText(self.model.floorplan.filename)

    def select_image(self):
        file = self.ask_image_file("Select bitmap image")
        if isinstance(file, str) and file != '' and os.path.exists(file):
            self.view.image_label.setText(file)
            self.load_image()
            self.main_controller.view.set_focus(labels.PIXEL_SIZE_CM)

    def load_image(self):
        file = self.view.image_label.text()
        
        if isinstance(file, str) and file != '' and os.path.exists(file):
            if self.model.floorplan.filename != file:
                self.model.floorplan.filename = file
                
                if not self.view.keep_geometry.isChecked():
                    self.model.geometry = Geometry()
                         
    def ask_image_file(self, title):
        extensions = "Image Files (*.png *.jpg *.jpeg, *.tiff, *.bmp)"
        return ask_existing_file(title, extensions)


class EditOriginController(ModelUpdateController):

    def __init__(self, view=None, model=None, mpl_controller=None):
        ModelUpdateController.__init__(self)
        self.view = view
        self.model = model
        self.mpl_controller = mpl_controller

        
        
        self.view.measure_button.clicked.connect(self.measure)
        
        
        self.view.confirm_fixed.clicked.connect(lambda _: self.confirm_fixed())
        self.view.confirm_moving.clicked.connect(lambda _: self.confirm_moving())
        
    def connect_model(self):
        self.model.connect(self, self.model.floorplan.EVENT_UPDATE_GEOMETRY, 
                           self.model_to_view)
        
        self.refresh()
    
    def refresh(self):
        self.model_to_view()
        
    def get_new_origin(self):
        return (self.view.get_position()[0],
                self.view.get_position()[1])
     
    def model_to_view(self):
        self.view.set_position(self.model.floorplan.geometry.origin_cm)
        
    def measure(self):
        self.point_clicker = PointClicker(self.mpl_controller)
        self.point_clicker.connect(self, self.point_clicker.EVENT_POINT_CLICKED,
                                   self.set_position)

        
    def set_position(self, position):
        origin = self.model.floorplan.geometry.origin_cm
        
        new_origin = [origin[0] + position[0],
                      origin[1] + position[1]]
        
        self.view.set_position(new_origin)
        
        dx = new_origin[0]  - origin[0]
        dy = new_origin[1]  - origin[1]
        

        self.mpl_controller.origin.mpl_item.set_xdata(dx)
        self.mpl_controller.origin.mpl_item.set_ydata(dy)
        self.mpl_controller.draw()


    def confirm_fixed(self, origin_cm=None):
        if origin_cm is None:
            origin_cm = self.model.floorplan.geometry.origin_cm

        new_origin = self.get_new_origin()
        
        shiftx = origin_cm[0] - new_origin[0] 
        shifty = origin_cm[1] - new_origin[1] 
        
        self.model.shift_cm(shiftx, shifty)
            
        self.model.floorplan.geometry.origin_cm = new_origin
        self.mpl_controller.origin.set_visible(True)
        
    
    def confirm_moving(self):
        new_origin = self.view.get_position()
        self.model.floorplan.geometry.origin_cm = new_origin
        self.mpl_controller.origin.set_visible(True)
      
        
        
    
    
        
class EditPixelSizeController(ModelUpdateController):
    _geometry = None
    
    def __init__(self, view=None, model=None, mpl_controller=None):
        ModelUpdateController.__init__(self)
        self.view = view
        self.model = model
        self.mpl_controller = mpl_controller
        
        self.view.connect(self, self.view.EVENT_VIEW_UPDATE, self.update_by_view)
        self.view.measure_button.clicked.connect(self.measure)
        self.view.confirm_button.clicked.connect(self.view_to_model)
        
        self.model_to_view()
        
    def connect_model(self):
        self.model.connect(self, self.model.floorplan.EVENT_UPDATE_GEOMETRY, 
                           self.model_to_view)
        
        self.refresh()
        
    def update_by_view(self, _=None):
        if self.view.choose_measured.isChecked():
            try:
                distance_cm = float(self.view.physical_distance.text())
                pixel_distance = float(self.view.pixel_distance.text())
            except:
                
                return
            if pixel_distance > 0:
                pixel_size_cm = distance_cm / pixel_distance
            else:
                return
            
            self.view.pixel_size_measured.setText(str(round(pixel_size_cm, 3)))
            self.view.pixel_size.setText('')
            
    
    def refresh(self):
        self.model_to_view()
        
    def update_by_line(self, vv):
        distance_cm = math.sqrt((vv[0][0]-vv[1][0])**2\
                                + (vv[0][1] - vv[1][1])**2)
            
        
        vvp = [self.model.floorplan.geometry.cm_to_pixels(vv[0]),
               self.model.floorplan.geometry.cm_to_pixels(vv[1])]
        
        
        pixel_distance = math.sqrt((vvp[0][0]-vvp[1][0])**2\
                                 + (vvp[0][1] - vvp[1][1])**2)
            
        self.view.pixel_distance.setText(str(round(pixel_distance)))
        # triggers update pixel size
        self.view.physical_distance.setText(str(round(distance_cm)))
        


        
    def model_to_view(self, _=None):
        if isinstance(self.model.floorplan.geometry, MeasuredGeometry):
            distance_cm = self.model.floorplan.geometry.distance_cm
            pixel_distance = self.model.floorplan.geometry.distance_pixels
            pixel_size_cm = self.model.floorplan.geometry.pixel_size_cm
            
            self.view.physical_distance.setText(str(round(distance_cm)))
            self.view.pixel_distance.setText(str(round(pixel_distance)))
            self.view.pixel_size_measured.setText(str(round(pixel_size_cm, 3)))
            self.view.physical_distance.setText(str(distance_cm))
            self.view.set_choose_measured()
            self.view.pixel_size.setText('')
            self.mpl_controller.pixel_size.update()
            
        else:
            self.view.choose_measured.setChecked(False)
            self.view.choose_fixed.setChecked(True)
            self.view.pixel_size.setText(str(self.model.floorplan.geometry.pixel_size_cm))
            self.view.set_choose_fixed()
            
            self.view.physical_distance.setText('')
            self.view.pixel_size_measured.setText('')
            self.view.pixel_distance.setText('')
            
    
    
    def calculate_new_origin(self, new_pixel_size_cm):
        geometry = self.model.floorplan.geometry
        origin_pixels = geometry.cm_to_pixels((0, 0))
        
        new_origin_cm = [oi * new_pixel_size_cm for oi in origin_pixels]
        return new_origin_cm
    
    
        
    def move_model_for_new_origin(self, new_origin_cm):
        # if only pixel_size changes the origin_cm will be displayed on a different
        # location on the floorplan
        # move all objects in model to keep origin in place
        # as long as origin is (0, 0) nothing will happen
        
        
        origin_cm = self.model.floorplan.geometry.origin_cm
        dx = new_origin_cm[0] - origin_cm[0]
        dy = new_origin_cm[1] - origin_cm[1]
        
        self.model.shift_cm(dx, dy)
        
        

    def view_to_model(self, vertices=None):
       
      
        if self.view.choose_fixed.isChecked():
    
            try:
                new_pixel_size_cm = float(self.view.pixel_size.text())
            except:
                return
            
            if new_pixel_size_cm <= 0:
                return
            
            new_origin_cm = self.calculate_new_origin(new_pixel_size_cm)
            
            new_geometry = Geometry(pixel_size_cm=new_pixel_size_cm,
                                origin_cm=new_origin_cm)


        elif self.view.choose_measured.isChecked(): 
            
            try:
                distance_cm = float(self.view.physical_distance.text())
            except:
                return
            
            xx = self.mpl_controller.pixel_size.mpl_item.get_xdata()
            yy = self.mpl_controller.pixel_size.mpl_item.get_ydata()
            
            geometry = self.model.floorplan.geometry
            
            
            vvp = [geometry.cm_to_pixels((xx[0], yy[0])),
                   geometry.cm_to_pixels((xx[1], yy[1]))]
            
            new_geometry = MeasuredGeometry(distance_cm=distance_cm,
                                            vertices_pixels=vvp)
        
            new_origin_cm = self.calculate_new_origin(
                new_geometry.pixel_size_cm)

            new_geometry.origin_cm = new_origin_cm
            
        self.move_model_for_new_origin(new_origin_cm)
        self.model.floorplan.geometry = new_geometry
        

    def measure(self):
        
        self.drawer = LineDrawer(self.mpl_controller, 
                                 self.mpl_controller.pixel_size.mpl_item)
        
        self.drawer.connect(self, self.drawer.EVENT_DRAW_FINISHED, 
                            self.update_by_line)
        





    




        
        
