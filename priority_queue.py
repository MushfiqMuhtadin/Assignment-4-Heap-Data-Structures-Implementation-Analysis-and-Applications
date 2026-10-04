"""
priority_queue.py
-----------------
A priority queue built on a binary MAX-HEAP stored in a Python list.

Why a list?
  - A complete binary tree fits perfectly in a list with no gaps.
  - Parent/child are found with simple math (no pointers needed).
  - Appending to the end is O(1), which is exactly where a new item goes.

Why a MAX-heap?
  - In my scheduler, a bigger priority number means "more important",
    so the most important task should come out first.

Extra trick: a dictionary `position` remembers where each task is
in the list. That lets increase_key / decrease_key find a task in O(1)
instead of searching the whole list (which would be O(n)).
"""
from dataclasses import dataclass, field


@dataclass
class Task:
    task_id: int
    priority: int              # bigger number = more important
    arrival_time: int = 0      # when the task shows up
    deadline: int = 0          # when it should be finished by
    duration: int = 1          # how long it takes to run
    name: str = field(default="")

    def __repr__(self):
        return f"Task(id={self.task_id}, pri={self.priority})"


class PriorityQueue:
    def __init__(self):
        self.heap = []         # the actual heap (list of Task objects)
        self.position = {}     # task_id -> index in self.heap

    # ---------- small helpers ----------
    def _parent(self, i): return (i - 1) // 2
    def _left(self, i):   return 2 * i + 1
    def _right(self, i):  return 2 * i + 2

    def _higher(self, a, b):
        """
        True if task a should come out before task b.
        Ties on priority are broken by earlier arrival time (fair = first come first served).
        """
        if a.priority != b.priority:
            return a.priority > b.priority
        return a.arrival_time < b.arrival_time

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        # keep the position map up to date
        self.position[self.heap[i].task_id] = i
        self.position[self.heap[j].task_id] = j

    def _sift_up(self, i):
        """Move a task UP while it's more important than its parent."""
        while i > 0:
            p = self._parent(i)
            if self._higher(self.heap[i], self.heap[p]):
                self._swap(i, p)
                i = p
            else:
                break

    def _sift_down(self, i):
        """Move a task DOWN while one of its children is more important."""
        n = len(self.heap)
        while True:
            best = i
            l, r = self._left(i), self._right(i)
            if l < n and self._higher(self.heap[l], self.heap[best]):
                best = l
            if r < n and self._higher(self.heap[r], self.heap[best]):
                best = r
            if best == i:
                break
            self._swap(i, best)
            i = best

    # ---------- core operations ----------
    def insert(self, task):
        """
        Add a task. Put it at the end, then bubble it up.
        Time: O(log n) - it can climb at most the height of the tree.
        """
        if task.task_id in self.position:
            raise ValueError(f"Task {task.task_id} is already in the queue")
        self.heap.append(task)
        self.position[task.task_id] = len(self.heap) - 1
        self._sift_up(len(self.heap) - 1)

    def extract_max(self):
        """
        Remove and return the most important task.
        Move the last item to the root, then sink it down.
        Time: O(log n).
        """
        if self.is_empty():
            raise IndexError("extract_max from an empty priority queue")
        top = self.heap[0]
        last = self.heap.pop()
        del self.position[top.task_id]
        if self.heap:                     # if anything is left
            self.heap[0] = last
            self.position[last.task_id] = 0
            self._sift_down(0)
        return top

    def peek(self):
        """Look at the top task without removing it. Time: O(1)."""
        if self.is_empty():
            raise IndexError("peek from an empty priority queue")
        return self.heap[0]

    def increase_key(self, task_id, new_priority):
        """
        Make a task MORE important. It can only move up.
        Time: O(log n) (O(1) to find it thanks to the dictionary).
        """
        i = self.position[task_id]
        if new_priority < self.heap[i].priority:
            raise ValueError("New priority is smaller - use decrease_key instead")
        self.heap[i].priority = new_priority
        self._sift_up(i)

    def decrease_key(self, task_id, new_priority):
        """
        Make a task LESS important. It can only move down.
        Time: O(log n).
        """
        i = self.position[task_id]
        if new_priority > self.heap[i].priority:
            raise ValueError("New priority is bigger - use increase_key instead")
        self.heap[i].priority = new_priority
        self._sift_down(i)

    def change_priority(self, task_id, new_priority):
        """Convenience: works in either direction."""
        old = self.heap[self.position[task_id]].priority
        if new_priority >= old:
            self.increase_key(task_id, new_priority)
        else:
            self.decrease_key(task_id, new_priority)

    def is_empty(self):
        """Time: O(1)."""
        return len(self.heap) == 0

    def __len__(self):
        return len(self.heap)


if __name__ == "__main__":
    pq = PriorityQueue()
    for t in [Task(1, 3), Task(2, 9), Task(3, 5), Task(4, 1), Task(5, 7)]:
        pq.insert(t)
    print("Top task:", pq.peek())                 # id 2, priority 9
    pq.increase_key(4, 10)                        # task 4 jumps to the top
    pq.decrease_key(2, 2)                         # task 2 drops down
    print("Order they come out:")
    while not pq.is_empty():
        print("  ", pq.extract_max())
