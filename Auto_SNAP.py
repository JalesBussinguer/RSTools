# This is a Python script for process Sentinel-1 imagery for
# water masks extraction

# Imports

# Basic Libraries

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import os

# Snappy modules

from snappy import Product
from snappy import ProductIO
from snappy import ProductUtils
from snappy import WKTReader
from snappy import HashMap
from snappy import GPF
from snappy import jpy

# ------------------------------------------------------------------------------------

# Orthorectification

def ApplyOrbitFile(data):

    parameters = HashMap()

    Operator_load = GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()

    parameters.put('orbitType', 'Sentinel Precise (Auto Download)')
    parameters.put('polyDegree', '3')
    parameters.put('continueOnFail', 'false')

    apply_orbit_file = Operator_load.createProduct('Apply-Orbit-File', parameters, data)

    return apply_orbit_file

# Subset the image

def Subset(data, x, y, w, h):

    HashMap = jpy.get_type('java.util.HashMap')
    Operator_load = GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()

    parameters = HashMap()
    parameters.put('copyMetadata', True)
    parameters.put('region', "%s,%s,%s,%s" % (x, y, w, h))
    subset = Operator_load.createProduct('Subset', parameters, data)

    return subset

# Getting information from the dataset

def Information(data):

    # Getting the width of the scene
    width = data.getSceneRasterWidth()
    print('Width: {} px'.format(width))

    # Getting the height of the scene
    height = data.getSceneRasterHeight()
    print('Height: {} px'.format(height))

    # Getting the dataset name
    name = data.getName()
    print('Name: {}'.format(name))

    # Getting the band names in the imagery
    band_names = data.getBandNames()
    print('Band names: {}'.format(', '.join(band_names)))

    return width, height, name, band_names

# ploting the image

def plotBand(data, banda):
    
    w = data.getSceneRasterWidth()
    h = data.getSceneRasterHeight()
    band = data.getBand(banda)
    print(w, h)

    band_data = np.zeros(w * h, np.float32)
    band.readPixels(0, 0, w, h, band_data)

    band_data.shape = h, w

    width = 12
    height = 12

    plt.figure(figsize=(width, height))
    imgplot = plt.imshow(band_data, cmap=plt.cm.binary)

    return imgplot

# ------------------------------------------------------------------------------------------------------

# Path to the data
s1_path = 'C:/Users/jales/Desktop/S1A.zip'

# Reading the data
product = ProductIO.readProduct(s1_path)

# ------------------------------------------------------------------------------------------------------

S1_Orb = ApplyOrbitFile(product)

S1_Orb_Subset = Subset(S1_Orb, 0, 9928, 25580, 16846)

Information(S1_Orb_Subset)

# ------------------------------------------------------------------------------------------------------

#plotBand(S1_Orb_Subset, 'Intensity_VH')

# ------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------