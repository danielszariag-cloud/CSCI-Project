"""
Name: CSCI Coders
File: game_controller.py
Term Paper
"""

import random
import tkinter as tk
from tkinter import ttk

from game_algorithms import linear_search, binary_search
from game_quiz import random_question


class Controller:

    def __init__(self, gui):
        self.gui   = gui
        self.lst   = []
        self.score = 0

        # Step lists — filled when a round starts
        self.linear_steps_list = []
        self.binary_steps_list = []

        # Current position inside each step list
        self.linear_idx = 0
        self.binary_idx = 0

        # Tracks whether each algorithm has finished
        self.linear_done = False
        self.binary_done = False

        # Final step counts used to pick the winner
        self.linear_steps = 0
        self.binary_steps = 0

        # Indices that binary search has already eliminated (shown grey)
        self.binary_discarded = set()

        # Prevents the end-of-round summary firing more than once
        self.round_finished = False

        # Ensures the mid-round question appears only once per round
        self.mid_question_asked = False

        # Blocks multiple quiz windows opening at once
        self.quiz_active = False

        # Queue so explanation messages appear one at a time
        self.explanation_queue = []
        self.explaining        = False

    # ------------------------------------------------------------------ #
    #  Explanation pacing                                                  #
    # ------------------------------------------------------------------ #

    def queue_explanation(self, text):
        self.explanation_queue.append(text)
        if not self.explaining:
            self._process_explanations()

    def _process_explanations(self):
        if not self.explanation_queue:
            self.explaining = False
            return
        self.explaining = True
        self.gui.write_explanation(self.explanation_queue.pop(0))
        self.gui.root.after(650, self._process_explanations)

    # ------------------------------------------------------------------ #
    #  Round setup                                                         #
    # ------------------------------------------------------------------ #

    def new_round(self):
        self.lst = sorted(random.sample(range(1, 100), 15))

        self.linear_steps_list = []
        self.binary_steps_list = []
        self.linear_idx   = 0
        self.binary_idx   = 0
        self.linear_done  = False
        self.binary_done  = False
        self.linear_steps = 0
        self.binary_steps = 0
        self.binary_discarded = set()
        self.round_finished   = False
        self.mid_question_asked = False

        self.gui.draw_list(self.gui.canvas_linear, self.lst, mode="linear")
        self.gui.draw_list(self.gui.canvas_binary, self.lst, mode="binary")

        self._update_step_counter()

        self.queue_explanation("── New Round! ──")
        self.queue_explanation("A brand new sorted list of 15 numbers has been created.")
        self.queue_explanation("Both searches will look for the SAME target at the same time.")
        self.queue_explanation("Which one do YOU think will find it faster? Make your prediction!")
        self.queue_explanation("Type a target number and hit 'Start Showdown'.")

    # ------------------------------------------------------------------ #
    #  Starting the showdown                                               #
    # ------------------------------------------------------------------ #

    def start_round(self):
        if not self.lst:
            self.queue_explanation("Click 'New Round' first to generate a list.")
            return

        if not self.gui.prediction.get():
            self.queue_explanation("Please choose a prediction (Linear or Binary) before starting.")
            return

        try:
            target = int(self.gui.target_entry.get())
        except ValueError:
            self.queue_explanation("Please enter a valid whole number as the target.")
            return

        self.queue_explanation(f"Target: {target}  |  Let the showdown begin!")

        self.linear_steps_list = linear_search(self.lst, target)
        self.binary_steps_list = binary_search(self.lst, target)
        self.linear_idx = 0
        self.binary_idx = 0

        self._step_linear()
        self._step_binary()

    # ------------------------------------------------------------------ #
    #  Linear search animation                                            #
    # ------------------------------------------------------------------ #

    def _step_linear(self):
        if self.linear_done:
            return

        if self.linear_idx >= len(self.linear_steps_list):
            self.linear_done = True
            self._check_end()
            return

        step = self.linear_steps_list[self.linear_idx]
        self.linear_idx  += 1
        idx               = step["index"]
        self.linear_steps = step["steps"]

        if idx == -1:
            self.linear_done = True
            self.queue_explanation("[Linear] Target not found in the list.")
            self._check_end()
            return

        self.gui.draw_list(
            self.gui.canvas_linear, self.lst,
            highlight=idx, mode="linear", grow=True
        )
        self._update_step_counter()
        self.queue_explanation("[Linear] " + step["message"])

        if step["found"]:
            self.linear_done = True
            self.queue_explanation("[Linear] ✓ Found it!")
            self._flash_found(self.gui.canvas_linear, idx, mode="linear")
            self._check_end()
            return

        self.gui.root.after(450, self._step_linear)

    # ------------------------------------------------------------------ #
    #  Binary search animation                                            #
    # ------------------------------------------------------------------ #

    def _step_binary(self):
        if self.binary_done:
            return

        if self.binary_idx >= len(self.binary_steps_list):
            self.binary_done = True
            self._check_end()
            return

        step = self.binary_steps_list[self.binary_idx]
        self.binary_idx += 1

        if step["type"] == "check":
            idx               = step["index"]
            self.binary_steps = step["steps"]

            if idx == -1:
                self.binary_done = True
                self.queue_explanation("[Binary] Target not found in the list.")
                self._check_end()
                return

            self.gui.draw_list(
                self.gui.canvas_binary, self.lst,
                highlight=idx, discarded=self.binary_discarded,
                mode="binary", grow=True
            )
            self._update_step_counter()
            self.queue_explanation("[Binary] " + step["message"])

            if step["found"]:
                self.binary_done = True
                self.queue_explanation("[Binary] ✓ Found it!")
                self._flash_found(self.gui.canvas_binary, idx, mode="binary")
                self._check_end()
                return

        elif step["type"] == "discard":
            low, high = step["range"]
            for i in range(low, high + 1):
                self.binary_discarded.add(i)

            self.gui.draw_list(
                self.gui.canvas_binary, self.lst,
                discarded=self.binary_discarded, mode="binary"
            )
            self.queue_explanation("[Binary] " + step["message"])

            if not self.mid_question_asked:
                self.mid_question_asked = True
                self._ask_mid_question()

        self.gui.root.after(450, self._step_binary)

    # ------------------------------------------------------------------ #
    #  Flash animation when element is found                              #
    # ------------------------------------------------------------------ #

    def _flash_found(self, canvas, index, mode="linear", flashes=4):
        def flash(count, show_green):
            if count == 0:
                self.gui.draw_list(
                    canvas, self.lst,
                    highlight=index,
                    discarded=self.binary_discarded if mode == "binary" else None,
                    mode=mode
                )
                return

            if show_green:
                x = 20 + index * 55
                self.gui.draw_list(canvas, self.lst, mode=mode)
                canvas.create_rectangle(x, 35, x + 50, 95, fill="#93c47d")
                canvas.create_text(
                    x + 25, 65,
                    text=str(self.lst[index]),
                    font=("Arial", 11, "bold")
                )
            else:
                self.gui.draw_list(
                    canvas, self.lst,
                    highlight=index,
                    discarded=self.binary_discarded if mode == "binary" else None,
                    mode=mode, grow=True
                )

            self.gui.root.after(150, lambda: flash(count - 1, not show_green))

        flash(flashes, True)

    # ------------------------------------------------------------------ #
    #  End-of-round summary                                               #
    # ------------------------------------------------------------------ #

    def _check_end(self):
        if self.round_finished:
            return
        if not (self.linear_done and self.binary_done):
            return

        self.round_finished = True

        if self.linear_steps < self.binary_steps:
            winner, winner_name = "linear", "Linear Search"
        elif self.binary_steps < self.linear_steps:
            winner, winner_name = "binary", "Binary Search"
        else:
            winner, winner_name = "tie", "Tie"

        self.queue_explanation(
            f"Round over!  Linear took {self.linear_steps} step(s)  |  "
            f"Binary took {self.binary_steps} step(s)."
        )

        if winner == "tie":
            self.queue_explanation("It's a tie! Both found it in the same number of steps.")
        else:
            self.queue_explanation(f"Winner this round: {winner_name}!")

        if winner != "tie" and self.gui.prediction.get() == winner:
            self.score += 1
            self.queue_explanation("🎉 Your prediction was CORRECT! +1 point.")
        elif winner == "tie":
            pass
        else:
            self.queue_explanation("Your prediction was incorrect this time — keep going!")

        self.gui.update_score(self.score)
        self._ask_quiz()

    # ------------------------------------------------------------------ #
    #  Mid-round concept check pop-up                                     #
    # ------------------------------------------------------------------ #

    def _ask_mid_question(self):
        if self.quiz_active:
            return
        self.quiz_active = True

        win = tk.Toplevel(self.gui.root)
        win.title("Quick Concept Check")
        win.geometry("430x220")
        win.resizable(False, False)

        ttk.Label(
            win,
            text=(
                "Binary search just eliminated half the list in ONE step!\n"
                "Why is it allowed to skip all those numbers?"
            ),
            font=("Arial", 12),
            wraplength=400, justify="center"
        ).pack(pady=15)

        answer_var = tk.StringVar()
        choices = [
            "Because the list is sorted, we know which half can't have the target.",
            "Because it already secretly checked every element in that half.",
        ]
        for c in choices:
            ttk.Radiobutton(win, text=c, variable=answer_var, value=c).pack(
                anchor="w", padx=20, pady=3
            )

        def submit():
            if not answer_var.get():
                return
            if answer_var.get() == choices[0]:
                self.queue_explanation(
                    "✅ Correct! Because the list is sorted, if the middle is too small, "
                    "EVERYTHING to the left is also too small. No need to check them!"
                )
            else:
                self.queue_explanation(
                    "Not quite! Binary search skips numbers because the list is SORTED. "
                    "If it weren't sorted, we couldn't safely skip anything."
                )
            self.quiz_active = False
            win.destroy()

        ttk.Button(win, text="Submit Answer", command=submit).pack(pady=12)

    # ------------------------------------------------------------------ #
    #  End-of-round quiz pop-up                                           #
    # ------------------------------------------------------------------ #

    def _ask_quiz(self):
        if self.quiz_active:
            return
        self.quiz_active = True

        q = random_question()

        win = tk.Toplevel(self.gui.root)
        win.title("End-of-Round Quiz")
        win.geometry("450x270")
        win.resizable(False, False)

        ttk.Label(
            win,
            text=q["q"],
            font=("Arial", 13, "bold"),
            wraplength=420, justify="center"
        ).pack(pady=15)

        answer_var = tk.StringVar()
        for c in q["choices"]:
            ttk.Radiobutton(win, text=c, variable=answer_var, value=c).pack(
                anchor="w", padx=20, pady=3
            )

        def submit():
            if not answer_var.get():
                return
            if answer_var.get() == q["answer"]:
                self.score += 1
                self.queue_explanation("Quiz: Correct! +1 point.")
            else:
                self.queue_explanation(f"Quiz: The answer was: {q['answer']}.")
            self.gui.update_score(self.score)
            self.quiz_active = False
            win.destroy()

        ttk.Button(win, text="Submit Answer", command=submit).pack(pady=12)

    # ------------------------------------------------------------------ #
    #  Helper — update live step counter labels                           #
    # ------------------------------------------------------------------ #

    def _update_step_counter(self):
        if hasattr(self.gui, "linear_step_label"):
            self.gui.linear_step_label.config(text=f"Steps: {self.linear_steps}")
        if hasattr(self.gui, "binary_step_label"):
            self.gui.binary_step_label.config(text=f"Steps: {self.binary_steps}")
