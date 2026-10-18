# Modelo concreto para el ejemplo de pinturas (poco eficiente la forma de trabajar con pyomo)
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
model.x1 = pyo.Var(domain=pyo.NonNegativeReals)
model.x2 = pyo.Var(domain=pyo.NonNegativeReals, bounds= (0, 2))

# Establecer la función objetivo
model.OBJ = pyo.Objective(expr = 5*model.x1 + 4*model.x2, sense=pyo.maximize)

# Establecer las restricciones
model.Constraint1 = pyo.Constraint(expr = 6*model.x1 + 4*model.x2 <= 24)
model.Constraint2 = pyo.Constraint(expr = model.x1 + 2*model.x2 <= 6)
model.Constraint3 = pyo.Constraint(expr = -model.x1 + model.x2 <= 1)
# model.Constraint4 = pyo.Constraint(expr =  model.x2 <= 2) # Tambien se podría poner como una cota (bound) al definir la variable


# Para mostrar las soluciones ejecutar 'pyomo solve' en linea de comandos con la opción --summary

# Para que se muestren directamente al ejecutar desde python (con  p ej. IDLE)
#solver=pyo.SolverFactory('glpk')
#results = solver.solve(model)
#print(results)
#model.display()


'''
conda activate OpMa && pyomo solve --solver=glpk --summary pinturas_concrete.py
'''
