from PyQt5.QtWidgets import (QWidget, QCheckBox, QPushButton, QVBoxLayout, 
                             QLineEdit, QSpinBox, QGridLayout, QLabel, 
                             QComboBox, QDoubleSpinBox, QColorDialog, 
                             QRadioButton, QScrollBar)
from PyQt5 import QtCore
import qtawesome as qta
from pyrateshield import labels, Observable
from pyrateshield.model_items import Constants

MAX_VALUE = 999999999
CONSTANTS = Constants()

WIDGET_WIDTH = 300



        
class EditViewBase(QWidget, Observable):
    EVENT_VIEW_UPDATE = 'event_view_update'
    _layout = None
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        Observable.__init__(self)
        self.create_widgets()
        self.create_layout()
        self.set_callbacks()
        self.set_stretch()
        
    def set_callbacks(self):
        pass
    
    def create_widgets(self):
        pass
    
    def create_layout(self):
        pass
    
    def emit_change(self):
        self.emit(self.EVENT_VIEW_UPDATE, self)
    
    def set_stretch(self):
        self.stretch_layout = QVBoxLayout()
        if hasattr(self, 'explanation'):
            label = QLabel(self.explanation)
            label.setWordWrap(True)
            self.stretch_layout.addWidget(label)
        self.stretch_layout.addLayout(self.layout)
        self.stretch_layout.addStretch(1)
        self.setLayout(self.stretch_layout)
        
    @property
    def layout(self):
        if self._layout is None:
            self._layout = QGridLayout()
        return self._layout
    
    @staticmethod
    def set_combo_to_text(combo, text):
        combo.setCurrentIndex(combo.findText(str(text)))
        
    def set_enabled(self, enabled):
        index = self.layout.count()
        for i in range(index):
            widget = self.layout.itemAt(i).widget()
            widget.setEnabled(enabled)
            
            
        

        
class LoadSaveView(EditViewBase):
    explanation = "Loading or a new project will destroy any unsaved changes!"
    def create_widgets(self):
        
        
        self.save_project_button = QPushButton("Save Project")
        self.load_project_button = QPushButton("Load Project")
        
        
        #self.advanced_label = QPushButton("Save/Load config in editable format without floor plan image")
        
        self.save_yaml_button = QPushButton("Save To Yaml")
        self.load_yaml_button = QPushButton("Load From Yaml")
        
    def create_layout(self):
        row = 0
        
        self.layout.addWidget(self.save_project_button, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.load_project_button, row, 0, 1, 2)
        
        row += 1
        self.layout.addWidget(self.save_project_button, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.save_yaml_button, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.load_yaml_button, row, 0, 1, 2)
        
        self.setFixedWidth(WIDGET_WIDTH)



class EditListViewBase(EditViewBase):
    _name_text = "Name:"
    EVENT_LIST_SELECTION = 'event_list_selection'
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(WIDGET_WIDTH)
        
    def create_widgets(self):
        self.list = QComboBox(self)
        
        # self.save_button = QPushButton('Save', self)
        # self.undo_button = QPushButton('Undo', self)
        #self.new_button = QPushButton('Add', self)
        #self.delete_button = QPushButton('Delete', self)
    
        self.name_label = QLabel(self._name_text)
        self.name_input = QLineEdit()
        
        self.enabled_checkbox = QCheckBox('Enabled')
        
    def set_enabled(self, enabled):
        super().set_enabled(enabled)   
        
        self.list.setEnabled(True)

    def set_callbacks(self):
       
        self.name_input.returnPressed.connect(self.emit_change)
        self.enabled_checkbox.stateChanged.connect(lambda _: self.emit_change())
        self.list.currentIndexChanged.connect(lambda _: self.list_selection())

        
    def list_selection(self):
       
        self.emit(self.EVENT_LIST_SELECTION, event_data=self.list.currentIndex())

        
    def create_layout(self):
        row = 0
        
        self.layout.addWidget(self.list, row , 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.name_label, row, 0)
        self.layout.addWidget(self.name_input, row, 1)
      
        self.create_layout_body()
        
        row  = self.layout.rowCount() + 1
        #self.layout.addWidget(self.new_button, row, 0)
        #self.layout.addWidget(self.delete_button, row, 1)
        
        #row += 1
        
        self.layout.addWidget(self.enabled_checkbox, row, 0)
        
     
        #self.layout.addWidget(self.undo_button, 2, 0)
        #self.layout.addWidget(self.save_button, 2, 1)
        
    def create_layout_body(self):
        pass
        
    def clear(self):
        self.name_input.clear()      
    
    def emit_change(self):
        self.emit(self.EVENT_VIEW_UPDATE, self.to_dict())
        
    def to_dict(self):
        return {labels.NAME: self.name_input.text(),
                labels.ENABLED: self.enabled_checkbox.isChecked()}
    
    def from_dict(self, dct):
        self.disable_connection(event_name=self.EVENT_VIEW_UPDATE)
        self.disable_connection()
        
        
        self.name_input.setText(dct[labels.NAME])
        self.set_combo_to_text(self.list, dct[labels.NAME])
        self.enabled_checkbox.setChecked(dct[labels.ENABLED])
        self.enable_connection(event_name=self.EVENT_VIEW_UPDATE)

        
    
            
       
        
        
