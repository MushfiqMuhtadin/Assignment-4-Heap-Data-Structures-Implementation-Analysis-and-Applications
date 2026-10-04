# Assignment 4: Heap Data Structures

Heapsort, a heap-based Priority Queue, and a small task scheduler, all in Python.

## Files

| File | What it does |
|---|---|
| `heapsort.py` | Heapsort (build max-heap, then extract max repeatedly) |
| `other_sorts.py` | Quicksort (random pivot) and Merge Sort for comparison |
| `compare_sorts.py` | Times all three on different sizes and input types, saves a chart |
| `priority_queue.py` | `Task` class + max-heap `PriorityQueue` (insert, extract_max, increase/decrease_key, is_empty) |
| `scheduler.py` | Priority scheduling simulation, with and without aging |
| `test_heap.py` | Simple tests for everything |
| `REPORT.md` | Full report: design choices, complexity analysis, results |
| `sort_comparison.png` | Chart from `compare_sorts.py` |
| `compare_output.txt`, `scheduler_output.txt` | Saved output from my runs |

## How to run

You need **Python 3.8+**. The only optional extra is `matplotlib`, for the chart.

```bash
pip install matplotlib        # optional, only for the chart

python heapsort.py            # demo + self-check
python priority_queue.py      # demo of the priority queue
python test_heap.py           # run the tests
python compare_sorts.py       # sorting benchmark (takes ~10-20 seconds)
python scheduler.py           # scheduler simulation
```

