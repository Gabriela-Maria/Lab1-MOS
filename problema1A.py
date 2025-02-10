
from __future__ import division
from pyomo.environ import *
import matplotlib.pyplot as plt

from pyomo.opt import SolverFactory

Model = ConcreteModel()

# Data de entrada
numTareas=11
capacidad = 52

# Conjuntos
T=RangeSet(1, numTareas)

# Parámetros
puntosHistoria ={1:5, 2:3, 3:13, 4:1, 5:21, 6:2, 7:2, 8:5, 9:8, 10:13, 11:21}

prioridad = {1:7, 2:5, 3:6, 4:3, 5:1, 6:4, 7:6, 8:6, 9:2, 10:7, 11:6}

# Variable de decisión
Model.x = Var(T, domain=Binary)

# Función objetivo
Model.obj = Objective(expr = sum(Model.x[i]*prioridad[i] for i in T), sense=maximize)

# Restricciones
# no se puede exceder la capacidad de 52
Model.rest1 = Constraint(expr = sum(Model.x[i]*puntosHistoria[i] for i in T) <= capacidad)

# Especificación del solver
SolverFactory('glpk').solve(Model)

Model.display()

#tareas seleccionadas por todos los desarrolladores
tareas_seleccionadas = [i for i in range(1, numTareas+1) if Model.x[i]() == 1]

puntos_historia_seleccionados = [puntosHistoria[i] for i in tareas_seleccionadas]
total_puntos_historia = sum(puntos_historia_seleccionados)

#grafico
plt.figure(figsize=(10, 6))
plt.bar(tareas_seleccionadas, puntos_historia_seleccionados, color='skyblue', edgecolor='black')

#titulos
plt.xlabel('Tareas Seleccionadas')
plt.ylabel('Puntos de Historia')
plt.title('Tareas Seleccionadas en la Parte A')
plt.xticks(tareas_seleccionadas)

for i, v in enumerate(puntos_historia_seleccionados):
    plt.text(tareas_seleccionadas[i], v + 0.5, str(v), ha='center', fontsize=12)

plt.text(0.5, -0.1, f'Total de puntos de historia: {total_puntos_historia}', 
         ha='center', va='top', transform=plt.gca().transAxes, fontsize=14, fontweight='bold')

plt.show()