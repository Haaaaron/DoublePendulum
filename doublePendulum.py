import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


g = 9.81
dt = 0.03
l = 1
time = 120

w1 = 3*l/(2*g)
w2 = l/(2*g)

c1 = 7/(8*np.sqrt(5))
c2 = np.sqrt(5)/8

#ODE for small oscillations
def derivative(coord,t,l,g):

    theta1, theta1dot, theta2, theta2dot = coord
    
    theta1dotdot = g/(3*l)*(theta2 - 4*theta1)
    theta2dotdot = (4*g)/(3*l)*(theta1-theta2)

    return theta1dot, theta1dotdot, theta2dot, theta2dotdot

def normalCoordinate(coordEta,t,l,g):

    eta1, eta1dot, eta2, eta2dot = coordEta
    
    eta1dotdot = c1*np.cos(w1*t)*(1/w1)
    eta2dotdot = c2*np.cos(w2*t)*(1/w2)

    return eta1dot, eta1dotdot, eta2dot, eta2dotdot


t =  np.arange(0,time+dt,dt)

#initial conditions
coord0 = np.array([0.3,0,0.1,0])
coord0eta = np.array([c1,0,c2,0])

#Calclulating theta_1 and theta_2 with scipy odeint
coordTheta = odeint(derivative,coord0,t,args=(l,g))
#Calclulating normal coordinates with scipy odeint
coordEta = odeint(normalCoordinate,coord0eta,t,args=(l,g))

#Cartesian Coordinates
x1 = l*np.sin(coordTheta[:,0])
y1 = -l*np.cos(coordTheta[:,0])
x2 = x1 + l*np.sin(coordTheta[:,2])
y2 = y1 - l*np.cos(coordTheta[:,2])

#Uncomment this bit if you would like to plot the coordinates and normal coordinates of the system.
"""
thetaPlots, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex=True)
thetaPlots.suptitle("Potting the coordinates (upper) of the double pendulun weights, and the systems normal coordinates (lower)")
#Plotting Theta1
ax1.plot(t,coordTheta[:,0])
ax1.set_xlabel("t")
ax1.set_ylabel("$\Theta_1$(t)")

#Plotting Theta2
ax2.plot(t,coordTheta[:,2])
ax2.set_xlabel("t")
ax2.set_ylabel("$\Theta_2$(t)")

ax3.plot(t,coordEta[:,0])
ax3.set_xlabel("t")
ax3.set_ylabel("$\eta_1$(t)")

ax4.plot(t,coordEta[:,2])
ax4.set_xlabel("t")
ax4.set_ylabel("$\eta_2$(t)")

plt.show()

"""
#Plotting double pendulum animation:
animationFigure = plt.figure()
ax = animationFigure.add_subplot(111, autoscale_on=False, xlim=(-2, 2), ylim=(-2.5, 0))
ax.set_aspect('equal')

line, = ax.plot([], [], 'o-', lw=2)
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

#initial frame for animation
def init():
    line.set_data([], [])
    time_text.set_text('')
    return line, time_text


def animate(i):

    #coordinates of the masees and the origin 
    thisx = [0, x1[i], x2[i]]
    thisy = [0, y1[i], y2[i]]

    #draws lines between all three dots (origin, first mass, second mass)
    line.set_data(thisx, thisy)

    time_text.set_text(time_template % (i*dt))
    return line, time_text

ani = FuncAnimation(animationFigure, animate, np.arange(1, len(coordTheta)),
                              interval=25, blit=True, init_func=init)

plt.show()