from state import *
from queue import PriorityQueue
import time
import os

class Search:
    def __init__(self, state: State):
        self.init_state = state
           
    def BFS(self):
        start_time = time.time()
        queue = [self.init_state]
        visited = []
        
        while len(queue) != 0:
            current_state = queue.pop(0)
            visited.append(current_state)
            if isBFSGoalState(current_state):
                execute_time = time.time() - start_time
                total_generated_states = len(queue) + len(visited)
                print(f"Execute time: {execute_time}\nTotal generated state: {len(queue) + len(visited)}")
                return current_state, execute_time, total_generated_states
            else:
                next_states_list = genNextStatesList(current_state)
                for s in next_states_list:
                    if s not in visited and s not in queue:
                        queue.append(s)
                        
    def A_Star(self):
        start_time = time.time()
        queue = PriorityQueue()
        queue.put(self.init_state)
        visited = []
        
        while (queue.qsize() != 0):
            current_state = queue.get()
            visited.append(current_state)
            if isAStarGoalState(current_state):
                execute_time = time.time() - start_time
                total_generated_states = queue.qsize() + len(visited)
                print(f"Execute time: {execute_time}\nTotal generated state: {queue.qsize() + len(visited)}")
                return current_state, execute_time, total_generated_states
            else:
                next_state_list = genNextStatesList(current_state)
                for s in next_state_list:
                    if s not in visited:
                        queue.put(s)