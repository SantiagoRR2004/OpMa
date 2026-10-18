# Modelo abstracto para el problema del transporte genérico
# Con este código, a las conexiones que no exisytan hay que asignarles un coste muy grande

import pyomo.environ as pyo

# Crear el modelo
model = pyo.AbstractModel()

# Definir los Parámetros
model.Origenes = pyo.Set()  # Conjunto de Origenes
model.Destinos = pyo.Set()  # Conjunto de Destinos

model.Oferta = pyo.Param(
    model.Origenes
)  # Oferta de los origenes (se podría exigir que fuesen enteros para garantizar la unimodularidad)
model.Demanda = pyo.Param(
    model.Destinos
)  # Demanda de los destinos (se podría exigir que fuesen enteros para garantizar la unimodularidad)
model.Costes = pyo.Param(
    model.Origenes, model.Destinos
)  # Coste unitario Origen-Destino


# Definir las variables y su dominio
model.Flujo = pyo.Var(
    model.Origenes, model.Destinos, domain=pyo.NonNegativeReals
)  # Por la propiedad de unimodularidad NO sería necesario exigir que sean valores enteros si las ofertas y las demandas son también números enteros


# Establecer la función objetivo en dos pasos:
# 1. se define la expresión de la función objetivo
def obj_expression(m):
    return pyo.summation(m.Costes, m.Flujo)


# 2. Se establece la función objetivo
model.Coste = pyo.Objective(rule=obj_expression, sense=pyo.minimize)


# Establecer la restricción de Oferta:
# 1. se define la expresión del bloque de restricciones
def oferta_constraint_rule(m, i):
    # devuelve la expresión para el origen i
    return sum(m.Flujo[i, j] for j in m.Destinos) <= m.Oferta[i]


# 2. Se crea la restricción de oferta máxima
model.maxOferta = pyo.Constraint(model.Origenes, rule=oferta_constraint_rule)


# Establecer la restricción de demanda:
# 1. se define la expresión del bloque de restricciones
def demanda_constraint_rule(m, j):
    # devuelve la expresión para el Destino j
    return sum(m.Flujo[i, j] for i in m.Origenes) == m.Demanda[j]


# 2. Se crea la restricción de demanda mínima
model.minDemanda = pyo.Constraint(model.Destinos, rule=demanda_constraint_rule)


# # Si queremos obtener los duales y los costes reducidos debemos de solicitarlo ANTES de resolver el modelo/instancia
model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)
model.rc = pyo.Suffix(direction=pyo.Suffix.IMPORT)

# Para mostrar las soluciones ejecutar 'pyomo solve' en linea de comandos:
# pyomo solve --solver=glpk --solver-options="ranges=netflix_sensibilidad.txt" --symbolic-solver-labels --show-results Transporte.py Netflix_1.dat

####################################################################################
# Para que se muestren directamente al ejecutar desde python (con  p ej. IDLE)
solver = pyo.SolverFactory("glpk")
# Se crea una instancia: modelo abstracto + datos
instancia = model.create_instance("Netflix_1.dat")

# Muestra la instancia sin resolver para comprobar si lo ha hecho bien:
# instancia.pprint()


# Se resuelve la instancia
results = solver.solve(instancia)
# Para devolver el informe de sensibilidad comentar la linea anterior y descomentar la siguiente:
results = solver.solve(
    instancia,
    symbolic_solver_labels=True,
    options={"ranges": "netflix_sensibilidad.txt"},
)
# Imprime la información sobre la ejecución del solver
print(results)


# Salida formateada:
print("\nSolución:")
print(f"\nCoste Total = {instancia.Coste()}")

# OJO!!: Para el problema abstracto se trabaja con la instancia y se utiliza component_data_objects
# para acceder a las variables del problema.
print("\nVariables (!=0) en el óptimo:")
for v in instancia.component_data_objects(pyo.Var, active=True):
    # Sólo se imprimen los datos distintos de 0
    if v() > 0:
        print(f"\t{v} = {v()}")

print("\nRestricciones en el óptimo:")
for c in instancia.component_data_objects(pyo.Constraint, active=True):
    print(f"\t{c} = {c()}")

# Si se quiere realizar un informe de sensibilidad, descomentar las siguientes lineas
print("\nCostes reducidos")
for v in instancia.component_data_objects(pyo.Var, active=True):
    print(f"\t{v} = {instancia.rc[v]}")


print("\nDuales")
for c in instancia.component_data_objects(pyo.Constraint, active=True):
    print(f"\t{c} = {instancia.dual[c]}")
####### Hasta aquí

# Muestra la instancia sin resolver:
# instancia.pprint()

# Muestra la instancia resuelta
# instancia.display()
