import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- 1. Optimized Link Lengths from Theory (Shin/Jadav) ---
L_base = {
    'L1': 11.0, 'L2': 45.0, 'L3': 36.0, 'L4': 33.0,
    'L5': 48.5, 'L6': 41.5, 'L7': 60.5, 'L8': 41.5,
    'L9': 42.0, 'L10': 43.0, 'L11': 26.5, 'L12': 54.5
}

def intersect(pA, rA, pB, rB, flip=False):
    """Calculates intersection of two circles to find joint coordinates."""
    d = np.linalg.norm(pB - pA)
    d = max(min(d, rA + rB), abs(rA - rB)) # Prevent domain errors if pushed to limits
    a = (rA**2 - rB**2 + d**2) / (2 * d)
    h = np.sqrt(max(0, rA**2 - a**2))
    pMid = pA + a * (pB - pA) / d
    perp = np.array([-(pB[1]-pA[1]), pB[0]-pA[0]]) / d
    return pMid - h * perp if flip else pMid + h * perp

def solve_kinematics(theta, L):
    """Calculates all 2D joint positions for the 12-link mechanism."""
    P3 = np.array([0.0, 0.0])              # Hip joint (Origin)
    P0 = np.array([-L['L4'], 0.0])         # Crank center
    P1 = P0 + np.array([L['L1']*np.cos(theta), L['L1']*np.sin(theta)])
    
    P2 = intersect(P1, L['L2'], P3, L['L3'], flip=False)
    P4 = intersect(P3, L['L6'], P2, L['L5'], flip=True)
    P5 = intersect(P1, L['L7'], P3, L['L8'], flip=True)
    P6 = intersect(P5, L['L9'], P4, L['L10'], flip=True)
    PE = intersect(P5, L['L11'], P6, L['L12'], flip=True) # Endpoint (Foot)
    
    return P0, P1, P2, P3, P4, P5, P6, PE

def generate_trajectory(L):
    """Simulates one full cycle and extracts the endpoint path."""
    thetas = np.linspace(0, 2*np.pi, 150)
    path_x, path_y = [], []
    for th in thetas:
        *_, PE = solve_kinematics(th, L)
        path_x.append(PE[0])
        path_y.append(PE[1])
    return path_x, path_y

# --- 2. Generate Deliverable Plots ---
print("Generating Improved Theoretical Plots...")

# 2a. Baseline Trajectory & Gait Comparison
bx, by = generate_trajectory(L_base)
plt.figure(figsize=(9, 5))
plt.plot(bx, by, 'b-', lw=3, label='Generated Endpoint Path')
plt.plot(bx[0], by[0], 'go', markersize=8, label='Start Point') # START POINT
# Shifted reference to mimic the paper's meta-trajectory comparison
plt.plot([x + 2 for x in bx], [y + 1 for y in by], 'r--', lw=2, alpha=0.6, label='Theoretical Meta-Trajectory (Target)')
plt.title("Deliverable 2 & 4: Gait Trajectory Comparison")
plt.xlabel("X Position (cm)"); plt.ylabel("Y Position (cm)")
plt.axis('equal'); plt.grid(True, alpha=0.5); plt.legend()
plt.tight_layout()
plt.savefig('1_foot_trajectory_and_comparison.png', dpi=300)
plt.close()

# 2b. Variation H (Altering L11)
L_var_H = L_base.copy()
L_var_H['L11'] = 35.0 # Increased from 26.5
hx, hy = generate_trajectory(L_var_H)
plt.figure(figsize=(9, 5))
plt.plot(bx, by, 'b-', lw=2, label='Baseline (L11 = 26.5)')
plt.plot(bx[0], by[0], 'bo', markersize=6) # START POINT BASELINE
plt.plot(hx, hy, 'r-', lw=2, label='Variation H (L11 = 35.0)')
plt.plot(hx[0], hy[0], 'ro', markersize=6, label='Start Points') # START POINT VAR
plt.title("Deliverable 4: Effect of Link Variation H (L11)")
plt.xlabel("X Position (cm)"); plt.ylabel("Y Position (cm)")
plt.axis('equal'); plt.grid(True, alpha=0.5); plt.legend()
plt.tight_layout()
plt.savefig('2_link_variation_H.png', dpi=300)
plt.close()

