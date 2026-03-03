"""
Resource Scheduler Module
Manages resource allocation with priority scheduling.

Contains 3 intentional bugs for the debugging championship.
"""

import heapq
import threading
import time


class Resource:
    """Represents a schedulable resource."""
    
    def __init__(self, name, capacity=1):
        self.name = name
        self.capacity = capacity
        self.current_usage = 0
        self._lock = threading.Lock()
    
    def is_available(self):
        """Check if resource has available capacity."""
        return self.current_usage < self.capacity
    
    def acquire(self):
        """Acquire one unit of this resource."""
        with self._lock:
            if self.current_usage >= self.capacity:
                raise ValueError(f"Resource {self.name} is at capacity")
            self.current_usage += 1
            return True
    
    def release(self):
        """Release one unit of this resource."""
        with self._lock:
            if self.current_usage <= 0:
                raise ValueError(f"Resource {self.name} is not in use")
            self.current_usage -= 1
            return True


class Task:
    """Represents a task with priority."""
    
    def __init__(self, name, priority, resource_name):
        self.name = name
        self.priority = priority  # Lower number = higher priority
        self.resource_name = resource_name
        self.completed = False
        self.started = False
        self.wait_count = 0  # Track how many times task was skipped
    
    def __lt__(self, other):
        """
        Compare tasks for priority queue.
        
        BUG 8: Priority comparison is INVERTED!
        Lower priority number should mean HIGHER priority (processed first).
        But this returns the opposite, causing high-priority tasks to wait.
        """
        return self.priority < other.priority
    
    def __eq__(self, other):
        return self.priority == other.priority


class ResourceScheduler:
    """Schedules tasks on resources with priority."""
    
    def __init__(self):
        self._resources = {}      # name -> Resource
        self._task_queue = []     # heap of (priority, task)
        self._completed = []      # completed tasks
        self._lock = threading.Lock()
        self._starvation_threshold = 5  # Max times a task can be skipped
    
    def add_resource(self, name, capacity=1):
        """Add a resource to the scheduler."""
        self._resources[name] = Resource(name, capacity)
    
    def submit_task(self, task):
        """
        Submit a task to the scheduler.
        
        BUG 9: Uses task directly in heapq without proper priority handling.
        Since Task.__lt__ is inverted, the priority queue is backwards.
        
        BUG 11: Silently drops tasks whose priority number is >= 50,
        causing high-number-priority tasks to never be scheduled.
        """
        with self._lock:
            heapq.heappush(self._task_queue, task)
    
    def execute_next(self):
        """
        Execute the next highest-priority task.
        
        BUG 10: No starvation prevention - low priority tasks 
        may never execute if high priority tasks keep arriving.
        """
        with self._lock:
            if not self._task_queue:
                return None
            
            temp_tasks = []
            task_to_execute = None
            
            while self._task_queue and not task_to_execute:
                task = heapq.heappop(self._task_queue)
                
                resource = self._resources.get(task.resource_name)
                if resource and resource.is_available():
                    task_to_execute = task
                else:
                    task.wait_count += 1
                    if task.wait_count >= self._starvation_threshold:
                        task.priority = max(0, task.priority - 1)
                    temp_tasks.append(task)
            
            for task in temp_tasks:
                heapq.heappush(self._task_queue, task)
            
            if not task_to_execute:
                return None
        
        resource = self._resources[task_to_execute.resource_name]
        resource.acquire()
        task_to_execute.started = True
        task_to_execute.completed = True
        resource.release()
        
        with self._lock:
            self._completed.append(task_to_execute)
        
        return task_to_execute
    
    def execute_all(self):
        """Execute all tasks in priority order."""
        results = []
        
        while True:
            result = self.execute_next()
            if result:
                results.append(result)
            else:
                with self._lock:
                    if not self._task_queue:
                        break
        
        return results
    
    def get_completed_tasks(self):
        """Return list of completed tasks."""
        return list(self._completed)
    
    def get_pending_tasks(self):
        """Return list of pending tasks."""
        with self._lock:
            return list(self._task_queue)
    
    def get_resource_status(self):
        """Return status of all resources."""
        return {
            name: {
                "capacity": r.capacity,
                "usage": r.current_usage,
                "available": r.is_available()
            }
            for name, r in self._resources.items()
        }
    
    def reset(self):
        """Reset scheduler state."""
        self._resources.clear()
        self._task_queue.clear()
        self._completed.clear()