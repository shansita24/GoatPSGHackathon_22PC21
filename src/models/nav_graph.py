class NavGraph:
    def __init__(self, graph_data):
        self.vertices = []
        self.lanes = []
        self.parse_graph(graph_data)
        
    def parse_graph(self, graph_data):
        self.vertices = []
        self.lanes = []
        
        for idx, vertex in enumerate(graph_data["vertices"]):
            x, y, attrs = vertex
            name = attrs.get("name", f"V{idx}")
            is_charger = attrs.get("is_charger", False)
            
            self.vertices.append({
                "id": idx,
                "x": x,
                "y": y,
                "name": name,
                "is_charger": is_charger
            })
        
        for lane in graph_data["lanes"]:
            start_idx, end_idx = lane
            self.lanes.append({
                "start": start_idx,
                "end": end_idx
            })
    
    def get_vertex_by_id(self, vertex_id):
        for vertex in self.vertices:
            if vertex["id"] == vertex_id:
                return vertex
        return None
    
    def get_vertex_by_position(self, x, y, tolerance=5):
        for vertex in self.vertices:
            if abs(vertex["x"] - x) <= tolerance and abs(vertex["y"] - y) <= tolerance:
                return vertex
        return None
    
    def get_connected_vertices(self, vertex_id):
        connected = []
        for lane in self.lanes:
            if lane["start"] == vertex_id:
                connected.append(lane["end"])
            elif lane["end"] == vertex_id:
                connected.append(lane["start"])
        return connected
    
    def find_path(self, start_id, end_id):
        visited = set()
        queue = [[start_id]]
        
        if start_id == end_id:
            return [start_id]
            
        while queue:
            path = queue.pop(0)
            node = path[-1]
            
            if node not in visited:
                neighbors = self.get_connected_vertices(node)
                
                for neighbor in neighbors:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
                    
                    if neighbor == end_id:
                        return new_path
                        
                visited.add(node)
                
        return None