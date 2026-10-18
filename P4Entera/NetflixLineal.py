import pyomo.environ as pyo

# Crear el modelo
model = pyo.AbstractModel()

# Definir los Parámetros
model.m = pyo.Param(within=pyo.NonNegativeIntegers) #número de servidores
model.n = pyo.Param(within=pyo.NonNegativeIntegers) #número de clientes

model.I = pyo.RangeSet(1, model.m) # Conjunto de servidores
model.J = pyo.RangeSet(1, model.n) # Conjunto de clientes

model.time = pyo.Param(model.I, model.J) # Tiempo entre servidor i y cliente j
model.capacity = pyo.Param(model.I)  # Capacidad de cada servidor
model.demand = pyo.Param(model.J)  # Demanda de cada cliente


# Definir las variables y su dominio
model.x = pyo.Var(model.I, model.J, domain=pyo.NonNegativeReals)

# Establecer la función objetivo en dos pasos:
# 1. se define la expresión de la función objetivo
def obj_expression(model):
    return pyo.summation(model.time, model.x)
# 2. Se establece la función objetivo
model.OBJ = pyo.Objective(rule=obj_expression,sense=pyo.minimize)

# 1. se define la expresión del bloque de restricciones
def mp_constraint_rule(model, i):
    # devuelve la expresión para la restricción de la capacidad
    return sum(model.x[i,j] for j in model.J) <= model.capacity[i]

# 2. Se crea una restricción para cada servidor
model.M_P_Constraint = pyo.Constraint(model.I, rule=mp_constraint_rule)

# 1. se define la expresión del bloque de restricciones
def dp_constraint_rule(model, j):
    return sum(model.x[i,j] for i in model.I) == model.demand[j]

model.D_P_Constraint = pyo.Constraint(model.J, rule=dp_constraint_rule)


# Para mostrar las soluciones ejecutar 'pyomo solve' en linea de comandos con la opción --summary:
'''
conda activate OpMa && pyomo solve --solver=glpk --summary Netflix.py Netflix1.dat
'''

####################################################################################
# # Para que se muestren directamente al ejecutar desde python (con  p ej. IDLE)
solver = pyo.SolverFactory('glpk')
# # Se crea una instancia: modelo abstracto + datos
instance = model.create_instance('Netflix3.dat')
# #Se resuleve la instancia
results = solver.solve(instance)
# # Se muestran los resultados
print(results)
instance.display()
