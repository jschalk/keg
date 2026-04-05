"""
etl_gui.py  —  Simple GUI launcher for the Excel ETL pipeline.

Usage:
    python etl_gui.py

Requires:
    Python 3.8+ (tkinter is included in the standard library)

To integrate your CLI logic, replace the `create_today_punchs()` call inside
`_run()` with your actual ETL function / subprocess call.
"""

import os
import platform
from src.ch21_world.world import create_today_punchs
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# ──────────────────────────────────────────────
#  Stub — replace with your real ETL logic
# ──────────────────────────────────────────────


# ──────────────────────────────────────────────
#  Helpers
# ──────────────────────────────────────────────
MONO = ("Courier New", 9) if platform.system() == "Windows" else ("Menlo", 10)

BG = "#1a1a1f"
BG_CARD = "#22222a"
BORDER = "#33333d"
ACCENT = "#e8c547"  # amber — classic ETL/data pipeline energy
ACCENT_DIM = "#b89a2f"
FG = "#e4e4e8"
FG_DIM = "#7a7a88"
ENTRY_BG = "#13131a"
BTN_ACTIVE = "#f0d060"


class OptionTable(tk.Frame):
    def __init__(self, parent, options: dict, **kwargs):
        super().__init__(parent, **kwargs)
        self.options = options  # {description: function}
        self._build()

    def _build(self):
        # Scrollable Treeview
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("action",),
            show="headings",
            selectmode="browse",
            yscrollcommand=scrollbar.set,
            height=5,  # always shows exactly 5 rows
        )
        scrollbar.config(command=self.tree.yview)

        self.tree.heading("action", text="Additional Special Actions")
        self.tree.column("action", anchor=tk.W)

        for description in self.options:
            self.tree.insert("", tk.END, values=(description,))

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def _on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        description = self.tree.item(selected[0], "values")[0]
        fn = self.options.get(description)
        if callable(fn):
            fn()


def open_directory(path: str) -> None:
    """Open a folder in the OS file explorer."""
    system = platform.system()
    if system == "Windows":
        os.startfile(path)  # noqa: S606
    elif system == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


