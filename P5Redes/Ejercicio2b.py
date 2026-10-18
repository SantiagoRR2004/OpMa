"""
2. (Problema de transporte) Una empresa suministradora de agua dispone de dos depósitos (D1 , D2 ) cuyas
capacidades son 45 y 65 hectómetros cúbicos. Cada día la empresa debe suministrar el agua a tres pueblos
A, B y C, cuyas demandas de agua son 30, 40 y 30 hectómetros cúbicos, respectivamente. El coste del
transporte (por hectómetro cúbico de agua) está dado en la tabla siguiente:

    A   B   C
D1  6   7   4
D2  5   8   6

¿Qué cantidad de agua se debe enviar desde cada depósito a cada ciudad para que, satisfaciéndose todas
las demandas, los costes de transporte sean mínimos?

b) Resolver el problema como un problema de flujo en red a coste mínimo.
"""
import pyomo.environ as pyo

model = pyo.ConcreteModel()

model.D1A = pyo.Var(domain=pyo.NonNegativeReals)
model.D1B = pyo.Var(domain=pyo.NonNegativeReals)
model.D1C = pyo.Var(domain=pyo.NonNegativeReals)

model.D2A = pyo.Var(domain=pyo.NonNegativeReals)
model.D2B = pyo.Var(domain=pyo.NonNegativeReals)
model.D2C = pyo.Var(domain=pyo.NonNegativeReals)

# N is the extra node
model.ND1 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 45))
model.ND2 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 65))

model.AN = pyo.Var(domain=pyo.NonNegativeReals, bounds=(30, 30))
model.BN = pyo.Var(domain=pyo.NonNegativeReals, bounds=(40, 40))
model.CN = pyo.Var(domain=pyo.NonNegativeReals, bounds=(30, 30))

model.objective = pyo.Objective(
    expr=6 * model.D1A
    + 7 * model.D1B
    + 4 * model.D1C
    + 5 * model.D2A
    + 8 * model.D2B
    + 6 * model.D2C,
    sense=pyo.minimize,
)


# No stragglers
model.RD1 = pyo.Constraint(expr=model.D1A + model.D1B + model.D1C - model.ND1 == 0)
model.RD2 = pyo.Constraint(expr=model.D2A + model.D2B + model.D2C - model.ND2 == 0)

model.RA = pyo.Constraint(expr=model.AN - model.D1A - model.D2A == 0)
model.RB = pyo.Constraint(expr=model.BN - model.D1B - model.D2B == 0)
model.RC = pyo.Constraint(expr=model.CN - model.D1C - model.D2C == 0)

model.RN = pyo.Constraint(
    expr=model.ND1 + model.ND2 - model.AN - model.BN - model.CN == 0
)

model.rc = pyo.Suffix(direction=pyo.Suffix.IMPORT)
model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)

solver = pyo.SolverFactory("glpk")
solver.options = {"ranges": "sensibilidad.txt"}

results = solver.solve(model, symbolic_solver_labels=True)

print(results)
model.display()

"""
D1B = 15
D1C = 30
D2A = 30
D2B = 25
"""


print("\nDuales")
for i in model.dual:
    print(f"\t{i} = {model.dual[i]}")

print("\nRestricciones")
for i in model.rc:
    print(f"\t{i} = {model.rc[i]}")