class EditListViewPositionBase(EditListViewBase):
    _position_x_text = "X [cm]:"
    _position_y_text = "Y [cm]:"
    
    
    def set_callbacks(self):
        super().set_callbacks()
        self.x.valueChanged.connect(self.emit_change)
        self.y.valueChanged.connect(self.emit_change)
        

    def to_dict(self):
        dct = super().to_dict()
        dct[labels.POSITION] = self.get_position()
        return dct

    def from_dict(self, dct):
        super().from_dict(dct)
        self.disable_connection(event_name=self.EVENT_VIEW_UPDATE)
        self.set_position(dct[labels.POSITION])
        self.enable_connection(event_name=self.EVENT_VIEW_UPDATE)
  
    def create_widgets(self):
        super().create_widgets()

        x = QSpinBox()
        x.setRange(-MAX_VALUE, MAX_VALUE)
        y = QSpinBox()
        y.setRange(-MAX_VALUE, MAX_VALUE)
        
        self.x = x
        self.y = y
        self.position_x_label = QLabel(self._position_x_text)
        self.position_y_label = QLabel(self._position_y_text)
        
        #self.position_button = QPushButton("Set Position By Mouse")
        
    def create_layout_body(self):
        row = self.layout.rowCount() + 1
        self.layout.addWidget(self.position_x_label, row, 0)
        self.layout.addWidget(self.x, row, 1)
        row += 1
        self.layout.addWidget(self.position_y_label, row, 0)
        self.layout.addWidget(self.y, row, 1)
        # row += 1
        # self.layout.addWidget(self.position_button, row, 0, 1, 2)
        
    def clear(self):
        super().clear()
        self.x.clear()
        self.y.clear()
        
    def set_position(self, coords):
        self.x.setValue(coords[0])
        self.y.setValue(coords[1])
    
    def get_position(self):
        return [self.x.value(), self.y.value()]
        

        
        
