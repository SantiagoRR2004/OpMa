import pyomo.environ as pyo


model = pyo.ConcreteModel()

model.x = pyo.Var(domain=pyo.NonNegativeReals)
model.y = pyo.Var(domain=pyo.NonNegativeReals)

model.objective = pyo.Objective(
    expr=(model.x - 2) ** 2 + (model.y - 1) ** 2, sense=pyo.minimize
)

model.R1 = pyo.Constraint(expr=model.x + model.y <= 1)


model.rc = pyo.Suffix(direction=pyo.Suffix.IMPORT)
model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)


"""
conda activate OpMa
"""
solver = pyo.SolverFactory("ipopt")
solver.option = {"ranges": "sensibilidad.txt"}
results = solver.solve(model, symbolic_solver_labels=True)

print(results)
model.display()


print("Duales")
for i in model.dual:
    print(f"\t{i} == {model.dual[i]}")

print("Restricciones")
for i in model.rc:
    print(f"\t{i} == {model.rc[i]}")
