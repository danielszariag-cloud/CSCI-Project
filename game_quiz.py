"""
Name: CSCI Coders
File: game_quiz.py
Term Paper
"""

import random

QUESTIONS = [
    {
        "q": "Which search algorithm requires the list to be sorted before it can work?",
        "choices": ["Linear search", "Binary search", "Both of them"],
        "answer": "Binary search"
    },
    {
        "q": "Linear search checks position 0, then 1, then 2. What does it do next?",
        "choices": ["Jumps to the middle", "Checks position 3", "Stops and gives up"],
        "answer": "Checks position 3"
    },
    {
        "q": "A sorted list has 64 items. About how many steps does binary search need?",
        "choices": ["About 6 steps", "About 32 steps", "All 64 steps"],
        "answer": "About 6 steps"
    },
    {
        "q": "Why can binary search skip half the list at each step?",
        "choices": [
            "Because the list is sorted, smaller or larger values can be ruled out",
            "Because it gets lucky and guesses right",
            "Because it secretly checks everything first"
        ],
        "answer": "Because the list is sorted, smaller or larger values can be ruled out"
    },
    {
        "q": "You have an unsorted list. Which algorithm should you use to search it?",
        "choices": ["Linear search", "Binary search", "Either one works the same"],
        "answer": "Linear search"
    },
    {
        "q": "Which is faster for finding a name in a giant sorted phone book?",
        "choices": ["Linear search", "Binary search", "They take the same time"],
        "answer": "Binary search"
    },
    {
        "q": "What does the target mean in a search algorithm?",
        "choices": [
            "The number or item we are trying to find",
            "The first item in the list",
            "The middle item in the list"
        ],
        "answer": "The number or item we are trying to find"
    },
    {
        "q": "What happens if you use binary search on an unsorted list?",
        "choices": [
            "It might skip over the target and give a wrong answer",
            "It works perfectly fine",
            "It automatically sorts the list first"
        ],
        "answer": "It might skip over the target and give a wrong answer"
    },
]


def random_question():
    """Return a randomly selected question from the pool."""
    return random.choice(QUESTIONS)
