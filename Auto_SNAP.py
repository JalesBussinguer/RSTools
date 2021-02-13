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
"""
Funções para executar os operadores do SNAP

"""

# Ortorretificação (Orthorectification) - Apply Orbit File
# Função que faz a correção do posicionamento de órbita da imagem

def ApplyOrbitFile(data):

    parameters = HashMap()

    GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()

    parameters.put('orbitType', 'Sentinel Precise (Auto Download)')
    parameters.put('polyDegree', '3')
    parameters.put('continueOnFail', 'false')

    apply_orbit_file = GPF.createProduct('Apply-Orbit-File', parameters, data)

    return apply_orbit_file

# Recorte - Subset
# Função que faz o recorte de uma imagem

def Subset(data, x, y, w, h):

    HashMap = jpy.get_type('java.util.HashMap')
    GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()

    parameters = HashMap()
    parameters.put('copyMetadata', True)
    parameters.put('region', "%s,%s,%s,%s" % (x, y, w, h))
    subset = GPF.createProduct('Subset', parameters, data)

    return subset

# Informações - Information
# Função que retorna informações básicas da imagem como o número de pixels em X e Y, o nome da imagem e das bandas

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

# Plotagem - Plotting
# Função que plota a imagem em um gráfico

def plotBand(data, banda, vmin, vmax):
    
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
    imgplot = plt.imshow(band_data, cmap='binary', vmin=vmin, vmax=vmax)

    return imgplot

# Calibração Radiométrica - Radiometric Calibration
# Função que aplica uma correção radiométrica na imagem, transformando os números digitais dos pixels em valroes com significado físico

def Calibration(data, band, pol):
    
    parameters = HashMap()

    parameters.put('outputSigmaBand', True)
    parameters.put('sourceBands', band)
    parameters.put('selectedPolarisations', pol)
    parameters.put('outputImageScaleInDb', False)

    Sigma0 = GPF.createProduct('Calibration', parameters, data)

    return Sigma0

# Filtragem Speckle - Speckle Filtering
# Função que aplica um filtro para a redução de speckle na imagem

def SpeckleFilter(data, filter, filterSizeX, filterSizeY):

    X = str(filterSizeX)
    Y = str(filterSizeY)

    parameters = HashMap()

    parameters.put('sourceBands', data)
    parameters.put('filter', filter)
    parameters.put('filterSizeX', X)
    parameters.put('filterSizeY', Y)
    parameters.put('dampingFactor', '2')
    parameters.put('estimateENL', 'true')
    parameters.put('enl', '1.0')
    parameters.put('numLooksStr', '1')
    parameters.put('targetWindowSizeStr', '3x3')
    parameters.put('sigmaStr', '0.9')
    parameters.put('anSize', '50')

    speckle_filter = GPF.createProduct('Speckle-Filter', parameters, data)

    return speckle_filter


# Correção Geométrica (Range Doppler Terrain Correction)
# Função que ...

def Terrain_Correction(data):

    parameters = HashMap()

    parameters.put('demName', 'SRTM 3Sec (Auto Download)')
    parameters.put('demResamplingMethod', 'BILINEAR_INTERPOLATION')
    parameters.put('imgResamplingMethod', 'BILINEAR_INTERPOLATION')
    parameters.put('pixelSpacingInMeter', 10.0)
    parameters.put('sourceBands', data)

    terrain_corrected = GPF.createProduct('Terrain-Correction', parameters, data)

    return terrain_corrected

# Conversão para decibel (LinearToFromdB)
# 

def Convert_to_dB(data):
    
    print('Converting to dB...')

    parameters = HashMap()

    parameters.put('sourceBands', data)

    converted = GPF.createProduct('LinearToFromdB', parameters, data)

    return converted

# Função que reo

def listParams(operator_name):

    GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
    
    op_spi = GPF.getDefaultInstance().getOperatorSpiRegistry().getOperatorSpi(operator_name)

    print('Operator name:', op_spi.getOperatorDescriptor().getName())
    print('Operator alias:', op_spi.getOperatorDescriptor().getAlias())

    param_desc = op_spi.getOperatorDescriptor().getParameterDescriptors()

    for param in param_desc:
        print(param.getName(), 'or', param.getAlias())
        
# ------------------------------------------------------------------------------------------------------

# Path to the data
s1_path = 'C:/Users/jales/Desktop/S1A.zip'

# Reading the data
product = ProductIO.readProduct(s1_path)

# ------------------------------------------------------------------------------------------------------

Information(product)

S1_Orb = ApplyOrbitFile(product)

S1_Orb_Subset = Subset(S1_Orb, 0, 9928, 25580, 16846)

Information(S1_Orb_Subset)

listParams('Terrain-Correction')

# ------------------------------------------------------------------------------------------------------

#plotBand(S1_Orb_Subset, 'Intensity_VH')

# ------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------