# ──────────────────────────────────────────────
#  Main application window
# ──────────────────────────────────────────────
class ETLApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ETL Pipeline")
        self.resizable(False, False)
        self.configure(bg=BG)

        # Set a reasonable minimum size and centre on screen
        self.update_idletasks()
        w, h = 560, 430
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h+120}+{x}+{y}")

        # String vars ─ empty string = "not set" (optional dirs stay None)
        self._working = tk.StringVar()
        self._input = tk.StringVar()
        self._output = tk.StringVar()
        self._person = tk.StringVar()

        # Your config: description -> function
        self._build_ui()

    def create_five_time_config_file(self):
        # TODO dataframes and save to file
        # prnt("create_five_time_config_file...")
        pass

    def create_random_time_config_file(self):
        # TODO dataframes and save to file
        # prnt("create_random_time_config_file...")
        pass

    def create_emmanuel_stance_file(self):
        # TODO dataframes and save to file
        # prnt("create_emmanuel_stance_file...")
        pass

    def create_example_moment_ledger_file(self):
        # TODO dataframes and save to file
        # prnt("create_example_moment_ledger_file...")
        pass

    def create_example_moment_budget_file(self):
        # TODO dataframes and save to file
        # prnt("create_example_moment_budget_file...")
        pass

    # ── UI construction ────────────────────────
    def _build_ui(self):
        # ── header bar ──────────────────────────
        header = tk.Frame(self, bg=ACCENT, height=4)
        header.pack(fill="x")

        title_frame = tk.Frame(self, bg=BG, pady=18)
        title_frame.pack(fill="x", padx=28)

        tk.Label(
            title_frame,
            text="ETL  PIPELINE",
            font=(
                ("Courier New", 17, "bold")
                if platform.system() == "Windows"
                else ("Menlo", 16, "bold")
            ),
            bg=BG,
            fg=ACCENT,
            anchor="w",
        ).pack(side="left")

        tk.Label(
            title_frame,
            text="xlsx → transform → output",
            font=MONO,
            bg=BG,
            fg=FG_DIM,
            anchor="e",
        ).pack(side="right", pady=(4, 0))

        # ── divider ─────────────────────────────
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=28)

        # ── directory pickers ───────────────────
        card = tk.Frame(self, bg=BG_CARD, bd=0, padx=24, pady=20)
        card.pack(fill="x", padx=28, pady=(16, 0))

        self._dir_row(
            card,
            0,
            "WORKING DIR",
            self._working,
            required=True,
            tip="Root directory for the ETL process",
        )
        self._dir_row(
            card,
            1,
            "INPUT DIR  ",
            self._input,
            required=False,
            tip="Source Excel files  (optional)",
        )
        self._dir_row(
            card,
            2,
            "OUTPUT DIR ",
            self._output,
            required=False,
            tip="Destination for results  (optional — opened on finish)",
        )
        self._text_row(
            card,
            3,
            "PERSON NAME",
            self._person,
            required=False,
            tip="Filter by person name  (optional)",
        )

        # ── run button ──────────────────────────
        btn_frame = tk.Frame(self, bg=BG, pady=22)
        btn_frame.pack()

        self._run_btn = tk.Button(
            btn_frame,
            text="▶  RUN PIPELINE",
            font=(
                ("Courier New", 11, "bold")
                if platform.system() == "Windows"
                else ("Menlo", 11, "bold")
            ),
            bg=ACCENT,
            fg="#0d0d10",
            activebackground=BTN_ACTIVE,
            activeforeground="#0d0d10",
            relief="flat",
            bd=0,
            padx=28,
            pady=10,
            cursor="hand2",
            command=self._run,
        )
        self._run_btn.pack()

        options = {
            "create_five_time_config_file": self.create_five_time_config_file,
            "create_random_time_config_file": self.create_random_time_config_file,
            "create_emmanuel_stance_file": self.create_emmanuel_stance_file,
            "create_example_moment_ledger_file": self.create_example_moment_ledger_file,
            "create_example_moment_budget_file": self.create_example_moment_budget_file,
        }
        table = OptionTable(self, options)
        table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # hover effect
        self._run_btn.bind("<Enter>", lambda _: self._run_btn.configure(bg=BTN_ACTIVE))
        self._run_btn.bind("<Leave>", lambda _: self._run_btn.configure(bg=ACCENT))

        # ── status bar ──────────────────────────
        self._status = tk.StringVar(value="Ready.")
        status_bar = tk.Label(
            self,
            textvariable=self._status,
            font=MONO,
            bg=BG,
            fg=FG_DIM,
            anchor="w",
            padx=28,
            pady=6,
        )
        status_bar.pack(fill="x", side="bottom")

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", side="bottom")

    def _dir_row(self, parent, row, label, var, *, required, tip):
        """Render one label + entry + browse button row."""
        lbl_text = f"{'*' if required else ' '} {label}"

        tk.Label(
            parent,
            text=lbl_text,
            font=MONO,
            bg=BG_CARD,
            fg=ACCENT if required else FG_DIM,
            width=14,
            anchor="w",
        ).grid(row=row, column=0, padx=(0, 10), pady=7, sticky="w")

        entry = tk.Entry(
            parent,
            textvariable=var,
            font=MONO,
            bg=ENTRY_BG,
            fg=FG,
            insertbackground=ACCENT,
            relief="flat",
            bd=0,
            width=32,
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=ACCENT,
        )
        entry.grid(row=row, column=1, pady=7, ipady=5, sticky="ew")

        # Tooltip-style placeholder
        if not required:
            self._placeholder(entry, var, tip)

        tk.Button(
            parent,
            text="…",
            font=MONO,
            bg=BORDER,
            fg=FG,
            activebackground=ACCENT,
            activeforeground="#0d0d10",
            relief="flat",
            bd=0,
            padx=10,
            pady=4,
            cursor="hand2",
            command=lambda v=var: self._browse(v),
        ).grid(row=row, column=2, padx=(8, 0), pady=7)

        parent.columnconfigure(1, weight=1)

    def _text_row(self, parent, row, label, var, *, required, tip):
        """Render one label + plain text entry row (no browse button)."""
        lbl_text = f"{'*' if required else ' '} {label}"

        tk.Label(
            parent,
            text=lbl_text,
            font=MONO,
            bg=BG_CARD,
            fg=ACCENT if required else FG_DIM,
            width=14,
            anchor="w",
        ).grid(row=row, column=0, padx=(0, 10), pady=7, sticky="w")

        entry = tk.Entry(
            parent,
            textvariable=var,
            font=MONO,
            bg=ENTRY_BG,
            fg=FG,
            insertbackground=ACCENT,
            relief="flat",
            bd=0,
            width=32,
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=ACCENT,
        )
        entry.grid(row=row, column=1, columnspan=2, pady=7, ipady=5, sticky="ew")

        if not required:
            self._placeholder(entry, var, tip)

    @staticmethod
    def _placeholder(entry, var, tip):
        """Light placeholder text for optional fields."""
        entry.configure(fg=FG_DIM)
        entry.insert(0, tip)

        def on_focus_in(_):
            if var.get() == tip:
                entry.delete(0, "end")
                entry.configure(fg=FG)

        def on_focus_out(_):
            if not entry.get():
                entry.insert(0, tip)
                entry.configure(fg=FG_DIM)
                var.set("")  # keep the StringVar clean

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    # ── browse helper ──────────────────────────
    @staticmethod
    def _browse(var: tk.StringVar):
        if path := filedialog.askdirectory(title="Select directory"):
            var.set(path)

    # ── run handler ────────────────────────────
    def _run(self):
        working = self._working.get().strip()
        input_ = self._input.get().strip()
        output = self._output.get().strip()
        person = self._person.get().strip()

        # Treat placeholder text as empty
        input_ = input_ if os.path.isdir(input_) else None
        output = output if os.path.isdir(output) else None
        person = person if person and not person.startswith("Filter by") else None

        # Validate required field
        if not working or not os.path.isdir(working):
            messagebox.showerror(
                "Missing working directory",
                "Please select a valid working directory before running.",
            )
            return

        # Lock UI
        self._run_btn.configure(state="disabled", text="⏳  Running…", bg=ACCENT_DIM)
        self._status.set("Running ETL pipeline…")
        self.update_idletasks()

        try:
            create_today_punchs(working, input_, output, person)
            self._status.set("✔  Pipeline completed successfully.")
            messagebox.showinfo("Done", "ETL pipeline finished successfully.")
        except Exception as exc:  # noqa: BLE001
            self._status.set(f"✘  Error: {exc}")
            messagebox.showerror("Pipeline error", str(exc))
        finally:
            self._run_btn.configure(state="normal", text="▶  RUN PIPELINE", bg=ACCENT)

        # Open output directory if one was given
        if output and os.path.isdir(output):
            open_directory(output)


# ──────────────────────────────────────────────
#  Entry point
# ──────────────────────────────────────────────
if __name__ == "__main__":
    app = ETLApp()
    app.mainloop()
