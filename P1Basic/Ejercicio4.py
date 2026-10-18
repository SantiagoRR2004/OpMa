import pyomo.environ as pyo

# Crear el modelo
model = pyo.ConcreteModel()

# Definir las variables y su dominio
model.x1 = pyo.Var(domain=pyo.NonNegativeReals)
model.x2 = pyo.Var(domain=pyo.NonNegativeReals)

# Establecer la función objetivo
model.OBJ = pyo.Objective(expr = -5*model.x2, sense=pyo.minimize)

# Establecer las restricciones
model.Constraint1 = pyo.Constraint(expr = -4*model.x1 + 6*model.x2 <= 8)
model.Constraint2 = pyo.Constraint(expr =  4*model.x1 - 8*model.x2 <= 8)
model.Constraint3 = pyo.Constraint(expr =  3*model.x1 - 4*model.x2 <= 4)

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
conda activate OpMa && pyomo solve --solver=glpk --summary Ejercicio4.py
conda activate OpMa && python Ejercicio4.py
'''
