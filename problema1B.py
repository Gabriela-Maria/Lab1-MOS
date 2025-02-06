
from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

Model = ConcreteModel()

# Data de entrada
numTareas=11
numEquipo=4

capacidad = 13 #capacidad por desarrollador

T=RangeSet(1, numTareas)
E=RangeSet(1,numEquipo)
 
puntosHistoria ={1:5, 2:3, 3:13, 4:1, 5:21, 6:2, 7:2, 8:5, 9:8, 10:13, 11:21}

prioridad = {1:7, 2:5, 3:6, 4:3, 5:1, 6:4, 7:6, 8:6, 9:2, 10:7, 11:6}

# Variable de decisión
Model.x = Var(T, E, domain=Binary)

# Función objetivo
Model.obj = Objective(expr = sum(Model.x[i, j]*prioridad[i] for i in T for j in E), sense=maximize)

# Restricciones
#Capacidad de desarrollador no se supere
Model.trabajosIndividual = ConstraintList()
for j in E:
    Model.trabajosIndividual.add(expr = sum(Model.x[i,j]*puntosHistoria[i] for i in T) <= capacidad)

# Cada trabajo se realiza solo una vez


# Especificación del solver
SolverFactory('glpk').solve(Model)

Model.display()

