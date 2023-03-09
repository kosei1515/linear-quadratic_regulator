from linear_quadratic_regulator.libs import riccati_solver
from linear_quadratic_regulator.libs import lqr
import yaml
import os
import sys
import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm

class InvertePendulum:
    def __init__(self):
        config_path = sys.argv[1]
        with open(config_path) as yml:
            self.config = yaml.safe_load(yml)
            
        self.g = self.config['phisical_parameters']['g']
        self.m1 = self.config['phisical_parameters']['m1']
        self.m2 = self.config['phisical_parameters']['m2']
        self.l = self.config['phisical_parameters']['l']
        
        self.lqr = lqr.LQR()
        
    def non_linear_state_equation(self, x, F):
        p = x[0]
        theta = x[1]
        dp = x[2]
        dtheta = x[3]

        dx = np.zeros(4)

        dx[0] = dp
        dx[1] = dtheta
        dx[2] = (-self.l*self.m2*np.sin(theta)*dtheta**2 + self.g*self.m2*np.sin(2*theta)/2 + F)/(self.m1 + self.m2*np.sin(theta)**2)
        dx[3] = (self.g*(self.m1 + self.m2)*np.sin(theta) - (self.l*self.m2*np.sin(theta)*dtheta**2 - F)*np.cos(theta))/(self.l*(self.m1 + self.m2*np.sin(theta)**2))
        
        return dx
            
    def linear_model_matrix(self):
        A = np.array([ 
                [0, 0, 1, 0],
                [0, 0, 0, 1],
                [0, self.g*self.m2/self.m1, 0, 0],
                [0, self.g*(self.m1 + self.m2)/(self.l*self.m1), 0, 0]
            ])

        B = np.array([
                [0],
                [0],
                [1/self.m1],
                [1/(self.l*self.m1)]
            ])

        return A, B

    def plot_graph(self, t, data, labels, scales):
        fig = plt.figure()

        nrow = int(np.ceil(data.shape[1] / 2))
        ncol = min(data.shape[1], 2)

        for i in range(data.shape[1]):
            ax = fig.add_subplot(nrow, ncol, i + 1)
            ax.plot(t, data[:,i] * scales[i])

            ax.set_xlabel('Time [s]')
            ax.set_ylabel(labels[i])
            ax.grid()
            ax.set_xlim(t[0], t[-1])

        fig.tight_layout()
        
    def draw_pendulum(self, ax, t, xt, theta, l):
        cart_w = 1.0
        cart_h = 0.4
        radius = 0.1

        cx = np.array([-0.5, 0.5, 0.5, -0.5, -0.5]) * cart_w + xt
        cy = np.array([0.0, 0.0, 1.0, 1.0, 0.0]) * cart_h + radius * 2.0

        bx = np.array([0.0, l * np.sin(-theta)]) + xt
        by = np.array([cart_h, l * np.cos(-theta) + cart_h]) + radius * 2.0

        angles = np.arange(0.0, np.pi * 2.0, np.radians(3.0))
        ox = radius * np.cos(angles)
        oy = radius * np.sin(angles)

        rwx = ox + cart_w / 4.0 + xt
        rwy = oy + radius
        lwx = ox - cart_w / 4.0 + xt
        lwy = oy + radius

        wx = ox + float(bx[1])
        wy = oy + float(by[1])

        ax.cla()
        ax.plot(cx, cy, "-b")
        ax.plot(bx, by, "-k")
        ax.plot(rwx, rwy, "-k")
        ax.plot(lwx, lwy, "-k")
        ax.plot(wx, wy, "-k")
        ax.axis("equal")
        # ax.set_xlim([-cart_w, cart_w])
        ax.set_title("t:%5.2f x:%5.2f theta:%5.2f" % (t, xt, theta))

    
    def main(self):
        A, B = self.linear_model_matrix()
        Q = np.array(self.config['lqr']['Q'])
        R = np.array(self.config['lqr']['R'])
        
        print(Q)
        print(R)

        P, K, E = self.lqr.lqr(A, B, Q, R)

        T = self.config['simulation']['terminal_time']
        dt = self.config['simulation']['discrete_time']
        x0 = np.array(self.config['simulation']['x0']) #+ np.random.randn(1)
        
        print(dt)

        t = np.arange(0, T, dt)
        x = np.zeros([len(t), 4])
        u = np.zeros([len(t), 1])

        x[0,:] = x0
        u[0] = 0

        for i in range(1, len(t)):
            u[i] = -K @ x[i-1,:] #+ np.random.randn(1)
            # print(u)
            dx = self.non_linear_state_equation(x[i-1,:], u[i])
            x[i,:] = x[i-1,:] + dx * dt

        plt.close('all')

        lbls = (r'$p$ [m]', r'$\theta$ [deg]', r'$\dot{p}$ [m/s]', r'$\dot{\theta}$ [deg/s]')
        scls = (1, 180/np.pi, 1, 180/np.pi)
        self.plot_graph(t, x, lbls, scls)

        lbls = (r'$F$ [N]',)
        scls = (1,)
        self.plot_graph(t, u, lbls, scls)

        fig, ax = plt.subplots()
        for i in range(len(t)):
            if i % 1 == 0:
                self.draw_pendulum(ax, t[i], x[i,0], x[i,1], self.l)
                plt.pause(0.01)
        
    
if __name__ == "__main__":
    print("test")
    problem = InvertePendulum()
    problem.main()