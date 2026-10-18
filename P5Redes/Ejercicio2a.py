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

a) Resolver el problema como un problema de Transporte y realiza un informe de sensibilidad indicando:

entre qué valores se podrían modificar las disponibilidades de los almacenes 
y las demandas de los puntos de venta sin que cambie la solución básica factible

Como cambiaría el coste de transporte total por cada unidad que se puedan modificar las disponibilidades y las demandas.
"""
import pyomo.environ as pyo

model = pyo.ConcreteModel()

model.D1A = pyo.Var(domain=pyo.NonNegativeReals)
model.D1B = pyo.Var(domain=pyo.NonNegativeReals)
model.D1C = pyo.Var(domain=pyo.NonNegativeReals)
model.D2A = pyo.Var(domain=pyo.NonNegativeReals)
model.D2B = pyo.Var(domain=pyo.NonNegativeReals)
model.D2C = pyo.Var(domain=pyo.NonNegativeReals)

model.objective = pyo.Objective(
    expr=6 * model.D1A
    + 7 * model.D1B
    + 4 * model.D1C
    + 5 * model.D2A
    + 8 * model.D2B
    + 6 * model.D2C,
    sense=pyo.minimize,
)

model.RD1 = pyo.Constraint(expr=model.D1A + model.D1B + model.D1C <= 45)
model.RD2 = pyo.Constraint(expr=model.D2A + model.D2B + model.D2C <= 65)

model.RA = pyo.Constraint(expr=model.D1A + model.D2A >= 30)
model.RB = pyo.Constraint(expr=model.D1B + model.D2B >= 40)
model.RC = pyo.Constraint(expr=model.D1C + model.D2C >= 30)

model.rc = pyo.Suffix(direction=pyo.Suffix.IMPORT)
model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)

solver = pyo.SolverFactory("glpk")
solver.options = {"ranges": "sensibilidad.txt"}

results = solver.solve(model, symbolic_solver_labels=True)
print(results)
model.display()

"""
Solución:

D1B = 15
D1C = 30
D2A = 30
D2B = 25

Los que faltan son cero
"""

"""
Para el primer punto nos fijamos
en la columna de Activity Range de fichero
excepto de las restricciones no se saturan

No se satura el depósito 2

35 <= RD1 <= 70
55 <= RD2

0 <= RA <= 40
15 <= RB <= 50
5 <= RC <= 40
"""

print("\nDuales")
for i in model.dual:
    print(f"\t{i} = {model.dual[i]}")

"""
Duales
        RD1 = -1.0
        RD2 = 0.0
        RA = 5.0
        RB = 8.0
        RC = 5.0

Por cada unidad que apliemos los depósitos 
se reduce 1 por el primero y nada por el segundo

Por cada hectómetro cúbico que reduzcamos la necesidad
de los pueblos:
el primero reduce el coste por 5
el segundo reduce el coste por 8
el tercero reduce el coste por 5
"""