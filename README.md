# Fleet Management System with Traffic Negotiation for Multi-Robots

## Approach

This project implements a **graph-based fleet management system** for multiple autonomous robots, ensuring smooth navigation and efficient traffic handling. The core of this system is built around **real-time pathfinding, lane reservation, and a dynamic GUI**, enabling intuitive interaction and monitoring of robot movements.

### Key Aspects of the Approach:

1. **Graph-Based Navigation**
   - The environment is represented as a **graph** where:
     - Nodes (vertices) represent locations.
     - Edges (lanes) define paths between locations.
   - This allows for efficient path planning and decision-making.

2. **Real-Time Traffic Management**
   - A **traffic manager** ensures safe movement by preventing multiple robots from occupying the same lane.
   - Robots request lane access before moving, reducing congestion and avoiding deadlocks.

3. **Multi-Robot Coordination**
   - Each robot follows an assigned **path** with dynamic obstacle avoidance.
   - Robots **wait if a lane is occupied**, ensuring smooth coordination without collisions.

4. **Scalable and Interactive GUI**
   - The GUI provides a **visual representation** of robot movement, lane occupancy, and navigation.
   - Users can **select, assign tasks, and monitor** robots in real-time.
   - Features include **zoom, pan, and interactive clicks** to enhance usability.

## Strengths of This Approach

### ✅ **Efficient Pathfinding and Navigation**
- The **graph-based structure** enables efficient path search, ensuring that robots take the shortest available routes.
- **Real-time traffic control** prevents collisions and optimizes robot flow.

### ✅ **Scalable Multi-Robot System**
- The approach is **scalable**, allowing multiple robots to operate simultaneously.
- Supports **dynamic robot spawning** at any node without disrupting the system.

### ✅ **Effective Traffic Negotiation**
- **Lane reservation logic** ensures only one robot moves through a path segment at a time.
- Prevents **traffic deadlocks** and congestion.

### ✅ **User-Friendly and Intuitive Interface**
- **Interactive GUI** provides real-time visualization of the fleet’s status.
- Users can **assign tasks, track movement, and monitor robot states** with ease.

### ✅ **Thread-Based Real-Time Execution**
- Uses **multi-threading** for parallel execution of robot movements.
- Robots update their position smoothly, improving simulation realism.

## Installation and Setup

### Prerequisites
- Python 3.x
- Pip package manager

### Steps to Run the Project
1. Clone the repository:
   ```sh
   git clone https://github.com/shansita24/GoatPSGHackathon_22PC21
   cd fleet-management
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Start the application:
   ```sh
   python -m src.main
   ```

## Working
- ![image](https://github.com/user-attachments/assets/1.png)
  This image shows the gui where we can view the graph with the corresponding vertices and edges which can be changed in the nav_graph.json file.
- ![image](https://github.com/user-attachments/assets/2.png)
  After selection of the vertex B when we click on vertex A the robot moves from B to A in the shortest route possible.
- ![image](https://github.com/user-attachments/assets/3.png)
  This image shows the Robot 1 charging on the vertex G again this charging vertices also can be changed in the nav_graph.json file.Now we can spawn a new Robot 2 again in the vertex B, now this robot 2 would not be able to pass through or be able to be placed on the vertex in which robot 1 is present.
- ![image](https://github.com/user-attachments/assets/4.png)

## 🎬 Demo Video  
📺 **[Click here to watch the demo](https://drive.google.com/file/d/1kWCWr9Ho79J3QptR_fbKF6V5ZFtmoI3h/view?usp=sharing)** 


## Conclusion

This approach provides a **highly interactive, scalable, and efficient** fleet management solution. By integrating **graph-based navigation, traffic negotiation, and a real-time GUI**, it offers a **practical and user-friendly** system for managing autonomous robots in dynamic environments.
