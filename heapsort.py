"""
heapsort.py
-----------
Heapsort written step by step so it's easy to follow.

The big idea:
  1. Turn the list into a MAX-HEAP (the biggest number ends up at index 0).
  2. Swap the biggest number to the end of the list. That spot is now "done".
  3. Fix the heap for the remaining (smaller) part of the list.
  4. Repeat until everything is in place.

We store the heap inside a normal Python list. For any position i:
  left child  = 2*i + 1
  right child = 2*i + 2
  parent      = (i - 1) // 2
"""


def heapify(arr, heap_size, i):
    """
    Push the value at index i DOWN until it's bigger than both its children.
    We only look at the first `heap_size` items (the rest are already sorted).

    I wrote this with a loop instead of recursion so it doesn't
    use extra stack space.
    """
    while True:
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        # Is the left child bigger than the current largest?
        if left < heap_size and arr[left] > arr[largest]:
            largest = left

        # Is the right child bigger than the current largest?
        if right < heap_size and arr[right] > arr[largest]:
            largest = right

        # If the parent is already the biggest, we're done.
        if largest == i:
            break

        # Otherwise swap with the bigger child and keep going down.
        arr[i], arr[largest] = arr[largest], arr[i]
        i = largest


def build_max_heap(arr):
    """
    Turn any list into a max-heap.
    Leaves (the second half of the list) are already tiny heaps by themselves,
    so we start from the last non-leaf node and work backwards to the root.
    """
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)


def heapsort(arr):
    """
    Sort the list IN PLACE in ascending order and also return it
    (returning it just makes testing easier).
    """
    n = len(arr)
    build_max_heap(arr)

    # Move the current max (index 0) to the end, shrink the heap, fix it.
    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        heapify(arr, end, 0)

    return arr


if __name__ == "__main__":
    # Quick demo
    data = [12, 3, 17, 8, 34, 25, 1, 9]
    print("Before:", data)
    heapsort(data)
    print("After: ", data)

    # Small self-check against Python's built-in sort
    import random
    for _ in range(200):
        test = [random.randint(-1000, 1000) for _ in range(random.randint(0, 100))]
        assert heapsort(test.copy()) == sorted(test)
    print("All 200 random tests passed!")
