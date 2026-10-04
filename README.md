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

## Summary of findings

- **Heapsort is O(n log n) in best, average, and worst case** and sorts in place with **O(1)** extra memory.
- In my benchmark it was **about 1.3–2.5× slower** than Quicksort and Merge Sort. Big-O is the same, but Heapsort does more comparisons and jumps around memory a lot. Its times barely changed between random, sorted, and reverse input, which is what the theory says.
- Merge Sort got faster on already-ordered data. Quicksort stayed fast on sorted data **only because it uses a random pivot**. A fixed last-element pivot would make sorted input its O(n²) worst case.
- The **priority queue** uses a max-heap stored in a list, plus a dictionary of positions so `increase_key` and `decrease_key` don't need to search. insert / extract_max / increase_key / decrease_key are all **O(log n)**. peek and is_empty are **O(1)**.
- In the **scheduler**, adding aging cut the longest wait from **53 to 42** and average wait from **22.67 to 21.53**. Low-priority jobs waited 11 units less, while a couple of mid-priority jobs waited a bit longer, so it's a fairness trade-off.

See `REPORT.md` for the full write-up.

## References

The main sources were *Introduction to Algorithms* (CLRS, 4th ed.) for heaps, Heapsort and Quicksort, and *Operating System Concepts* (Silberschatz et al., 10th ed.) for priority scheduling and aging. The full reference list is at the end of `REPORT.md`.