class EditShieldingView(EditListViewBase):
    _color = 'r'
    _DEFAULT_THICKNESS = 1
    _DEFAULT_LINEWIDTH = 1
    def from_dict(self, dct):
        super().from_dict(dct)

        self.disable_connection(event_name=self.EVENT_VIEW_UPDATE)
        
        
        materials = dct[labels.MATERIALS]
        
        if len(materials) > 0:
             material1, thickness1 = materials[0]
        else:
            material1, thickness1 = [labels.EMPTY_MATERIAL, 0]
            
        if len(materials) > 1:
            material2, thickness2 = materials[1]
        else:
            material2, thickness2 = [labels.EMPTY_MATERIAL, 0]

        self.set_combo_to_text(self.material1_list, material1)
        self.set_combo_to_text(self.material2_list, material2)
        
        self.thickness1_input.setValue(thickness1)
        self.thickness2_input.setValue(thickness2)
        
        self._color = dct[labels.COLOR]
        icon = qta.icon('fa5s.circle', color=self.color)
        
        self.color_button.setIcon(icon)
        
        self.line_width.setValue(dct[labels.LINEWIDTH])
        
        
        self.enable_connection(event_name=self.EVENT_VIEW_UPDATE)
 
    
    @property
    def color(self):
       
        return self._color
    
    @color.setter
    def color(self, color):
        self._color = color
        self.emit(self.EVENT_VIEW_UPDATE)
    
    
    def select_color(self):
        color = QColorDialog().getColor()
        if color.isValid():
            self.color = color.name()
            
    def to_dict(self):
        dct = super().to_dict()
        dct.pop(labels.ENABLED)
        
        
        dct[labels.LINEWIDTH] = self.line_width.value()
        dct[labels.COLOR] = self.color
        
        material1 = self.material1_list.currentText()
        thickness1 = self.thickness1_input.value()
        
        material2 = self.material2_list.currentText()
        thickness2 =  self.thickness2_input.value()
        
        materials = [[material1, thickness1], [material2, thickness2]]
        
        
        dct[labels.MATERIALS] = materials
        
        return dct
        
    def create_widgets(self):
        super().create_widgets()
        
        #icon = qta.icon('fa5s.circle', color='red')
        self.color_button = QPushButton("Select Color", self)
        #self.color_button.setIcon(icon)

        self.material1_label = QLabel(labels.MATERIAL + ' 1')
        self.material1_list = QComboBox()

    
        self.thickness1_label = QLabel(labels.THICKNESS)
        self.thickness1_input = QDoubleSpinBox(decimals=3)
    
        self.material2_label = QLabel(labels.MATERIAL + ' 2')
        self.material2_list = QComboBox()

        materials = [material.name for material in CONSTANTS.materials]
        
        self.material1_list.addItems(materials)
        self.material2_list.addItems(materials)

        self.thickness2_label = QLabel(labels.THICKNESS)
        self.thickness2_input = QDoubleSpinBox(decimals=3)
        
        self.line_width_label = QLabel(labels.LINEWIDTH)
        self.line_width = QDoubleSpinBox()
        
        self.enabled_checkbox.setVisible(False)
        self.new_button = QPushButton('Add', self)
        self.delete_button = QPushButton("Delete")
        
        
    def set_enabled(self, enabled):
        super().set_enabled(enabled)
        self.new_button.setEnabled(True)
        

    def set_callbacks(self):
        super().set_callbacks()
        self.enabled_checkbox.stateChanged.disconnect()
        
        self.material1_list.currentTextChanged.connect(self.emit_change)
        self.material2_list.currentTextChanged.connect(self.emit_change)
        self.thickness1_input.valueChanged.connect(self.emit_change)
        self.thickness2_input.valueChanged.connect(self.emit_change)
        self.line_width.valueChanged.connect(self.emit_change)
        self.color_button.clicked.connect(self.select_color)
        
    def create_layout_body(self):
        
        row = self.layout.rowCount() + 1
        self.layout.addWidget(self.material1_label, row, 0)
        self.layout.addWidget(self.material1_list, row, 1)
        row += 1
        self.layout.addWidget(self.thickness1_label, row, 0)
        self.layout.addWidget(self.thickness1_input, row, 1)
        row += 1
        self.layout.addWidget(self.material2_label, row, 0)
        self.layout.addWidget(self.material2_list, row, 1)
        row += 1
        self.layout.addWidget(self.thickness2_label, row, 0)
        self.layout.addWidget(self.thickness2_input, row, 1)
        
        row += 1
        self.layout.addWidget(self.color_button, row, 0, 1, 2)
        
        row += 1
        self.layout.addWidget(self.line_width_label, row, 0)
        self.layout.addWidget(self.line_width, row, 1)
        super().create_layout_body()
        
        row += 1
        
        self.layout.addWidget(self.new_button, row, 0)
        self.layout.addWidget(self.delete_button, row, 1)
        
        
    def clear(self):
        super().clear()

        self.thickness1_input.setValue(self._DEFAULT_THICKNESS)
        self.thickness2_input.setValue(self._DEFAULT_THICKNESS)
        self.line_width.setValue(self._DEFAULT_LINEWIDTH)
        
        


        


