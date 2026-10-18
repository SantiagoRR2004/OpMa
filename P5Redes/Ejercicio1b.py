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

b) Resolver el problema como un problema de flujo en red a coste mínimo.
"""

import pyomo.environ as pyo

model = pyo.ConcreteModel()

model.A1V1 = pyo.Var(domain=pyo.NonNegativeReals)
model.A1V2 = pyo.Var(domain=pyo.NonNegativeReals)

model.A2V1 = pyo.Var(domain=pyo.NonNegativeReals)
model.A2V2 = pyo.Var(domain=pyo.NonNegativeReals)

model.A3V2 = pyo.Var(domain=pyo.NonNegativeReals)
model.A3V3 = pyo.Var(domain=pyo.NonNegativeReals)

# N is our extra node
model.NA1 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 4))
model.NA2 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 2))
model.NA3 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 3))

model.NV1 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(3, 3))
model.NV2 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(3, 3))
model.NV3 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(3, 3))

model.objective = pyo.Objective(
    expr=3 * model.A1V1
    + model.A1V2
    + 4 * model.A2V1
    + 2 * model.A2V2
    + 3 * model.A3V2
    + 3 * model.A3V3,
    sense=pyo.minimize,
)


# We need to have a restriction so every node is zero
model.RA1 = pyo.Constraint(expr=model.A1V1 + model.A1V2 - model.NA1 == 0)
model.RA2 = pyo.Constraint(expr=model.A2V1 + model.A2V2 - model.NA2 == 0)
model.RA3 = pyo.Constraint(expr=model.A3V2 + model.A3V3 - model.NA3 == 0)

model.RV1 = pyo.Constraint(expr=model.NV1 - model.A1V1 - model.A2V1 == 0)
model.RV2 = pyo.Constraint(expr=model.NV2 - model.A1V2 - model.A2V2 - model.A3V2 == 0)
model.RV3 = pyo.Constraint(expr=model.NV3 - model.A3V3 == 0)

model.RN = pyo.Constraint(
    expr=model.NV1 + model.NV2 + model.NV3 - model.NA1 - model.NA2 - model.NA3 == 0
)

model.rc = pyo.Suffix(direction=pyo.Suffix.IMPORT)
model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)

solver = pyo.SolverFactory("glpk")
solver.options = {"ranges":"sensibilidad.txt"}

results = solver.solve(model,symbolic_solver_labels=True)

print(results)
model.display()


print("Duales")
for i in model.dual:
    print(f"\t{i} == {model.dual[i]}")

print("Restricciones en el dual")
for i in model.rc:
    print(f"\t{i} == {model.rc[i]}")