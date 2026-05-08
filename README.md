# Theo Jansen Walking Mechanism Simulation

## Project Overview

This project presents the simulation and analysis of a Theo Jansen walking mechanism for gait generation using MATLAB. The mechanism generates a walking-like trajectory using a single rotational input and multiple interconnected linkages.

The project was developed for the course:

IE410: Introduction to Robotics

---

## Objectives

- Model a Theo Jansen linkage mechanism
- Generate gait-like foot trajectories
- Analyze the effect of varying link lengths
- Compare generated trajectories with theoretical gait curves
- Visualize mechanism motion through simulation

---

## Software Used

- MATLAB
- Simulink
- Simscape Multibody

---

## Results

### 1. Foot Trajectory and Gait Comparison

![Foot Trajectory](Results/1_foot_trajectory_and_comparison.jpg)

The generated endpoint trajectory closely resembles a natural gait-like walking curve. The dashed curve represents the theoretical target trajectory.

---

### 2. Effect of Link Variation H (L11)

![Variation H](Results/2_link_variation_H.jpg)

Increasing link length L11 changes the trajectory shape significantly, affecting both stride length and vertical motion.

---

### 3. Effect of Link Variation M (Crank L1)

![Variation M](Results/3_link_variation_M.jpg)

Changing crank length L1 increases the trajectory amplitude and modifies the walking motion characteristics.

---

### 4. Theo Jansen Mechanism Configuration

![Mechanism](Results/4_mechanism.jpg)

Simulation snapshot showing the linkage structure and ankle trajectory.

---

## Simulation Video

The complete simulation video is available in:

```text
Videos/Mechanism_Simulation.mp4
```

---

## Repository Structure

```text
Theo-Jansen-Walking-Mechanism
│
├── MATLAB_Code
├── Results
├── Videos
├── Report
└── README.md
```

---

## Conclusion

The Theo Jansen mechanism successfully generates a smooth gait-like trajectory using a single actuator. Link dimensions strongly influence the trajectory shape, stride length, and walking behavior. The generated results demonstrate how mechanical linkages can imitate biological walking patterns.