class EditWallsView(EditViewBase):
    EVENT_SCROLL = 'event_scroll'
    start_x1, start_y1, start_x2, start_y2 = ['X1 [cm]', 'Y1 [cm]', 
                                              'X2 [cm]', 'Y2 [cm]']
    
    def create_widgets(self):
        super().create_widgets()
        self.shielding_label = QLabel("Shielding")
        self.shielding_list = QComboBox()
        
        self.position_input = {}
        self.position_label = {}
        for text in (self.start_x1, self.start_y1, 
                     self.start_x2, self.start_y2):
            self.position_input[text] = QDoubleSpinBox()
            self.position_input[text].setRange(-MAX_VALUE, MAX_VALUE)
            self.position_label[text] = QLabel(text)
            
            
        self.scroll_widget = QScrollBar(QtCore.Qt.Horizontal)
        self.scroll_widget.setPageStep(1)
        
        # self.position1_button = QPushButton('Set Position By Mouse')
        # self.position2_button = QPushButton('Set Position By Mouse')
    

        
        #self.draw_new_button = QPushButton("Draw New Wall")
        #self.delete_button = QPushButton("Delete")
        
        self.index_label = QLabel()
        
    def set_callbacks(self):
        
        self.shielding_list.currentTextChanged.connect(self.emit_change)
        
        for text in (self.start_x1, self.start_y1, 
                     self.start_x2, self.start_y2):
            self.position_input[text].valueChanged.connect(self.emit_change)
            
        self.scroll_widget.valueChanged.connect(lambda _: self.scroll())
            
    def scroll(self):
        self.emit(self.EVENT_SCROLL, self.scroll_widget.value())
        
            
    def to_dict(self):
        dct =  {labels.VERTICES: self.get_vertices(),
                labels.SHIELDING: self.shielding_list.currentText()}

        return dct
        
    def set_index(self, index=None):
        if index is None:
            return
        
        self.scroll_widget.setValue(index)
        self.index_label.setText(f'Wall index {index}')
        
    def create_layout(self): 
        row = 0
        
        self.layout.addWidget(self.scroll_widget, row , 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.index_label)
        
        row += 1
        
        self.layout.addWidget(self.shielding_label, row, 0)
        self.layout.addWidget(self.shielding_list, row, 1)
        
        row += 1
        
        text = self.start_x1
        self.layout.addWidget(self.position_label[text], row, 0)
        self.layout.addWidget(self.position_input[text], row, 1)
        
        row += 1
        
        text = self.start_y1
        self.layout.addWidget(self.position_label[text], row, 0)
        self.layout.addWidget(self.position_input[text], row, 1)
        
        # row += 1
        
        # self.layout.addWidget(self.position1_button, row, 0, 1, 2)
        
        row += 1
        
        text = self.start_x2
        self.layout.addWidget(self.position_label[text], row, 0)
        self.layout.addWidget(self.position_input[text], row, 1)
        
        row += 1
        
        text = self.start_y2
        self.layout.addWidget(self.position_label[text], row, 0)
        self.layout.addWidget(self.position_input[text], row, 1)
        
        # row += 1
        
        # self.layout.addWidget(self.position2_button, row, 0, 1, 2)
        
        #row += 1
        
        #self.layout.addWidget(self.draw_new_button, row, 0)
        #self.layout.addWidget(self.delete_button, row, 1)
        
        
     
    # def set_enabled(self, enabled):
    #     super().set_enabled(enabled)
    #     self.draw_new_button.setEnabled(True)
            
    def from_dict(self, dct):

        self.disable_connection(event_name=self.EVENT_VIEW_UPDATE)
        self.set_combo_to_text(self.shielding_list, dct[labels.SHIELDING])        
        self.set_vertices(dct[labels.VERTICES])
        self.enable_connection(event_name=self.EVENT_VIEW_UPDATE)
        
    def get_vertices(self):
        return [[self.position_input[self.start_x1].value(),
                 self.position_input[self.start_y1].value()],
                [self.position_input[self.start_x2].value(),
                 self.position_input[self.start_y2].value()]]
        
    def set_vertices(self, vertices):
        self.position_input[self.start_x1].setValue(vertices[0][0])
        self.position_input[self.start_y1].setValue(vertices[0][1])
        self.position_input[self.start_x2].setValue(vertices[1][0])
        self.position_input[self.start_y2].setValue(vertices[1][1])
        

        
    def clear(self):
        for text in (self.start_x1, self.start_y1, 
                     self.start_x2, self.start_y2):
            
            self.position_input[text].setValue(0)
            
            
        # self.scroll_widget.setValue(0)
        # self.scroll_widget.setMaximum(0)
        
        self.shielding_list.setCurrentIndex(0)
        

        
