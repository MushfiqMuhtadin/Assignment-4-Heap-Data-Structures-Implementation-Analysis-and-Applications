"""
scheduler.py
------------
A small simulation of a CPU / job scheduler using my PriorityQueue.

How it works (non-preemptive priority scheduling):
  - Time moves forward one step at a time.
  - Tasks "arrive" at their arrival_time and go into the priority queue.
  - Whenever the CPU is free, it picks the most important waiting task
    (extract_max) and runs it until it's finished.
  - AGING: every few time units, waiting tasks get +1 priority.
    This stops low-priority tasks from waiting forever ("starvation").
    Aging uses increase_key, so it's a real use of that operation.

At the end it prints each task's waiting time, finish time,
and whether it met its deadline.

Run:  python scheduler.py
"""
import random
from priority_queue import PriorityQueue, Task

AGING_INTERVAL = 5   # every 5 time units...
AGING_AMOUNT = 1     # ...waiting tasks get +1 priority


def make_tasks(count=15, seed=9):
    """Make a busy workload: lots of tasks arriving close together,
    so tasks actually have to wait and priorities matter."""
    random.seed(seed)
    tasks = []
    for i in range(1, count + 1):
        arrival = random.randint(0, 15)
        duration = random.randint(1, 6)
        tasks.append(Task(
            task_id=i,
            priority=random.randint(1, 10),
            arrival_time=arrival,
            duration=duration,
            deadline=arrival + duration + random.randint(5, 30),
            name=f"Job-{i}",
        ))
    return tasks


def simulate(tasks, use_aging=True, verbose=True):
    pending = sorted(tasks, key=lambda t: t.arrival_time)   # not arrived yet
    original_priority = {t.task_id: t.priority for t in tasks}
    pq = PriorityQueue()
    time = 0
    results = []
    idx = 0

    while idx < len(pending) or not pq.is_empty():
        # 1. Put every task that has arrived by now into the queue
        while idx < len(pending) and pending[idx].arrival_time <= time:
            pq.insert(pending[idx])
            idx += 1

        # 2. CPU is idle and nothing is waiting -> skip ahead
        if pq.is_empty():
            time = pending[idx].arrival_time
            continue

        # 3. Pick the most important task and run it to completion
        task = pq.extract_max()
        start = time
        finish = time + task.duration
        if verbose:
            print(f"t={start:>3}: run {task.name:<7} (priority {task.priority:>2}, "
                  f"original {original_priority[task.task_id]:>2}) until t={finish}")

        # 4. While it runs, time passes. Let new tasks arrive and age the waiting ones.
        for t in range(start + 1, finish + 1):
            while idx < len(pending) and pending[idx].arrival_time <= t:
                pq.insert(pending[idx])
                idx += 1
            if use_aging and t % AGING_INTERVAL == 0:
                for waiting in list(pq.heap):
                    pq.increase_key(waiting.task_id, waiting.priority + AGING_AMOUNT)
        time = finish

        results.append({
            "id": task.task_id,
            "name": task.name,
            "priority": original_priority[task.task_id],
            "arrival": task.arrival_time,
            "start": start,
            "finish": finish,
            "wait": start - task.arrival_time,
            "deadline": task.deadline,
            "met": finish <= task.deadline,
        })
    return results


def print_report(results, title):
    print(f"\n=== {title} ===")
    print(f"{'Task':<8}{'Pri':>4}{'Arrive':>8}{'Start':>7}{'Finish':>8}"
          f"{'Wait':>6}{'Deadline':>10}{'Met?':>6}")
    for r in sorted(results, key=lambda r: r["id"]):
        print(f"{r['name']:<8}{r['priority']:>4}{r['arrival']:>8}{r['start']:>7}"
              f"{r['finish']:>8}{r['wait']:>6}{r['deadline']:>10}"
              f"{'yes' if r['met'] else 'NO':>6}")
    avg_wait = sum(r["wait"] for r in results) / len(results)
    max_wait = max(r["wait"] for r in results)
    met = sum(r["met"] for r in results)
    print(f"Average wait: {avg_wait:.2f}   Longest wait: {max_wait}   "
          f"Deadlines met: {met}/{len(results)}")
    return avg_wait, max_wait, met


if __name__ == "__main__":
    print("Run log (with aging):")
    with_aging = simulate(make_tasks(), use_aging=True)
    print_report(with_aging, "Priority scheduling WITH aging")

    without_aging = simulate(make_tasks(), use_aging=False, verbose=False)
    print_report(without_aging, "Priority scheduling WITHOUT aging")
