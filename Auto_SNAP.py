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

# Path to the data
s1_path = 'C:/Users/jales/Desktop/S1A.zip'

# Reading the data
product = ProductIO.readProduct(s1_path)

x = 0
y = 9928
w = 25580
h = 16846

HashMap = jpy.get_type('java.util.HashMap')
GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()

parameters = HashMap()
parameters.put('copyMetadata', True)
parameters.put('region', "%s,%s,%s,%s" % (x, y, w, h))
subset = GPF.createProduct('Subset', parameters, product)

# Getting the width of the scene
width = subset.getSceneRasterWidth()
print('Width: {} px'.format(width))

# Getting the height of the scene
height = subset.getSceneRasterHeight()
print('Height: {} px'.format(height))

# Getting the dataset name
name = subset.getName()
print('Name: {}'.format(name))

# Getting the band names in the imagery
band_names = subset.getBandNames()
print('Band names: {}'.format(', '.join(band_names)))

# ------------------------------------------------------------------------------------------------------

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

plotBand(subset, 'Intensity_VH')

# --------------------------------------------------------------

# Orthorectification

#parameters = HashMap()

#GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()

#parameters.put('orbitType', "Sentinel Precise (Auto Download)')
#parameters.put('polyDegree', '3')
#parameters.put('continueOnFail', 'false')

#apply_orbit_file = GPF.createProduct('Apply-Orbit-File', parameters, data)

# ---------------------------------------------------------------