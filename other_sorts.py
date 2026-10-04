"""
other_sorts.py
--------------
Quicksort and Merge Sort, used only to compare against Heapsort.
"""
import random


def quicksort(arr):
    """
    In-place quicksort with a RANDOM pivot.
    Random pivot = it doesn't fall apart on already-sorted input.
    Uses a loop on the bigger half so the recursion stays shallow.
    """
    def partition(lo, hi):
        p = random.randint(lo, hi)
        arr[p], arr[hi] = arr[hi], arr[p]
        pivot = arr[hi]
        i = lo - 1
        for j in range(lo, hi):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
        return i + 1

    def _qs(lo, hi):
        while lo < hi:
            p = partition(lo, hi)
            # Recurse on the smaller side, loop on the bigger side
            if p - lo < hi - p:
                _qs(lo, p - 1)
                lo = p + 1
            else:
                _qs(p + 1, hi)
                hi = p - 1

    _qs(0, len(arr) - 1)
    return arr


def merge_sort(arr):
    """Classic top-down merge sort. Returns a NEW sorted list."""
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged
