"""
etl_gui.py  —  Simple GUI launcher for the Excel ETL pipeline.

Usage:
    python etl_gui.py

Requires:
    Python 3.8+ (tkinter is included in the standard library)

To integrate your CLI logic, replace the `create_today_punchs()` call inside
`_run()` with your actual ETL function / subprocess call.
"""

from ch00_py.file_toolbox import delete_dir, open_file, set_dir
from ch17_brick.brick_db_tool import prettify_excel_files
from ch25_kpi.gcalendar import mind_to_person_gcal_day_punchs
from ch26_world.world import create_today_punchs
from ch30_etl_app.etl_gui_tool import (
    fill_spark_face_in_directory,
    get_app_default_dir,
    get_app_default_dirs,
    get_app_default_me_personname,
    get_app_default_you_personname,
    get_app_glb_attrs,
    get_option_table_options,
)
from importlib.metadata import version as metadata_version
from os import listdir as os_listdir
from os.path import (
    isdir as os_path_isdir,
    isfile as os_path_isfile,
    join as os_path_join,
)
from platform import system as platform_system
from subprocess import Popen as subprocess_Popen
from tkinter import (
    BOTH as tk_BOTH,
    END as tk_END,
    LEFT as tk_LEFT,
    RIGHT as tk_RIGHT,
    VERTICAL as tk_VERTICAL,
    WORD as tk_WORD,
    Button as tk_Button,
    Entry as tk_Entry,
    Frame as tk_Frame,
    Label as tk_Label,
    StringVar as tk_StringVar,
    Text as tk_Text,
    Tk as tk_Tk,
    W as tk_W,
    Y as tk_Y,
    filedialog as tkinter_filedialog,
    messagebox as tkinter_messagebox,
    ttk as tkinter_ttk,
)
from tkinter.scrolledtext import ScrolledText as tk_ScrolledText


class OptionTable(tk_Frame):
    def __init__(
        self,
        parent,
        options: dict,
        i_src_dir: str,
        me_personname,
        on_select_callback=None,
        **kwargs,
    ):
        super().__init__(parent, **kwargs)
        self.options = options
        self.i_src_dir = i_src_dir
        self.me_personname = me_personname
        self.on_select_callback = on_select_callback
        self._build()

    def _build(self):
        # Scrollable Treeview
        tree_frame = tk_Frame(self)
        tree_frame.pack(fill=tk_BOTH, expand=True)

        scrollbar = tkinter_ttk.Scrollbar(tree_frame, orient=tk_VERTICAL)
        self.tree = tkinter_ttk.Treeview(
            tree_frame,
            columns=("action",),
            show="headings",
            selectmode="browse",
            yscrollcommand=scrollbar.set,
            height=5,  # always shows exactly 5 rows
        )
        scrollbar.config(command=self.tree.yview)

        action_str = "Click to add Example Ideas to Ideas Directory"
        self.tree.heading("action", text=action_str)
        self.tree.column("action", anchor=tk_W)

        for description in self.options:
            self.tree.insert("", tk_END, values=(description,))

        self.tree.pack(side=tk_LEFT, fill=tk_BOTH, expand=True)
        scrollbar.pack(side=tk_RIGHT, fill=tk_Y)

        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def _on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        description = self.tree.item(selected[0], "values")[0]
        fn = self.options.get(description)
        if callable(fn):
            fn(self.i_src_dir())  # ← call it to get the current string value
        fill_spark_face_in_directory(self.i_src_dir(), self.me_personname())
        if self.on_select_callback:
            self.on_select_callback()


def open_directory(path: str) -> None:
    system = platform_system()

    if system == "Windows":
        subprocess_Popen(["explorer", path])

    elif system == "Darwin":
        subprocess_Popen(["open", path])

    else:
        subprocess_Popen(["xdg-open", path])


class ETLAppMissingDefaultError(Exception):
    pass


