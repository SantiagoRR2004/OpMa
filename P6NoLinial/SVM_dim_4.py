# Ejemplo de aplicación de optimización en aprendizaje automático: Support Vectpr Machines (SVM).
# Ejemplo tomado de: https://mobook.github.io/MO-book/notebooks/05/04-svm-binary-classification.html

# Bibliotecas necesarias: pyomo matplotlib numpy pandas scikit-learn

# Establecemos los optimizadores:
# Programación No lineal
solver_NLO = "ipopt"

# Programación Lineal
solver_LO = "glpk"

import pyomo.environ as pyo 

# Las siguientes bibliotecas solo son necesarias para calcular las estadísticas y mostrar datos
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


# Definimos los objetos con los interfaces de los solvers lineales y no lineales
SOLVER_LO = pyo.SolverFactory(solver_LO)
SOLVER_NLO = pyo.SolverFactory(solver_NLO)

########################################
# Funciones y clases auxiliares        ########################################################################
########################################

# Linear Support Vector Machine (SVM) class
class LinearSVM:
    # Initialize the Linear SVM with weights w and bias b
    def __init__(self, w, b):
        self.w = pd.Series(w)
        self.b = float(b)

    # Call method to compute the decision function using the input data X
    def __call__(self, X):
        return np.sign(X.dot(self.w) + self.b)

    # String representation method for the Linear SVM class
    def __repr__(self):
        return f"LinearSvm(w = {self.w.to_dict()}, b = {self.b})"


#función que proporciona las medidas de validación de la clasificación y la matriz de confusión
def validate(y_true, y_pred, verbose=True):
    # Calculate the elements of the confusion matrix
    true_positives = sum((y_true > 0) & (y_pred > 0))
    false_negatives = sum((y_true > 0) & (y_pred < 0))
    false_positives = sum((y_true < 0) & (y_pred > 0))
    true_negatives = sum((y_true < 0) & (y_pred < 0))
    total = true_positives + true_negatives + false_positives + false_negatives

    # Calculate the Matthews correlation coefficient (MCC)
    mcc_numerator = (true_positives * true_negatives) - (
        false_positives * false_negatives
    )
    mcc_denominator = np.sqrt(
        (true_positives + false_positives)
        * (true_positives + false_negatives)
        * (true_negatives + false_positives)
        * (true_negatives + false_negatives)
    )
    mcc = mcc_numerator / mcc_denominator

    if verbose:
        print(f"Matthews correlation coefficient (MCC) = {mcc:0.3f}")

        # report sensitivity and precision, and accuracy
        sensitivity = true_positives / (true_positives + false_negatives)
        precision = true_positives / (true_positives + false_positives)
        accuracy = (true_positives + true_negatives) / total

        print(f"Sensitivity = {100 * sensitivity: 0.1f}%")
        print(f"Precision = {100 * precision: 0.1f}%")
        print(f"Accuracy = {100 * accuracy: 0.1f}%")

        # Display the binary confusion matrix
        confusion_matrix = pd.DataFrame(
            [
                [true_positives, false_negatives],
                [false_positives, true_negatives],
            ],
            index=["Actual Positive", "Actual Negative"],
            columns=["Predicted Positive", "Predicted Negative"],
        )
        print(confusion_matrix,"\n")
    return mcc

# Función que dibuja e imprime el comportamiento de la herramienta.
def test(svm, X_test, y_test):
    y_pred = svm(X_test)
    print(svm, "\n")
    validate(y_test, y_pred)


# Función que crea el modelo de optimización lineal para SVM
def svm_linear(X, y, lambd=1):
    m = pyo.ConcreteModel("Linear SVM")

    # Use dataframe columns and index to index variables and constraints
    m.P = pyo.Set(initialize=X.columns)
    m.N = pyo.Set(initialize=X.index)

    # Decision variables
    m.wp = pyo.Var(m.P, domain=pyo.NonNegativeReals)
    m.wn = pyo.Var(m.P, domain=pyo.NonNegativeReals)
    m.b = pyo.Var()
    m.z = pyo.Var(m.N, domain=pyo.NonNegativeReals)

    def w(m, p):
        return m.wp[p] - m.wn[p]
    m.w = pyo.Expression(m.P, rule=w)
    
    
    def lasso(m):
        return sum(m.z[i] for i in m.N) / len(m.N) + lambd * sum(
            m.wp[p] + m.wn[p] for p in m.P
        )
    m.lasso = pyo.Objective(rule=lasso, sense=pyo.minimize)
    
    
    def hingeloss(m, i):
        return m.z[i] >= 1 - y[i] * (sum(m.w[p] * X.loc[i, p] for p in m.P) + m.b)
    m.hingeloss = pyo.Constraint(m.N, rule=hingeloss)
    
    return m
    
    
