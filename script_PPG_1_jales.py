# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 12:00:24 2021

@author: jales
"""

# Programa que calcula a cota em pontos intermediários a outros com cotas previamente medidas

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Leitura do arquivo contendo os dados de entrada

medicoes = pd.read_csv('dados_cotas.csv', sep=',')

marco = medicoes['marco']
cota = medicoes['cota']
distancia = medicoes['distancia']

# Plotagem inicial dos dados (visualização primária)

plt.figure(figsize=(9,7))
plt.title('Distância X Cota')
plt.xlabel('Distância [m]')
plt.xticks(np.arange(0, 1100, step=100))
plt.ylabel('Cota [m]')
plt.yticks(np.arange(0, 900, step=50))

plt.plot(distancia, cota)

# Entrada

print('Insira a distância da medição:')

x = float(input())

print(f'x =', x)

#for i in len(dados_entrada):
    
if 0 < x < 100:
    y = 3.82 * x + 382
    print(y)
elif 101 < x < 200:
    y = 0.3 * x + 736
    print(y)
elif 201 < x < 300:
    y = -6.09 * x + 2014
    print(y)
elif 301 < x < 400:
    y = 3.03 * x - 722
    print(y)
elif 401 < x < 500:
    y = -0.44 * x + 666
    print(y)
elif 501 < x < 600:
    y = 2.01 * x - 559
    print(y)
elif 601 < x < 700:
    y = 0.63 * x + 269
    print(y)
elif 701 < x < 800:
    y = 0.45 * x + 395
    print(y)
elif 801 < x < 900:
    y = -4.78 * x + 4579
    print(y)
elif 901 < x < 1000:
    y = 2.03 * x - 1550
    print(y)
else:
    print('dados fora do domínio')