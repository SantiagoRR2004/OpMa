import pyomo.environ as pyo

# Crear el modelo
model = pyo.ConcreteModel()

# Definir las variables y su dominio
model.x1 = pyo.Var(domain=pyo.NonNegativeReals)
model.x2 = pyo.Var(domain=pyo.NonNegativeReals)
model.x3 = pyo.Var(domain=pyo.NonNegativeReals)
model.x4 = pyo.Var(domain=pyo.NonNegativeReals)

# Establecer la función objetivo
model.OBJ = pyo.Objective(expr = 31*model.x1 + 36*model.x2 + 42*model.x3 + 53*model.x4, sense=pyo.minimize)

# Establecer las restricciones
model.Constraint1 = pyo.Constraint(expr = -1*model.x1 + 22*model.x2 -  5*model.x3 + 30*model.x4 >=  0)
model.Constraint2 = pyo.Constraint(expr = -5*model.x1 +  0*model.x2 -  7*model.x3 +  9*model.x4 >=  0)
model.Constraint3 = pyo.Constraint(expr =-13*model.x1 -  8*model.x2 - 15*model.x3 +  1*model.x4 <=  0)
model.Constraint4 = pyo.Constraint(expr = 17*model.x1 -  8*model.x2 - 45*model.x3 - 51*model.x4 <=  0)
model.Constraint5 = pyo.Constraint(expr =  1*model.x1 +  1*model.x2 +  1*model.x3 +  1*model.x4 >=862)

model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)
model.rc = pyo.Suffix(direction=pyo.Suffix.IMPORT)

# Para mostrar las soluciones ejecutar 'pyomo solve' en linea de comandos con la opción --summary

# Para que se muestren directamente al ejecutar desde python (con  p ej. IDLE)
solver=pyo.SolverFactory('glpk')
solver.options = {'ranges': 'sensibilidad.txt'}
results = solver.solve(model,symbolic_solver_labels=True)
print(results)
##model.display()

print("\nSolución:")
for v in model.component_objects(pyo.Objective, active=True):
    print(f"\t{v} = {v()}")


print("\nVariables en el óptimo:")
for v in model.component_objects(pyo.Var, active=True):
    print(f"\t{v} = {v()}")


print("\nRestricciones en el óptimo:")
for c in model.component_objects(pyo.Constraint, active=True):
    print(f"\t{c} = {c()}")


print("\nCostes reducidos")
for v in model.component_objects(pyo.Var, active=True):
    print(f"\t{v} = {model.rc[v]}")


print("\nDuales")
for c in model.component_objects(pyo.Constraint, active=True):
    print(f"\t{c} = {model.dual[c]}")


'''
conda activate OpMa && pyomo solve --solver=glpk --summary Ejercicio3.py
conda activate OpMa && python Ejercicio3.py
'''
