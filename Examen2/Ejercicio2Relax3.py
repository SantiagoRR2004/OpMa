import pyomo.environ as pyo

model = pyo.ConcreteModel()

model.x1 = pyo.Var(domain=pyo.NonNegativeReals)
model.x2 = pyo.Var(domain=pyo.NonNegativeReals)
model.x3 = pyo.Var(domain=pyo.NonNegativeReals)
model.x4 = pyo.Var(domain=pyo.NonNegativeReals)
model.r4 = pyo.Constraint(expr= model.x4 >= 3)

model.minimizer = pyo.Objective(expr=-116*model.x1-60*model.x2-46*model.x3-78*model.x4,sense=pyo.minimize)

model.r1 = pyo.Constraint(expr= 2*model.x1 + 3*model.x2 + 2*model.x3 + 13*model.x4 <= 45)
model.r2 = pyo.Constraint(expr= 8*model.x1 + 5*model.x2 + 8*model.x3 - 5*model.x4 <= 46)
model.r3 = pyo.Constraint(expr= 5*model.x1 + 12*model.x2 + 14*model.x3 + 12*model.x4 <= 122)

solver = pyo.SolverFactory("glpk")


"""
pyomo solve --solver=glpk  --summary Ejercicio2Relax3.py
"""