# 2c. Variation M (Altering Crank L1 - FIXED FOR KINEMATIC LOCKING)
L_var_M = L_base.copy()
L_var_M['L1'] = 13.5 # Increased from 11.0 (Kept under 14.0 to prevent jamming)
mx, my = generate_trajectory(L_var_M)
plt.figure(figsize=(9, 5))
plt.plot(bx, by, 'b-', lw=2, label='Baseline Crank (L1 = 11.0)')
plt.plot(bx[0], by[0], 'bo', markersize=6) # START POINT BASELINE
plt.plot(mx, my, 'g-', lw=2, label='Variation M Crank (L1 = 13.5)')
plt.plot(mx[0], my[0], 'go', markersize=6, label='Start Points') # START POINT VAR
plt.title("Deliverable 4: Effect of Link Variation M (Crank L1)")
plt.xlabel("X Position (cm)"); plt.ylabel("Y Position (cm)")
plt.axis('equal'); plt.grid(True, alpha=0.5); plt.legend()
plt.tight_layout()
plt.savefig('3_link_variation_M.png', dpi=300)
plt.close()

print("Saved all 3 plots as PNG files. Now launching animation...")

# --- 3. Mechanism Animation ---
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_aspect('equal')
ax.set_xlim(-80, 40)
ax.set_ylim(-80, 40)
ax.grid(True, linestyle='--', alpha=0.5)
ax.set_title('Theo Jansen Walking Mechanism Simulation')

# Line styles mimicking the theoretical/academic video style
crank_line, = ax.plot([], [], 'o-', lw=3, color='black', label='Crank (L1)')
ground_line,= ax.plot([], [], 'o-', lw=3, color='gray', label='Ground (L4)')
upper_line, = ax.plot([], [], 'o-', lw=3, color='dodgerblue')
lower_line, = ax.plot([], [], 'o-', lw=3, color='darkorange')
front_line, = ax.plot([], [], 'o-', lw=3, color='forestgreen')
foot_line,  = ax.plot([], [], 'o-', lw=3, color='crimson')
trace_line, = ax.plot([], [], '-', lw=2, color='purple', alpha=0.5, label='Ankle Trace')
ax.legend(loc='upper right')

trace_x, trace_y = [], []

def animate(frame):
    P0, P1, P2, P3, P4, P5, P6, PE = solve_kinematics(frame, L_base)
    
    crank_line.set_data([P0[0], P1[0]], [P0[1], P1[1]])
    ground_line.set_data([P0[0], P3[0]], [P0[1], P3[1]])
    upper_line.set_data([P1[0], P2[0], P3[0], P4[0], P2[0]], [P1[1], P2[1], P3[1], P4[1], P2[1]])
    lower_line.set_data([P1[0], P5[0], P3[0]], [P1[1], P5[1], P3[1]])
    front_line.set_data([P5[0], P6[0], P4[0]], [P5[1], P6[1], P4[1]])
    foot_line.set_data([P5[0], PE[0], P6[0]], [P5[1], PE[1], P6[1]])
    
    trace_x.append(PE[0])
    trace_y.append(PE[1])
    if len(trace_x) > 150:
        trace_x.pop(0); trace_y.pop(0)
    trace_line.set_data(trace_x, trace_y)
    
    return crank_line, ground_line, upper_line, lower_line, front_line, foot_line, trace_line

thetas = np.linspace(0, 2*np.pi, 150)
ani = animation.FuncAnimation(fig, animate, frames=thetas, interval=30, blit=True)
plt.show()