# Función que crea el modelo de **optimización Cuadrático** para SVM
def svm_quadratic(X, y, c=1):
    m = pyo.ConcreteModel("SVM quadratic with L2 regularization")

    # Use dataframe columns and index to index variables and constraints
    m.P = pyo.Set(initialize=X.columns)
    m.N = pyo.Set(initialize=X.index)

    # Decision variables
    m.w = pyo.Var(m.P)
    m.b = pyo.Var()
    m.z = pyo.Var(m.N, domain=pyo.NonNegativeReals)

    
    def qp(m):
        return sum(m.w[i] ** 2 for i in m.P) / 2 + (c / len(m.N)) * sum(
            m.z[i] for i in m.N
        )
    m.qp = pyo.Objective(rule=qp, sense=pyo.minimize)
    
    
    def hingeloss(m, i):
        return m.z[i] >= 1 - y[i] * (sum(m.w[p] * X.loc[i, p] for p in m.P) + m.b)
    m.hingeloss = pyo.Constraint(m.N, rule=hingeloss)

    return m

############################################################
# FIN funciones y clases auxiliares                        ############################################################
############################################################



############################################################
# PASO 1: Leer los datos de internet 
# (Más información de estos datos en: https://archive.ics.uci.edu/dataset/267/banknote+authentication)
df = pd.read_csv(
    "https://raw.githubusercontent.com/mobook/MO-book/main/datasets/data_banknote_authentication.txt",
    header=None,
)
df.columns = ["variance", "skewness", "curtosis", "entropy", "class"]
df.name = "Banknotes"



#########################
# PASO 2: Separar el conjunto de datos de entrenamiento de los de validación.

# En este caso apartamos un 20% de los datos para la validación de la herramienta


# create training and validation test sets, random_state=0 for reproducibility
df_train, df_test = train_test_split(df, test_size=0.2, random_state=0)

# select training features (NOTA: Sólo se seleccionan 2 para poder dibujar el comportamiento del SVM)
features = ["variance", "skewness", "curtosis", "entropy"]

# separate into features and outputs
X_train = df_train[features]
y_train = 1 - 2 * df_train["class"]

# separate into features and outputs
X_test = df_test[features]
y_test = 1 - 2 * df_test["class"]

# Muestra cuantos datos hay en cada subconjunto de datos
xtrain_samples = df_train.shape[0]
xtest_samples = df_test.shape[0]

print(f'There are {xtrain_samples} samples for training and {xtest_samples} samples for testing.')

#######################################################
# PASO 3: Encontrar el mejor hiperplano de separación
#           (diferentes opciones: Lineal, cuadrático, dual , kernel, .....

### Linear optimization model

print("\nLinear Support Vector Machine")
# Se crea el modelo de optimización con los datos de entrenamiento
m = svm_linear(X_train, y_train)
# Se resuelve utilizando un optimizador lineal
SOLVER_LO.solve(m)
# Se almacenan los parámetros que definen el hiperplano separador
w = pd.Series([m.w[p]() for p in m.P], index=m.P)
b = m.b()

######################################################
# PASO 4: se comprueba el comportamiento del plano encontrado
#         con los datos de validación

# Se crea un objeto de la clase LinearSVM con los datos del hiperplano obtenido
linear_svm = LinearSVM(w, b)
# Se muestra gráfica y analíticamente el comportamiento sobre los datos de validación
test(linear_svm, X_test, y_test)


# Quadratic optimization model

print("\nQuadratic Support Vector Machine")
# Se crea el modelo de optimización los datos de entrenamiento
m = svm_quadratic(X_train, y_train)
# Se resuelve utilizando un optimizador NO lineal
SOLVER_NLO.solve(m)
# Se almacenan los parámetros que definen el hiperplano separador
w = pd.Series([m.w[p]() for p in m.P], index=m.P)
b = m.b()

######################################################
# PASO 4: se comprueba el comportamiento del plano encontrado
#         con los datos de validación

# Se crea un objeto de la clase LinearSVM con los datos del plano obtenido
quadratic_svm = LinearSVM(w, b)
# Se muestra gráfica y analíticamente el comportamiento sobre los datos de validación
test(quadratic_svm, X_test, y_test)
