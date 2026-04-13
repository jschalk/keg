"""
etl_gui.py  —  Simple GUI launcher for the Excel ETL pipeline.

Usage:
    python etl_gui.py

Requires:
    Python 3.8+ (tkinter is included in the standard library)

To integrate your CLI logic, replace the `create_today_punchs()` call inside
`_run()` with your actual ETL function / subprocess call.
"""

from os.path import isdir as os_path_isdir
from platform import system as platform_system
from src.ch21_world.world import create_today_punchs
from src.ch30_etl_app.etl_gui_tool import (
    get_app_default_dir,
    get_app_default_dirs,
    get_app_default_person_name,
    get_app_glb_attrs,
    get_option_table_options,
)
from subprocess import Popen as subprocess_Popen
import tkinter as tk
from tkinter import (
    filedialog as tkinter_filedialog,
    messagebox as tkinter_messagebox,
    ttk as tkinter_ttk,
)


class OptionTable(tk.Frame):
    def __init__(self, parent, options: dict, b_src_dir: str, **kwargs):
        super().__init__(parent, **kwargs)
        self.options = options
        self.b_src_dir = b_src_dir
        self._build()

    def _build(self):
        # Scrollable Treeview
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = tkinter_ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        self.tree = tkinter_ttk.Treeview(
            tree_frame,
            columns=("action",),
            show="headings",
            selectmode="browse",
            yscrollcommand=scrollbar.set,
            height=5,  # always shows exactly 5 rows
        )
        scrollbar.config(command=self.tree.yview)

        self.tree.heading("action", text="Click to add Beliefs to Beliefs Directory")
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
            fn(self.b_src_dir())  # ← call it to get the current string value


def open_directory(path: str) -> None:
    system = platform_system()

    if system == "Windows":
        subprocess_Popen(["explorer", path])

    elif system == "Darwin":
        subprocess_Popen(["open", path])

    else:
        subprocess_Popen(["xdg-open", path])


