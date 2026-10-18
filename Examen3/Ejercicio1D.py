import pyomo.environ as pyo

model = pyo.ConcreteModel()


model.A1V2 = pyo.Var(domain=pyo.NonNegativeReals)

model.A2V1 = pyo.Var(domain=pyo.NonNegativeReals)
model.A2V2 = pyo.Var(domain=pyo.NonNegativeReals)
model.A2V3 = pyo.Var(domain=pyo.NonNegativeReals)

model.A3V1 = pyo.Var(domain=pyo.NonNegativeReals)
model.A3V3 = pyo.Var(domain=pyo.NonNegativeReals)

model.NA1 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 4))
model.NA2 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 2))
model.NA3 = pyo.Var(domain=pyo.NonNegativeReals, bounds=(0, 3))

model.V1N = pyo.Var(domain=pyo.NonNegativeReals, bounds=(2, 2))
model.V2N = pyo.Var(domain=pyo.NonNegativeReals, bounds=(2, 2))
model.V3N = pyo.Var(domain=pyo.NonNegativeReals, bounds=(2, 2))


model.objective = pyo.Objective(
    expr=7 * model.A1V2
    + 9 * model.A2V1
    + 1 * model.A2V2
    + 5 * model.A2V3
    + 9 * model.A3V1
    + 3 * model.A3V3,
    sense=pyo.minimize,
)


# Restrictions
model.RA1 = pyo.Constraint(expr=model.A1V2 - model.NA1 == 0)
model.RA2 = pyo.Constraint(expr=model.A2V1 + model.A2V2 + model.A2V3 - model.NA2 == 0)
model.RA3 = pyo.Constraint(expr=model.A3V1 + model.A3V3 - model.NA3 == 0)

model.RV1 = pyo.Constraint(expr=model.V1N - model.A2V1 - model.A3V1 == 0)
model.RV2 = pyo.Constraint(expr=model.V2N - model.A1V2 - model.A2V2 == 0)
model.RV3 = pyo.Constraint(expr=model.V3N - model.A2V3 - model.A3V3 == 0)


model.RN = pyo.Constraint(
    expr=model.NA1 + model.NA2 + model.NA3 - model.V1N - model.V2N - model.V3N == 0
)


model.rc = pyo.Suffix(direction=pyo.Suffix.IMPORT)
model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)

"""
conda activate OpMa
"""
solver = pyo.SolverFactory("glpk")
solver.options = {"ranges": "sensibilidad.txt"}
results = solver.solve(model, symbolic_solver_labels=True)


print(results)
model.display()
