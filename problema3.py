
from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

Model = ConcreteModel()

# Data de entrada
numRecursos=5
numAviones=3

capacidad = 13 #capacidad por desarrollador

R=RangeSet(1, numRecursos)
A=RangeSet(1,numAviones)
 
recursos = {
    1: {"valor": 50, "peso": 15, "volumen": 8},
    2: {"valor": 100, "peso": 5, "volumen": 2},
    3: {"valor": 120, "peso": 20, "volumen": 10},
    4: {"valor": 60, "peso": 18, "volumen": 12},
    5: {"valor": 40, "peso": 10, "volumen": 6},
}

aviones= {
    1: {"capPeso": 30, "capVolumen": 25},
    2: {"capPeso": 40, "capVolumen": 30},
    3: {"capPeso": 50, "capVolumen": 35}
}

# Variable de decisión
Model.x = Var(R, A, domain=Binary)

# Función objetivo
Model.obj = Objective(expr = sum(Model.x[i, j]*recursos[i]["valor"] for i in R for j in A), sense=maximize)

# Restricciones
#1 - Seguridad de medicamentos 
Model.res1 = Constraint(expr = (Model.x[2,1]) == 0)

#2 - compatibilidad entre equipos medicos y agua
Model.aviones = ConstraintList()
Model.aviones.add(expr = sum(Model.x[3,j]+ Model.x[4,j]for j in A) <= 1)

#3 - Capacidad de peso en aviones
Model.pesos = ConstraintList()
for j in A:
    Model.pesos.add(expr = sum(Model.x[i,j]*recursos[i]["peso"] for i in R) <= aviones[j]["capPeso"])

#4 - Capacidad de volumen en aviones
Model.volumenes = ConstraintList()
for j in A:
    Model.volumenes.add(expr = sum(Model.x[i,j]*recursos[i]["volumen"] for i in R) <= aviones[j]["capVolumen"])


# Especificación del solver
SolverFactory('glpk').solve(Model)

Model.display()

