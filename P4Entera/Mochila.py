# Modelo abstracto para el problema de la mochila

import pyomo.environ as pyo

# Crear el modelo
model = pyo.AbstractModel()

# Definir los Parámetros
model.J = pyo.Set() # Conjunto de objetos

model.u = pyo.Param(model.J)  # Utilidad de cada objeto 
model.p = pyo.Param(model.J, within=pyo.NonNegativeReals)  # Peso/volumen de cada objeto
model.P = pyo.Param(within=pyo.NonNegativeReals) # Capacidad (peso o volumen máximo) de la mochila


# Definir las variables y su dominio
model.x = pyo.Var(model.J, domain=pyo.Binary)

# Establecer la función objetivo en dos pasos:
# 1. se define la expresión de la función objetivo
def obj_expression(m):
    return pyo.summation(m.u, m.x)
# 2. Se establece la función objetivo
model.Objetivo = pyo.Objective(rule=obj_expression,sense=pyo.maximize)

# Establecer la restricción de capacidad:
# 1. se define la expresión del bloque de restricciones
def capacidad_constraint_rule(m):
    return pyo.summation(m.p, m.x) <= m.P

# 2. Se crea la restricción de capacidad
model.Capacidad = pyo.Constraint(rule=capacidad_constraint_rule)


# Para mostrar las soluciones ejecutar 'pyomo solve' en linea de comandos con la opción --summary:
# pyomo solve --solver=glpk --show-results Mochila.py Mochila_1.dat

####################################################################################
# Para que se muestren directamente al ejecutar desde python (con  p ej. IDLE)
solver = pyo.SolverFactory('glpk')
# Se crea una instancia: modelo abstracto + datos
instancia = model.create_instance('Ejercicio1.dat')

#Se resuelve la instancia
results = solver.solve(instancia) #Añadir ,options={'nomip':''} para que resuelva el problema relajado (solo glpk)
# Imprime la información sobre la ejecución del solver
print(results)

# Salida formateada:
print("\nSolución:")
print(f"\tBeneficio = {instancia.Objetivo()}")

# OJO!!: Para el problema abstracto se trabaja con la instancia y se utiliza component_data_objects
# para acceder a las variables del problema.
print("\nVariables en el óptimo:")
for v in instancia.component_data_objects(pyo.Var, active=True):
    print(f"\t{v} = {v()}")


print("\nRestricciones en el óptimo:")
for c in instancia.component_data_objects(pyo.Constraint, active=True):
    print(f"\t{c} = {c()}")

# Muestra la instancia sin resolver
instancia.pprint()

# Muestra la instancia resuelta
instancia.display()