class EditSourcesNMView(EditListViewPositionBase):
    def from_dict(self, dct):
        super().from_dict(dct)
        self.disable_connection(event_name=self.EVENT_VIEW_UPDATE)
        self.duration.setValue(dct[labels.DURATION])
        self.activity.setValue(dct[labels.ACTIVITY])
        self.set_combo_to_text(self.isotope_input, dct[labels.ISOTOPE])
        self.set_combo_to_text(self.self_shielding_list, dct[labels.SELF_SHIELDING])
        self.number_of_exams_input.setValue(dct[labels.NUMBER_OF_EXAMS])
        self.decay_correction.setChecked(dct[labels.APPLY_DECAY_CORRECTION])
        self.biological_decay.setChecked(dct[labels.APPLY_BIOLOGICAL_DECAY])
        
        half_life = CONSTANTS.isotopes[dct[labels.ISOTOPE]].half_life
        self.isotope_halflife_value.setText(str(half_life))
        self.biological_halflife_value.setValue(dct[labels.BIOLOGICAL_HALFLIFE])
        self.enable_connection(event_name=self.EVENT_VIEW_UPDATE)
    
    def to_dict(self):
        dct = super().to_dict()
        dct[labels.DURATION] = self.duration.value()
        dct[labels.ACTIVITY] =  self.activity.value()
        dct[labels.ISOTOPE] = self.isotope_input.currentText()
        dct[labels.SELF_SHIELDING] = self.self_shielding_list.currentText()
        dct[labels.NUMBER_OF_EXAMS] = self.number_of_exams_input.value()
        dct[labels.APPLY_DECAY_CORRECTION] = self.decay_correction.isChecked()
        dct[labels.APPLY_BIOLOGICAL_DECAY] = self.biological_decay.isChecked()
        dct[labels.BIOLOGICAL_HALFLIFE] = self.biological_halflife_value.value()
        return dct
   
    
    def create_widgets(self):
        super().create_widgets()
    
        self.duration = QDoubleSpinBox()
        self.duration.setRange(0, MAX_VALUE)
        self.duration_label = QLabel(labels.DURATION)
        
        
       
        self.activity = QSpinBox()
        self.activity.setRange(0, MAX_VALUE)
        self.activity_label = QLabel(labels.ACTIVITY)
        
        self.isotope_input = QComboBox()
        self.isotope_input.addItems(CONSTANTS.isotopes.isotope_names)
        
        self.isotope_label = QLabel(labels.ISOTOPE)
        
        self.self_shielding_list = QComboBox()
        self.self_shielding_list.addItems(CONSTANTS.isotopes[0].self_shielding_options)
        self.self_shielding_label = QLabel(labels.SELF_SHIELDING)
        
        
        self.number_of_exams_label = QLabel(labels.NUMBER_OF_EXAMS)
        self.number_of_exams_input = QSpinBox()
        self.number_of_exams_input.setRange(0, MAX_VALUE)
        

        self.decay_correction = QCheckBox(labels.APPLY_DECAY_CORRECTION)
        
        self.isotope_halflife_label = QLabel(labels.HALF_LIFE)
        self.isotope_halflife_value = QLineEdit("")
        self.isotope_halflife_value.setReadOnly(True)

        self.biological_decay = QCheckBox(labels.APPLY_BIOLOGICAL_DECAY)
        self.biological_halflife_label = QLabel(labels.HALF_LIFE)
        
        self.biological_halflife_value = QDoubleSpinBox()
        self.biological_halflife_value.setRange(-MAX_VALUE, MAX_VALUE)

     
    def set_callbacks(self):
        super().set_callbacks()
        
        self.duration.valueChanged.connect(self.emit_change)
        self.activity.valueChanged.connect(self.emit_change)
        self.isotope_input.currentTextChanged.connect(self.emit_change)
        self.self_shielding_list.currentTextChanged.connect(self.emit_change)
        self.number_of_exams_input.valueChanged.connect(self.emit_change)
        self.decay_correction.stateChanged.connect(lambda _: self.emit_change())
        self.biological_decay.stateChanged.connect(lambda _: self.emit_change())
        self.biological_halflife_value.valueChanged.connect(self.emit_change)
        
    def clear(self):
        super().clear()
        self.activity.clear()
        self.number_of_exams_input.clear()
        self.decay_correction.setChecked(False)
        self.isotope_halflife_value.clear()
        self.biological_decay.setChecked(False)
        self.biological_halflife_value.clear()
        self.duration.clear()
        
        

    def create_layout_body(self):
        

        row = self.layout.rowCount() + 1
        
        self.layout.addWidget(self.number_of_exams_label, row, 0)
        self.layout.addWidget(self.number_of_exams_input, row, 1, 1, 2)
        
        row += 1
        self.layout.addWidget(self.activity_label, row, 0)
        self.layout.addWidget(self.activity, row, 1, 1, 2)
        row += 1
        self.layout.addWidget(self.isotope_label, row, 0)
        self.layout.addWidget(self.isotope_input, row, 1)
        row += 1
        self.layout.addWidget(self.self_shielding_label, row, 0)
        self.layout.addWidget(self.self_shielding_list, row, 1)
        row += 1
        self.layout.addWidget(self.duration_label, row, 0)
        self.layout.addWidget(self.duration, row, 1)
        row += 1
        self.layout.addWidget(self.decay_correction, row, 0, 1, 2)
        row += 1
        self.layout.addWidget(self.isotope_halflife_label, row, 0)
        self.layout.addWidget(self.isotope_halflife_value, row, 1)
        row += 1
        self.layout.addWidget(self.biological_decay, row, 0, 1, 2)
        row += 1
        self.layout.addWidget(self.biological_halflife_label, row, 0)
        self.layout.addWidget(self.biological_halflife_value, row, 1)
        super().create_layout_body()


class EditCriticalPointsView(EditListViewPositionBase):
             
    def from_dict(self, dct):
        super().from_dict(dct)
        self.disable_connection(event_name=self.EVENT_VIEW_UPDATE)
        self.occupancy_factor_input.setValue(dct[labels.OCCUPANCY_FACTOR])
        self.enable_connection(event_name=self.EVENT_VIEW_UPDATE)
    def to_dict(self):
        dct = super().to_dict()
        dct[labels.OCCUPANCY_FACTOR] = self.occupancy_factor_input.value()
        return dct

    def create_widgets(self):
        super().create_widgets()
    
        self.occupancy_factor_label = QLabel("Occupancy Factor:")
        self.occupancy_factor_input = QDoubleSpinBox()
        self.occupancy_factor_input.setSingleStep(0.05)
        self.occupancy_factor_input.setRange(0, 1)
        self.occupancy_factor_input.setValue(1)
        self.clear()

    def set_callbacks(self):
        super().set_callbacks()
        
        self.occupancy_factor_input.valueChanged.connect(self.emit_change)
        
        
        
    def clear(self):
        super().clear()
        self.name_input.clear()
        self.occupancy_factor_input.clear()
        
    def create_layout_body(self):
        
        row = self.layout.rowCount() + 1

        self.layout.addWidget(self.occupancy_factor_label, row, 0)
        self.layout.addWidget(self.occupancy_factor_input, row, 1)
        super().create_layout_body() 

        
