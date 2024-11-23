## Adaptive Navigation Algorithms for a 2D Self-Driving Car Simulation

This project explores the application of adaptive navigation algorithms within a 2D simulation of a self-driving car. It implements and compares the performance of **Feed-Forward Neural Networks (FNNs)** and **Recurrent Neural Networks (RNNs)**, using the **NEAT (NeuroEvolution of Augmenting Topologies)** algorithm for evolving neural network structures. The project focuses on collision avoidance and pathfinding through reinforcement learning.

### Features
- **Simulation Environment**: 
  - Developed using the Python-based **Pygame** library.
  - Includes two real-world Formula 1 circuits, **Austin** and **Silverstone**, each with unique challenges.
  - Dynamic obstacles with oscillating motion to test adaptability.

- **Neural Network Architectures**:
  - **Feed-Forward Networks**: Efficient in simpler scenarios, leveraging direct input-output mappings.
  - **Recurrent Networks**: Perform better in complex environments due to memory retention and sequential decision-making.

- **Reinforcement Learning**:
  - Fitness function rewards forward movement and penalizes collisions, driving adaptive behavior.
  - Real-time decision-making based on sensor data from 9 simulated sensors.

- **Algorithm**:
  - Utilizes NEAT for evolving network weights and topologies, ensuring adaptive performance over generations.

### Methodology
- **Simulation Environment**:
  - Circuit layouts with variable starting angles.
  - Collision detection and path optimization based on neural network outputs.
- **Adaptive Learning**:
  - Fitness evaluation over multiple iterations (300+) to identify optimal behaviors.
  - Real-time reinforcement learning to improve decision-making.
- **Neural Network Comparison**:
  - Performance analysis based on fitness scores, lap completion rates, and collision avoidance.
  - Graphical comparison of learning trends across networks and circuit configurations.

### Results
- RNNs demonstrated superior performance in complex environments due to their ability to retain and reuse past information.
- FNNs excelled in straightforward scenarios with fewer environmental variables, offering faster initial learning and simpler decision-making.

### Future Research Directions
- **Extended Simulations**: Test networks under longer simulation durations to evaluate performance stability.
- **Increased Complexity**: Introduce dynamic weather, varied obstacle patterns, and more intricate circuit layouts.
- **Multi-Objective Optimization**: Balance objectives like speed, safety, and energy efficiency.

### Libraries and Tools
- **Pygame**: For simulation graphics and event handling.
- **NEAT-Python**: To evolve neural network architectures.
- Mathematical models for car dynamics and sensor logic.

---

This repository serves as a foundation for exploring adaptive navigation in autonomous systems. Contributions are welcome for extending the research scope or improving the simulation's features.
