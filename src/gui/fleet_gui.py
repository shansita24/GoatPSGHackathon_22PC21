import tkinter as tk
from tkinter import messagebox
import json
import math

class FleetGUI:
    def __init__(self, root, fleet_manager, nav_graph):
        self.root = root
        self.fleet_manager = fleet_manager
        self.nav_graph = nav_graph
        
        self.root.title("Fleet Management System")
        self.root.geometry("1000x700")
        
        self.canvas_width = 800
        self.canvas_height = 600
        self.canvas_offset_x = 0
        self.canvas_offset_y = 0
        self.scale_factor = 1.0
        
        self.setup_ui()
        self.setup_bindings()
        
        self.update_interval = 50
        self.update_display()
    
    def setup_ui(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.control_frame = tk.Frame(self.main_frame, width=200)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas_frame = tk.Frame(self.main_frame)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg="white", width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.status_bar = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Controls
        tk.Label(self.control_frame, text="Fleet Management", font=("Arial", 14, "bold")).pack(pady=10)
        
        self.info_frame = tk.LabelFrame(self.control_frame, text="Information")
        self.info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.info_label = tk.Label(self.info_frame, text="Click on a vertex to spawn a robot\nSelect a robot and click on a vertex to set destination", justify=tk.LEFT)
        self.info_label.pack(pady=5)
        
        self.status_frame = tk.LabelFrame(self.control_frame, text="Status")
        self.status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.status_text = tk.Text(self.status_frame, height=10, width=25)
        self.status_text.pack(pady=5)
        
        # Buttons
        self.button_frame = tk.Frame(self.control_frame)
        self.button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.spawn_btn = tk.Button(self.button_frame, text="Spawn Robot", command=self.spawn_robot_ui)
        self.spawn_btn.pack(fill=tk.X, pady=2)
        
        self.clear_btn = tk.Button(self.button_frame, text="Clear Selection", command=self.clear_selection)
        self.clear_btn.pack(fill=tk.X, pady=2)
        
        self.stop_btn = tk.Button(self.button_frame, text="Stop All Robots", command=self.fleet_manager.stop_all_robots)
        self.stop_btn.pack(fill=tk.X, pady=2)
        
        # Calculate the initial scaling and offset
        self.calculate_transform()
    
    def setup_bindings(self):
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)  # Windows
        self.canvas.bind("<Button-4>", self.on_mousewheel)    # Linux scroll up
        self.canvas.bind("<Button-5>", self.on_mousewheel)    # Linux scroll down
        self.canvas.bind("<ButtonPress-2>", self.start_pan)
        self.canvas.bind("<B2-Motion>", self.pan)
        
    def calculate_transform(self):
        # Find bounds of the graph
        min_x = min(v["x"] for v in self.nav_graph.vertices)
        max_x = max(v["x"] for v in self.nav_graph.vertices)
        min_y = min(v["y"] for v in self.nav_graph.vertices)
        max_y = max(v["y"] for v in self.nav_graph.vertices)
        
        # Add padding
        padding = 50
        graph_width = max_x - min_x + 2 * padding
        graph_height = max_y - min_y + 2 * padding
        
        # Calculate scale factor to fit the graph in the canvas
        scale_x = self.canvas_width / graph_width
        scale_y = self.canvas_height / graph_height
        self.scale_factor = min(scale_x, scale_y)
        
        # Calculate offsets to center the graph
        self.canvas_offset_x = -min_x + padding + (self.canvas_width / self.scale_factor - graph_width) / 2
        self.canvas_offset_y = -min_y + padding + (self.canvas_height / self.scale_factor - graph_height) / 2
    
    def world_to_canvas(self, x, y):
        canvas_x = (x + self.canvas_offset_x) * self.scale_factor
        canvas_y = (y + self.canvas_offset_y) * self.scale_factor
        return canvas_x, canvas_y
    
    def canvas_to_world(self, canvas_x, canvas_y):
        world_x = canvas_x / self.scale_factor - self.canvas_offset_x
        world_y = canvas_y / self.scale_factor - self.canvas_offset_y
        return world_x, world_y
    
    def on_canvas_click(self, event):
        world_x, world_y = self.canvas_to_world(event.x, event.y)
        
        # Check if clicked on a robot
        robot = self.fleet_manager.get_robot_at_position(world_x, world_y)
        if robot:
            self.fleet_manager.select_robot(robot.id)
            self.update_status(f"Selected Robot {robot.id}")
            return
        
        # Check if clicked on a vertex
        vertex = self.nav_graph.get_vertex_by_position(world_x, world_y)
        if vertex:
            if self.fleet_manager.selected_robot:
                success, message = self.fleet_manager.assign_task(self.fleet_manager.selected_robot, vertex)
                self.update_status(message)
            else:
                self.spawn_robot(vertex)
    
    def on_mousewheel(self, event):
        # Zoom in/out centered on mouse position
        world_x, world_y = self.canvas_to_world(event.x, event.y)
        
        # Determine zoom direction
        if event.num == 5 or event.delta < 0:
            self.scale_factor *= 0.9  # Zoom out
        else:
            self.scale_factor *= 1.1  # Zoom in
        
        # Adjust offsets to zoom centered on mouse position
        new_world_x, new_world_y = self.canvas_to_world(event.x, event.y)
        self.canvas_offset_x += (world_x - new_world_x)
        self.canvas_offset_y += (world_y - new_world_y)
    
    def start_pan(self, event):
        self.canvas.scan_mark(event.x, event.y)
    
    def pan(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        # Update the offsets based on the canvas scrolling
        self.canvas_offset_x -= (self.canvas.canvasx(0) - self.canvas_width/2) / self.scale_factor
        self.canvas_offset_y -= (self.canvas.canvasy(0) - self.canvas_height/2) / self.scale_factor
    
    def spawn_robot(self, vertex):
        robot = self.fleet_manager.spawn_robot(vertex)
        self.update_status(f"Spawned Robot {robot.id} at {vertex['name']}")
    
    def spawn_robot_ui(self):
        self.update_status("Click on a vertex to spawn a robot")
    
    def clear_selection(self):
        self.fleet_manager.selected_robot = None
        self.update_status("Selection cleared")
    
    def update_status(self, message):
        self.status_bar.config(text=message)
        
        # Update status text
        self.status_text.delete(1.0, tk.END)
        
        # Add robots status
        for robot_id, robot in self.fleet_manager.robots.items():
            status = robot.status
            location = robot.current_vertex["name"] if robot.current_vertex else "Unknown"
            
            if robot.target_vertex:
                destination = robot.target_vertex["name"]
                self.status_text.insert(tk.END, f"Robot {robot_id}: {status}\nAt: {location}\nTo: {destination}\n\n")
            else:
                self.status_text.insert(tk.END, f"Robot {robot_id}: {status}\nAt: {location}\n\n")
    
    def update_display(self):
        self.canvas.delete("all")
        
        # Draw lanes
        for lane in self.nav_graph.lanes:
            start = self.nav_graph.get_vertex_by_id(lane["start"])
            end = self.nav_graph.get_vertex_by_id(lane["end"])
            
            start_x, start_y = self.world_to_canvas(start["x"], start["y"])
            end_x, end_y = self.world_to_canvas(end["x"], end["y"])
            
            # Check if lane is occupied
            lane_id = f"{lane['start']}-{lane['end']}"
            reverse_id = f"{lane['end']}-{lane['start']}"
            
            line_color = "gray"
            if lane_id in self.fleet_manager.traffic_manager.occupied_lanes or reverse_id in self.fleet_manager.traffic_manager.occupied_lanes:
                line_color = "red"
            
            self.canvas.create_line(start_x, start_y, end_x, end_y, fill=line_color, width=2)
        
        # Draw vertices
        for vertex in self.nav_graph.vertices:
            x, y = self.world_to_canvas(vertex["x"], vertex["y"])
            
            # Draw different shapes for different vertex types
            if vertex.get("is_charger", False):
                self.canvas.create_rectangle(x-10, y-10, x+10, y+10, fill="yellow", outline="black")
            else:
                self.canvas.create_oval(x-8, y-8, x+8, y+8, fill="lightblue", outline="black")
            
            # Draw vertex name
            self.canvas.create_text(x, y-15, text=vertex["name"], font=("Arial", 8))
        
        # Draw robots
        for robot_id, robot in self.fleet_manager.robots.items():
            x, y = self.world_to_canvas(robot.x, robot.y)
            
            # Base color from robot
            color = robot.color
            
            # Change border based on status
            outline = "black"
            if robot.status == "waiting":
                outline = "red"
            elif robot.status == "charging":
                outline = "yellow"
            
            # Highlight selected robot
            width = 1
            if self.fleet_manager.selected_robot and self.fleet_manager.selected_robot.id == robot.id:
                width = 3
                outline = "blue"
            
            # Draw robot
            self.canvas.create_oval(x-12, y-12, x+12, y+12, fill=color, outline=outline, width=width)
            self.canvas.create_text(x, y, text=str(robot_id), font=("Arial", 9, "bold"))
            
            # Draw status indicator
            status_y = y + 20
            self.canvas.create_text(x, status_y, text=robot.status, font=("Arial", 7))
        
        # Schedule next update
        self.root.after(self.update_interval, self.update_display)