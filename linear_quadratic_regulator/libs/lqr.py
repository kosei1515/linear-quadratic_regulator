from linear_quadratic_regulator.libs import riccati_solver
import numpy.linalg as LA

class LQR:
    def __init__(self):
        self.solver = riccati_solver.RiccatiSolver()
        pass
    
    def lqr(self, A, B, Q, R):
        P = self.solver.solverArimotoPotter(A, B, Q, R)
        K = LA.inv(R) @ B.T @ P
        E = LA.eigvals(A- B @ K)
        
        return P, K, E
    
if __name__ == "__main__":
    lqr_problem = LQR()