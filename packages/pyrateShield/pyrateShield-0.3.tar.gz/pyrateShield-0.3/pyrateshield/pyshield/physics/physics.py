import yaml
import os
import pandas as pd
from pyrateshield.pyshield.constants import PHYSICS_CONFIG, ISOTOPES, RADIATION_TYPE, ENERGY_keV, ABUNDANCE, DECAY_CONSTANT
folder = os.path.dirname(__file__)
import math

def load(item):
    full_item = os.path.join(folder, item)
    
    if os.path.splitext(full_item)[1] == '.yml':
        with open(full_item) as file:
            contents = yaml.safe_load(file)
    elif os.path.splitext(full_item)[1] == '.xls':
        contents = pd.read_excel(full_item, sheet_name=None)
    else:
        raise ValueError(item)
        
    
    return contents
                    



physics_file = os.path.join(folder, PHYSICS_CONFIG)



with open(physics_file) as file:
    PHYSICS = yaml.safe_load(file)
    
for key, item in PHYSICS.items():
    PHYSICS[key] = load(item)
    

        
        
def get_isopes():
    LOW_ENERGY_BOUND_KEV = 30 # no buildup available
    LOW_YIELD_BOUND = 1E-4 # Stabin
    photons = ['G', 'G-AN','G-X-K', 'G-X-KA1', 'G-X-KA2', 'G-X-KB', 'G-X-L']
    
    selection = ['F-18', 'Ga-68', 'Ga-67', 'I-123', 'I-131', 'Ho-166', 'Lu-177', 
                 'Tc-99', 'Fr-221', 'Bi-213', 'Ac-225']
    
    table = PHYSICS[ISOTOPES]
    
    table = table[table[RADIATION_TYPE].isin(photons)]
    
    table = table[table[ENERGY_keV] > LOW_ENERGY_BOUND_KEV]
    
    table[ABUNDANCE] = table['Radiation Intensity (%)'] / 100
    
    table = table[table[ABUNDANCE] > LOW_YIELD_BOUND]
    
    tables = []
    for isotope in selection:
        elem, A = isotope.split('-')
        itable = table[table['ELEM'] == elem.upper()]
        itable = itable[itable['A'] == float(A)]
        tables += [itable]
        
    selection_table = pd.concat(tables).reset_index()
    
    #selection_table.to_excel('selection.xlsx')
    
    # deal with metastable states manually
    
    selection_table = pd.read_excel('selection.xlsx')
    
    isotopes = {}
    
    
    def decay_constant(half_life, half_life_units):
        factor = {'NS': 1/(1E9 * 3600),
                  'US': 1/(1E3) * 3600,
                  'MS': 1/(1E3 * 3600),
                  'S': 1/3600,
                  'M': 1/60,
                  'H': 1,
                  'D': 24,
                  'Y': 365 * 24}
        return math.log(2) / (half_life * factor[half_life_units])
    
    
    for item in selection_table.to_dict('records'):
        elem, A = item['ELEM'], item['A']
        if len(elem) > 1:
            elem = elem[0] + elem[1].lower() + elem[2:]
        
        isotope = elem + '-' + str(A)
        print(isotope)
        
        if isotope not in isotopes:
            dc = decay_constant(item['Half-Life'], item['Half-life Units'])
            isotopes[isotope] = {ENERGY_keV: [], ABUNDANCE:[],
                                 DECAY_CONSTANT: dc}
        
        isotopes[isotope][ENERGY_keV] += [item[ENERGY_keV]]
        isotopes[isotope][ABUNDANCE] += [item[ABUNDANCE]]
        
        
        
        
        
        
    
    

    
    
    
