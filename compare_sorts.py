"""
compare_sorts.py
----------------
Times Heapsort, Quicksort and Merge Sort on different sizes and
input types (random, sorted, reverse-sorted), then prints a table
and saves a chart (sort_comparison.png) if matplotlib is installed.

Run:  python compare_sorts.py
"""
import random
import time

from heapsort import heapsort
from other_sorts import quicksort, merge_sort

SIZES = [1000, 5000, 10000, 50000, 100000]
REPEATS = 3          # run each test a few times and keep the best time
random.seed(42)      # same "random" data every run


def make_data(kind, n):
    if kind == "random":
        return [random.randint(0, n) for _ in range(n)]
    if kind == "sorted":
        return list(range(n))
    if kind == "reverse":
        return list(range(n, 0, -1))
    raise ValueError(kind)


def time_it(sort_func, data):
    best = float("inf")
    for _ in range(REPEATS):
        copy = data.copy()
        start = time.perf_counter()
        result = sort_func(copy)
        elapsed = time.perf_counter() - start
        best = min(best, elapsed)
    # sanity check: make sure it actually sorted
    assert result == sorted(data)
    return best


def main():
    algorithms = {"Heapsort": heapsort, "Quicksort": quicksort, "Merge Sort": merge_sort}
    kinds = ["random", "sorted", "reverse"]
    results = {}  # (kind, algo) -> list of times

    print(f"{'Input':<9}{'n':>8} | " + " | ".join(f"{a:>10}" for a in algorithms))
    print("-" * 55)
    for kind in kinds:
        for n in SIZES:
            data = make_data(kind, n)
            row = []
            for name, fn in algorithms.items():
                t = time_it(fn, data)
                results.setdefault((kind, name), []).append(t)
                row.append(t)
            print(f"{kind:<9}{n:>8} | " + " | ".join(f"{t:>9.4f}s" for t in row))
        print("-" * 55)

    # Optional chart
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), sharey=True)
        for ax, kind in zip(axes, kinds):
            for name in algorithms:
                ax.plot(SIZES, results[(kind, name)], marker="o", label=name)
            ax.set_title(f"{kind.capitalize()} input")
            ax.set_xlabel("Input size (n)")
            ax.grid(alpha=0.3)
        axes[0].set_ylabel("Time (seconds)")
        axes[0].legend()
        plt.tight_layout()
        plt.savefig("sort_comparison.png", dpi=130)
        print("Chart saved to sort_comparison.png")
    except ImportError:
        print("(matplotlib not installed - skipping chart)")


if __name__ == "__main__":
    main()
