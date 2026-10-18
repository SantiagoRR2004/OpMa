"""
1. (Problema de transporte) Un empresario dispone de tres almacenes (A1 , A2 y A3 )
 y tres puntos de venta (V1 , V2 y V3 ). En cada punto de venta tiene apalabradas 
 3 toneladas de mercancía.En el almacén A1 tiene disponibles 4 toneladas de mercancía,
   2 toneladas en el almacén A2 y 3 toneladas en el almacén A3 . Los costes de transporte 
   de cada almacén a cada punto de venta son los dados en la tabla siguiente:

V1
V2
V3
A1
3
1
No hay transporte
A2
4
2
No hay transporte
A3
No hay transporte
3
3

¿Qué cantidad de mercancía se debe transportar desde cada almacén a cada punto de venta para que,satisfaciéndose todos los compromisos, los costes de transporte sean mínimos?

a) Resolver el problema como un problema de Transporte y realiza un informe de sensibilidad indicando entre qué valores se podrían modificar las disponibilidades de los almacenes y las demandas de los puntos de venta sin que cambie la solución básica factible
 Como cambiaría el coste de transporte total por cada unidad que se puedan modificar las disponibilidades y las demandas.

"""

import pyomo.environ as pyo

model = pyo.ConcreteModel()

model.A1V1 = pyo.Var(domain=pyo.NonNegativeReals)
model.A2V1 = pyo.Var(domain=pyo.NonNegativeReals)
model.A1V2 = pyo.Var(domain=pyo.NonNegativeReals)
model.A2V2 = pyo.Var(domain=pyo.NonNegativeReals)
model.A3V2 = pyo.Var(domain=pyo.NonNegativeReals)
model.A3V3 = pyo.Var(domain=pyo.NonNegativeReals)

# Flujos con sus costes
model.objective = pyo.Objective(
    expr=3 * model.A1V1
    + 4 * model.A2V1
    + model.A1V2
    + 2 * model.A2V2
    + 3 * model.A3V2
    + 3 * model.A3V3,
    sense=pyo.minimize,
)

# Puntos de venta
model.RV1 = pyo.Constraint(expr=model.A1V1 + model.A2V1 == 3)
model.RV2 = pyo.Constraint(expr=model.A1V2 + model.A2V2 + model.A3V2 == 3)
model.RV3 = pyo.Constraint(expr=model.A3V3 == 3)

# Almacenes
model.RA1 = pyo.Constraint(expr=model.A1V1 + model.A1V2 <= 4)
model.RA2 = pyo.Constraint(expr=model.A2V1 + model.A2V2 <= 2)
model.RA3 = pyo.Constraint(expr=model.A3V2 + model.A3V3 <= 3)


# model.rc = pyo.Suffix(direction=pyo.Suffix.IMPORT)
model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)

"""
conda activate OpMa
"""
solver = pyo.SolverFactory("glpk")

solver.options = {"ranges": "sensibilidad.txt"}
results = solver.solve(model, symbolic_solver_labels=True)

print(results)
model.display()


"""
A1V1 = 3
A1V2 = 1
A2V2 = 2
A3V3 = 3

Vemos el archivo de sensibilidad.txt para el primer punto

Para cambiar las disponibilidades tenemos que ver Activity range en la primera tabla.
Vemos que para los ventas no se puede subir y que el primero 
y el segundo se puede bajar a uno y el tercero se puede 
bajar a cero.


Si nos fijamos en los almacenes podemos ver también su rango de valores.
Nos fijamos en aquellos cuyos valores están en orden
Excepto en 2 que es desde 2 hasta infinito
"""

"""
for i in model.rc:
    print(f"{i} = {model.rc[i]}")
"""
for i in model.dual:
    print(f"{i} = {model.dual[i]}")
"""
Para el segundo punto vemos lo que acabamos de 
imprimir de los duales. Vemos cuanto cambia el
óptimo  por cada unidad que reducimos de costes
y demandas

RV1 = 4.0
RV2 = 2.0
RV3 = 3.0
RA1 = -1.0
RA2 = 0.0
RA3 = 0.0
"""
