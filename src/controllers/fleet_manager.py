import json
import time
from datetime import datetime

class FleetManager:
    def __init__(self, nav_graph, traffic_manager):
        self.nav_graph = nav_graph
        self.traffic_manager = traffic_manager
        self.robots = {}
        self.robot_colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF", 
                           "#FFA500", "#800080", "#008000", "#000080", "#800000", "#008080"]
        self.color_index = 0
        self.log_file = "logs/fleet_logs.txt"
        self.selected_robot = None
        self.initialize_log_file()
    
    def initialize_log_file(self):
        with open(self.log_file, 'w') as f:
            f.write(f"=== Fleet Management System Log - {datetime.now()} ===\n")
    
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        log_message = f"[{timestamp}] {message}"
        with open(self.log_file, 'a') as f:
            f.write(log_message + "\n")
    
    def spawn_robot(self, vertex):
        robot_id = len(self.robots) + 1
        color = self.robot_colors[self.color_index % len(self.robot_colors)]
        self.color_index += 1
        
        from src.models.robot import Robot
        new_robot = Robot(robot_id, vertex, color, self)
        self.robots[robot_id] = new_robot
        
        self.log(f"Robot {robot_id} spawned at vertex {vertex['name']}")
        return new_robot
    
    def assign_task(self, robot, target_vertex):
        if robot.status == "moving" or robot.status == "waiting":
            self.log(f"Robot {robot.id} is already moving or waiting. Cannot assign new task.")
            return False, "Robot is already moving or waiting"
        
        start_id = robot.current_vertex["id"]
        end_id = target_vertex["id"]
        
        path = self.nav_graph.find_path(start_id, end_id)
        
        if not path:
            self.log(f"No path found from {robot.current_vertex['name']} to {target_vertex['name']}")
            return False, "No path found"
        
        self.log(f"Assigning task to Robot {robot.id}: Move from {robot.current_vertex['name']} to {target_vertex['name']}")
        success = robot.assign_task(target_vertex, path)
        
        return success, "Task assigned successfully" if success else "Failed to assign task"
    
    def select_robot(self, robot_id):
        if robot_id in self.robots:
            self.selected_robot = self.robots[robot_id]
            self.log(f"Selected Robot {robot_id}")
            return True
        return False
    
    def get_robot_at_position(self, x, y, tolerance=15):
        for robot_id, robot in self.robots.items():
            if abs(robot.x - x) <= tolerance and abs(robot.y - y) <= tolerance:
                return robot
        return None
    
    def stop_all_robots(self):
        for robot in self.robots.values():
            robot.stop_movement()
        self.log("All robots stopped")