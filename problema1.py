
from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

Model = ConcreteModel()

# Data de entrada
numProyectos=8

p=RangeSet(1, numProyectos)

valor={1:2, 2:5, 3:4, 4:2, 5:6, 6:3, 7:1, 8:4}

# Variable de decisión
Model.x = Var(p, domain=Binary)

# Función objetivo
Model.obj = Objective(expr = sum(Model.x[i]*valor[i] for i in p), sense=maximize)

# Restricciones
Model.res1 = Constraint(expr = sum(Model.x[i] for i in p) == 2)

# Especificación del solver
SolverFactory('glpk').solve(Model)

Model.display()

