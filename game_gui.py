"""
Name: CSCI Coders
File: game_gui.py
Term Paper
"""

import tkinter as tk
from tkinter import ttk
from game_controller import Controller

# Colour palette
BG_DARK       = "#1e1e2f"
BG_CANVAS     = "#11111b"
COLOUR_LINEAR = "#ffb347"
COLOUR_BINARY = "#6fa8dc"
COLOUR_GOLD   = "#ffd966"
COLOUR_WHITE  = "#ffffff"
COLOUR_GREEN  = "#6aa84f"
COLOUR_GREY   = "#555555"


class SearchGameGUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Search Showdown: Linear vs Binary")
        self.root.geometry("1020x800")
        self.root.configure(bg=BG_DARK)
        self._build_layout()
        self.controller = Controller(self)

    # ------------------------------------------------------------------ #
    #  Screen management                                                   #
    # ------------------------------------------------------------------ #

    def show_screen(self, screen):
        self.concept_frame.pack_forget()
        self.prequiz_frame.pack_forget()
        self.game_frame.pack_forget()
        screen.pack(fill="both", expand=True)

    def _build_layout(self):
        self._build_concept_screen()
        self._build_prequiz_screen()
        self._build_game_screen()
        self.show_screen(self.concept_frame)

    # ------------------------------------------------------------------ #
    #  Screen 1: Concept + interactive demos                              #
    # ------------------------------------------------------------------ #

    def _build_concept_screen(self):
        self.concept_frame = tk.Frame(self.root, bg=BG_DARK)

        # Scrollable wrapper so all content fits
        scroll_canvas = tk.Canvas(self.concept_frame, bg=BG_DARK, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.concept_frame, orient="vertical", command=scroll_canvas.yview)
        scroll_canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        scroll_canvas.pack(side="left", fill="both", expand=True)

        inner_frame = tk.Frame(scroll_canvas, bg=BG_DARK)
        canvas_window = scroll_canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        inner_frame.bind("<Configure>", lambda e: scroll_canvas.configure(
            scrollregion=scroll_canvas.bbox("all")))
        scroll_canvas.bind("<Configure>", lambda e: scroll_canvas.itemconfig(
            canvas_window, width=e.width))
        scroll_canvas.bind_all("<MouseWheel>", lambda e: scroll_canvas.yview_scroll(
            int(-1 * (e.delta / 120)), "units"))

        # Title
        tk.Label(
            inner_frame,
            text="Understanding Linear vs Binary Search",
            font=("Arial", 26, "bold"),
            fg=COLOUR_GOLD, bg=BG_DARK
        ).pack(pady=20)

        # Side-by-side descriptions
        columns_frame = tk.Frame(inner_frame, bg=BG_DARK)
        columns_frame.pack(pady=10)

        tk.Label(
            columns_frame,
            text=(
                "Linear Search:\n"
                "- Looks at each item ONE BY ONE\n"
                "- Like checking every locker\n"
                "  until you find the right one\n"
                "- Works on ANY list\n"
                "- Can be slow on big lists (O(n))\n"
                "  (n = number of items in the list)"
            ),
            font=("Consolas", 14),
            fg=COLOUR_LINEAR, bg=BG_DARK,
            justify="left"
        ).grid(row=0, column=0, padx=40, sticky="n")

        tk.Frame(columns_frame, bg="#444444", width=2).grid(
            row=0, column=1, sticky="ns", padx=10)

        tk.Label(
            columns_frame,
            text=(
                "Binary Search:\n"
                "- Jumps to the MIDDLE first\n"
                "- Like opening a dictionary\n"
                "  to the middle and going left or right\n"
                "- Cuts out HALF the list each step\n"
                "- ONLY works if the list is sorted!\n"
                "- Very fast on big lists (O(log n))\n"
                "  (log n ≈ 6 steps for 64 items!)"
            ),
            font=("Consolas", 14),
            fg=COLOUR_BINARY, bg=BG_DARK,
            justify="left"
        ).grid(row=0, column=2, padx=40, sticky="n")

        # Sandbox container
        sandbox_frame = tk.Frame(inner_frame, bg=BG_DARK)
        sandbox_frame.pack(pady=15)

        # ── Binary search sandbox ─────────────────────────────────────────
        tk.Label(
            sandbox_frame,
            text="Your Turn: Do Binary Search!",
            font=("Arial", 20, "bold"),
            fg=COLOUR_BINARY, bg=BG_DARK
        ).pack(pady=8)

        self.sandbox_list       = [5, 12, 18, 27, 33, 41, 56, 62, 74]
        self.sandbox_target     = 56
        self.sandbox_low        = 0
        self.sandbox_high       = len(self.sandbox_list) - 1
        self.sandbox_solved     = False
        self.sandbox_step_count = 0

        tk.Label(
            sandbox_frame,
            text=f"🎯 Find the number {self.sandbox_target} — click the MIDDLE number each time!",
            font=("Consolas", 14),
            fg=COLOUR_WHITE, bg=BG_DARK
        ).pack(pady=6)

        self.sandbox_canvas = tk.Canvas(
            sandbox_frame, width=700, height=120,
            bg=BG_CANVAS, highlightthickness=0
        )
        self.sandbox_canvas.pack()

        self.sandbox_message = tk.Label(
            sandbox_frame,
            text="Binary search always starts at the middle. Click the number in the center!",
            font=("Consolas", 13),
            fg=COLOUR_GOLD, bg=BG_DARK
        )
        self.sandbox_message.pack(pady=6)

        self.sandbox_step_label = tk.Label(
            sandbox_frame,
            text="Steps taken: 0",
            font=("Consolas", 13),
            fg=COLOUR_BINARY, bg=BG_DARK
        )
        self.sandbox_step_label.pack()

        def draw_sandbox(highlight=None, faded=None):
            self.sandbox_canvas.delete("all")
            faded = faded or set()
            x = 20
            for i, val in enumerate(self.sandbox_list):
                if i in faded:
                    colour = COLOUR_GREY
                elif i == highlight:
                    colour = COLOUR_WHITE
                else:
                    colour = "#3c78d8"
                self.sandbox_canvas.create_rectangle(x, 40, x + 60, 90, fill=colour)
                self.sandbox_canvas.create_text(
                    x + 30, 65, text=str(val),
                    fill=BG_DARK if colour == COLOUR_WHITE else COLOUR_WHITE,
                    font=("Arial", 13, "bold")
                )
                x += 70

        def reset_sandbox():
            self.sandbox_low        = 0
            self.sandbox_high       = len(self.sandbox_list) - 1
            self.sandbox_solved     = False
            self.sandbox_step_count = 0
            self.sandbox_step_label.config(text="Steps taken: 0")
            self.sandbox_message.config(
                text="Binary search always starts at the middle. Click the number in the center!"
            )
            draw_sandbox()

        def sandbox_click(event):
            if self.sandbox_solved:
                return
            if self.sandbox_low > self.sandbox_high:
                return

            clicked_index = (event.x - 20) // 70

            if clicked_index < 0 or clicked_index >= len(self.sandbox_list):
                return

            mid = (self.sandbox_low + self.sandbox_high) // 2

            if clicked_index != mid:
                self.sandbox_message.config(
                    text="Not quite! Always click the middle of the numbers that are NOT greyed out."
                )
                return

            mid_val = self.sandbox_list[mid]
            self.sandbox_step_count += 1
            self.sandbox_step_label.config(text=f"Steps taken: {self.sandbox_step_count}")
            draw_sandbox(highlight=mid)

            if mid_val == self.sandbox_target:
                self.sandbox_solved = True
                self.sandbox_message.config(
                    text=f"🎉 Found it! You found {self.sandbox_target} using binary search. "
                         f"Notice how you never had to check every number!"
                )
                tk.Button(
                    sandbox_frame,
                    text="Continue to Quick Quiz  →",
                    font=("Arial", 14, "bold"),
                    bg=COLOUR_GREEN, fg=COLOUR_WHITE,
                    command=lambda: self.show_screen(self.prequiz_frame)
                ).pack(pady=12)

            elif mid_val < self.sandbox_target:
                faded = set(range(self.sandbox_low, mid + 1))
                draw_sandbox(faded=faded)
                self.sandbox_message.config(
                    text=f"{mid_val} is too small — so {self.sandbox_target} must be on the RIGHT side. "
                         f"We can ignore everything on the left!"
                )
                self.sandbox_low = mid + 1
            else:
                faded = set(range(mid, self.sandbox_high + 1))
                draw_sandbox(faded=faded)
                self.sandbox_message.config(
                    text=f"{mid_val} is too large — so {self.sandbox_target} must be on the LEFT side. "
                         f"We can ignore everything on the right!"
                )
                self.sandbox_high = mid - 1

        self.sandbox_canvas.bind("<Button-1>", sandbox_click)
        draw_sandbox()

        tk.Button(
            sandbox_frame,
            text="Reset",
            font=("Arial", 13, "bold"),
            bg="#444444", fg=COLOUR_WHITE,
            command=reset_sandbox
        ).pack(pady=5)

        # ── Linear search demo ────────────────────────────────────────────
        tk.Label(
            sandbox_frame,
            text="Watch Linear Search — It Checks Every Single Number:",
            font=("Arial", 18, "bold"),
            fg=COLOUR_LINEAR, bg=BG_DARK
        ).pack(pady=(25, 5))

        self.linear_demo_list   = [5, 12, 18, 27, 33, 41, 56, 62, 74]
        self.linear_demo_target = 56
        self.linear_demo_index  = [0]

        self.linear_canvas = tk.Canvas(
            sandbox_frame, width=700, height=120,
            bg=BG_CANVAS, highlightthickness=0
        )
        self.linear_canvas.pack()

        self.linear_message = tk.Label(
            sandbox_frame,
            text=f"Press 'Step' to check one number at a time. How many steps to find {self.linear_demo_target}?",
            font=("Consolas", 13),
            fg=COLOUR_GOLD, bg=BG_DARK
        )
        self.linear_message.pack(pady=6)

        def draw_linear_demo(highlight=None, found_idx=None):
            self.linear_canvas.delete("all")
            x = 20
            for i, val in enumerate(self.linear_demo_list):
                if i == found_idx:
                    colour = "#93c47d"
                elif i == highlight:
                    colour = COLOUR_WHITE
                elif highlight is not None and i < highlight:
                    colour = COLOUR_GREY
                else:
                    colour = "#cc6600"
                self.linear_canvas.create_rectangle(x, 40, x + 60, 90, fill=colour)
                self.linear_canvas.create_text(
                    x + 30, 65, text=str(val),
                    fill=BG_DARK if colour in (COLOUR_WHITE, "#93c47d") else COLOUR_WHITE,
                    font=("Arial", 13, "bold")
                )
                x += 70

        draw_linear_demo()

        def linear_step():
            i = self.linear_demo_index[0]
            if i >= len(self.linear_demo_list):
                self.linear_message.config(
                    text="Linear search had to check every number in the list!"
                )
                return
            val = self.linear_demo_list[i]
            if val == self.linear_demo_target:
                draw_linear_demo(found_idx=i)
                self.linear_message.config(
                    text=f"✅ Found {self.linear_demo_target} at position {i}! "
                         f"It took {i + 1} check(s). Now imagine if the list had 1,000 numbers..."
                )
                self.linear_demo_index[0] = len(self.linear_demo_list)
            else:
                draw_linear_demo(highlight=i)
                self.linear_message.config(
                    text=f"Checking position {i}: the value is {val}. Not {self.linear_demo_target} — keep going!"
                )
                self.linear_demo_index[0] += 1

        def reset_linear_demo():
            self.linear_demo_index[0] = 0
            draw_linear_demo()
            self.linear_message.config(
                text=f"Press 'Step' to check one number at a time. How many steps to find {self.linear_demo_target}?"
            )

        linear_btn_frame = tk.Frame(sandbox_frame, bg=BG_DARK)
        linear_btn_frame.pack(pady=8)

        tk.Button(
            linear_btn_frame, text="Step →",
            font=("Arial", 14, "bold"),
            bg="#cc6600", fg=COLOUR_WHITE,
            command=linear_step
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            linear_btn_frame, text="Reset",
            font=("Arial", 14, "bold"),
            bg="#444444", fg=COLOUR_WHITE,
            command=reset_linear_demo
        ).grid(row=0, column=1, padx=10)

    # ------------------------------------------------------------------ #
    #  Screen 2: Pre-game quiz (3 questions)                              #
    # ------------------------------------------------------------------ #

    def _build_prequiz_screen(self):
        self.prequiz_frame = tk.Frame(self.root, bg=BG_DARK)

        tk.Button(
            self.prequiz_frame,
            text="← Back",
            font=("Arial", 11),
            bg="#444444", fg=COLOUR_WHITE,
            command=lambda: self.show_screen(self.concept_frame)
        ).pack(anchor="w", padx=20, pady=(15, 0))

        tk.Label(
            self.prequiz_frame,
            text="Quick Check Before You Play",
            font=("Arial", 24, "bold"),
            fg=COLOUR_BINARY, bg=BG_DARK
        ).pack(pady=15)

        # ── Question 1 ────────────────────────────────────────────────────
        tk.Label(
            self.prequiz_frame,
            text="1.  Which search algorithm requires the list to be sorted?",
            font=("Consolas", 15),
            fg=COLOUR_WHITE, bg=BG_DARK
        ).pack(pady=(10, 2))

        self.prequiz_answer1 = tk.StringVar()

        tk.Radiobutton(
            self.prequiz_frame, text="Linear Search",
            variable=self.prequiz_answer1, value="linear",
            font=("Arial", 13), fg=COLOUR_LINEAR,
            bg=BG_DARK, selectcolor=BG_DARK
        ).pack()

        tk.Radiobutton(
            self.prequiz_frame, text="Binary Search",
            variable=self.prequiz_answer1, value="binary",
            font=("Arial", 13), fg=COLOUR_BINARY,
            bg=BG_DARK, selectcolor=BG_DARK
        ).pack()

        # ── Question 2 ────────────────────────────────────────────────────
        tk.Label(
            self.prequiz_frame,
            text="2.  Which algorithm checks every item one by one from left to right?",
            font=("Consolas", 15),
            fg=COLOUR_WHITE, bg=BG_DARK
        ).pack(pady=(15, 2))

        self.prequiz_answer2 = tk.StringVar()

        tk.Radiobutton(
            self.prequiz_frame, text="Linear Search",
            variable=self.prequiz_answer2, value="linear",
            font=("Arial", 13), fg=COLOUR_LINEAR,
            bg=BG_DARK, selectcolor=BG_DARK
        ).pack()

        tk.Radiobutton(
            self.prequiz_frame, text="Binary Search",
            variable=self.prequiz_answer2, value="binary",
            font=("Arial", 13), fg=COLOUR_BINARY,
            bg=BG_DARK, selectcolor=BG_DARK
        ).pack()

        # ── Question 3 ────────────────────────────────────────────────────
        tk.Label(
            self.prequiz_frame,
            text="3.  A sorted list has 64 items. About how many steps does binary search need?",
            font=("Consolas", 15),
            fg=COLOUR_WHITE, bg=BG_DARK
        ).pack(pady=(15, 2))

        self.prequiz_answer3 = tk.StringVar()

        tk.Radiobutton(
            self.prequiz_frame, text="About 6 steps",
            variable=self.prequiz_answer3, value="6",
            font=("Arial", 13), fg=COLOUR_BINARY,
            bg=BG_DARK, selectcolor=BG_DARK
        ).pack()

        tk.Radiobutton(
            self.prequiz_frame, text="About 32 steps",
            variable=self.prequiz_answer3, value="32",
            font=("Arial", 13), fg=COLOUR_BINARY,
            bg=BG_DARK, selectcolor=BG_DARK
        ).pack()

        tk.Radiobutton(
            self.prequiz_frame, text="All 64 steps",
            variable=self.prequiz_answer3, value="64",
            font=("Arial", 13), fg=COLOUR_BINARY,
            bg=BG_DARK, selectcolor=BG_DARK
        ).pack()

        # ── Feedback + submit ─────────────────────────────────────────────
        self.prequiz_feedback = tk.Label(
            self.prequiz_frame,
            text="",
            font=("Arial", 13, "italic"),
            fg=COLOUR_GOLD, bg=BG_DARK
        )
        self.prequiz_feedback.pack(pady=10)

        tk.Button(
            self.prequiz_frame,
            text="Submit & Start the Game",
            font=("Arial", 14, "bold"),
            bg="#3c78d8", fg=COLOUR_WHITE,
            command=self._submit_prequiz
        ).pack(pady=15)

    def _submit_prequiz(self):
        # Require all three questions to be answered
        if not self.prequiz_answer1.get() or not self.prequiz_answer2.get() or not self.prequiz_answer3.get():
            self.prequiz_feedback.config(
                text="Please answer all three questions before continuing!",
                fg="#e06666"
            )
            return

        correct = 0
        if self.prequiz_answer1.get() == "binary":
            correct += 1
        if self.prequiz_answer2.get() == "linear":
            correct += 1
        if self.prequiz_answer3.get() == "6":
            correct += 1

        if correct == 3:
            self.prequiz_feedback.config(
                text="✅ Perfect! 3/3 correct! You're ready to play!",
                fg=COLOUR_GREEN
            )
        elif correct == 2:
            self.prequiz_feedback.config(
                text=f"Good job! {correct}/3 correct. Let's see the algorithms in action!",
                fg=COLOUR_GOLD
            )
        else:
            self.prequiz_feedback.config(
                text=f"{correct}/3 correct — try reviewing the concept screen! Let's play anyway.",
                fg="#e06666"
            )

        self.root.after(1800, lambda: self.show_screen(self.game_frame))

    # ------------------------------------------------------------------ #
    #  Screen 3: Main game                                                #
    # ------------------------------------------------------------------ #

    def _build_game_screen(self):
        self.game_frame = tk.Frame(self.root, bg=BG_DARK)

        tk.Label(
            self.game_frame,
            text="Search Showdown: Linear vs Binary",
            font=("Arial", 22, "bold"),
            fg=COLOUR_WHITE, bg=BG_DARK
        ).pack(pady=8)

        tk.Button(
            self.game_frame,
            text="← Back",
            font=("Arial", 11),
            bg="#444444", fg=COLOUR_WHITE,
            command=lambda: self.show_screen(self.prequiz_frame)
        ).pack(anchor="w", padx=20)

        # Score + prediction row
        top_row = tk.Frame(self.game_frame, bg=BG_DARK)
        top_row.pack(pady=5)

        self.score_label = tk.Label(
            top_row, text="Score: 0",
            font=("Arial", 14, "bold"),
            fg=COLOUR_GOLD, bg=BG_DARK
        )
        self.score_label.grid(row=0, column=0, padx=20)

        tk.Label(
            top_row, text="Predict the winner:",
            font=("Arial", 13),
            fg=COLOUR_WHITE, bg=BG_DARK
        ).grid(row=0, column=1, padx=10)

        self.prediction = tk.StringVar()

        tk.Radiobutton(
            top_row, text="Linear",
            variable=self.prediction, value="linear",
            font=("Arial", 12), fg=COLOUR_LINEAR,
            bg=BG_DARK, selectcolor=BG_DARK
        ).grid(row=0, column=2, padx=5)

        tk.Radiobutton(
            top_row, text="Binary",
            variable=self.prediction, value="binary",
            font=("Arial", 12), fg=COLOUR_BINARY,
            bg=BG_DARK, selectcolor=BG_DARK
        ).grid(row=0, column=3, padx=5)

        # Algorithm hint row
        hint_row = tk.Frame(self.game_frame, bg=BG_DARK)
        hint_row.pack(pady=3)

        tk.Label(
            hint_row,
            text="Linear: checks every element in order   O(n)",
            font=("Arial", 11, "bold"),
            fg=COLOUR_LINEAR, bg=BG_DARK
        ).grid(row=0, column=0, padx=25)

        tk.Label(
            hint_row,
            text="Binary: cuts the list in half each step   O(log n)",
            font=("Arial", 11, "bold"),
            fg=COLOUR_BINARY, bg=BG_DARK
        ).grid(row=0, column=1, padx=25)

        # Linear canvas + labels
        self.canvas_linear = tk.Canvas(
            self.game_frame, width=950, height=110,
            bg=BG_CANVAS, highlightthickness=0
        )
        self.canvas_linear.pack(pady=6)

        tk.Label(
            self.game_frame, text="Linear Search",
            font=("Arial", 11, "bold"),
            fg=COLOUR_LINEAR, bg=BG_DARK
        ).pack()

        self.linear_step_label = tk.Label(
            self.game_frame, text="Steps: 0",
            font=("Arial", 10), fg=COLOUR_LINEAR, bg=BG_DARK
        )
        self.linear_step_label.pack()

        # Binary canvas + labels
        self.canvas_binary = tk.Canvas(
            self.game_frame, width=950, height=110,
            bg=BG_CANVAS, highlightthickness=0
        )
        self.canvas_binary.pack(pady=6)

        tk.Label(
            self.game_frame, text="Binary Search",
            font=("Arial", 11, "bold"),
            fg=COLOUR_BINARY, bg=BG_DARK
        ).pack()

        self.binary_step_label = tk.Label(
            self.game_frame, text="Steps: 0",
            font=("Arial", 10), fg=COLOUR_BINARY, bg=BG_DARK
        )
        self.binary_step_label.pack()

        # Control buttons
        control_row = tk.Frame(self.game_frame, bg=BG_DARK)
        control_row.pack(pady=8)

        tk.Button(
            control_row, text="New Round",
            command=lambda: self.controller.new_round(),
            font=("Arial", 12, "bold"),
            bg="#3c78d8", fg=COLOUR_WHITE,
            activebackground="#285bac"
        ).grid(row=0, column=0, padx=10)

        tk.Label(
            control_row, text="Target:",
            font=("Arial", 12),
            fg=COLOUR_WHITE, bg=BG_DARK
        ).grid(row=0, column=1)

        self.target_entry = tk.Entry(control_row, width=8, font=("Arial", 12))
        self.target_entry.grid(row=0, column=2, padx=5)

        tk.Button(
            control_row, text="Start Showdown",
            command=lambda: self.controller.start_round(),
            font=("Arial", 12, "bold"),
            bg=COLOUR_GREEN, fg=COLOUR_WHITE,
            activebackground="#38761d"
        ).grid(row=0, column=3, padx=10)

        # Explanation text box
        self.explanation = tk.Text(
            self.game_frame, height=7, width=110,
            wrap="word", bg="#1b1b2f", fg=COLOUR_WHITE,
            font=("Consolas", 13, "bold")
        )
        self.explanation.pack(pady=6)
        self.explanation.insert("end", "Click 'New Round' to generate a list and begin.\n")
        self.explanation.config(state="disabled")

    # ------------------------------------------------------------------ #
    #  Drawing helpers                                                     #
    # ------------------------------------------------------------------ #

    def draw_list(self, canvas, lst, highlight=None, discarded=None, mode="linear", grow=False):
        canvas.delete("all")
        discarded   = discarded or set()
        base_colour = COLOUR_LINEAR if mode == "linear" else COLOUR_BINARY
        x = 20

        for i, val in enumerate(lst):
            if i in discarded:
                colour = COLOUR_GREY
            elif i == highlight:
                colour = COLOUR_WHITE
            else:
                colour = base_colour

            w, h = (50, 60) if (i == highlight and grow) else (40, 50)
            x1, y1 = x, 35
            x2, y2 = x1 + w, y1 + h

            canvas.create_rectangle(x1, y1, x2, y2, fill=colour, outline="#000000")
            canvas.create_text(
                (x1 + x2) // 2, (y1 + y2) // 2,
                text=str(val),
                fill=BG_DARK if colour == COLOUR_WHITE else COLOUR_WHITE,
                font=("Arial", 11, "bold")
            )
            x += 55

    def write_explanation(self, text):
        self.explanation.config(state="normal")
        self.explanation.insert("end", text + "\n")
        self.explanation.see("end")
        self.explanation.config(state="disabled")

    def update_score(self, score):
        self.score_label.config(text=f"Score: {score}")

    def run(self):
        self.root.mainloop()
