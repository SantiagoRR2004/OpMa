import pyomo.environ as pyo

model = pyo.ConcreteModel()

model.silla = pyo.Var(domain=pyo.NonNegativeReals)
model.mesa = pyo.Var(domain=pyo.NonNegativeReals)
model.escritorio = pyo.Var(domain=pyo.NonNegativeReals)
model.armario = pyo.Var(domain=pyo.NonNegativeReals)


model.minimizer = pyo.Objective(expr=26*model.silla+24*model.mesa+30*model.escritorio+93*model.armario,sense=pyo.minimize)

model.pino = pyo.Constraint(expr= 3*model.silla + 5*model.mesa + 10*model.escritorio + 12*model.armario <= 62)
model.roble = pyo.Constraint(expr= 3*model.silla + 6*model.mesa + 8*model.escritorio + 10*model.armario <= 74)
model.obra = pyo.Constraint(expr= 2*model.silla + 6*model.mesa + 9*model.escritorio + 10*model.armario <= 79)
model.prod_min = pyo.Constraint(expr= model.silla + model.mesa + model.escritorio + model.armario >= 15)

model.rc = pyo.Suffix(direction = pyo.Suffix.IMPORT)
model.dual = pyo.Suffix(direction = pyo.Suffix.IMPORT)

solver = pyo.SolverFactory('glpk')
solver.options = {"ranges":"results.txt"}

results = solver.solve(model, symbolic_solver_labels =True)

print(results)
model.display()

for i in model.rc:
    print(f"{i}  =  {model.rc[i]}")

for i in model.dual:
    print(f"{i}  =  {model.dual[i]}")


"""
pyomo solve --solver=glpk --solver-options='ranges=results.txt' --summary Ejercicio1.py
"""