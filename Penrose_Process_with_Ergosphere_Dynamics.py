import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint

# ==========================
# Kerr Black Hole Parameters
# ==========================
M = 1.0
a = 0.9

# Angular coordinate
phi = np.linspace(0, 20*np.pi, 4000)

# ==========================
# Particle Motion Equation
# ==========================
def trajectory(y, phi):
    r, dr = y

    delta = r**2 - 2*M*r + a**2

    if abs(delta) < 0.05:
        delta = 0.05

    d2r = -(M*r/delta)*dr**2

    return [dr, d2r]

# Solve orbit
sol = odeint(trajectory, [3.0, -0.02], phi)

r = np.clip(sol[:,0], 0.6, 10)

x = r*np.cos(phi)
y = r*np.sin(phi)

# ==========================
# Ergosphere
# ==========================
phi_ergo = np.linspace(0, 2*np.pi, 1000)

r_ergo = M + np.sqrt(
    M**2 - a**2*np.cos(phi_ergo)**2
)

# Event Horizon
r_h = M + np.sqrt(M**2 - a**2)

# ==========================
# Figure
# ==========================
plt.style.use("dark_background")

fig, ax = plt.subplots(figsize=(10,10))

# ==========================
# Stars
# ==========================
np.random.seed(42)

stars_x = np.random.uniform(-10,10,800)
stars_y = np.random.uniform(-10,10,800)

ax.scatter(
    stars_x,
    stars_y,
    s=2,
    color='white'
)

# ==========================
# Ergosphere Glow
# ==========================
ax.fill(
    r_ergo*np.cos(phi_ergo),
    r_ergo*np.sin(phi_ergo),
    color='orange',
    alpha=0.25,
    label="Ergosphere"
)

ax.plot(
    r_ergo*np.cos(phi_ergo),
    r_ergo*np.sin(phi_ergo),
    color='orange',
    linewidth=3
)

# ==========================
# Black Hole Shadow
# ==========================
shadow = plt.Circle(
    (0,0),
    r_h+0.3,
    color='purple',
    alpha=0.2
)
ax.add_patch(shadow)

# Event Horizon
black_hole = plt.Circle(
    (0,0),
    r_h,
    color='black'
)
ax.add_patch(black_hole)

# ==========================
# Accretion Disk
# ==========================
for rr in np.linspace(r_h+0.3, 3.2, 15):

    ring = plt.Circle(
        (0,0),
        rr,
        fill=False,
        color='cyan',
        alpha=0.15
    )

    ax.add_patch(ring)

# ==========================
# Relativistic Jets
# ==========================
ax.plot(
    [0,0],
    [3,8],
    color='magenta',
    linewidth=4,
    alpha=0.7
)

ax.plot(
    [0,0],
    [-3,-8],
    color='magenta',
    linewidth=4,
    alpha=0.7
)

# ==========================
# Animated Particle
# ==========================
trail, = ax.plot(
    [],
    [],
    color='cyan',
    linewidth=3,
    label='Particle'
)

particle, = ax.plot(
    [],
    [],
    'o',
    color='lime',
    markersize=10
)

# Energy extraction particles
escape_particle, = ax.plot(
    [],
    [],
    'o',
    color='yellow',
    markersize=8
)

fall_particle, = ax.plot(
    [],
    [],
    'o',
    color='red',
    markersize=8
)

# ==========================
# Animation Function
# ==========================
split_frame = 1500

def animate(i):

    trail.set_data(
        x[:i],
        y[:i]
    )

    particle.set_data(
        [x[i]],
        [y[i]]
    )

    # Penrose Split
    if i > split_frame:

        escape_particle.set_data(
            [x[i] + 1.2],
            [y[i] + 0.5]
        )

        fall_particle.set_data(
            [x[i] - 0.6],
            [y[i] - 0.6]
        )

    return (
        trail,
        particle,
        escape_particle,
        fall_particle
    )

ani = FuncAnimation(
    fig,
    animate,
    frames=len(x),
    interval=5,
    blit=True
)

# ==========================
# Labels
# ==========================
ax.set_title(
    "Animated Penrose Process in Kerr Ergosphere",
    fontsize=18
)

ax.set_xlabel("x")
ax.set_ylabel("y")

ax.set_xlim(-10,10)
ax.set_ylim(-10,10)

ax.set_aspect('equal')

ax.grid(alpha=0.2)

ax.legend()

plt.show()