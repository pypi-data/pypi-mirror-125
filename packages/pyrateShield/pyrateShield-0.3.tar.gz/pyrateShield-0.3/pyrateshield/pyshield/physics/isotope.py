# -*- coding: utf-8 -*-
"""
Isotope calculations for pyshield package

Last Updated 05-02-2016
"""
import numpy as np
from scipy.interpolate import interp2d, RectBivariateSpline
import scipy.interpolate as si
from pyrateshield.pyshield import PHYSICS
from pyrateshield.pyshield.constants import (ISOTOPES, BUILDUP_FACTORS, MATERIALS,
                                ATTENUATION, DENSITY, ENERGY_MeV,
                                MASS_ATTENUATION, MFP)

DEBUG = False

ISOTOPES = PHYSICS.get(ISOTOPES)
BUILDUP =  PHYSICS.get(BUILDUP_FACTORS)
MATERIALS = PHYSICS.get(MATERIALS)
ATTENUATION = PHYSICS.get(ATTENUATION)

make_list = lambda item: item if isinstance(item, (list, tuple)) else [item]


def attenuation(energy_keV, material, thickness):
    """
    Attenuation for a given energy through a matrial with thickness.
    Args:
        energy_keV: the energy of  the photon in keV
        material: name of the material
        thickness: thickness of the material
    Returns:
        a:  attenation factor (float)
    """
    thickness = np.asarray(thickness)
    
    a = np.exp(-u_linear(energy_keV, material) * thickness)

    #msg = 'Material: %s Thickness: %s Energy: %s Attenuation %s'
    # if DEBUG:
    #     ps.logger.debug(msg, material, thickness, energy_keV, attenuation)
    return a


def u_linear(energy_keV, material):
    """
    Args:
      energy_keV: the energy of  the photon in keV
      material: name of the material
    Returns:
      Linear attenuation coefficient in [cm^-1]
    Raises:
      NameError if material is not defined in the pyshield recources
    """

    #msg = 'Interpolated Mass attenuation coefficient {0}'
    mu_p_i = u_mass(energy_keV, material)
    # if DEBUG:
    #     ps.logger.debug(msg.format(mu_p_i))

    p = MATERIALS[material][DENSITY]

    return mu_p_i * p

def u_mass(energy_keV, material):
    try:
        table = ATTENUATION[material]
    except NameError:
        raise NameError(material + ' not in attenuation table!')

    energies = np.array(table[ENERGY_MeV])

    mu_p = np.array(table[MASS_ATTENUATION])

    interp_fcn = si.interp1d(energies, mu_p)

    mu_p_i = interp_fcn(energy_keV / 1e3)

    return mu_p_i

def interp2d_pairs(*args,**kwargs):
    # https://stackoverflow.com/questions/47087109/evaluate-the-output-from-scipy-2d-interpolation-along-a-curve
    """ Same interface as interp2d but the returned interpolant will evaluate its inputs as pairs of values.
    """
    # Internal function, that evaluates pairs of values, output has the same shape as input
    def interpolant(x,y,f):
        x,y = np.asarray(x), np.asarray(y)
        return (si.dfitpack.bispeu(f.tck[0], f.tck[1], f.tck[2], f.tck[3], f.tck[4], x.ravel(), y.ravel())[0]).reshape(x.shape)
    # Wrapping the scipy interp2 function to call out interpolant instead
    return lambda x,y: interpolant(x,y,si.interp2d(*args,**kwargs))

    # # Create the interpolant (same interface as interp2d)
    # f = interp2d_pairs(X,Y,Z,kind='cubic')
    # # Evaluate the interpolant on each pairs of x and y values
    # z=f(x,y)


        
        
            
            
            
    
    
    
def buildup(energy_keV, material, thickness):
    """
    Buildup for a given energy through a matrial with thickness.
    Args:
        energy_keV: the energy of  the photon in keV
        material: name of the material
        thickness: thickness of the material
    Returns:
        b:  buildup factor (float)
    """
    # if thickness == 0:
    #     return 1
    
    if isinstance(thickness, (float, int)) or thickness.ndim == 0:
        thickness = [float(thickness)]
    
    thickness = np.asarray(thickness)
    
    index = thickness > 0

    try:
        table = BUILDUP[material]
    except NameError:
        raise NameError(material + ' not in buildup table!')
    
    n_mfp       = np.asarray(table[MFP], 'float64')
    table       = table.drop(MFP, axis=1)
    
    factors     = np.asarray(table, 'float64')
    energies    = np.asarray(table.columns, dtype='float64')
    
    n_mfpi      = number_mean_free_path(energy_keV, 
                                      material, 
                                      thickness[index])
    # Z = factors
    # X = np.tile(energies, (factors.shape[0], 1))
    # Y = np.tile(n_mfp, (factors.shape[1], 1)).transpose()
    
    #interp_func = interp2d_pairs(X, Y, Z, kind='linear')
    #interp_func2d = RectBivariateSpline(energies, n_mfp, factors.T)
    interp_func2d = interp2d(energies, n_mfp, factors)
    
    
    interp_func1d = lambda ii: interp_func2d(energy_keV/1000, ii)
    
    n_mfpi    = number_mean_free_path(energy_keV, material, thickness[index])#[index])
    
    buildup_values = np.asarray([float(interp_func1d(ii)) for ii in n_mfpi])
    
    buildup = np.ones(len(thickness))
    buildup[index] = buildup_values.flatten()
    
    
    
    
    # 
    # xi      = np.ones(yi.shape[0]) * energy_keV/1000
    
    
    
    
    # # if DEBUG:
    # #     ps.logger.debug('Energies %s\nMean Free Path %s\nFactors\n',
    # #                     str(energies), str(n_mfp), str(factors))
    
    # #interp_func = interp2d(energies, n_mfp, factors, kind='linear')
    # zi     = interp_func(xi, yi)
    # zi2    = [float(interp_func2(energy_keV/1000, ii)) for ii in yi]
    
    
    
    #buildup = np.ones(thickness.shape).flatten()
    #buildup[index.flatten()] = factor.flatten()
    # if DEBUG:
    #     ps.logger.debug('Buildup factor:  ' + str(factor))
    #     ps.logger.debug('Material: '        + str(material))
    #     ps.logger.debug('Thickness: '       + str(thickness))
    #     ps.logger.debug('Energy: '          + str(energy_MeV))

    return buildup


def number_mean_free_path(energy_keV, material, thickness):
    """"
    Args:
      energy_keV: the energy of  the photon in keV
      material: name of the material
      thickness: thickness of the material
    Retuns:
      number of mean free paths for a given photon enery, material and
      material thicknesss
    """
    
    # 1 mean free path = 1 / u_lin
    

    return thickness * u_linear(energy_keV, material)


if __name__ == "__main__":
    isotope = 'F-18'
    
    a = attenuation(511, 'Water', 25)
    b = buildup(511, 'Water', 25)










