import numpy as np
import numpy.linalg as LA
from linear_quadratic_regulator.libs import riccati_solver

def test_1():
    solver = riccati_solver.RiccatiSolver()
    A = np.array([[3., 1.],[0., 1.]])
    B = np.array([[1.2], [1.]])
    Q = np.array([[1., 0.2], [0.2, 1.0]])
    R = np.array([[1.]])
    P = solver.solverArimotoPotter(A, B, Q, R)
    print("P")
    print(P)
    print("RiccatiEquation: left part")
    print(A@P + P@A.T + Q - P@B@LA.inv(R)@B.T@P)

if __name__ == "__main__":
    pass