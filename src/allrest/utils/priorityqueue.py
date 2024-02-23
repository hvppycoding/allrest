import itertools
import heapq


class PriorityQueue:
    # REF: https://docs.python.org/3/library/heapq.html
    def __init__(self):
        self.pq = []                        # list of entries arranged in a heap
        self.entry_finder = {}              # mapping of tasks to entries
        self.REMOVED = '<removed-task>'     # placeholder for a removed task
        self.counter = itertools.count()    # unique sequence count
        self.n_tasks = 0
        
    def add_task(self, task, priority=0):
        'Add a new task or update the priority of an existing task'
        if task in self.entry_finder:
            self.remove_task(task)
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heapq.heappush(self.pq, entry)
        self.n_tasks += 1

    def remove_task(self, task):
        'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED
        self.n_tasks -= 1

    def pop_task(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.pq:
            priority, count, task = heapq.heappop(self.pq)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                self.n_tasks -= 1
                return task
        raise KeyError('pop from an empty priority queue')
    
    def empty(self):
        return self.n_tasks == 0
    
    
if __name__ == "__main__":
    pq = PriorityQueue()
    pq.add_task('task1', 1)
    pq.add_task('task1', 2)
    pq.pop_task()
    print(pq.empty())
    pq.add_task('task1', 2)
    pq.add_task('task2', 1)
    print(pq.empty())
    pq.pop_task()
    pq.pop_task()
    print(pq.empty())
    