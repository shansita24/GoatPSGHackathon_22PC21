class TrafficManager:
    def __init__(self):
        self.occupied_lanes = {}
        self.lane_queue = {}
    
    def request_lane(self, robot, lane):
        lane_id = self._get_lane_id(lane)
        reverse_lane_id = self._get_lane_id((lane[1], lane[0]))
        
        if lane_id in self.occupied_lanes or reverse_lane_id in self.occupied_lanes:
            self._add_to_queue(robot, lane_id)
            return False
            
        self.occupied_lanes[lane_id] = robot.id
        return True
    
    def release_lane(self, robot, lane):
        lane_id = self._get_lane_id(lane)
        
        if lane_id in self.occupied_lanes and self.occupied_lanes[lane_id] == robot.id:
            del self.occupied_lanes[lane_id]
            self._process_queue(lane_id)
            return True
        
        return False
    
    def _get_lane_id(self, lane):
        return f"{lane[0]}-{lane[1]}"
    
    def _add_to_queue(self, robot, lane_id):
        if lane_id not in self.lane_queue:
            self.lane_queue[lane_id] = []
        
        if robot.id not in [r.id for r in self.lane_queue[lane_id]]:
            self.lane_queue[lane_id].append(robot)
    
    def _process_queue(self, lane_id):
        if lane_id in self.lane_queue and self.lane_queue[lane_id]:
            next_robot = self.lane_queue[lane_id].pop(0)
            lane = tuple(map(int, lane_id.split('-')))
            self.request_lane(next_robot, lane)
    
    def is_lane_occupied(self, lane):
        lane_id = self._get_lane_id(lane)
        reverse_lane_id = self._get_lane_id((lane[1], lane[0]))
        
        return lane_id in self.occupied_lanes or reverse_lane_id in self.occupied_lanes
    
    def get_queue_length(self, lane):
        lane_id = self._get_lane_id(lane)
        
        if lane_id in self.lane_queue:
            return len(self.lane_queue[lane_id])
        
        return 0