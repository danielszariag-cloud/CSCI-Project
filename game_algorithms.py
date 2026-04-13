"""
Name: CSCI Coders
File: game_algorithms.py
Term Paper
"""


def linear_search(lst, target):
    """
    Checks every element one by one from left to right.
    Returns a list of steps — each step is one comparison.
    """
    steps = []
    count = 0

    for i in range(len(lst)):
        count += 1
        steps.append({
            "index": i,
            "found": lst[i] == target,
            "steps": count,
            "message": f"Step {count}: Looking at position {i} — the value there is {lst[i]}."
        })
        if lst[i] == target:
            return steps

    # Target was not found anywhere in the list
    steps.append({
        "index": -1,
        "found": False,
        "steps": count,
        "message": f"Target not found after checking all {count} elements."
    })
    return steps


def binary_search(lst, target):
    """
    Jumps to the middle each time and cuts the list in half.
    Returns a list of steps — each step is either a 'check' or a 'discard'.
    ONLY works because the list is sorted!
    """
    steps = []
    low  = 0
    high = len(lst) - 1
    count = 0

    while low <= high:
        mid   = (low + high) // 2
        count += 1

        # --- check step: look at the middle element ---
        steps.append({
            "type":    "check",
            "index":   mid,
            "found":   lst[mid] == target,
            "steps":   count,
            "message": f"Step {count}: The middle position is {mid}, which holds the value {lst[mid]}."
        })

        if lst[mid] == target:
            return steps

        elif lst[mid] < target:
            steps.append({
                "type":    "discard",
                "range":   (low, mid),
                "found":   False,
                "steps":   count,
                "message": (
                    f"{lst[mid]} is smaller than our target, so everything to the LEFT "
                    f"is also too small. We can skip positions {low} to {mid} — "
                    f"that's {mid - low + 1} number(s) eliminated in one step!"
                )
            })
            low = mid + 1

        else:
            steps.append({
                "type":    "discard",
                "range":   (mid, high),
                "found":   False,
                "steps":   count,
                "message": (
                    f"{lst[mid]} is larger than our target, so everything to the RIGHT "
                    f"is also too large. We can skip positions {mid} to {high} — "
                    f"that's {high - mid + 1} number(s) eliminated in one step!"
                )
            })
            high = mid - 1

    # Target was not in the list
    steps.append({
        "type":    "check",
        "index":   -1,
        "found":   False,
        "steps":   count,
        "message": f"Target not found after {count} check(s)."
    })
    return steps
