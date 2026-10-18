# Modelo abstracto para el ejemplo de pinturas

import pyomo.environ as pyo

# Crear el modelo
model = pyo.AbstractModel()

# Definir los Parámetros
model.I = pyo.Set() # Conjunto de Materias primas
model.J = pyo.Set() # Conjunto de Tipos de pintura
model.Pref = pyo.Set(within=model.J) # Pinturas de referencia con respecto a las cuales se aplican las diferencias
model.J_Pref = pyo.Set(initialize=model.J-model.Pref) # Pinturas que no son referencia

model.p = pyo.Param(model.J)  # Precio de venta de cada tipo de pintura
model.prod = pyo.Param(model.I, model.J) # Consumo que hace de la materia prima i la pintura j
model.disp = pyo.Param(model.I) # Disponibilidad de cada materia prima
model.dif = pyo.Param(model.J_Pref)  # Diferencia máxima de producción con respecto a la pintura/s de referencia.

model.P_min = pyo.Param(model.J, within=pyo.Any) # demanda mínima a producir de cada pintura
model.P_max = pyo.Param(model.J, within=pyo.Any) # demanda máxima a producir de cada pintura

# se define la expresión de los pares de (cota_inferir, cota_superior) para las variables 
def Pbounds(model, j):
    return (model.P_min[j], model.P_max[j])

# Definir las variables y su dominio
model.x = pyo.Var(model.J, bounds=Pbounds, domain=pyo.NonNegativeReals)

# Establecer la función objetivo en dos pasos:
# 1. se define la expresión de la función objetivo
def obj_expression(m):
    return pyo.summation(m.p, m.x)
# 2. Se establece la función objetivo
model.OBJ = pyo.Objective(rule=obj_expression,sense=pyo.maximize)

# Establecer el bloque de restricciones sobre las materias primas:
# 1. se define la expresión del bloque de restricciones
def mp_constraint_rule(m, i):
    # devuelve la expresión para la restricción (materia prima) i
    return sum(m.prod[i,j] * m.x[j] for j in m.J) <= m.disp[i]

# 2. Se crea una restricción para cada materia prima
model.M_P_Constraint = pyo.Constraint(model.I, rule=mp_constraint_rule)

# Establecer el bloque de restricciones sobre la diferencia de producción con las pinturas de referencia:
# 1. se define la expresión del bloque de restricciones
def dp_constraint_rule(m, j, jref):
    # devuelve la expresión para la restricción (pintura) j 
    return m.x[j] - m.x[jref] <= m.dif[j]

# 2. Se crea una restricción para cada pintura j DISTINTA de las pinturas de referencia y para cada pintura de referencia.
model.D_P_Constraint = pyo.Constraint(model.J_Pref, model.Pref, rule=dp_constraint_rule)


# Para mostrar las soluciones ejecutar 'pyomo solve' en linea de comandos con la opción --summary:
'''
pyomo solve --solver=glpk --summary pinturas_abstract_v2.py pinturas_abstract_v2_ampl.dat
'''
# ####################################################################################
# # Para que se muestren directamente al ejecutar desde python (con  p ej. IDLE)
# solver = pyo.SolverFactory('glpk')
# # Se crea una instancia: modelo abstracto + datos
# instance = model.create_instance('pinturas_abstract_v2_ampl.dat')
# #Se resuleve la instancia
# results = solver.solve(instance)
# # Se muestran los resultados
# print(results)
# instance.display()
