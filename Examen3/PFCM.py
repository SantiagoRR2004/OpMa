# Modelo para el problema de flujo a coste mínimo (PFCM) sin  flujos externos

import pyomo.environ as pyo

# Crear el modelo
model = pyo.AbstractModel()

# Definir los Parámetros
model.Nodos = pyo.Set() # Conjunto de Nodos

model.Arcos = pyo.Set(within=model.Nodos*model.Nodos) # Sólo arcos disponibles

model.Costes = pyo.Param(model.Arcos, initialize= 0) # Coste unitario Arcos (se inicializa a 0)
model.l = pyo.Param(model.Arcos, initialize= 0) # Capacidad mínima Arcos (se inicializa a 0)
model.u = pyo.Param(model.Arcos, within=pyo.Any, initialize= None) # Capacidad máxima Arcos (se inicializa a None)


# Definir las variables, su dominio y las cotas

# se define la expresión de los pares de (cota_inferior, cota_superior) para las variables 
def Cotas(model, i,j):
    return (model.l[i,j], model.u[i,j])

model.Flujo = pyo.Var(model.Arcos, domain=pyo.NonNegativeReals, bounds=Cotas) # Por la propiedad de unimodularidad NO sería necesario exigir que sean valores enteros si las ofertas y las demandas son también números enteros

# Establecer la función objetivo en dos pasos:
# 1. se define la expresión de la función objetivo
def obj_expression(m):
    return pyo.summation(m.Costes, m.Flujo)
# 2. Se establece la función objetivo
model.Coste = pyo.Objective(rule=obj_expression,sense=pyo.minimize)

# Establecer la restricción de Conservación de flujo:
def conservacion_constraint_rule(m,i):
    # devuelve la expresión para el nodo i: el flujo que sale es igual al flujo que entra
    return sum(m.Flujo[k,j] for (k,j) in m.Arcos if k == i) - sum(m.Flujo[j,k] for (j,k) in m.Arcos if k == i) == 0
# 2. Se crea la restricción de oferta máxima
model.Conservacion = pyo.Constraint(model.Nodos,rule=conservacion_constraint_rule)    

# # Las cotas de los arcos se pueden poner como restricciones o como cotas en las variables
# # Establecer la restricción de cotas
# # 1. se define la expresión del bloque de restricciones
# def cotas_constraint_rule(m, i, j):
    # return (m.l[i, j], m.Flujo[i, j], m.u[i, j])

# # 2. Se crea la restricción de demanda mínima
# model.Cotas = pyo.Constraint(model.Arcos,rule=cotas_constraint_rule)


# # Si queremos obtener los duales y los costes reducidos debemos de solicitarlo ANTES de resolver el modelo/instancia
# model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)
# model.rc = pyo.Suffix(direction=pyo.Suffix.IMPORT)

# Para mostrar las soluciones ejecutar 'pyomo solve' en linea de comandos con la opción --summary:
# pyomo solve --solver=glpk --show-results Transporte.py Transporte_1.dat

####################################################################################
# Para que se muestren directamente al ejecutar desde python (con  p ej. IDLE)
solver = pyo.SolverFactory('glpk')
# Se crea una instancia: modelo abstracto + datos
instancia = model.create_instance('PFCM_1.dat')

# Muestra la instancia sin resolver para comprobar si lo ha hecho bien:
# instancia.pprint()

#Se resuelve la instancia
results = solver.solve(instancia)
# Para devolver el informe de sensibilidad comentar la linea anterior y descomentar la siguiente:
# results = solver.solve(instancia,symbolic_solver_labels=True, options={'ranges': 'PFCM_sensibilidad_1.txt'} ) 
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
# print("\nCostes reducidos")
# for v in instancia.component_data_objects(pyo.Var, active=True):
    # print(f"\t{v} = {instancia.rc[v]}")


# print("\nDuales")
# for c in instancia.component_data_objects(pyo.Constraint, active=True):
    # print(f"\t{c} = {instancia.dual[c]}")
####### Hasta aquí

# Muestra la instancia sin resolver:
#instancia.pprint()

# Muestra la instancia resuelta
#instancia.display()