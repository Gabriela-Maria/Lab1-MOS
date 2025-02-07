
from __future__ import division
from pyomo.environ import *

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

