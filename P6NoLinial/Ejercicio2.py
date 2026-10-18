import pyomo.environ as pyo

model = pyo.ConcreteModel()

model.X1 = pyo.Var(domain=pyo.NonNegativeReals)
model.X2 = pyo.Var(domain=pyo.NonNegativeReals)


model.objective = pyo.Objective(
    expr=(model.X1 - 3 / 2) ** 2 + (model.X2 - 5) ** 2, sense=pyo.minimize
)

model.R1 = pyo.Constraint(expr=-1 * model.X1 + model.X2 <= 2)
model.R2 = pyo.Constraint(expr=model.X1 + 2 * model.X2 <= 7)
model.R3 = pyo.Constraint(expr=2 * model.X1 + 2 * model.X2 <= 11)

solver = pyo.SolverFactory("ipopt")

results = solver.solve(model,symbolic_solver_labels=True)

print(results)
model.display()