class EditSourceXrayView(EditListViewPositionBase):
    def from_dict(self, dct):
        super().from_dict(dct)
        self.disable_connection(event_name=self.EVENT_VIEW_UPDATE)
        self.dap.setValue(dct[labels.DAP])
        self.set_combo_to_text(self.kvp, dct[labels.KVP])
        self.number_of_exams_input.setValue(dct[labels.NUMBER_OF_EXAMS])
        self.enable_connection(event_name=self.EVENT_VIEW_UPDATE)
    
    def to_dict(self):
        dct = super().to_dict()
        dct[labels.DAP] = self.dap.value()
        dct[labels.KVP] = int(self.kvp.currentText())
        dct[labels.NUMBER_OF_EXAMS] = self.number_of_exams_input.value()
        return dct
    
    @property
    def kvp_labels(self):
        return [str(item.kvp) for item in CONSTANTS.xray]
    
    def create_widgets(self):
        super().create_widgets()
        self.number_of_exams_input = QSpinBox()
        self.number_of_exams_input.setRange(0, MAX_VALUE)
        self.number_of_exams_label = QLabel(labels.NUMBER_OF_EXAMS)
        
        self.kvp = QComboBox()
        self.kvp.addItems(self.kvp_labels) 
        self.kvp_label = QLabel(labels.KVP)

        self.dap = QDoubleSpinBox()
        self.dap.setRange(0, MAX_VALUE)
        self.dap_label = QLabel(labels.DAP)
        
    def set_callbacks(self):
        super().set_callbacks()
        self.number_of_exams_input.valueChanged.connect(self.emit_change)
        self.kvp.currentTextChanged.connect(self.emit_change)
        self.dap.valueChanged.connect(self.emit_change)

    def create_layout_body(self):
        
        row = self.layout.rowCount() + 1
        self.layout.addWidget(self.number_of_exams_label, row, 0)
        self.layout.addWidget(self.number_of_exams_input, row, 1)
        
        row += 1
        self.layout.addWidget(self.kvp_label, row, 0)
        self.layout.addWidget(self.kvp, row, 1)
        row += 1
        self.layout.addWidget(self.dap_label, row, 0)
        self.layout.addWidget(self.dap, row, 1)
        super().create_layout_body() 

    def clear(self):
        super().clear()

        self.number_of_exams_input.clear()
        self.kvp.setCurrentIndex(0)
        self.dap.clear()

class EditSourceCTView(EditListViewPositionBase):
    def from_dict(self, dct):
        super().from_dict(dct)
        self.disable_connection(event_name=self.EVENT_VIEW_UPDATE)
        self.dlp.setValue(dct[labels.DLP])
        self.set_combo_to_text(self.body_part, dct[labels.BODY_PART])
        self.set_combo_to_text(self.kvp, dct[labels.KVP])
        self.number_of_exams_input.setValue(dct[labels.NUMBER_OF_EXAMS])
        self.enable_connection(event_name=self.EVENT_VIEW_UPDATE)
    
    def to_dict(self):
        dct = super().to_dict()
        dct[labels.DLP] = self.dlp.value()
        dct[labels.BODY_PART] = self.body_part.currentText()
        dct[labels.KVP] = int(self.kvp.currentText())
        dct[labels.NUMBER_OF_EXAMS] = self.number_of_exams_input.value()
        return dct
    
    @property
    def kvp_labels(self):
        return [str(item.kvp) for item in CONSTANTS.ct]
    
    def create_widgets(self):
        super().create_widgets()
        self.number_of_exams_input = QSpinBox()
        self.number_of_exams_input.setRange(0, MAX_VALUE)
        self.number_of_exams_label = QLabel(labels.NUMBER_OF_EXAMS)

        self.kvp = QComboBox()
        self.kvp.addItems(self.kvp_labels) 
        self.kvp_label = QLabel(labels.KVP)

        self.body_part = QComboBox()
        self.body_part.addItems(CONSTANTS.body_part_options) 
        self.body_part_label = QLabel(labels.BODY_PART)

        self.dlp = QDoubleSpinBox()
        self.dlp.setRange(0, MAX_VALUE)
        self.dlp_label = QLabel(labels.DLP)

        
    def set_callbacks(self):
        super().set_callbacks()
        self.number_of_exams_input.valueChanged.connect(self.emit_change)
        
        self.kvp.currentTextChanged.connect(self.emit_change)
        self.dlp.valueChanged.connect(self.emit_change)
        
    def create_layout_body(self):
        row = self.layout.rowCount() + 1
        self.layout.addWidget(self.number_of_exams_label, row, 0)
        self.layout.addWidget(self.number_of_exams_input, row, 1)
        row += 1
        self.layout.addWidget(self.kvp_label, row, 0)
        self.layout.addWidget(self.kvp, row, 1)
        row += 1
        self.layout.addWidget(self.body_part_label, row, 0)
        self.layout.addWidget(self.body_part, row, 1)
        row += 1
        self.layout.addWidget(self.dlp_label, row, 0)
        self.layout.addWidget(self.dlp, row, 1)
        
        super().create_layout_body()

    def clear(self):
        super().clear()
        self.number_of_exams_input.clear()
        self.kvp.setCurrentIndex(0)
        self.body_part.setCurrentIndex(0)
        self.dlp.clear()

 
