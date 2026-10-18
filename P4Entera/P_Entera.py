# Modelo concreto para un ejemplo de programación entera
#   Ejemplo

#   minimizar z=-5x1 - 8x2
#   s. a.
#   	x1 +  x2 <=  6
#      5x1 + 9x2 <= 45
#   	x1,x2 >= 0
#       x1,x2 in Z


import pyomo.environ as pyo

# Crear el modelo
model = pyo.ConcreteModel()

# Definir las variables y su dominio PARA EL PROBLEMA RELAJADO
# Si se quiere resolver el problema entero hay que comentar las dos líneas siguientes
# y descomentar las de después
#model.x1 = pyo.Var(domain=pyo.NonNegativeReals)
#model.x2 = pyo.Var(domain=pyo.NonNegativeReals)

# # Definir las variables y su dominio
model.x2 = pyo.Var(domain=pyo.NonNegativeIntegers)
model.x1 = pyo.Var(domain=pyo.NonNegativeIntegers)

# Establecer la función objetivo
model.Objetivo = pyo.Objective(expr = -5*model.x1 - 8*model.x2, sense=pyo.minimize)

# Establecer las restricciones
model.Rest1 = pyo.Constraint(expr = model.x1 + model.x2 <= 6)
model.Rest2 = pyo.Constraint(expr = 5*model.x1 + 9*model.x2 <= 45)


# Para mostrar las soluciones ejecutar 'pyomo solve' en linea de comandos con las opciones:
# antes de ello debeéis de comentar todas las líneas que vienen después de la siguiente:
# pyomo solve --solver=glpk --show-results P_Entera.py


# Para que se muestren directamente al ejecutar desde python
# Habría que escribir en el prompt: python P_Entera.py
# Descomentar las siguientes líneas, sólo el primer '#' de cada línea.

solver = pyo.SolverFactory('glpk')

results = solver.solve(model) #Añadir ,options={'nomip':''} para que resuelva el problema relajado (solo glpk)

# Imprime la información sobre la ejecución del solver
print(results)

# Salida formateada:
print("\nSolución:")
print(f"\tCoste = {model.Objetivo()}")

print("\nVariables en el óptimo:")
for v in model.component_objects(pyo.Var, active=True):
    print(f"\t{v} = {v()}")


print("\nRestricciones en el óptimo:")
for c in model.component_objects(pyo.Constraint, active=True):
    print(f"\t{c} = {c()}")
    
# Muestra el modelo sin resolver
##model.pprint()

# Muestra el modelo resuelto
##model.display()
