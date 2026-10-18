"""
3. (Problema de asignación) Tenemos 9 alumnos que han de realizar prácticas en dos laboratorios. El pri-
mero tiene capacidad para dos alumnos y el segundo para tres. Por tanto, hay que distribuir los alumnos
en turnos: T1 y T2 para el primer laboratorio y T3 y T4 para el segundo. Los alumnos han mostrado el
siguiente orden de preferencia sobre los turnos (1 prioridad máxima, 4 prioridad mínima):

    T1  T2  T3  T4
A1  3   2   1   4
A2  1   2   3   4
A3  1   4   3   2
A4  3   2   4   1
A5  2   1   3   4
A6  3   2   1   4
A7  2   1   3   4
A8  4   1   2   3
A9  3   1   2   4


Encontrar la asignación de alumnos a turnos que minimice el descontento total de los mismos (por ejem-
plo, si el alumno A1 es asignado al T1 , su descontento será de 2).

a) Resolver el problema como un problema de Transporte.
"""

import pyomo.environ as pyo

model = pyo.ConcreteModel()

model.A1T1 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1))
model.A1T2 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1))
model.A1T3 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1))
model.A1T4 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1))

model.A2T1 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1))
model.A2T2 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1))
model.A2T3 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1))
model.A2T4 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1))

model.A3T1 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1))
model.A3T2 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1))
model.A3T3 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1))
model.A3T4 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1))

model.A4T1 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1))
model.A4T2 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1))
model.A4T3 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1))
model.A4T4 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1))

model.A5T1 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1))
model.A5T2 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1))
model.A5T3 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1))
model.A5T4 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1))

model.A6T1 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1))
model.A6T2 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1))
model.A6T3 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1))
model.A6T4 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1))

model.A7T1 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1))
model.A7T2 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1))
model.A7T3 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1))
model.A7T4 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1))

model.A8T1 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1))
model.A8T2 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1))
model.A8T3 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1))
model.A8T4 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1))

model.A9T1 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1))
model.A9T2 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1))
model.A9T3 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1))
model.A9T4 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 1))

model.objective = pyo.Objective(
    expr=3 * model.A1T1
    + 2 * model.A1T2
    + 1 * model.A1T3
    + 4 * model.A1T4
    + 1 * model.A2T1
    + 2 * model.A2T2
    + 3 * model.A2T3
    + 4 * model.A2T4
    + 1 * model.A3T1
    + 4 * model.A3T2
    + 3 * model.A3T3
    + 2 * model.A3T4
    + 3 * model.A4T1
    + 2 * model.A4T2
    + 4 * model.A4T3
    + 1 * model.A4T4
    + 2 * model.A5T1
    + 1 * model.A5T2
    + 3 * model.A5T3
    + 4 * model.A5T4
    + 3 * model.A6T1
    + 2 * model.A6T2
    + 1 * model.A6T3
    + 4 * model.A6T4
    + 2 * model.A7T1
    + 1 * model.A7T2
    + 3 * model.A7T3
    + 4 * model.A7T4
    + 4 * model.A8T1
    + 1 * model.A8T2
    + 2 * model.A8T3
    + 3 * model.A8T4
    + 3 * model.A9T1
    + 1 * model.A9T2
    + 2 * model.A9T3
    + 4 * model.A9T4,
    sense=pyo.minimize,
)

# Students
model.RA1 = pyo.Constraint(expr=model.A1T1 + model.A1T2 + model.A1T3 + model.A1T4 == 1)
model.RA2 = pyo.Constraint(expr=model.A2T1 + model.A2T2 + model.A2T3 + model.A2T4 == 1)
model.RA3 = pyo.Constraint(expr=model.A3T1 + model.A3T2 + model.A3T3 + model.A3T4 == 1)
model.RA4 = pyo.Constraint(expr=model.A4T1 + model.A4T2 + model.A4T3 + model.A4T4 == 1)
model.RA5 = pyo.Constraint(expr=model.A5T1 + model.A5T2 + model.A5T3 + model.A5T4 == 1)
model.RA6 = pyo.Constraint(expr=model.A6T1 + model.A6T2 + model.A6T3 + model.A6T4 == 1)
model.RA7 = pyo.Constraint(expr=model.A7T1 + model.A7T2 + model.A7T3 + model.A7T4 == 1)
model.RA8 = pyo.Constraint(expr=model.A8T1 + model.A8T2 + model.A8T3 + model.A8T4 == 1)
model.RA9 = pyo.Constraint(expr=model.A9T1 + model.A9T2 + model.A9T3 + model.A9T4 == 1)

# Labs
model.RT1 = pyo.Constraint(
    expr=model.A1T1
    + model.A2T1
    + model.A3T1
    + model.A4T1
    + model.A5T1
    + model.A6T1
    + model.A7T1
    + model.A8T1
    + model.A9T1
    <= 2
)
model.RT2 = pyo.Constraint(
    expr=model.A1T2
    + model.A2T2
    + model.A3T2
    + model.A4T2
    + model.A5T2
    + model.A6T2
    + model.A7T2
    + model.A8T2
    + model.A9T2
    <= 2
)
model.RT3 = pyo.Constraint(
    expr=model.A1T3
    + model.A2T3
    + model.A3T3
    + model.A4T3
    + model.A5T3
    + model.A6T3
    + model.A7T3
    + model.A8T3
    + model.A9T3
    <= 3
)
model.RT4 = pyo.Constraint(
    expr=model.A1T4
    + model.A2T4
    + model.A3T4
    + model.A4T4
    + model.A5T4
    + model.A6T4
    + model.A7T4
    + model.A8T4
    + model.A9T4
    <= 3
)

model.rc = pyo.Suffix(direction=pyo.Suffix.IMPORT)
model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)

solver = pyo.SolverFactory("glpk")
solver.options = {"ranges": "sensibilidad.txt"}
results = solver.solve(model, symbolic_solver_labels=True)

print(results)
model.display()

print("\nDuales")
for i in model.dual:
    print(f"\t{i} = {model.dual[i]}")

print("\nRestricciones")
for i in model.rc:
    print(f"\t{i} = {model.rc[i]}")

"""
A1T3 = 1
A2T1 = 1
A3T1 = 1
A4T4 = 1
A5T1 = 1
A6T3 = 1
A7T2 = 1
A8T4 = 1
A9T3 = 1
"""
