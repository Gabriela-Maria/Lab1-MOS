
from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

Model = ConcreteModel()

# Data de entrada
numTrabajadores=3
numTrabajos=5


T=RangeSet(1, numTrabajadores) #trabajadores
A=RangeSet(1,numTrabajos) # trabajos
 
horasMaximas ={1:8, 2:10, 3:6} #disponibilidad por trabajador 

ganancia = {1:50, 2:60, 3:40, 4:70, 5:30} #ganancia por trabajo
tiempo = {1:4, 2:5, 3:3, 4:6, 5:2} #tiempo requerido por trabajo


# Variable de decisión
Model.x = Var(T, A, domain=Binary)

# Función objetivo
Model.obj = Objective(expr = sum(Model.x[i, j]*ganancia[j] for i in T for j in A), sense=maximize)

# Restricciones
Model.tiempoLimite = ConstraintList()
for i in T:
    Model.tiempoLimite.add(expr = sum(Model.x[i,j]*tiempo[j] for j in A) <= horasMaximas[i])

Model.trabajo = ConstraintList()
for j in A:
    Model.trabajo.add(expr = sum(Model.x[i,j] for i in T) <= 1)

Model.trabajador = Constraint(expr=Model.x[2,1]==0)
Model.trabajador = Constraint(expr=Model.x[3,1]==0)
Model.trabajador = Constraint(expr=Model.x[2,3]==0)

# Especificación del solver
SolverFactory('glpk').solve(Model)

Model.display()

