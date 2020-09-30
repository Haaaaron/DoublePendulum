import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


g = 9.81
dt = 0.01
l = 1
time = 15

L1, L2 = 1, 1
m1, m2 = 1, 3
def derivative(y,t,l,g):

    theta1, theta1dot, theta2, theta2dot = y
    
    theta1dotdot = g/(3*l)*(theta2 - 4*theta1)
    theta2dotdot = (4*g)/(3*l)*(theta1-theta2)

    return theta1dot, theta1dotdot, theta2dot, theta2dotdot

#defining the time step and calcultation time in seconds

def deriv(y, t, L1, L2, m1, m2):
    """Return the first derivatives of y = theta1, z1, theta2, z2."""
    theta1, z1, theta2, z2 = y
    print(z1)
    c, s = np.cos(theta1-theta2), np.sin(theta1-theta2)
    theta1dot = z1
    z1dot = (m2*g*np.sin(theta2)*c - m2*s*(L1*z1**2*c + L2*z2**2) -
             (m1+m2)*g*np.sin(theta1)) / L1 / (m1 + m2*s**2)
    theta2dot = z2
    z2dot = ((m1+m2)*(L1*z1**2*s - g*np.sin(theta2) + g*np.sin(theta1)*c) + 
             m2*L2*z2**2*s*c) / L2 / (m1 + m2*s**2)
    return z1, z1dot, theta2dot, z2dot

t =  np.arange(0,time+dt,dt)

#initial conditions
coord0 = np.array([0.05,0,0.1,0])

coord = odeint(derivative,coord0,t,args=(l,g))
#coord = odeint(deriv,coord0,t,args=(L1,L2,m1,m2))

print(coord)

#Cartesian Coordinates
x1 = l*np.sin(coord[:,0])
y1 = -l*np.cos(coord[:,0])
x2 = x1 + l*np.sin(coord[:,2])
y2 = y1 - l*np.cos(coord[:,2])

fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-2, 2), ylim=(-2, 2))
ax.set_aspect('equal')
ax.grid()

line, = ax.plot([], [], 'o-', lw=2)
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)


def init():
    line.set_data([], [])
    time_text.set_text('')
    return line, time_text


def animate(i):
    thisx = [0, x1[i], x2[i]]
    thisy = [0, y1[i], y2[i]]

    line.set_data(thisx, thisy)
    time_text.set_text(time_template % (i*dt))
    return line, time_text

ani = FuncAnimation(fig, animate, np.arange(1, len(coord)),
                              interval=25, blit=True, init_func=init)

plt.show()