# ──────────────────────────────────────────────
#  Main application window
# ──────────────────────────────────────────────
class ETLApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Listening using Keg2 — ETL Launcher")
        self.resizable(False, False)
        ax = get_app_glb_attrs()
        self.configure(bg=ax.bg)

        # Set a reasonable minimum size and centre on screen
        self.update_idletasks()
        app_width, app_height = 640, 540
        x = (self.winfo_screenwidth() - app_width) // 2
        y = (self.winfo_screenheight() - app_height) // 2
        self.geometry(f"{app_width}x{app_height+120}+{x}+{y}")

        # String vars ─ empty string = "not set" (optional dirs stay None)
        self._world_name = tk.StringVar()
        self._person = tk.StringVar()
        self._working = tk.StringVar()
        self._b_src_dir = tk.StringVar()
        self._i_src_dir = tk.StringVar()
        self._output = tk.StringVar()

        # Your config: description -> function
        self._build_ui()
        self._set_defaults()

    def _set_defaults(self):
        vars_map = {
            "world_name": self._world_name,
            "working": self._working,
            "beliefs_src": self._b_src_dir,
            "ideas_src": self._i_src_dir,
            "output": self._output,
            "person": self._person,
        }
        defaults = get_app_default_dirs(get_app_default_dir())
        defaults["person"] = get_app_default_person_name()
        defaults["person"] = get_app_default_person_name()

        for key, var in vars_map.items():
            if defaults.get(key) is None:
                raise Exception(f"Missing default {key=}")
            var.set(defaults[key])

    def _open_dir(self, var: tk.StringVar):
        path = var.get().strip()
        if os_path_isdir(path):
            open_directory(path)
        else:
            invalid_dir_str = f"Not a valid directory:\n{path}"
            tkinter_messagebox.showwarning("Invalid directory", invalid_dir_str)

    # ── UI construction ────────────────────────
    def get_main_rows_config(self) -> dict:
        return {
            "0": {
                "row_type": "text",
                "title": "PERSON NAME",
                "var": self._person,
                "required": True,
                "tip": "e.g. 'Emmanuel'",
            },
            "1": {
                "row_type": "dir",
                "title": "WORKING DIR",
                "var": self._working,
                "required": True,
                "tip": "Root directory for the ETL process",
            },
            "2": {
                "row_type": "dir",
                "title": "BELIEFS_DIR",
                "var": self._b_src_dir,
                "required": True,
                "tip": "Source of Beliefs. Non-sparked Ideas.",
            },
            "3": {
                "row_type": "dir",
                "title": "IDEAS_DIR  ",
                "var": self._i_src_dir,
                "required": True,
                "tip": "Source of Ideas files. Beliefs that have been sparked.",
            },
            "4": {
                "row_type": "dir",
                "title": "OUTPUT DIR ",
                "var": self._output,
                "required": True,
                "tip": "Destination for results (opened on finish)",
            },
        }

    def _create_dir_rows(self, card):
        for row_number, row_dict in self.get_main_rows_config().items():
            row_int = int(row_number)
            title = row_dict.get("title")
            var = row_dict.get("var")
            req = row_dict.get("required")
            tip = row_dict.get("tip")

            if row_dict.get("row_type") == "text":
                self._text_row(card, row_int, title, var, required=req, tip=tip)
            elif row_dict.get("row_type") == "dir":
                self._dir_row(card, row_int, title, var, required=req, tip=tip)

    def _dir_row(self, parent, row, label, var, *, required, tip):
        """Render one label + entry + browse button row."""
        ax = get_app_glb_attrs()
        lbl_text = f"{'*' if required else ' '} {label}"

        tk.Label(
            parent,
            text=lbl_text,
            font=ax.mono,
            bg=ax.bg_card,
            fg=ax.accent if required else ax.fg_dim,
            width=14,
            anchor="w",
        ).grid(row=row, column=0, padx=(0, 10), pady=7, sticky="w")

        entry = tk.Entry(
            parent,
            textvariable=var,
            font=ax.mono,
            bg=ax.entry_bg,
            fg=ax.fg,
            insertbackground=ax.accent,
            relief="flat",
            bd=0,
            width=32,
            highlightthickness=1,
            highlightbackground=ax.border,
            highlightcolor=ax.accent,
        )
        entry.grid(row=row, column=1, pady=7, ipady=5, sticky="ew")

        # Tooltip-style placeholder
        if not required:
            self._placeholder(entry, var, tip)

        tk.Button(
            parent,
            text="…",
            font=ax.mono,
            bg=ax.border,
            fg=ax.fg,
            activebackground=ax.accent,
            activeforeground=ax.fg_black,
            relief="flat",
            bd=0,
            padx=10,
            pady=4,
            cursor="hand2",
            command=lambda v=var: self._browse(v),
        ).grid(row=row, column=2, padx=(8, 0), pady=7)
        tk.Button(
            parent,
            text="📂",  # or use "📂" if your font supports it
            font=ax.mono,
            bg=ax.border,
            fg=ax.fg,
            activebackground=ax.accent,
            activeforeground=ax.fg_black,
            relief="flat",
            bd=0,
            padx=10,
            pady=4,
            cursor="hand2",
            command=lambda v=var: self._open_dir(v),
        ).grid(row=row, column=3, padx=(4, 0), pady=7)
        parent.columnconfigure(1, weight=1)
        parent.columnconfigure(3, weight=0)

    def _text_row(self, parent, row, label, var, *, required, tip):
        """Render one label + plain text entry row (no browse button)."""
        ax = get_app_glb_attrs()
        lbl_text = f"{'*' if required else ' '} {label}"

        tk.Label(
            parent,
            text=lbl_text,
            font=ax.mono,
            bg=ax.bg_card,
            fg=ax.accent if required else ax.fg_dim,
            width=14,
            anchor="w",
        ).grid(row=row, column=0, padx=(0, 10), pady=7, sticky="w")

        entry = tk.Entry(
            parent,
            textvariable=var,
            font=ax.mono,
            bg=ax.entry_bg,
            fg=ax.fg,
            insertbackground=ax.accent,
            relief="flat",
            bd=0,
            width=32,
            highlightthickness=1,
            highlightbackground=ax.border,
            highlightcolor=ax.accent,
        )
        entry.grid(row=row, column=1, columnspan=2, pady=7, ipady=5, sticky="ew")

        if not required:
            self._placeholder(entry, var, tip)

    def _build_ui(self):
        # ── header bar ──────────────────────────
        ax = get_app_glb_attrs()
        header = tk.Frame(self, bg=ax.accent, height=4)
        header.pack(fill="x")

        title_frame = tk.Frame(self, bg=ax.bg, pady=18)
        title_frame.pack(fill="x", padx=28)

        tk.Label(
            title_frame,
            text="Keg Listening App#1",
            font=ax.platform_font,
            bg=ax.bg,
            fg=ax.accent,
            anchor="w",
        ).pack(side="left")

        tk.Label(
            title_frame,
            text="excel files → db → daily agendas",
            font=ax.mono,
            bg=ax.bg,
            fg=ax.fg_dim,
            anchor="e",
        ).pack(side="right", pady=(4, 0))

        # ── divider ─────────────────────────────
        tk.Frame(self, bg=ax.border, height=1).pack(fill="x", padx=28)

        # ── directory pickers ───────────────────
        card = tk.Frame(self, bg=ax.bg_card, bd=0, padx=24, pady=20)
        card.pack(fill="x", padx=28, pady=(16, 0))
        self._create_dir_rows(card)

        # ── run button ──────────────────────────
        btn_frame = tk.Frame(self, bg=ax.bg, pady=22)
        btn_frame.pack()

        self._run_btn = tk.Button(
            btn_frame,
            text="▶  CREATE DAILY AGENDA",
            font=ax.platform_font,
            bg=ax.accent,
            fg=ax.fg_black,
            activebackground=ax.btn_active,
            activeforeground=ax.fg_black,
            relief="flat",
            bd=0,
            padx=28,
            pady=10,
            cursor="hand2",
            command=self._run,
        )
        self._run_btn.pack()
        options = get_option_table_options()
        table = OptionTable(self, options, b_src_dir=self._b_src_dir.get)
        table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # hover effect
        self._run_btn.bind(
            "<Enter>", lambda _: self._run_btn.configure(bg=ax.btn_active)
        )
        self._run_btn.bind("<Leave>", lambda _: self._run_btn.configure(bg=ax.accent))

        # ── status bar ──────────────────────────
        self._status = tk.StringVar(value="Ready.")
        status_bar = tk.Label(
            self,
            textvariable=self._status,
            font=ax.mono,
            bg=ax.bg,
            fg=ax.fg_dim,
            anchor="w",
            padx=28,
            pady=6,
        )
        status_bar.pack(fill="x", side="bottom")

        tk.Frame(self, bg=ax.border, height=1).pack(fill="x", side="bottom")

    @staticmethod
    def _placeholder(entry, var, tip):
        """Light placeholder text for optional fields."""
        ax = get_app_glb_attrs()
        entry.configure(fg=ax.fg_dim)
        entry.insert(0, tip)

        def on_focus_in(_):
            if var.get() == tip:
                entry.delete(0, "end")
                entry.configure(fg=ax.fg)

        def on_focus_out(_):
            if not entry.get():
                entry.insert(0, tip)
                entry.configure(fg=ax.fg_dim)
                var.set("")  # keep the StringVar clean

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    # ── browse helper ──────────────────────────
    @staticmethod
    def _browse(var: tk.StringVar):
        if path := tkinter_filedialog.askdirectory(title="Select directory"):
            var.set(path)

    # ── run handler ────────────────────────────
    def _run(self):
        ax = get_app_glb_attrs()
        person = self._person.get().strip()
        working = self._working.get().strip()
        b_src_dir_ = self._b_src_dir.get().strip()
        i_src_dir_ = self._i_src_dir.get().strip()
        output = self._output.get().strip()

        # Treat placeholder text as empty
        b_src_dir_ = b_src_dir_ if os_path_isdir(b_src_dir_) else None
        i_src_dir_ = i_src_dir_ if os_path_isdir(i_src_dir_) else None
        output = output if os_path_isdir(output) else None
        person = person if person and not person.startswith("Filter by") else None

        # Validate required field
        if not working or not os_path_isdir(working):
            tkinter_messagebox.showerror(
                "Missing working directory",
                "Please select a valid working directory before running.",
            )
            return

        # Lock UI
        self._run_btn.configure(state="disabled", text="⏳  Running…", bg=ax.accent_dim)
        self._status.set("Running ETL pipeline…")
        self.update_idletasks()

        try:
            create_today_punchs(
                person_name=person,
                world_name=self._world_name.get(),
                worlds_dir=self._working.get(),
                output_dir=self._output.get(),
                ideas_src_dir=self._i_src_dir.get(),
                beliefs_src_dir=self._b_src_dir.get(),
            )
            self._status.set("✔  Pipeline completed successfully.")
            tkinter_messagebox.showinfo("Done", "ETL pipeline finished successfully.")
        except Exception as exc:  # noqa: BLE001
            self._status.set(f"✘  Error: {exc}")
            tkinter_messagebox.showerror("Pipeline error", str(exc))
        finally:
            self._run_btn.configure(
                state="normal", text="▶  RUN PIPELINE", bg=ax.accent
            )

        # Open output directory if one was given
        if output and os_path_isdir(output):
            open_directory(output)


# ──────────────────────────────────────────────
#  Entry point
# ──────────────────────────────────────────────
if __name__ == "__main__":
    app = ETLApp()
    app.mainloop()
