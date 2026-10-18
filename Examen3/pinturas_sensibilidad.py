# Modelo concreto para el ejemplo de pinturas (poco eficiente)
#   Ejemplo

#   maximizar z=5x+4y
#   s. a.
#   	6x + 4y <= 24
#   	 x + 2y <=  6
#   	-x +  y <=  1
#	      y <=  2
#   	x,y >= 0

import pyomo.environ as pyo

# Crear el modelo
model = pyo.ConcreteModel()

# Definir las variables y su dominio
model.pExterior = pyo.Var(domain=pyo.NonNegativeReals)
model.pInterior = pyo.Var(domain=pyo.NonNegativeReals, bounds= (0, 2))

# Establecer la función objetivo
model.Coste = pyo.Objective(expr = 5*model.pExterior + 4*model.pInterior, sense=pyo.maximize)

# Establecer las restricciones
model.MatPrimaA = pyo.Constraint(expr = 6*model.pExterior + 4*model.pInterior <= 24)
model.MatPrimaB = pyo.Constraint(expr = model.pExterior + 2*model.pInterior <= 6)
model.EstMercado = pyo.Constraint(expr = -model.pExterior + model.pInterior <= 1)
# model.Constraint4 = pyo.Constraint(expr =  model.pInterior <= 2) # Tambien se podría poner como una cota (bound) al definir la variable


# Para extraer la información del dual y los costes reducidos 
model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)
model.rc = pyo.Suffix(direction=pyo.Suffix.IMPORT)


# Para mostrar las soluciones ejecutar 'pyomo solve' en linea de comandos con las opciones:
#      --summary o --show-results : muestra los resultados
#      --solver-options="ranges=sensibilidad_pinturas.txt" : guarda el informe de sensibilidad 
#                                                  en el fichero sensibilidad_pinturas.txt (específico para GLPK)
#      --symbolic-solver-labels : Para que en el informe de sensibilidad aparezcan los nombres de las variables y restricciones 

# antes de ello debeéis de comentar todas las líneas que vienen después de la siguiente:
# pyomo solve --solver=glpk --solver-options="ranges=sensibilidad_pinturas.txt" --symbolic-solver-labels --show-results pinturas_sensibilidad.py


# Para que se muestren directamente al ejecutar desde python el análisis de sensibilidad utilizando glpk
# Habría que escribir en el prompt: python pinturas_sensibilidad.py
# Descomentar las siguientes líneas, sólo el primer '#' de cada línea.

solver = pyo.SolverFactory('glpk')
#Para guardar el informe del análisis de sensibilidad en el fichero  sensibilidad_pinturas.txt
solver.options = {'ranges': 'sensibilidad_pinturas.txt'}

# symbolic_solver_labels=True es necesario para que en el informe de sensibilidad aparezcan los nombres 
# de las variables y restricciones 
results = solver.solve(model,symbolic_solver_labels=True)

# Imprime la información sobre la ejecución del solver
print(results)

# Imprimir el modelo
# model.pprint()

# Salida formateada:
print("\nSolución:")
print(f"\tCoste = {model.Coste()}")

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
