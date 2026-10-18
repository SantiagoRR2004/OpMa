# Ejemplo de problema de programación no lineal
#   max z=4xy
#   s. a.
#   	 x^2/3^2 + y^2/4^2 <=1
#   	       
#   	x,y >= 0

import pyomo.environ as pyo


# Crear el modelo
model = pyo.ConcreteModel()

# Definir las variables y su dominio
model.x = pyo.Var(domain=pyo.NonNegativeReals)
model.y = pyo.Var(domain=pyo.NonNegativeReals)

# Establecer la función objetivo
model.OBJ = pyo.Objective(expr = 4*model.x*model.y, sense=pyo.maximize)

# Establecer las restricciones
model.Restr1 = pyo.Constraint(expr = model.x**2/3**2 + model.y**2/4**2 <= 1)


# Para mostrar las soluciones ejecutar 'pyomo solve' en linea de comandos con las opciónes:
# pyomo solve --solver=ipopt --show-results Ej_nolineal.py


# Para que se muestren directamente al ejecutar desde python
# Habría que escribir en el prompt: python Ej_nolineal.py
# Descomentar las siguientes líneas, sólo el primer '#' de cada línea.

# # Imprimir el modelo sin resolver
# model.pprint()

solver=pyo.SolverFactory('ipopt')
results = solver.solve(model)

# Imprime la información sobre la ejecución del solver
print(results)


# Salida formateada:
print("\nSolución:")
print(f"\tCoste = {model.OBJ()}\n")

print("\nVariables en el óptimo:")
for v in model.component_objects(pyo.Var, active=True):
    print(f"\t{v} = {v()}")


print("\nRestricciones en el óptimo:")
for c in model.component_objects(pyo.Constraint, active=True):
    print(f"\t{c} = {c()}")


# # Imprimir salida similar a la del comando pyomo solve
# model.display()