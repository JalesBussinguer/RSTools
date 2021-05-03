# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 12:00:24 2021

@author: jales
"""

# Programa que calcula a cota em pontos intermediários a partir de um levantamento topográfico previamente realizado

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import OrderedDict

# Pergunta

arquivo_ref=str(input('Informe o arquivo de referência: ', ))


arquivo_esp=str(input('Informe os dados dos espaçamentos: ', ))
print()

# Leitura do arquivo contendo os dados de entrada

referencia = pd.read_csv(arquivo_ref, sep=',')

cota = referencia['cota']
distancia = referencia['distancia']

print(referencia)
print()

# Criação da lista com os valores de espaçamentos para a interpolação

medicoes = pd.read_csv(arquivo_esp, sep=',')

lista_esp = medicoes['espacamento'].tolist()
print()

print(f'espaçamentos para interpolação [m] = {(sorted(lista_esp))}')
print()

# Criação de um dicionário das coordenadas

dict_coords = {}

# Cálculo das cotas por interpolação linear do tipo y = ax + b

for i in lista_esp:
    if 0 < i < 100:
        y = 3.82 * i + 382
    elif 101 < i < 200:
        y = 0.3 * i + 736
    elif 201 < i < 300:
        y = -6.09 * i + 2014
    elif 301 < i < 400:
        y = 3.03 * i - 722
    elif 401 < i < 500:
        y = -0.44 * i + 666
    elif 501 < i < 600:
        y = 2.01 * i - 559
    elif 601 < i < 700:
        y = 0.63 * i + 269
    elif 701 < i < 800:
        y = 0.45 * i + 395
    elif 801 < i < 900:
        y = -4.78 * i + 4579
    elif 901 < i < 1000:
        y = 2.03 * i - 1550
    else:
        print('dados fora do domínio')
        
# População do dicionário com as coordenadas
    dict_coords.update({i:y})

# Organização do dicionário em ordem crescente
dict_final = OrderedDict(sorted(dict_coords.items()))

# Preparação do gráfico

plt.figure(figsize=(9,7))
plt.title('Distância X Cota')
plt.xlabel('Distância [m]')
plt.xticks(np.arange(0, 1100, step=100))
plt.ylabel('Cota [m]')
plt.yticks(np.arange(0, 900, step=50))

# Plotagem do levantamento topográfico (background)
plt.plot(distancia, cota, marker='o', color='blue', label='Levantamento Topográfico')
plt.legend(loc='lower right')

# Plotagem dos dados calculados
x = list(dict_final.keys())
y = list(dict_final.values())

plt.plot(x, y, linestyle='none', marker='o', color='red', label='Cotas Interpoladas')
plt.legend(loc='lower right')

#for key, value in dict_final.items():
#    plt.annotate(f'({key}, {round(value, 2)})', xy=(key, value), xytext=(7, 7), textcoords='offset points', xycoords='data')

# Exportação dos dados

df_resultados = pd.DataFrame(dict_final.items(), columns=['Distancia', 'Cota'])
print(df_resultados)

# Caminho onde o arquivo será salvo

path=str(input('Digite o caminho onde o arquivo será salvo:', ))

df_resultados.to_csv(f'{path}\cotas_interpoladas.csv', index=False, header=True, float_format='%.3f')