class EditPixelSizeView(EditViewBase):
  
    explanation =\
("The pixel size can be set by hand or by a measurement on the floor plan " 
 "image. Measurement is done by drawing a line between two points for which "
 "the real world distance in cm is known.")


    def create_widgets(self):
        #self.explanation = QLabel(self.explanation.replace('\n', ' '))
        
        
        self.choose_fixed = QRadioButton("Set Fixed")
        
        self.choose_measured = QRadioButton("Measure")

        
        self.measure_button = QPushButton('Measure On Floorplan')
        
        self.physical_distance_label = QLabel("Real world distance [cm]")
        self.physical_distance = QLineEdit()
        
        self.pixel_distance_label = QLabel("Distance [pixels]")
        self.pixel_distance = QLabel("Use Button To Measure")
        
        self.pixel_size_label = QLabel(labels.PIXEL_SIZE_CM)
        self.pixel_size = QLineEdit()
        
        self.confirm_button = QPushButton("Confirm")
        
        self.choose_fixed.toggled.connect(self.radio_button)
        self.choose_measured.toggled.connect(self.radio_button)
        
        
        self.pixel_size_measured_label = QLabel(labels.PIXEL_SIZE_CM)
        self.pixel_size_measured = QLabel()
        self.set_callbacks()
        
    def set_callbacks(self):
        self.physical_distance.textChanged.connect(self.emit_change)

    def radio_button(self):
 
        if self.choose_measured.isChecked():
            self.set_choose_measured()
        elif self.choose_fixed.isChecked():
            self.set_choose_fixed()
            
        
            
            
    def set_choose_fixed(self):
        self.choose_measured.setChecked(False)
        self.choose_fixed.setChecked(True)
        self.measure_button.setEnabled(False)
        self.physical_distance.setEnabled(False)
        self.pixel_size_label.setEnabled(True)
        self.pixel_size.setEnabled(True)
        self.pixel_size_measured.setText('')
        self.pixel_size_measured.setEnabled(False)
        
        

                
   
        
        
    def set_choose_measured(self):
        self.choose_measured.setChecked(True)
        self.choose_fixed.setChecked(False)
        self.measure_button.setEnabled(True)
        self.physical_distance.setEnabled(True)
        self.pixel_size.setEnabled(False)
        self.pixel_size_measured.setEnabled(True)
        self.pixel_size.setEnabled(False)
        
    def create_layout(self):
        
        row = self.layout.rowCount() + 1
        
        #self.layout.addWidget(self.explanation, row, 0, 1, 2)
        
        #row += 1
        
        self.layout.addWidget(self.choose_fixed, row, 0, 1, 2)

        row += 1
        
        self.layout.addWidget(self.pixel_size_label, row, 0)
        self.layout.addWidget(self.pixel_size, row, 1)
        
        row += 1
        
        self.layout.addWidget(self.choose_measured, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.physical_distance_label, row, 0)
        self.layout.addWidget(self.physical_distance, row, 1)
        
        row += 1
        
        self.layout.addWidget(self.pixel_distance_label, row, 0)
        self.layout.addWidget(self.pixel_distance, row, 1)
        
        row += 1
        
        self.layout.addWidget(self.pixel_size_measured_label, row, 0)
        self.layout.addWidget(self.pixel_size_measured, row, 1)
        
        row += 1
        
        self.layout.addWidget(self.measure_button, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.confirm_button, row, 0, 1, 2)

        
        self.set_choose_measured()
        self.setFixedWidth(WIDGET_WIDTH)
class EditOriginView(EditViewBase):
    _position_x_text = "X [cm]:"
    _position_y_text = "Y [cm]:"

  
    explanation =\
