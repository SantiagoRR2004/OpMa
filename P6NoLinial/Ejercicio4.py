import pyomo.environ as pyo

model = pyo.ConcreteModel()


model.x = pyo.Var(domain=pyo.NonNegativeReals)
model.y = pyo.Var(domain=pyo.NonNegativeReals)
model.z = pyo.Var(domain=pyo.NonNegativeReals)

model.objective = pyo.Objective(
    expr=0.2 * model.x**2 + 0.08 * model.y + 0.18 + model.z**2, sense=pyo.minimize
)

model.R1 = pyo.Constraint(expr=model.x + model.y + model.z <= 1000)
model.R2 = pyo.Constraint(expr=0.14*model.x + 0.08*model.y + 0.1*model.z >= 0.12*1000)

"""
conda activate OpMa
"""

solver = pyo.SolverFactory("ipopt")
results = solver.solve(model)

print(results)
model.display()
