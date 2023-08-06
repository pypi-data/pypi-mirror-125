NAME = "Name"
KVP = "kVp"

### Constants file


CRITICAL_POINT_DOSE_CORRECTED = 'Dose corrected for occupancy [mSv]'
CRITICAL_POINT_DOSE = 'Dose [mSv]'


                             
WALLS_AND_SHIELDING = "Walls && Shieldings"
SOURCES_NM_CT_XRAY = "Sources NM, CT, XRAY"
PROJECT = 'Project'


PYSHIELD = 'PyShield'
RADTRACER = 'Radtracer'


LOAD_SAVE = "Load/Save"
PREFERENCES = "Preferences"
CRITICAL_POINT_REPORT_VIEW = "Critical Point Report"
CANVAS = "Canvas"

ENABLED = 'Enabled'
LOCKED = 'Locked'

# Materials
MATERIALS = "Materials"
MATERIAL = 'Material'
DENSITY = "Density"
THICKNESS = "Thickness [cm]"

EMPTY_MATERIAL = 'None'
EMPTY_SHIELDING = 'None'

# Isotopes
ISOTOPES = "Isotopes"
HALF_LIFE = "Half life"
SELF_SHIELDING_OPTIONS = "Self shielding options"
BODY_PART_OPTIONS = "Body part options"

# Archer parameters
CT_PARAMETERS = "CT parameters"
XRAY_PARAMETERS = "Xray parameters"
ARCHER = "Archer"
DCC = "DCC"
DCC_DLP = "uSv/m^2 per mGycm"
DCC_DAP = "uSv/m^2 per Gycm2"
# 


### Model file
ENGINE = "Engine"
RADTRACER = "Radtracer"
PYSHIELD = "pyShield"

# Floor plan
FLOORPLAN = "Floor plan"
FILENAME = "Filename"
PIXEL_SIZE_CM = "Pixel size [cm]"
ORIGIN_CM = "Origin [cm]"
PIXEL_SIZE_METHOD = 'Pixel size method'
FIXED = 'fixed' # pixel size set by hand
MEASURED = 'measured' # measured form floor plan
REAL_WORLD_DISTANCE_CM = 'Real world distance [cm]' # distance set in gui
VERTICES_PIXELS = 'vertices [pixels]'

# Dose map
DOSEMAP = "Dose map"
GEOMETRY = "Geometry"
GRID_MATRIX_SIZE = "Grid matrix size"
EXTENT = "Extent [cm]"

# Model
CRITICAL_POINTS = "Critical points"
SHIELDINGS = "Shieldings"
WALLS = "Walls"
SOURCES_CT = 'Sources CT'
SOURCES_NM = 'Sources NM'
SOURCES_XRAY = 'Sources Xray'


### General
POSITION = "Position"

SELECTED_ENGINE = 'Selected Engine'
    
### Shielding
COLOR = "Color"
LINEWIDTH = "Linewidth [pt]"
MATERIAL_NAME = "Material name"
MATERIAL_THICKNESS = "Thickness [cm]"

### Wall
SHIELDING = "Shielding"
VERTICES = "Vertices"

### Critical point
OCCUPANCY_FACTOR = "Occupancy factor"

### Sources    
NUMBER_OF_EXAMS = "Number of exams"

# Nuclear
ISOTOPE = "Isotope"
ACTIVITY = "Activity [MBq]"
DURATION = "Duration [h]"
SELF_SHIELDING = "Self shielding"    
APPLY_DECAY_CORRECTION = "Apply decay correction"
BIOLOGICAL_HALFLIFE = "Biological half-life [h]"
APPLY_BIOLOGICAL_DECAY = "Apply biological decay"

# XRAY / CT
DAP = "DAP [Gycm2]"
DLP = "DLP [mGycm]"
BODY_PART = "Body part"


NEW_PROJECT = 'New Project'



MODEL_ITEMS = [SOURCES_CT, SOURCES_NM, SOURCES_XRAY, WALLS, SHIELDINGS,
               CRITICAL_POINTS]

SOURCES = [SOURCES_CT, SOURCES_NM, SOURCES_XRAY]




