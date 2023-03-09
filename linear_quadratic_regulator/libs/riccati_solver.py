import numpy as np
import numpy.linalg as LA
from tqdm import tqdm

class RiccatiSolver:
    # def __init__ (self):
    #     a=0
        
    # def solverIteration (self, A, B, Q, R, dt=0.001, tolerance = 1e-5, iter_max=100000):
    #     P=Q
        
    #     AT = np.array(A).T 
    #     BT = np.array(B).T
    #     Rinv = LA.inv(R)
        
    #     for i in tqdm(range(iter_max)): 
    #         diff = abs((P * A + AT * P - P * B * Rinv * P + Q) * dt)
    #         if diff < tolerance:
    #             print("iteratio_number = %d", i)
    #             return True
    #         P = P + (P * A + AT * P - P * B * Rinv * P + Q) * dt
        
    #     return False
    
    def solverArimotoPotter(self, A, B, Q, R):
        # Male Hamiltonian
        Hm = np.block([[A.T, -B@LA.inv(R)@B.T],[-Q, -A]])
        # Get eigen calue and eigen vector
        eigen_value, eigen_vector = LA.eig(Hm)
        
        n=len(eigen_vector[0])//2
        print(n)
        # U_11, U_21 = np.empty([0,0]), np.empty([0,0])
        
        # Sort eigen values
        index_array = sorted([i for i in range (2*n)], key=lambda x:eigen_value[x].real)
        
        U_11=np.array([eigen_vector[:n, index_array[0]]])
        U_21=np.array([eigen_vector[n:, index_array[0]]])
        # Get n vectors along the sort.
        for i in index_array[1:n]:
            U_11 = np.append(U_11, np.array([eigen_vector[:n,i]]), axis=0)
            U_21 = np.append(U_21, np.array([eigen_vector[n:,i]]), axis=0)
        
        # Return P
        U_11=U_11.T
        U_21=U_21.T
        if LA.det(U_11) != 0:
            return U_21 @ LA.inv(U_11)
        else:
            print("Warning: U_11 has wrong matrix. Result is probably wrong.")
            return U_21 @ LA.pinv(U_11)
        
        
if __name__== "__main__":
    solver = RiccatiSolver()
    
        
         
        
        
        
        
        
        
        
        




