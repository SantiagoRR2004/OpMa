import pyomo.environ as pyo

model = pyo.ConcreteModel()

model.x = pyo.Var(domain=pyo.NonNegativeReals)
model.y = pyo.Var(domain=pyo.NonNegativeReals)

model.objective = pyo.Objective(
    expr=((model.x - 1) ** 2 + (model.y - 3) ** 2) ** (1 / 2), sense=pyo.maximize
)


model.R = pyo.Constraint(expr=(model.x - 2) ** 2 + (model.y - 1) ** 2 == 2)

"""
conda activate OpMa
"""

solver = pyo.SolverFactory("ipopt")
results = solver.solve(model)

print(results)
model.display()