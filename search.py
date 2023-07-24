from state import *
from queue import PriorityQueue
import time
import os
import tracemalloc

class Search:
    def __init__(self, state: State):
        self.init_state = state
           
    def BFS(self):
        tracemalloc.start()
        start_time = time.time()
        queue = [self.init_state]
        visited = []
        
        while len(queue) != 0:
            current_state = queue.pop(0)
            visited.append(current_state)
            if isBFSGoalState(current_state):
                execute_time = time.time() - start_time
                total_generated_states = len(queue) + len(visited)
    
                snapshot = tracemalloc.take_snapshot()
                top_stats = snapshot.statistics('lineno')
                # Get Memory statistic
                tracing_string = "--------Memory statistic for the solution--------\n"
                length, count, avg = 0, 0, 0
                for stat in top_stats:
                    length += stat.size
                    count += stat.count
                avg = int(length/count)
                total_used_memory = int(length/1024)
                tracing_string += f'+ Total memory used for the solution: {int(length/1024)} KiB\n'
                tracing_string += f'+ Total number of allocations: {count}\n'
                tracing_string += f'+ The average memory usage per allocation: {avg} B\n'
                tracing_string += '--------------------------------------------------'

                # Print Memory statistic
                print(tracing_string)
                
                return current_state, execute_time, total_generated_states, total_used_memory

            else:
                next_states_list = genNextStatesList(current_state)
                for s in next_states_list:
                    if s not in visited and s not in queue:
                        queue.append(s)
                        
    def A_Star(self):
        tracemalloc.start()
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
                
                snapshot = tracemalloc.take_snapshot()
                top_stats = snapshot.statistics('lineno')
                # Get Memory statistic
                tracing_string = "--------Memory statistic for the solution--------\n"
                length, count, avg = 0, 0, 0
                for stat in top_stats:
                    length += stat.size
                    count += stat.count
                avg = int(length/count)
                total_used_memory = int(length/1024)
                tracing_string += f'+ Total memory used for the solution: {total_used_memory} KiB\n'
                tracing_string += f'+ Total number of allocations: {count}\n'
                tracing_string += f'+ The average memory usage per allocation: {avg} B\n'
                tracing_string += '--------------------------------------------------'

                # Print Memory statistic
                print(tracing_string)
                
                return current_state, execute_time, total_generated_states, total_used_memory
            else:
                next_state_list = genNextStatesList(current_state)
                for s in next_state_list:
                    if s not in visited:
                        queue.put(s)