import time
import threading
import math

class Robot:
    def __init__(self, robot_id, start_vertex, color, fleet_manager):
        self.id = robot_id
        self.current_vertex = start_vertex
        self.target_vertex = None
        self.path = []
        self.current_lane = None
        self.status = "idle"
        self.color = color
        self.fleet_manager = fleet_manager
        self.x = start_vertex["x"]
        self.y = start_vertex["y"]
        self.move_speed = 50
        self.move_thread = None
        self.stop_thread = False
    
    def assign_task(self, target_vertex, path):
        self.target_vertex = target_vertex
        self.path = path
        self.status = "moving"
        
        if self.move_thread is None or not self.move_thread.is_alive():
            self.stop_thread = False
            self.move_thread = threading.Thread(target=self.start_movement)
            self.move_thread.daemon = True
            self.move_thread.start()
        
        return True
    
    def start_movement(self):
        current_path_index = 0
        
        while current_path_index < len(self.path) - 1 and not self.stop_thread:
            current_vertex_id = self.path[current_path_index]
            next_vertex_id = self.path[current_path_index + 1]
            
            lane = (current_vertex_id, next_vertex_id)
            reserved = self.fleet_manager.traffic_manager.request_lane(self, lane)
            
            if not reserved:
                self.status = "waiting"
                time.sleep(0.5)
                continue
            
            self.status = "moving"
            self.current_lane = lane
            
            current_vertex = self.fleet_manager.nav_graph.get_vertex_by_id(current_vertex_id)
            next_vertex = self.fleet_manager.nav_graph.get_vertex_by_id(next_vertex_id)
            
            self.move_between_vertices(current_vertex, next_vertex)
            
            self.fleet_manager.traffic_manager.release_lane(self, lane)
            
            self.current_vertex = next_vertex
            self.x = next_vertex["x"]
            self.y = next_vertex["y"]
            current_path_index += 1
            
            self.fleet_manager.log(f"Robot {self.id} moved to {next_vertex['name']}")
        
        if not self.stop_thread:
            self.status = "idle"
            if self.current_vertex.get("is_charger", False):
                self.status = "charging"
            
            self.target_vertex = None
            self.current_lane = None
            self.fleet_manager.log(f"Robot {self.id} completed task at {self.current_vertex['name']}")
    
    def move_between_vertices(self, start_vertex, end_vertex):
        start_x, start_y = start_vertex["x"], start_vertex["y"]
        end_x, end_y = end_vertex["x"], end_vertex["y"]
        
        distance = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
        total_time = distance / self.move_speed
        
        steps = max(int(total_time * 30), 1)
        
        for step in range(1, steps + 1):
            if self.stop_thread:
                break
                
            progress = step / steps
            self.x = start_x + (end_x - start_x) * progress
            self.y = start_y + (end_y - start_y) * progress
            
            time.sleep(total_time / steps)
    
    def stop_movement(self):
        self.stop_thread = True
        if self.move_thread and self.move_thread.is_alive():
            self.move_thread.join(timeout=1)
        self.status = "idle"