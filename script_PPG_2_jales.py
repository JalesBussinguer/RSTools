# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 18:09:27 2021

@author: Jales Bussinguer
"""

# Importação das bibliotecas

import rasterio as rst
from rasterio import plot

# Leitura dos arquivos rasters que compõem a imagem

B_azul = rst.open('C:/Users/jales/Desktop/S2_PPG/Banda_2_azul.jp2', driver='JP2OpenJPEG', mode='r')
B_verde = rst.open('C:/Users/jales/Desktop/S2_PPG/Banda_3_verde.jp2', driver='JP2OpenJPEG', mode='r')
B_vermelho = rst.open('C:/Users/jales/Desktop/S2_PPG/Banda_4_vermelho.jp2', driver='JP2OpenJPEG', mode='r')
B_NIR = rst.open('C:/Users/jales/Desktop/S2_PPG/Banda_8_NIR.jp2', driver='JP2OpenJPEG', mode='r')

# Função que retorna os metadados das bandas

def relatorio_metadados(banda):
  
  print('Buscando os metadados...')
  print('')
  print('')
  print(f'O nome do arquivo é: {banda.name}')
  print('')
  print(f'As dimensões são: {banda.width} x {banda.height} pixels;')
  print('')
  print(f'O tipo de dado é: {banda.dtypes}')
  print('')
  print(f'O sistema de referência de coordenadas é: {banda.crs}')
  print('')
  print(f'As coordenadas de canto são: {banda.bounds}')
  print('')
  print('')
  
  # Plotagem da imagem da banda
  
  print('Plotando a imagem...')
  print('')
  if banda == B_azul:
    plot.show(banda, cmap='Blues', title='Banda do azul')
  elif banda == B_verde:
    plot.show(banda, cmap='Greens', title='Banda do verde')
  elif banda == B_vermelho:
    plot.show(banda, cmap='Reds', title='Banda do vermelho')
  elif banda == B_NIR:
    plot.show(banda, cmap='Oranges', title='Banda do infravermelho próximo')
  else:
    pass
  print('Imagem plotada com sucesso!')
  print('')
    
  # Plotagem do histograma

  print('Plotando o histograma...')
  print('')
  if banda == B_azul:
    plot.show_hist(banda, bins=100, lw=0.0, alpha=0.5, title='Histograma - Banda do Azul')
  elif banda == B_verde:
    plot.show_hist(banda, bins=100, lw=0.0, alpha=0.5, title='Histograma - Banda do Verde')
  elif banda == B_vermelho:
    plot.show_hist(banda, bins=100, lw=0.0, alpha=0.5, title='Histograma - Banda do Vermelho')
  elif banda == B_NIR:
    plot.show_hist(banda, bins=100, lw=0.0, alpha=0.5, title='Histograma - Banda do Infravermelho Próximo')
  else:
    pass
  print('Histograma plotado com sucesso!')
  print('')

  return

# Relatório de metadados da banda do azul
relatorio_metadados(B_azul)

# Relatório de metadados da banda do verde
relatorio_metadados(B_verde)

# Relatório de metadados da banda do vermelho
relatorio_metadados(B_vermelho)

# Relatório de metadados da banda do infravermelho próximo
relatorio_metadados(B_NIR)