("The origin can be set by a mouse click or manual. The origin defines the "
"(0, 0) coordinate. The origin can be updated by fixing the walls to the "
"floorplan by updating the internal coordinates. Or the origin the origin "
"can be updated by keeping the internal coordinates. This will effectively "
"move the walls relative to the floorplan.\n\n"
"For most use cases it is not needed to change the origin.")

    def create_widgets(self):
        # self.explanation = QLabel(self.explanation.replace('\n', ' '))
        # self.explanation.setWordWrap(True)
        
        self.x = QSpinBox()
        self.x.setRange(-MAX_VALUE, MAX_VALUE)
        self.y = QSpinBox()
        self.y.setRange(-MAX_VALUE, MAX_VALUE)
        
        self.position_x_label = QLabel(self._position_x_text)
        self.position_y_label = QLabel(self._position_y_text)
 
        self.measure_button = QPushButton('Select Origin on floorplan')
        
        self.confirm_fixed = QPushButton('Confirm & Fix Walls')
        self.confirm_moving = QPushButton('Confirm & Move Walls')        


        
    def create_layout(self):
        row = self.layout.rowCount() + 1
        
        # self.layout.addWidget(self.explanation, row, 0, 2, 2)
        
        # row += 2

        self.layout.addWidget(self.position_x_label, row, 0)
        self.layout.addWidget(self.x, row, 1)
        
        row += 1
        
        self.layout.addWidget(self.position_y_label, row, 0)
        self.layout.addWidget(self.y, row, 1)
        
        row += 1
        
        self.layout.addWidget(self.measure_button, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.confirm_fixed, row, 0)
        self.layout.addWidget(self.confirm_moving, row, 1)
        self.setFixedWidth(WIDGET_WIDTH)
    

    def set_position(self, coords):
        self.x.setValue(coords[0])
        self.y.setValue(coords[1])  
        
    def get_position(self):
        return [self.x.value(), self.y.value()]
    
    
class EditFloorplanView(EditViewBase):
    explanation =\
"""
Select a bitmap image to draw wall and sources on. 
"""
    def create_widgets(self):
        # self.explanation = QLabel(self.explanation.replace('\n', ' '))
        # self.explanation.setWordWrap(True)
        
        self.image_button   = QPushButton("Select Image")
        self.image_label    = QLabel('Select file...')
        self.keep_geometry = QCheckBox("Keep current pixel size and origin")
  
        
        
        
    def create_layout(self):
        row = self.layout.rowCount() + 1
        
        # self.layout.addWidget(self.explanation, row, 0, 1, 2)
        
        # row += 1
        
        self.layout.addWidget(self.keep_geometry, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.image_button, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.image_label, row, 0, 1, 2)
        self.setFixedWidth(WIDGET_WIDTH)
        
       
            
class NewProjectView(EditViewBase):
   

    def create_widgets(self):

        
        self.image_button = QPushButton("Select Image")
        self.image_label = QLabel('Select file...')
        

        self.choose_empty = QRadioButton("Empty Canvas")
        
        self.choose_image = QRadioButton("Load image")
        
        
        
        self.x = QSpinBox()
        self.x.setRange(-MAX_VALUE, MAX_VALUE)
        self.y = QSpinBox()
        self.y.setRange(-MAX_VALUE, MAX_VALUE)
        
        self.size_x_label = QLabel("Width [cm]")
        self.size_y_label = QLabel("Height [cm]")
        
        self.confirm_button = QPushButton("Confirm")
        
        self.choose_empty.toggled.connect(self.radio_button)
        self.choose_image.toggled.connect(self.radio_button)
        
        

        
        
        
    def create_layout(self):
        row = 0
        
        self.layout.addWidget(self.choose_image, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.image_button, row, 0, 1, 2)
        
        
        row += 1
        
        self.layout.addWidget(self.image_label, row, 0, 1, 2)
        
        row += 1
        
        self.layout.addWidget(self.choose_empty, row, 0)
        
        row += 1
        
        self.layout.addWidget(self.size_x_label, row, 0)
        self.layout.addWidget(self.x, row, 1)
        
        row += 1
        
        self.layout.addWidget(self.size_y_label, row, 0, 1, 2)
        self.layout.addWidget(self.y, row, 1)
        
        row += 1
        
        
        self.layout.addWidget(self.confirm_button, row, 0, 1, 2)
        
        self.set_choose_empty()
        self.setFixedWidth(WIDGET_WIDTH)
    
    def set_choose_image(self):
        if not self.choose_image.isChecked():
            self.choose_image.setChecked(True)
        
        self.x.setEnabled(False)
        self.y.setEnabled(False)
        self.size_x_label.setEnabled(False)
        self.size_y_label.setEnabled(False)
       
        
        self.image_button.setEnabled(True)
        self.image_label.setEnabled(True)

        
    def set_choose_empty(self):
        if not self.choose_empty.isChecked():
            self.choose_empty.setChecked(True)
            
        self.x.setEnabled(True)
        self.y.setEnabled(True)
        self.size_x_label.setEnabled(True)
        self.size_y_label.setEnabled(True)
        
        
        self.image_button.setEnabled(False)
        self.image_label.setEnabled(False)
        
        
    def radio_button(self):
        if self.choose_image.isChecked():
            self.set_choose_image()
        elif self.choose_empty.isChecked():
            self.set_choose_empty()           
    
