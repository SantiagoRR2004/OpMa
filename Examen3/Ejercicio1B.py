import pyomo.environ as pyo

model = pyo.ConcreteModel()


model.A1V2 = pyo.Var(domain=pyo.NonNegativeReals)
model.A2V1 = pyo.Var(domain=pyo.NonNegativeReals)
model.A2V2 = pyo.Var(domain=pyo.NonNegativeReals)
model.A2V3 = pyo.Var(domain=pyo.NonNegativeReals)
model.A3V1 = pyo.Var(domain=pyo.NonNegativeReals)
model.A3V3 = pyo.Var(domain=pyo.NonNegativeReals)


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
model.RA1 = pyo.Constraint(expr=model.A1V2 <= 4)
model.RA2 = pyo.Constraint(expr=model.A2V1 + model.A2V2 + model.A2V3 <= 2)
model.RA3 = pyo.Constraint(expr=model.A3V1 + model.A3V3 <= 3)

# Pongo mayor o igual para leer el informe de sensibilidad mejor
# La solución sería igual con ==
model.RV1 = pyo.Constraint(expr=model.A2V1 + model.A3V1 >= 2)
model.RV2 = pyo.Constraint(expr=model.A1V2 + model.A2V2 >= 2)
model.RV3 = pyo.Constraint(expr=model.A2V3 + model.A3V3 >= 2)


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

print("\nDuales")
for c in model.component_data_objects(pyo.Constraint, active=True):
    print(f"\t{c} = {model.dual[c]}")


print("\nCostes reducidos")
for v in model.component_data_objects(pyo.Var, active=True):
    print(f"\t{v} = {model.rc[v]}")


"""
Duales
        RA1 = 0.0
        RA2 = -6.0
        RA3 = -6.0
        RV1 = 15.0
        RV2 = 7.0
        RV3 = 9.0
"""
