"""
test_heap.py - simple checks. Run:  python test_heap.py
"""
import random
from heapsort import heapsort
from priority_queue import PriorityQueue, Task


def test_heapsort():
    assert heapsort([]) == []
    assert heapsort([5]) == [5]
    assert heapsort([2, 2, 1, 1]) == [1, 1, 2, 2]
    for _ in range(300):
        data = [random.randint(-50, 50) for _ in range(random.randint(0, 200))]
        assert heapsort(data.copy()) == sorted(data)


def test_priority_queue_order():
    pq = PriorityQueue()
    pris = [random.randint(1, 100) for _ in range(500)]
    for i, p in enumerate(pris):
        pq.insert(Task(i, p, arrival_time=i))
    out = []
    while not pq.is_empty():
        out.append(pq.extract_max().priority)
    assert out == sorted(pris, reverse=True)


def test_change_keys():
    pq = PriorityQueue()
    for i in range(50):
        pq.insert(Task(i, i))
    pq.increase_key(0, 1000)
    assert pq.peek().task_id == 0
    pq.decrease_key(0, -1)
    assert pq.peek().task_id == 49
    # position map must stay correct
    for idx, t in enumerate(pq.heap):
        assert pq.position[t.task_id] == idx


def test_empty():
    pq = PriorityQueue()
    assert pq.is_empty()
    try:
        pq.extract_max()
        assert False
    except IndexError:
        pass


if __name__ == "__main__":
    test_heapsort(); test_priority_queue_order(); test_change_keys(); test_empty()
    print("All tests passed!")
