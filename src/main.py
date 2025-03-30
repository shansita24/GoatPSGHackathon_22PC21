import os
import sys
import tkinter as tk
from tkinter import messagebox
import json

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import modules
from src.models.nav_graph import NavGraph
from src.models.robot import Robot
from src.controllers.fleet_manager import FleetManager
from src.controllers.traffic_manager import TrafficManager
from src.gui.fleet_gui import FleetGUI
from src.utils.helpers import load_nav_graph

def main():
    try:
        # Create logs directory if it doesn't exist
        os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'logs'), exist_ok=True)
        
        # Load navigation graph
        graph_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'nav_graph.json')
        
        if not os.path.exists(graph_file):
            messagebox.showerror("Error", "Navigation graph file not found. Please ensure nav_graph.json is in the data directory.")
            return
        
        graph_data = load_nav_graph(graph_file)
        
        # Create navigation graph and managers
        nav_graph = NavGraph(graph_data)
        traffic_manager = TrafficManager()
        fleet_manager = FleetManager(nav_graph, traffic_manager)
        
        # Set up GUI
        root = tk.Tk()
        gui = FleetGUI(root, fleet_manager, nav_graph)
        
        # Start GUI main loop
        root.mainloop()
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()