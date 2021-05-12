# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 18:09:27 2021

@author: Jales de Freitas Bussinguer
"""

# Importação das bibliotecas

import rasterio as rst
import matplotlib.pyplot as plt
import numpy as np
import glob
import subprocess

# Função que retorna os metadados das imagens brutas

def relatorio_metadados(banda):
  print()
  
  if banda == red:
      print ('Metadados da banda do vermelho:')
  elif banda == nir:
      print('Metadados da banda do Infravermelho Próximo:')
  else:
      pass
  
  print(f'O nome do arquivo é: {banda.name}')
  print()
  print(f'As dimensões são: {banda.width} x {banda.height} pixels;')
  print()
  print(f'O tipo de dado é: {banda.dtypes}')
  print()
  print(f'O sistema de referência de coordenadas é: {banda.crs}')
  print()
  print(f'As coordenadas de canto são: {banda.bounds}')
  print()

# Pasta que contém os dados das cenas (root)

data_path = "data/"

# Lista de arquivos com a extensão .TIF no diretório de dados

lista_bandas = glob.glob(data_path + '*.TIF')
print()
print('Banda do vermelho:', lista_bandas[0])
print()
print('Banda do NIR:', lista_bandas[1])

# Instanciando as bandas

with rst.open(lista_bandas[0], driver='GTiff', mode='r') as red:
    RED = red.read(1)

with rst.open(lista_bandas[1], driver='GTiff', mode='r') as nir:
    NIR = nir.read(1)

# Chamando o relatório de metadados das imagens brutas

relatorio_metadados(red)

relatorio_metadados(nir)

# Permitir divisão por zero

np.seterr(divide='ignore', invalid='ignore')

# Cálculo do NDVI

NDVI = (NIR.astype(np.float32) - RED.astype(np.float32)) / (NIR + RED)

# Plotagem do NDVI (apenas uma amostra da cena)

ndvi_subset = NDVI[2600:4000, 2600:4500] # Definição da região de visualização - zoom (amostra da imagem)

fig = plt.figure(figsize=(9,7))
plt.title('Landsat 8 - NDVI (Região de Brasília/DF)') # Título
image = plt.imshow(ndvi_subset, cmap='RdYlGn', vmin=0.0, vmax=1.0, aspect='equal')
fig.colorbar(image)
plt.show()

# Exportação da imagem do NDVI

# Atualização dos metadados do arquivo do NDVI

metadados = red.meta

metadados.update(
    dtype=rst.float32,
    count = 1)

with rst.open('data/NDVI.tif', 'w', **metadados) as dst:
        dst.write_band(1, NDVI.astype(rst.float32))
print()
print('NDVI salvo com sucesso!')
print()

# Relatorio de metadados do NDVI

print('Relatório de metadados do NDVI:')
print()
print(subprocess.check_output("gdalinfo " + data_path + 'NDVI.tif', shell=True, encoding='UTF-8'))