# ──────────────────────────────────────────────
#  Main application window
# ──────────────────────────────────────────────
class ETLApp(tk_Tk):
    def __init__(self):
        super().__init__()
        keg_version = metadata_version("keg2")
        self.title(f"Listening using Keg2 (v{keg_version})")
        self.resizable(False, False)
        ax = get_app_glb_attrs()
        self.configure(bg=ax.bg)

        # Set a reasonable minimum size and centre on screen
        self.update_idletasks()
        app_width, app_height = 1720, 760
        x = (self.winfo_screenwidth() - app_width) // 2
        y = (self.winfo_screenheight() - app_height) // 2
        self.geometry(f"{app_width}x{app_height}+{x}+{y}")
        self.resizable(False, False)

        # Holds data after a run: {person: [(moment, [paths])]}
        self._persons_punchs_data: dict = {}

        # String vars ─ empty string = "not set" (optional dirs stay None)
        self._world_name = tk_StringVar()
        self._me_personname = tk_StringVar()
        self._you_personname = tk_StringVar()
        self._working = tk_StringVar()
        self._i_src_dir = tk_StringVar()
        self._b_src_dir = tk_StringVar()
        self._output = tk_StringVar()

        # Your config: description -> function
        self._build_ui()
        self._set_defaults()

    def _set_defaults(self):
        vars_map = {
            "world_name": self._world_name,
            "working": self._working,
            "ideas_src": self._i_src_dir,
            "bricks_src": self._b_src_dir,
            "output": self._output,
            "me_personname": self._me_personname,
            "you_personname": self._you_personname,
        }
        defaults = get_app_default_dirs(get_app_default_dir())
        defaults["me_personname"] = get_app_default_me_personname()
        defaults["you_personname"] = get_app_default_you_personname()

        for key, var in vars_map.items():
            if defaults.get(key) is None:
                raise ETLAppMissingDefaultError(f"Missing default {key=}")
            var.set(defaults[key])

    def _open_dir(self, var: tk_StringVar):
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
                "title": "ME         ",
                "var": self._me_personname,
                "required": True,
                "tip": "e.g. 'Emmanuel'",
            },
            "1": {
                "row_type": "text",
                "title": "YOU        ",
                "var": self._you_personname,
                "required": True,
                "tip": "e.g. 'Emmanuel'",
            },
            "2": {
                "row_type": "dir",
                "title": "IDEAS_DIR",
                "var": self._i_src_dir,
                "required": True,
                "tip": "Source of Ideas. Non-sparked Bricks.",
            },
            "3": {
                "row_type": "dir",
                "title": "BRICKS_DIR  ",
                "var": self._b_src_dir,
                "required": True,
                "tip": "Source of Bricks files. Ideas that have been sparked.",
            },
            "4": {
                "row_type": "dir",
                "title": "WORKING DIR",
                "var": self._working,
                "required": True,
                "tip": "Root directory for the ETL process",
            },
            "5": {
                "row_type": "dir",
                "title": "AGENDAS DIR",
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

        tk_Label(
            parent,
            text=lbl_text,
            font=ax.mono,
            bg=ax.bg_card,
            fg=ax.accent if required else ax.fg_dim,
            width=14,
            anchor="w",
        ).grid(row=row, column=0, padx=(0, 10), pady=7, sticky="w")

        entry = tk_Entry(
            parent,
            textvariable=var,
            font=ax.mono,
            bg=ax.entry_bg,
            fg=ax.fg,
            insertbackground=ax.accent,
            relief="flat",
            bd=0,
            width=32,
            highlightthickness=0,
            highlightbackground=ax.border,
            highlightcolor=ax.accent,
        )
        entry.grid(row=row, column=1, pady=7, ipady=5, sticky="ew")

        # Tooltip-style placeholder
        if not required:
            self._placeholder(entry, var, tip)

        tk_Button(
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
        tk_Button(
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
        tk_Button(
            parent,
            text="🗑",
            font=ax.mono,
            bg=ax.border,
            fg=ax.fg,
            activebackground=ax.bg_red,
            activeforeground=ax.fg_black,
            relief="flat",
            bd=0,
            padx=10,
            pady=4,
            cursor="hand2",
            command=lambda v=var: self._confirm_delete(v),
        ).grid(row=row, column=4, padx=(4, 0), pady=7)
        parent.columnconfigure(1, weight=1)
        parent.columnconfigure(3, weight=0)

    def _confirm_delete(self, var: tk_StringVar):
        path = var.get().strip()
        if not os_path_isdir(path):
            tkinter_messagebox.showwarning(
                "Invalid directory", f"Not a valid directory:\n{path}"
            )
            return
        explain_str = f"Delete all contents in:\n{path}\n\nThis cannot be undone."
        if confirmed := tkinter_messagebox.askyesno("Confirm delete", explain_str):
            self._rebuild_dirs(path)

    def _rebuild_dirs(self, path):
        delete_dir(path)
        if len(self._working.get()) > 0:
            set_dir(self._working.get())
        if self._i_src_dir:
            set_dir(self._i_src_dir.get())
        if self._b_src_dir:
            set_dir(self._b_src_dir.get())
        if self._output:
            set_dir(self._output.get())
        self._status.set(f"✔  Deleted contents of {path}")
        self._refresh_ideas_list()
        self._refresh_bricks_list()

    def _text_row(self, parent, row, label, var, *, required, tip):
        """Render one label + plain text entry row (no browse button)."""
        ax = get_app_glb_attrs()
        lbl_text = f"{'*' if required else ' '} {label}"

        tk_Label(
            parent,
            text=lbl_text,
            font=ax.mono,
            bg=ax.bg_card,
            fg=ax.accent if required else ax.fg_dim,
            width=14,
            anchor="w",
        ).grid(row=row, column=0, padx=(0, 10), pady=7, sticky="w")

        entry = tk_Entry(
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
        ax = get_app_glb_attrs()

        # ── header bar ──────────────────────────
        header = tk_Frame(self, bg=ax.accent, height=4)
        header.pack(fill="x")

        title_frame = tk_Frame(self, bg=ax.bg, pady=18)
        title_frame.pack(fill="x", padx=28)

        tk_Label(
            title_frame,
            text="Listening using Keg2",
            font=ax.platform_font,
            bg=ax.bg,
            fg=ax.accent,
            anchor="w",
        ).pack(side="left")

        tk_Label(
            title_frame,
            text="excel files → db → daily agendas",
            font=ax.mono,
            bg=ax.bg,
            fg=ax.fg_dim,
            anchor="e",
        ).pack(side="right", pady=(4, 0))

        # ── divider ─────────────────────────────
        tk_Frame(self, bg=ax.border, height=1).pack(fill="x", padx=28)

        # ── status bar (packed to bottom first) ─
        self._status = tk_StringVar(value="Ready.")
        tk_Frame(self, bg=ax.border, height=1).pack(fill="x", side="bottom")
        tk_Label(
            self,
            textvariable=self._status,
            font=ax.mono,
            bg=ax.bg,
            fg=ax.fg_dim,
            anchor="w",
            padx=28,
            pady=6,
        ).pack(fill="x", side="bottom")

        # ── three-column body ──────────────────────
        body = tk_Frame(self, bg=ax.bg)
        body.pack(fill=tk_BOTH, expand=True)
        body.columnconfigure(0, weight=0, minsize=640)
        body.columnconfigure(1, weight=0, minsize=320)
        body.columnconfigure(2, weight=1)
        body.rowconfigure(0, weight=1)

        # LEFT PANEL ─────────────────────────────
        left = tk_Frame(body, bg=ax.bg, width=640)
        left.grid(row=0, column=0, sticky="nsew")

        card = tk_Frame(left, bg=ax.bg_card, bd=0, padx=24, pady=20)
        card.pack(fill="x", padx=28, pady=(16, 0))
        self._create_dir_rows(card)

        btn_frame = tk_Frame(left, bg=ax.bg, pady=22)
        btn_frame.pack()

        self._run_btn = tk_Button(
            btn_frame,
            text="▶  CREATE AGENDAS FOR TODAY",
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
        refresh_callback = lambda: (
            self._refresh_ideas_list(),
            self._refresh_bricks_list(),
        )
        table = OptionTable(
            left,
            options,
            self._i_src_dir.get,
            self._me_personname.get,
            on_select_callback=refresh_callback,
        )
        table.pack(fill=tk_BOTH, expand=True, padx=10, pady=10)

        self._run_btn.bind(
            "<Enter>", lambda _: self._run_btn.configure(bg=ax.btn_active)
        )
        self._run_btn.bind("<Leave>", lambda _: self._run_btn.configure(bg=ax.accent))

        # DIVIDER left|middle ─────────────────────
        tk_Frame(body, bg=ax.border, width=1).grid(row=0, column=0, sticky="nse")

        # MIDDLE PANEL ───────────────────────────
        middle = tk_Frame(body, bg=ax.bg, width=320)
        middle.grid(row=0, column=1, sticky="nsew")
        self._build_files_panel(middle)

        # DIVIDER middle|right ────────────────────
        tk_Frame(body, bg=ax.border, width=1).grid(row=0, column=1, sticky="nse")

        # RIGHT PANEL ────────────────────────────
        right = tk_Frame(body, bg=ax.bg_card)
        right.grid(row=0, column=2, sticky="nsew")
        self._build_viewer_panel(right)

    def _build_files_panel(self, parent):
        """Middle panel: scrollable lists of .xlsx files in Ideas and Bricks directories."""
        ax = get_app_glb_attrs()

        # ─── IDEAS SECTION ───────────────────────
        # Header
        ideas_hdr = tk_Frame(parent, bg=ax.bg, pady=12)
        ideas_hdr.pack(fill="x", padx=16)

        tk_Label(
            ideas_hdr,
            text="IDEAS (xlsx)",
            font=ax.mono,
            bg=ax.bg,
            fg=ax.accent,
            anchor="w",
        ).pack(side="left")

        ideas_refresh_btn = tk_Button(
            ideas_hdr,
            text="↺",
            font=ax.mono,
            bg=ax.border,
            fg=ax.fg,
            activebackground=ax.accent,
            activeforeground=ax.fg_black,
            relief="flat",
            bd=0,
            padx=8,
            pady=2,
            cursor="hand2",
            command=self._refresh_ideas_list,
        )
        ideas_refresh_btn.pack(side="right")

        tk_Frame(parent, bg=ax.border, height=1).pack(fill="x", padx=16)

        # Ideas Treeview
        ideas_tree_frame = tk_Frame(parent, bg=ax.bg)
        ideas_tree_frame.pack(fill=tk_BOTH, expand=True, padx=8, pady=8)

        ideas_scrollbar = tkinter_ttk.Scrollbar(ideas_tree_frame, orient=tk_VERTICAL)
        self._ideas_tree = tkinter_ttk.Treeview(
            ideas_tree_frame,
            columns=("filename",),
            show="headings",
            selectmode="browse",
            yscrollcommand=ideas_scrollbar.set,
        )
        ideas_scrollbar.config(command=self._ideas_tree.yview)
        self._ideas_tree.heading("filename", text="File")
        self._ideas_tree.column("filename", anchor=tk_W)
        self._ideas_tree.pack(side=tk_LEFT, fill=tk_BOTH, expand=True)
        ideas_scrollbar.pack(side=tk_RIGHT, fill=tk_Y)

        self._ideas_tree.bind("<Double-1>", self._on_ideas_double_click)

        # Ideas Hint
        self._ideas_hint = tk_Label(
            parent,
            text="Set IDEAS_DIR then click ↺",
            font=ax.mono,
            bg=ax.bg,
            fg=ax.fg_dim,
        )
        self._ideas_hint.pack(pady=8)

        # ─── BRICKS SECTION ──────────────────────
        # Header
        bricks_hdr = tk_Frame(parent, bg=ax.bg, pady=12)
        bricks_hdr.pack(fill="x", padx=16)

        tk_Label(
            bricks_hdr,
            text="BRICKS (Ideas ordered by Spark Numbers)",
            font=ax.mono,
            bg=ax.bg,
            fg=ax.accent,
            anchor="w",
        ).pack(side="left")

        bricks_refresh_btn = tk_Button(
            bricks_hdr,
            text="↺",
            font=ax.mono,
            bg=ax.border,
            fg=ax.fg,
            activebackground=ax.accent,
            activeforeground=ax.fg_black,
            relief="flat",
            bd=0,
            padx=8,
            pady=2,
            cursor="hand2",
            command=self._refresh_bricks_list,
        )
        bricks_refresh_btn.pack(side="right")

        tk_Frame(parent, bg=ax.border, height=1).pack(fill="x", padx=16)

        # Bricks Treeview
        bricks_tree_frame = tk_Frame(parent, bg=ax.bg)
        bricks_tree_frame.pack(fill=tk_BOTH, expand=True, padx=8, pady=8)

        bricks_scrollbar = tkinter_ttk.Scrollbar(bricks_tree_frame, orient=tk_VERTICAL)
        self._bricks_tree = tkinter_ttk.Treeview(
            bricks_tree_frame,
            columns=("filename",),
            show="headings",
            selectmode="browse",
            yscrollcommand=bricks_scrollbar.set,
        )
        bricks_scrollbar.config(command=self._bricks_tree.yview)
        self._bricks_tree.heading("filename", text="File")
        self._bricks_tree.column("filename", anchor=tk_W)
        self._bricks_tree.pack(side=tk_LEFT, fill=tk_BOTH, expand=True)
        bricks_scrollbar.pack(side=tk_RIGHT, fill=tk_Y)

        self._bricks_tree.bind("<Double-1>", self._on_bricks_double_click)

        # Bricks Hint
        self._bricks_hint = tk_Label(
            parent,
            text="Set BRICKS_DIR then click ↺",
            font=ax.mono,
            bg=ax.bg,
            fg=ax.fg_dim,
        )
        self._bricks_hint.pack(pady=8)

        # Populate immediately if dirs are already set
        self._i_src_dir.trace_add("write", lambda *_: self._refresh_ideas_list())
        self._b_src_dir.trace_add("write", lambda *_: self._refresh_bricks_list())
        self._refresh_ideas_list()
        self._refresh_bricks_list()

    def _refresh_ideas_list(self):
        """Scan IDEAS_DIR for .xlsx files and populate the tree."""
        self._ideas_tree.delete(*self._ideas_tree.get_children())
        self._ideas_paths = {}
        ideas_dir = self._i_src_dir.get().strip()
        if not ideas_dir or not os_path_isdir(ideas_dir):
            self._ideas_hint.pack(pady=8)
            return
        try:
            files = sorted(
                f
                for f in os_listdir(ideas_dir)
                if f.lower().endswith(".xlsx")
                and os_path_isfile(os_path_join(ideas_dir, f))
            )
        except OSError:
            self._ideas_hint.pack(pady=8)
            return
        if not files:
            self._ideas_hint.configure(text="No .xlsx files found.")
            self._ideas_hint.pack(pady=8)
            return
        self._ideas_hint.pack_forget()
        for fname in files:
            item_id = self._ideas_tree.insert("", tk_END, values=(fname,))
            self._ideas_paths[item_id] = os_path_join(ideas_dir, fname)

    def _refresh_bricks_list(self):
        """Scan BRICKS_DIR for .xlsx files and populate the tree."""
        self._bricks_tree.delete(*self._bricks_tree.get_children())
        self._bricks_paths = {}
        bricks_dir = self._b_src_dir.get().strip()
        if not bricks_dir or not os_path_isdir(bricks_dir):
            self._bricks_hint.pack(pady=8)
            return
        try:
            files = sorted(
                f
                for f in os_listdir(bricks_dir)
                if f.lower().endswith(".xlsx")
                and os_path_isfile(os_path_join(bricks_dir, f))
            )
        except OSError:
            self._bricks_hint.pack(pady=8)
            return
        if not files:
            self._bricks_hint.configure(text="No .xlsx files found.")
            self._bricks_hint.pack(pady=8)
            return
        self._bricks_hint.pack_forget()
        for fname in files:
            item_id = self._bricks_tree.insert("", tk_END, values=(fname,))
            self._bricks_paths[item_id] = os_path_join(bricks_dir, fname)

    def _on_ideas_double_click(self, _event):
        """Open the selected Ideas file with the default application."""
        selected = self._ideas_tree.selection()
        if not selected:
            return
        path = self._ideas_paths.get(selected[0])
        if path and os_path_isfile(path):
            subprocess_Popen(["cmd", "/c", "start", "", path], shell=False)

    def _on_bricks_double_click(self, _event):
        """Open the selected Bricks file with the default application."""
        selected = self._bricks_tree.selection()
        if not selected:
            return
        path = self._bricks_paths.get(selected[0])
        if path and os_path_isfile(path):
            subprocess_Popen(["cmd", "/c", "start", "", path], shell=False)

    def _build_viewer_panel(self, parent):
        """Build the right-side punch file viewer."""
        ax = get_app_glb_attrs()

        # ── header ──────────────────────────────
        hdr = tk_Frame(parent, bg=ax.bg_card, pady=12)
        hdr.pack(fill="x", padx=16)

        tk_Label(
            hdr,
            text="PUNCH VIEWER",
            font=ax.mono,
            bg=ax.bg_card,
            fg=ax.accent,
            anchor="w",
        ).pack(side="left")

        self._copy_btn = tk_Button(
            hdr,
            text="⧉  Copy",
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
            command=self._copy_punch_text,
        )
        self._copy_btn.pack(side="right")

        tk_Frame(parent, bg=ax.border, height=1).pack(fill="x", padx=16)

        # ── selectors ───────────────────────────
        sel_frame = tk_Frame(parent, bg=ax.bg_card, pady=10)
        sel_frame.pack(fill="x", padx=16)

        tk_Label(
            sel_frame,
            text="Person",
            font=ax.mono,
            bg=ax.bg_card,
            fg=ax.fg_dim,
            width=8,
            anchor="w",
        ).grid(row=0, column=0, padx=(0, 8), pady=4, sticky="w")

        self._person_var = tk_StringVar()
        self._person_combo = tkinter_ttk.Combobox(
            sel_frame,
            textvariable=self._person_var,
            state="readonly",
            font=ax.mono,
            width=20,
        )
        self._person_combo.grid(row=0, column=1, pady=4, sticky="ew")
        self._person_combo.bind("<<ComboboxSelected>>", self._on_person_selected)

        tk_Label(
            sel_frame,
            text="Moment",
            font=ax.mono,
            bg=ax.bg_card,
            fg=ax.fg_dim,
            width=8,
            anchor="w",
        ).grid(row=1, column=0, padx=(0, 8), pady=4, sticky="w")

        self._moment_var = tk_StringVar()
        self._moment_combo = tkinter_ttk.Combobox(
            sel_frame,
            textvariable=self._moment_var,
            state="readonly",
            font=ax.mono,
            width=20,
        )
        self._moment_combo.grid(row=1, column=1, pady=4, sticky="ew")
        self._moment_combo.bind("<<ComboboxSelected>>", self._on_moment_selected)
        sel_frame.columnconfigure(1, weight=1)

        tk_Frame(parent, bg=ax.border, height=1).pack(fill="x", padx=16)

        # ── text display ────────────────────────
        text_frame = tk_Frame(parent, bg=ax.bg_card)
        text_frame.pack(fill=tk_BOTH, expand=True, padx=16, pady=(8, 16))

        v_scroll = tkinter_ttk.Scrollbar(text_frame, orient=tk_VERTICAL)
        self._punch_text = tk_Text(
            text_frame,
            font=ax.mono,
            bg=ax.entry_bg,
            fg=ax.fg,
            insertbackground=ax.accent,
            relief="flat",
            bd=0,
            wrap=tk_WORD,
            state="disabled",
            yscrollcommand=v_scroll.set,
            highlightthickness=1,
            highlightbackground=ax.border,
        )
        v_scroll.config(command=self._punch_text.yview)
        v_scroll.pack(side=tk_RIGHT, fill=tk_Y)
        self._punch_text.pack(side=tk_LEFT, fill=tk_BOTH, expand=True)

        # Hint label when empty
        punch_files_str = "Run the pipeline to load punch files."
        self._viewer_hint = tk_Label(
            parent, text=punch_files_str, font=ax.mono, bg=ax.bg_card, fg=ax.fg_dim
        )
        # self._viewer_hint.place(relx=0.5, rely=0.55, anchor="center")
        self._viewer_hint.pack(pady=20)

    # ── viewer helpers ─────────────────────────
    def _populate_viewer(self, persons_punchs: dict):
        """Store data and populate the person combobox."""
        self._persons_punchs_data = persons_punchs
        names = list(persons_punchs.keys())
        self._person_combo["values"] = names
        self._moment_combo["values"] = []
        self._moment_var.set("")
        self._person_var.set("")
        self._set_punch_text("")
        if names:
            self._person_combo.current(0)
            self._on_person_selected(None)
            # self._viewer_hint.place_forget()
            self._viewer_hint.pack_forget()

    def _on_person_selected(self, _event):
        person = self._person_var.get()
        moments = self._persons_punchs_data.get(person, [])
        moment_names = [str(m) for m, _paths in moments.items()]
        self._moment_combo["values"] = moment_names
        self._moment_var.set("")
        self._set_punch_text("")
        if moment_names:
            self._moment_combo.current(0)
            self._on_moment_selected(None)

    def _on_moment_selected(self, _event):
        person = self._person_var.get()
        moment_label = self._moment_var.get()
        moments = self._persons_punchs_data.get(person, [])
        for moment_rope, day_punch_paths in moments.items():
            if str(moment_rope) == moment_label:
                combined = []
                for path in day_punch_paths:
                    try:
                        combined.append(open_file(path))
                    except Exception as exc:
                        combined.append(f"[Error reading {path}: {exc}]")
                self._set_punch_text("\n\n".join(combined))
                return

    def _set_punch_text(self, text: str):
        self._punch_text.configure(state="normal")
        self._punch_text.delete("1.0", tk_END)
        if text:
            self._punch_text.insert("1.0", text)
        self._punch_text.configure(state="disabled")

    def _copy_punch_text(self):
        if text := self._punch_text.get("1.0", tk_END).strip():
            self.clipboard_clear()
            self.clipboard_append(text)
            self._copy_btn.configure(text="✔  Copied!")
            self.after(1500, lambda: self._copy_btn.configure(text="⧉  Copy"))

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
    def _browse(var: tk_StringVar):
        if path := tkinter_filedialog.askdirectory(title="Select directory"):
            var.set(path)

    # ── run handler ────────────────────────────
    def _run(self):
        ax = get_app_glb_attrs()
        me_person = self._me_personname.get().strip()
        you_person = self._you_personname.get().strip()
        working = self._working.get().strip()
        i_src_dir_ = self._i_src_dir.get().strip()
        b_src_dir_ = self._b_src_dir.get().strip()
        output = self._output.get().strip()

        # Treat placeholder text as empty
        i_src_dir_ = i_src_dir_ if os_path_isdir(i_src_dir_) else None
        b_src_dir_ = b_src_dir_ if os_path_isdir(b_src_dir_) else None
        output = output if os_path_isdir(output) else None
        # person = person if person and not person.startswith("Filter ") else None

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
            self.create_me_you_today_punchs_and_display(me_person, you_person)
        except Exception as exc:  # noqa: BLE001
            self._status.set(f"✘  Error: {exc}")
            tkinter_messagebox.showerror("Pipeline error", str(exc))
        finally:
            _run_btn_str = "▶  CREATE AGENDAS FROM IDEAS/BRICKS"
            self._run_btn.configure(state="normal", text=_run_btn_str, bg=ax.accent)

        # Open output directory if one was given
        if output and os_path_isdir(output):
            open_directory(output)

    def create_me_you_today_punchs_and_display(self, me_person: str, you_person: str):
        persons_punchs = create_today_punchs(
            person_names={me_person, you_person},
            world_name=self._world_name.get(),
            worlds_dir=self._working.get(),
            output_dir=self._output.get(),
            bricks_src_dir=self._b_src_dir.get(),
            ideas_src_dir=self._i_src_dir.get(),
        )
        self._status.set("✔  Pipeline completed successfully.")
        self._populate_viewer(persons_punchs)
        prettify_excel_files(self._i_src_dir.get())
        prettify_excel_files(self._b_src_dir.get())
        self._refresh_ideas_list()
        self._refresh_bricks_list()
        tkinter_messagebox.showinfo("Done", "ETL pipeline finished successfully.")


# ──────────────────────────────────────────────
#  Entry point
# ──────────────────────────────────────────────
if __name__ == "__main__":
    app = ETLApp()
    app.mainloop()
