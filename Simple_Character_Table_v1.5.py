#!/usr/bin/env python3
"""
Tablica Znaków Unicode
Alternatywa dla windowsowskiego charmap.exe
Wymaga tylko Python 3 (wbudowany tkinter)
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import unicodedata
import os
import sys
import json
import re

APP_VERSION = "v1.5"

LANG = {
    "en": {
        "title": "Simple Character Table",
        "category": "Category:",
        "search": "Search:",
        "count_chars": "{} characters",
        "count_char": "{} character",
        "no_name": "(no name)",
        "click_hint": "Click a character to see details (Double-click to add to builder)",
        "copy_char": "📋  Copy character",
        "copy_seq": "Copy sequence",
        "copied": "✓ Copied!",
        "favorites": "⭐ Favorites",
        "add_to_fav": "Add to favorites",
        "remove_from_fav": "Remove from favorites",
        "about": "About",
        "about_title": "About Simple Character Table",
        "program_name": "Simple Character Table",
        "version": "Version:",
        "author": "Author:",
        "mail": "Mail:",
        "github": "GitHub:",
        "global_search": "Search all categories",
        "history": "🕘 History",
        "frequent": "📊 Frequent",
        "options": "⋮",
        "export_fav": "Export favorites…",
        "import_fav": "Import favorites…",
        "clear_history": "Clear history",
        "clear_frequent": "Clear frequent stats",
        "export_title": "Export favorites",
        "import_title": "Import favorites",
        "export_success": "Exported {} favorite(s) to:\n{}",
        "import_success": "Imported {} new favorite(s).",
        "export_error": "Export failed:\n{}",
        "import_error": "Import failed:\n{}",
        "no_favorites": "No favorites yet. Right-click a character to add one.",
        "no_history": "No characters copied yet.",
        "no_frequent": "No statistics collected yet.",
        "shortcuts_hint": "Ctrl+C: copy selected   •   Ctrl+F: focus search   •   Esc: clear   •   Enter in search: copy 1st result",
        "builder_label": "String Builder (Double-click characters to add):",
        "builder_copy": "📋 Copy String",
        "builder_clear": "Clear",
        "categories": [
            "Basic Latin", "Latin Extended", "IPA Phonetic Alphabet", "Greek and Coptic",
            "Cyrillic", "Hebrew", "Arabic", "Currency", "Letterlike Symbols",
            "Punctuation", "Arrows", "Mathematical", "Misc Technical", "Geometric Shapes",
            "Misc Symbols", "Dingbats", "Emoji (Basic)", "Emoji (Transport)",
            "Emoji (Faces/Gestures)", "Mahjong and Cards"
        ]
    },
    "pl": {
        "title": "Simple Character Table",
        "category": "Kategoria:",
        "search": "Szukaj:",
        "count_chars": "{} znaków",
        "count_char": "{} znak",
        "no_name": "(brak nazwy)",
        "click_hint": "Kliknij znak, by zobaczyć szczegóły (Podwójne kliknięcie dodaje do schowka podręcznego)",
        "copy_char": "📋  Kopiuj znak",
        "copy_seq": "Kopiuj sekwencję",
        "copied": "✓ Skopiowano!",
        "favorites": "⭐ Ulubione",
        "add_to_fav": "Dodaj do ulubionych",
        "remove_from_fav": "Usuń z ulubionych",
        "about": "O programie",
        "about_title": "O programie Simple Character Table",
        "program_name": "Simple Character Table",
        "version": "Wersja:",
        "author": "Autor:",
        "mail": "Mail:",
        "github": "GitHub:",
        "global_search": "Szukaj we wszystkich kategoriach",
        "history": "🕘 Historia",
        "frequent": "📊 Częste",
        "options": "⋮",
        "export_fav": "Eksportuj ulubione…",
        "import_fav": "Importuj ulubione…",
        "clear_history": "Wyczyść historię",
        "clear_frequent": "Wyczyść statystyki częstych",
        "export_title": "Eksportuj ulubione",
        "import_title": "Importuj ulubione",
        "export_success": "Wyeksportowano {} ulubionych do:\n{}",
        "import_success": "Zaimportowano {} nowych ulubionych.",
        "export_error": "Eksport nie powiódł się:\n{}",
        "import_error": "Import nie powiódł się:\n{}",
        "no_favorites": "Brak ulubionych. Kliknij prawym przyciskiem na znak, aby go dodać.",
        "no_history": "Nie skopiowano jeszcze żadnego znaku.",
        "no_frequent": "Brak zebranych statystyk użycia znaków.",
        "shortcuts_hint": "Ctrl+C: kopiuj zaznaczony  •  Ctrl+F: szukaj  •  Esc: wyczyść  •  Enter w szukaj: kopiuj 1. wynik",
        "builder_label": "Schowek podręczny (Podwójne kliknięcie dodaje znak):",
        "builder_copy": "📋 Kopiuj ciąg",
        "builder_clear": "Wyczyść",
        "categories": [
            "Łacińskie podstawowe", "Łacińskie rozszerzone", "Alfabet fonetyczny (IPA)", "Grecki i koptyjski",
            "Cyrylica", "Hebrajski", "Arabski", "Waluty", "Literopodobne symbole",
            "Znaki interpunkcji", "Strzałki", "Matematyczne", "Różne techniczne", "Geometryczne kształty",
            "Różne symbole", "Dingbats", "Emoji (podstawowe)", "Emoji (transport)",
            "Emoji (twarze/gesty)", "Mahjong i karty"
        ]
    }
}

CATEGORIES = [
    ("Basic Latin",     0x0020, 0x007E),
    ("Latin Extended",    0x00C0, 0x02AF),
    ("IPA Phonetic Alphabet", 0x0250, 0x02AF),
    ("Greek and Coptic",       0x0370, 0x03FF),
    ("Cyrillic",                 0x0400, 0x04FF),
    ("Hebrew",                0x0590, 0x05FF),
    ("Arabic",                  0x0600, 0x06FF),
    ("Currency",                   0x20A0, 0x20CF),
    ("Letterlike Symbols",    0x2100, 0x214F),
    ("Punctuation",       0x2000, 0x206F),
    ("Arrows",                 0x2190, 0x21FF),
    ("Mathematical",             0x2200, 0x22FF),
    ("Misc Technical",         0x2300, 0x23FF),
    ("Geometric Shapes",    0x25A0, 0x25FF),
    ("Misc Symbols",            0x2600, 0x26FF),
    ("Dingbats",                 0x2700, 0x27BF),
    ("Emoji (Basic)",       0x1F300, 0x1F5FF),
    ("Emoji (Transport)",        0x1F680, 0x1F6FF),
    ("Emoji (Faces/Gestures)",     0x1F900, 0x1F9FF),
    ("Mahjong and Cards",          0x1F000, 0x1F0FF),
]

COLS = 16
HISTORY_MAX = 60

# Wyjściowe palety kolorów dla Motywu Jasnego i Ciemnego
THEMES = {
    "light": {
        "bg": "#f3f4f9", "panel_bg": "#ffffff", "border": "#e1e4ec", "text": "#1e2130",
        "text_muted": "#767c8c", "text_subtle": "#9aa0ad", "accent": "#4f46e5",
        "accent_hover": "#4338ca", "accent_light": "#ecebfd", "btn_bg": "#ffffff",
        "btn_hover": "#eef0f7", "btn_border": "#dadde6", "btn_active_bg": "#e3e0fb",
        "char_btn_bg": "#ffffff", "char_btn_hover": "#ecebfd", "char_btn_selected": "#4f46e5",
        "char_btn_selected_fg": "#ffffff", "char_btn_fav": "#fff3cd", "char_btn_fav_hover": "#ffe9a8",
        "success_bg": "#dcfce7", "success_text": "#15803d", "scrollbar_bg": "#c7cbd8",
        "scrollbar_trough": "#f3f4f9", "tooltip_bg": "#1e2130", "tooltip_fg": "#ffffff"
    },
    "dark": {
        "bg": "#111827", "panel_bg": "#1f2937", "border": "#374151", "text": "#f9fafb",
        "text_muted": "#9ca3af", "text_subtle": "#6b7280", "accent": "#6366f1",
        "accent_hover": "#4f46e5", "accent_light": "#312e81", "btn_bg": "#1f2937",
        "btn_hover": "#374151", "btn_border": "#4b5563", "btn_active_bg": "#3730a3",
        "char_btn_bg": "#1f2937", "char_btn_hover": "#374151", "char_btn_selected": "#6366f1",
        "char_btn_selected_fg": "#ffffff", "char_btn_fav": "#78350f", "char_btn_fav_hover": "#92400e",
        "success_bg": "#064e3b", "success_text": "#a7f3d0", "scrollbar_bg": "#4b5563",
        "scrollbar_trough": "#111827", "tooltip_bg": "#f9fafb", "tooltip_fg": "#111827"
    }
}

FONT_FAMILY = "Segoe UI"
FONT_NORMAL = (FONT_FAMILY, 10)
FONT_SMALL = (FONT_FAMILY, 9)
FONT_TINY = (FONT_FAMILY, 8)
FONT_BOLD = (FONT_FAMILY, 10, "bold")
FONT_TITLE = (FONT_FAMILY, 13, "bold")
FONT_SUBTITLE = (FONT_FAMILY, 12, "bold")
FONT_CHAR = (FONT_FAMILY, 14)
FONT_PREVIEW = (FONT_FAMILY, 34)
FONT_MONO = ("Consolas", 10)

_all_chars_cache = None

def get_chars(start, end):
    result = []
    for cp in range(start, end + 1):
        try:
            ch = chr(cp)
            if unicodedata.category(ch) not in ("Cc", "Cs", "Co"):
                result.append(cp)
        except (ValueError, OverflowError):
            pass
    return result

def get_all_chars():
    global _all_chars_cache
    if _all_chars_cache is None:
        seen = {}
        for _, start, end in CATEGORIES:
            for cp in get_chars(start, end):
                seen[cp] = True
        _all_chars_cache = sorted(seen.keys())
    return _all_chars_cache

def char_name(cp, lang="en"):
    try:
        return unicodedata.name(chr(cp))
    except ValueError:
        return LANG[lang]["no_name"]

def get_resource_path(filename):
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(__file__), filename)

def get_app_data_dir():
    app_name = "SimpleCharacterTable"
    if sys.platform.startswith("win"):
        base = os.environ.get("APPDATA") or os.path.expanduser("~")
    elif sys.platform == "darwin":
        base = os.path.join(os.path.expanduser("~"), "Library", "Application Support")
    else:
        base = os.environ.get("XDG_CONFIG_HOME") or os.path.join(os.path.expanduser("~"), ".config")
    path = os.path.join(base, app_name)
    os.makedirs(path, exist_ok=True)
    return path

class ToolTip:
    def __init__(self, widget, text_func, app_ref, delay=450):
        self.widget = widget
        self.text_func = text_func
        self.app = app_ref
        self.delay = delay
        self.tipwindow = None
        self.after_id = None
        widget.bind("<Enter>", self._schedule, add="+")
        widget.bind("<Leave>", self._hide, add="+")
        widget.bind("<Button-1>", self._hide, add="+")
        widget.bind("<Button-3>", self._hide, add="+")

    def _schedule(self, _event=None):
        self._cancel()
        self.after_id = self.widget.after(self.delay, self._show)

    def _show(self):
        text = self.text_func()
        if not text or self.tipwindow is not None:
            return
        try:
            x = self.widget.winfo_rootx() + 10
            y = self.widget.winfo_rooty() + self.widget.winfo_height() + 6
        except tk.TclError:
            return
        tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        try:
            tw.wm_attributes("-topmost", True)
        except tk.TclError:
            pass
        tw.wm_geometry(f"+{x}+{y}")
        c = THEMES[self.app.theme_name]
        label = tk.Label(
            tw, text=text, justify="left", background=c["tooltip_bg"], foreground=c["tooltip_fg"],
            relief="flat", borderwidth=0, font=FONT_SMALL, padx=8, pady=5
        )
        label.pack()
        self.tipwindow = tw

    def _cancel(self):
        if self.after_id is not None:
            self.widget.after_cancel(self.after_id)
            self.after_id = None

    def _hide(self, _event=None):
        self._cancel()
        if self.tipwindow is not None:
            self.tipwindow.destroy()
            self.tipwindow = None

class TablicaZnakow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.settings_file = os.path.join(get_app_data_dir(), "ustawienia.json")
        
        # Wczytanie preferencji użytkownika
        settings = self._load_settings()
        self.lang = settings.get("lang", "en")
        self.theme_name = settings.get("theme", "light")
        
        self.title(f'{LANG[self.lang]["title"]} {APP_VERSION}')

        ico_path = get_resource_path("tz-ico.ico")
        png_path = get_resource_path("tz-png.png")
        if os.path.exists(ico_path):
            try: self.iconbitmap(ico_path)
            except tk.TclError: pass
        elif os.path.exists(png_path):
            try:
                self.icon_img = tk.PhotoImage(file=png_path)
                self.iconphoto(True, self.icon_img)
            except tk.TclError: pass

        self.minsize(880, 600)
        
        # Wycentrowanie okna
        window_width, window_height = 985, 730
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{window_width}x{window_height}+{int(screen_width/2 - window_width/2)}+{int(screen_height/2 - window_height/2)}")

        self.selected_cp = None
        self.char_buttons = []
        self.char_button_map = {}
        self.current_rendered_cps = []
        self.tooltips = []
        self.favorites = []
        self.history = []
        self.frequent = {} # cp -> count
        
        self.favorites_file = os.path.join(get_app_data_dir(), "ulubione.txt")
        self.history_file = os.path.join(get_app_data_dir(), "historia.txt")
        self.frequent_file = os.path.join(get_app_data_dir(), "czeste.json")
        
        self.view_mode = "category" # category | favorites | history | frequent

        self._load_favorites()
        self._load_history()
        self._load_frequent()
        self._build_ui()
        self._bind_shortcuts()
        self._set_view_mode("category")
        self._apply_theme()

    def _load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except: return {}
        return {}

    def _save_settings(self):
        try:
            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump({"lang": self.lang, "theme": self.theme_name}, f, ensure_ascii=False, indent=2)
        except: pass

    def _add_hover(self, btn, type_="standard"):
        def _on_enter(_e=None):
            if btn.cget("state") == "disabled":
                return
            c = THEMES[self.theme_name]
            if type_ == "accent": btn.config(bg=c["accent_hover"])
            elif type_ == "char":
                cp = getattr(btn, "_cp", None)
                btn.config(bg=c["char_btn_fav_hover"] if cp in self.favorites else c["char_btn_hover"])
            else: btn.config(bg=c["btn_hover"])

        def _on_leave(_e=None):
            if btn.cget("state") == "disabled":
                return
            btn.config(bg=getattr(btn, "_normal_bg", btn.cget("bg")))

        btn.bind("<Enter>", _on_enter, add="+")
        btn.bind("<Leave>", _on_leave, add="+")

    def _flat_button(self, parent, text, command, font=FONT_NORMAL, padx=12, pady=6, type_="standard", **kwargs):
        btn = tk.Button(parent, text=text, font=font, command=command, relief="flat", bd=0, padx=padx, pady=pady, cursor="hand2", highlightthickness=1, **kwargs)
        self._add_hover(btn, type_)
        return btn

    def _apply_theme(self):
        c = THEMES[self.theme_name]
        self.configure(bg=c["bg"])
        
        # Stylizacja TTK
        style = ttk.Style(self)
        try: style.theme_use("clam")
        except: pass
        style.configure("TCombobox", fieldbackground=c["panel_bg"], background=c["panel_bg"], foreground=c["text"], arrowcolor=c["accent"], bordercolor=c["border"], lightcolor=c["panel_bg"], darkcolor=c["panel_bg"], padding=4, relief="flat")
        style.map("TCombobox", fieldbackground=[("readonly", c["panel_bg"])], foreground=[("readonly", c["text"])], bordercolor=[("focus", c["accent"])])
        self.option_add("*TCombobox*Listbox.background", c["panel_bg"])
        self.option_add("*TCombobox*Listbox.foreground", c["text"])
        self.option_add("*TCombobox*Listbox.selectBackground", c["accent_light"])
        self.option_add("*TCombobox*Listbox.selectForeground", c["text"])
        
        style.configure("TCheckbutton", background=c["bg"], foreground=c["text"], font=FONT_SMALL)
        style.map("TCheckbutton", background=[("active", c["bg"])])
        style.configure("Vertical.TScrollbar", background=c["scrollbar_bg"], troughcolor=c["scrollbar_trough"], bordercolor=c["bg"], arrowcolor=c["text_muted"], relief="flat", width=12)
        style.map("Vertical.TScrollbar", background=[("active", c["accent"])])

        # Aktualizacja elementów tła okna głównego i paneli
        self.top_wrap.config(bg=c["panel_bg"], highlightbackground=c["border"], highlightcolor=c["border"])
        self.top_panel.config(bg=c["panel_bg"])
        self.row1.config(bg=c["panel_bg"])
        self.row2.config(bg=c["panel_bg"])
        self.shortcuts_bar.config(bg=c["bg"])
        self.grid_frame.config(bg=c["bg"])
        self.canvas.config(bg=c["bg"])
        self.inner.config(bg=c["bg"])
        self.info_wrap.config(bg=c["bg"])
        self.info_panel.config(bg=c["panel_bg"], highlightbackground=c["border"], highlightcolor=c["border"])
        self.builder_wrap.config(bg=c["bg"])
        self.builder_panel.config(bg=c["panel_bg"], highlightbackground=c["border"], highlightcolor=c["border"])

        # Etykiety i pola tekstowe
        for lbl in [self.cat_label, self.search_label, self.global_chk]:
            lbl.config(bg=c["panel_bg"], fg=c["text"])
        self.count_label.config(bg=c["panel_bg"], fg=c["text_muted"])
        self.shortcuts_label.config(bg=c["bg"], fg=c["text_subtle"])
        self.name_label.config(bg=c["panel_bg"], fg=c["text"])
        self.code_label.config(bg=c["panel_bg"], fg=c["text_muted"])
        self.preview_label.config(bg=c["accent_light"], fg=c["accent"], highlightbackground=c["border"])
        self.builder_lbl.config(bg=c["panel_bg"], fg=c["text"])

        self.search_entry.config(bg=c["panel_bg"], fg=c["text"], insertbackground=c["text"], highlightbackground=c["btn_border"], highlightcolor=c["accent"])
        self.builder_entry.config(bg=c["bg"], fg=c["text"], insertbackground=c["text"], highlightbackground=c["border"], highlightcolor=c["accent"])

        # Przełącznik motywu ikona
        self.theme_btn.config(text="☀️" if self.theme_name == "light" else "🌙")

        # Odświeżenie przycisków w top barze
        self._refresh_button_theme(self.fav_btn, "favorites")
        self._refresh_button_theme(self.history_btn, "history")
        self._refresh_button_theme(self.freq_btn, "frequent")
        self._refresh_button_theme(self.options_btn, "standard")
        self._refresh_button_theme(self.about_btn, "standard")
        self._refresh_button_theme(self.lang_btn, "accent")
        self._refresh_button_theme(self.theme_btn, "standard")
        self._refresh_button_theme(self.builder_copy_btn, "accent")
        self._refresh_button_theme(self.builder_clear_btn, "standard")
        self._refresh_button_theme(self.copy_btn, "accent")
        self._refresh_button_theme(self.copy_seq_btn, "standard")

        # Przerysowanie siatki, aby nadać nowe kolory kafelkom
        self._refresh_current_view()

    def _refresh_button_theme(self, btn, type_):
        c = THEMES[self.theme_name]
        if type_ == "accent":
            btn.config(bg=c["accent"], fg="#ffffff", activebackground=c["accent_hover"], activeforeground="#ffffff", highlightbackground=c["accent"], highlightcolor=c["accent"])
            btn._normal_bg = c["accent"]
        elif type_ in ("favorites", "history", "frequent"):
            active = (self.view_mode == type_)
            bg_col = c["btn_active_bg"] if active else c["btn_bg"]
            btn.config(bg=bg_col, fg=c["text"], activebackground=c["btn_hover"], activeforeground=c["text"], highlightbackground=c["btn_border"], highlightcolor=c["btn_border"])
            btn._normal_bg = bg_col
        else:
            btn.config(bg=c["btn_bg"], fg=c["text"], activebackground=c["btn_hover"], activeforeground=c["text"], highlightbackground=c["btn_border"], highlightcolor=c["btn_border"])
            btn._normal_bg = c["btn_bg"]

    def _toggle_theme(self):
        self.theme_name = "dark" if self.theme_name == "light" else "light"
        self._save_settings()
        self._apply_theme()

    def _switch_language(self):
        self.lang = "pl" if self.lang == "en" else "en"
        self.title(f'{LANG[self.lang]["title"]} {APP_VERSION}')
        self._save_settings()
        self._update_ui_text()
        self.search_var.set("")
        self._refresh_current_view()

    def _update_ui_text(self):
        self.cat_label.config(text=LANG[self.lang]["category"])
        self.search_label.config(text=LANG[self.lang]["search"])
        self.fav_btn.config(text=LANG[self.lang]["favorites"])
        self.history_btn.config(text=LANG[self.lang]["history"])
        self.freq_btn.config(text=LANG[self.lang]["frequent"])
        self.global_chk.config(text=LANG[self.lang]["global_search"])
        self.lang_btn.config(text="PL" if self.lang == "en" else "EN")
        self.about_btn.config(text=LANG[self.lang]["about"])
        self.options_btn.config(text=LANG[self.lang]["options"])
        self.shortcuts_label.config(text=LANG[self.lang]["shortcuts_hint"])
        self.builder_lbl.config(text=LANG[self.lang]["builder_label"])
        self.builder_copy_btn.config(text=LANG[self.lang]["builder_copy"])
        self.builder_clear_btn.config(text=LANG[self.lang]["builder_clear"])
        if self.selected_cp is None:
            self.name_label.config(text=LANG[self.lang]["click_hint"])
        self.copy_btn.config(text=LANG[self.lang]["copy_char"])
        self.copy_seq_btn.config(text=LANG[self.lang]["copy_seq"])
        current_idx = self.cat_combo.current()
        self.cat_combo.config(values=LANG[self.lang]["categories"])
        if current_idx >= 0: self.cat_combo.current(current_idx)

    def _build_ui(self):
        # Top panel wrappery
        self.top_wrap = tk.Frame(self, highlightthickness=1)
        self.top_wrap.pack(fill="x", side="top")
        self.top_panel = tk.Frame(self.top_wrap, pady=10, padx=16)
        self.top_panel.pack(fill="x")

        self.row1 = tk.Frame(self.top_panel)
        self.row1.pack(fill="x")
        self.row2 = tk.Frame(self.top_panel)
        self.row2.pack(fill="x", pady=(10, 0))

        # Row 1 elementy
        self.cat_label = tk.Label(self.row1, font=FONT_NORMAL)
        self.cat_label.pack(side="left")
        self.cat_var = tk.StringVar()
        self.cat_combo = ttk.Combobox(self.row1, textvariable=self.cat_var, values=LANG[self.lang]["categories"], state="readonly", width=22, font=FONT_NORMAL)
        self.cat_combo.current(0)
        self.cat_combo.pack(side="left", padx=(6, 16))
        self.cat_combo.bind("<<ComboboxSelected>>", self._on_category)

        self.search_label = tk.Label(self.row1, font=FONT_NORMAL)
        self.search_label.pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._on_search)
        self.search_entry = tk.Entry(self.row1, textvariable=self.search_var, font=FONT_NORMAL, width=18, relief="flat", bd=0, highlightthickness=1)
        self.search_entry.pack(side="left", padx=(6, 0), ipady=4)

        self.global_search_var = tk.BooleanVar(value=False)
        self.global_chk = tk.Checkbutton(self.row1, variable=self.global_search_var, command=self._on_search, activebackground="#ffffff", highlightthickness=0, bd=0, cursor="hand2")
        self.global_chk.pack(side="left", padx=(10, 0))

        self.count_label = tk.Label(self.row1, font=FONT_SMALL)
        self.count_label.pack(side="right")

        # Row 2 elementy
        self.fav_btn = self._flat_button(self.row2, "", self._toggle_favorites_panel)
        self.fav_btn.pack(side="left")
        self.history_btn = self._flat_button(self.row2, "", self._toggle_history_panel)
        self.history_btn.pack(side="left", padx=(8, 0))
        self.freq_btn = self._flat_button(self.row2, "", self._toggle_frequent_panel)
        self.freq_btn.pack(side="left", padx=(8, 0))
        self.options_btn = self._flat_button(self.row2, "", self._show_options_menu, font=FONT_SUBTITLE, padx=10, pady=4)
        self.options_btn.pack(side="left", padx=(8, 0))

        self.about_btn = self._flat_button(self.row2, "", self._show_about, padx=14, pady=6)
        self.about_btn.pack(side="right")
        self.lang_btn = self._flat_button(self.row2, "", self._switch_language, font=FONT_BOLD, padx=14, pady=6)
        self.lang_btn.pack(side="right", padx=(8, 0))
        self.theme_btn = self._flat_button(self.row2, "", self._toggle_theme, font=FONT_BOLD, padx=10, pady=6)
        self.theme_btn.pack(side="right", padx=(8, 0))

        # Pasek skrótów
        self.shortcuts_bar = tk.Frame(self, padx=16)
        self.shortcuts_bar.pack(fill="x")
        self.shortcuts_label = tk.Label(self.shortcuts_bar, font=FONT_TINY, anchor="w")
        self.shortcuts_label.pack(side="left", pady=(5, 2))

        # --- Dolna Sekcja (Wprowadzone UI) ---
        # 1. String Builder (Schowek Podręczny)
        self.builder_wrap = tk.Frame(self)
        self.builder_wrap.pack(fill="x", side="bottom", padx=16, pady=(0, 10))
        self.builder_panel = tk.Frame(self.builder_wrap, padx=14, pady=10, highlightthickness=1)
        self.builder_panel.pack(fill="x")
        
        self.builder_lbl = tk.Label(self.builder_panel, font=FONT_SMALL, anchor="w")
        self.builder_lbl.pack(fill="x", side="top", pady=(0, 4))
        
        builder_control_frame = tk.Frame(self.builder_panel, bg="")
        builder_control_frame.pack(fill="x", side="top")
        builder_control_frame.bind("<Configure>", lambda e: builder_control_frame.config(bg=THEMES[self.theme_name]["panel_bg"]))
        
        self.builder_entry = tk.Entry(builder_control_frame, font=FONT_CHAR, relief="flat", bd=0, highlightthickness=1)
        self.builder_entry.pack(side="left", fill="x", expand=True, ipady=4)
        
        self.builder_clear_btn = self._flat_button(builder_control_frame, "", self._clear_builder, font=FONT_SMALL, padx=10, pady=4)
        self.builder_clear_btn.pack(side="right", padx=(8, 0))
        self.builder_copy_btn = self._flat_button(builder_control_frame, "", self._copy_builder, font=FONT_SMALL, padx=14, pady=4)
        self.builder_copy_btn.pack(side="right", padx=(8, 0))

        # 2. Informacje i szczegóły znaku
        self.info_wrap = tk.Frame(self)
        self.info_wrap.pack(fill="x", side="bottom", padx=16, pady=(0, 8))
        self.info_panel = tk.Frame(self.info_wrap, padx=18, pady=12, highlightthickness=1)
        self.info_panel.pack(fill="x")

        self.preview_label = tk.Label(self.info_panel, font=FONT_PREVIEW, width=2, anchor="center", relief="flat", bd=0, highlightthickness=1)
        self.preview_label.grid(row=0, column=0, rowspan=2, padx=(0, 16), sticky="ns")
        self.name_label = tk.Label(self.info_panel, font=FONT_BOLD, anchor="w")
        self.name_label.grid(row=0, column=1, sticky="w")
        self.code_label = tk.Label(self.info_panel, font=FONT_MONO, anchor="w")
        self.code_label.grid(row=1, column=1, sticky="w", pady=(4, 0))

        self.copy_btn = self._flat_button(self.info_panel, "", self._copy_char, padx=14, pady=6, type_="accent", state="disabled")
        self.copy_btn.grid(row=0, column=2, rowspan=2, padx=(18, 0), sticky="e")
        self.copy_seq_btn = self._flat_button(self.info_panel, "", self._copy_seq, padx=12, pady=6, type_="standard", state="disabled")
        self.copy_seq_btn.grid(row=0, column=3, rowspan=2, padx=(8, 0), sticky="e")
        self.info_panel.columnconfigure(1, weight=1)

        # Siatka znaków
        self.grid_frame = tk.Frame(self, padx=16)
        self.grid_frame.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(self.grid_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.grid_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.inner = tk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))

        def _on_mousewheel(event):
            if event.num == 4: self.canvas.yview_scroll(-1, "units")
            elif event.num == 5: self.canvas.yview_scroll(1, "units")
            else: self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

        self.canvas.bind("<Enter>", lambda e: (self.canvas.bind_all("<MouseWheel>", _on_mousewheel), self.canvas.bind_all("<Button-4>", _on_mousewheel), self.canvas.bind_all("<Button-5>", _on_mousewheel)))
        self.canvas.bind("<Leave>", lambda e: (self.canvas.unbind_all("<MouseWheel>"), self.canvas.unbind_all("<Button-4>"), self.canvas.unbind_all("<Button-5>")))

        self._update_ui_text()

    def _bind_shortcuts(self):
        self.bind_all("<Control-c>", self._on_ctrl_c)
        self.bind_all("<Control-C>", self._on_ctrl_c)
        self.bind_all("<Control-f>", self._on_ctrl_f)
        self.bind_all("<Control-F>", self._on_ctrl_f)
        self.bind_all("<Escape>", self._on_escape)
        self.search_entry.bind("<Return>", self._on_search_enter)

    def _on_ctrl_c(self, event=None):
        focused = self.focus_get()
        if isinstance(focused, tk.Entry): return
        if self.selected_cp is not None: self._copy_char()
        return "break"

    def _on_ctrl_f(self, event=None):
        self.search_entry.focus_set()
        self.search_entry.select_range(0, tk.END)
        self.search_entry.icursor(tk.END)
        return "break"

    def _on_escape(self, event=None):
        if self.search_var.get(): self.search_var.set("")
        self.focus_set()
        return "break"

    def _on_search_enter(self, event=None):
        """Szybki Enter: Kopiuje pierwszy znak z pasujących na liście wyszukiwania."""
        if self.current_rendered_cps:
            first_cp = self.current_rendered_cps[0]
            self._select(first_cp)
            self._copy_char()
        return "break"

    def _clear_builder(self):
        self.builder_entry.delete(0, tk.END)

    def _copy_builder(self):
        text = self.builder_entry.get()
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
            
            # Animacja błysku sukcesu dla kopiowania całego ciągu
            orig = self.builder_copy_btn.cget("text")
            c = THEMES[self.theme_name]
            self.builder_copy_btn.config(text=LANG[self.lang]["copied"], bg=c["success_bg"], fg=c["success_text"])
            self.builder_copy_btn._normal_bg = c["success_bg"]
            self.after(1200, lambda: (self.builder_copy_btn.config(text=orig, bg=c["accent"], fg="#ffffff"), setattr(self.builder_copy_btn, "_normal_bg", c["accent"])))

    def _append_to_builder(self, cp):
        self.builder_entry.insert(tk.END, chr(cp))

    def _current_category_chars(self):
        idx = self.cat_combo.current()
        if idx < 0: idx = 0
        _, start, end = CATEGORIES[idx]
        return get_chars(start, end)

    def _refresh_current_view(self):
        if self.view_mode == "favorites": self._render_grid(self.favorites)
        elif self.view_mode == "history": self._render_grid(self.history)
        elif self.view_mode == "frequent":
            sorted_freq = [item[0] for item in sorted(self.frequent.items(), key=lambda x: x[1], reverse=True)]
            self._render_grid(sorted_freq)
        else: self._on_search()

    def _on_category(self, event=None):
        self.search_var.set("")
        self._clear_selection()

    def _on_search(self, *args):
        q = self.search_var.get().strip().lower()
        if self.view_mode == "favorites": source = self.favorites
        elif self.view_mode == "history": source = self.history
        elif self.view_mode == "frequent": source = [item[0] for item in sorted(self.frequent.items(), key=lambda x: x[1], reverse=True)]
        elif self.global_search_var.get() and q: source = get_all_chars()
        else: source = self._current_category_chars()

        if not q:
            self._render_grid(source)
            return

        # Zaawansowane filtry: Obsługa zakresu Unicode (np. U+0030..U+0039)
        range_match = re.match(r'^(?:u\+)?([0-9a-f]{2,6})\.\.(?:u\+)?([0-9a-f]{2,6})$', q)
        if range_match:
            try:
                start_r = int(range_match.group(1), 16)
                end_r = int(range_match.group(2), 16)
                filtered = [cp for cp in source if start_r <= cp <= end_r]
                self._render_grid(filtered)
                return
            except: pass

        filtered = []
        for cp in source:
            ch = chr(cp)
            hex_code = f"u+{cp:04x}"
            name = char_name(cp, self.lang).lower()
            if q in hex_code or q in str(cp) or q in ch.lower() or q in name:
                filtered.append(cp)
        self._render_grid(filtered)

    def _render_grid(self, chars):
        self.current_rendered_cps = chars
        for tip in self.tooltips: tip._hide()
        self.tooltips.clear()
        for btn in self.char_buttons: btn.destroy()
        self.char_buttons.clear()
        self.char_button_map = {}
        self.selected_cp = None

        c = THEMES[self.theme_name]

        if not chars:
            self.count_label.config(text=LANG[self.lang]["count_char"].format(0))
            empty_text = None
            if self.view_mode == "favorites": empty_text = LANG[self.lang]["no_favorites"]
            elif self.view_mode == "history": empty_text = LANG[self.lang]["no_history"]
            elif self.view_mode == "frequent": empty_text = LANG[self.lang]["no_frequent"]
            if empty_text:
                placeholder = tk.Label(self.inner, text=empty_text, bg=c["bg"], fg=c["text_muted"], font=FONT_NORMAL, wraplength=600, justify="left")
                placeholder.grid(row=0, column=0, columnspan=COLS, sticky="w", pady=10, padx=4)
                self.char_buttons.append(placeholder)
            self.canvas.yview_moveto(0)
            return

        count_text = LANG[self.lang]["count_char"] if len(chars) == 1 else LANG[self.lang]["count_chars"]
        self.count_label.config(text=count_text.format(len(chars)))

        for i, cp in enumerate(chars):
            ch = chr(cp)
            is_fav = cp in self.favorites
            rest_bg = c["char_btn_fav"] if is_fav else c["char_btn_bg"]
            
            btn = tk.Button(self.inner, text=ch, font=FONT_CHAR, width=2, height=1, relief="flat", bd=0, bg=rest_bg, fg=c["text"], activebackground=c["char_btn_hover"], activeforeground=c["text"], highlightthickness=1, highlightbackground=c["border"], highlightcolor=c["border"], cursor="hand2", command=lambda _cp=cp: self._select(_cp))
            btn._cp = cp
            btn._normal_bg = rest_bg
            
            self._add_hover(btn, "char")
            btn.bind("<Button-3>", lambda e, _cp=cp: self._show_context_menu(e, _cp))
            # Podwójne kliknięcie -> String Builder
            btn.bind("<Double-Button-1>", lambda e, _cp=cp: self._append_to_builder(_cp))
            btn.grid(row=i // COLS, column=i % COLS, padx=3, pady=3, sticky="nsew")
            
            self.char_buttons.append(btn)
            self.char_button_map[cp] = btn
            self.tooltips.append(ToolTip(btn, (lambda _cp=cp: f"{char_name(_cp, self.lang)}\nU+{_cp:04X}"), self))

        for col in range(COLS): self.inner.columnconfigure(col, weight=1, minsize=42)
        self.canvas.yview_moveto(0)

    def _select(self, cp):
        self.selected_cp = cp
        c = THEMES[self.theme_name]
        ch = chr(cp)
        self.preview_label.config(text=ch)
        self.name_label.config(text=char_name(cp, self.lang))
        self.code_label.config(text=f"U+{cp:04X}   HTML: &#{cp};   Python: " + (f"\\u{cp:04X}" if cp <= 0xFFFF else f"\\U{cp:08X}") + f"   Dec: {cp}")
        self.copy_btn.config(state="normal")
        self.copy_seq_btn.config(state="normal")

        for btn_cp, btn in self.char_button_map.items():
            rest_bg = c["char_btn_fav"] if btn_cp in self.favorites else c["char_btn_bg"]
            btn.config(bg=rest_bg, fg=c["text"])
            btn._normal_bg = rest_bg
        
        selected_btn = self.char_button_map.get(cp)
        if selected_btn is not None:
            selected_btn.config(bg=c["char_btn_selected"], fg=c["char_btn_selected_fg"])
            selected_btn._normal_bg = c["char_btn_selected"]

    def _clear_selection(self):
        self.selected_cp = None
        self.preview_label.config(text="")
        self.name_label.config(text=LANG[self.lang]["click_hint"])
        self.code_label.config(text="")
        self.copy_btn.config(state="disabled")
        self.copy_seq_btn.config(state="disabled")

    def _copy_char(self):
        if self.selected_cp is not None:
            self.clipboard_clear()
            self.clipboard_append(chr(self.selected_cp))
            self._add_to_history(self.selected_cp)
            self._increment_frequent(self.selected_cp)
            self._flash_btn()

    def _copy_seq(self):
        if self.selected_cp is not None:
            cp = self.selected_cp
            seq = f"\\u{cp:04X}" if cp <= 0xFFFF else f"\\U{cp:08X}"
            self.clipboard_clear()
            self.clipboard_append(seq)
            self._add_to_history(cp)
            self._increment_frequent(cp)
            self._flash_btn(seq=True)

    # Ulubione logika
    def _load_favorites(self):
        if os.path.exists(self.favorites_file):
            with open(self.favorites_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try: self.favorites.append(int(line))
                        except: pass

    def _save_favorites(self):
        with open(self.favorites_file, "w", encoding="utf-8") as f:
            for cp in self.favorites: f.write(f"{cp}\n")

    def _toggle_favorite(self, cp):
        c = THEMES[self.theme_name]
        if cp in self.favorites: self.favorites.remove(cp)
        else: self.favorites.append(cp)
        self._save_favorites()
        if self.view_mode == "favorites": self._refresh_current_view()
        elif cp in self.char_button_map:
            btn = self.char_button_map[cp]
            rest_bg = c["char_btn_fav"] if cp in self.favorites else c["char_btn_bg"]
            if cp == self.selected_cp: btn._normal_bg = c["char_btn_selected"]
            else: btn.config(bg=rest_bg); btn._normal_bg = rest_bg

    def _export_favorites(self):
        if not self.favorites:
            messagebox.showinfo(LANG[self.lang]["export_title"], LANG[self.lang]["no_favorites"])
            return
        path = filedialog.asksaveasfilename(title=LANG[self.lang]["export_title"], defaultextension=".json", filetypes=[("JSON", "*.json"), ("Text", "*.txt")])
        if not path: return
        try:
            if path.lower().endswith(".json"):
                data = [{"cp": cp, "char": chr(cp), "name": char_name(cp, self.lang)} for cp in self.favorites]
                with open(path, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=2)
            else:
                with open(path, "w", encoding="utf-8") as f:
                    for cp in self.favorites: f.write(f"{cp}\n")
            messagebox.showinfo(LANG[self.lang]["export_title"], LANG[self.lang]["export_success"].format(len(self.favorites), path))
        except OSError as e: messagebox.showerror(LANG[self.lang]["export_title"], LANG[self.lang]["export_error"].format(e))

    def _import_favorites(self):
        path = filedialog.askopenfilename(title=LANG[self.lang]["import_title"], filetypes=[("JSON/Text", "*.json *.txt"), ("All files", "*.*")])
        if not path: return
        try:
            added = 0
            if path.lower().endswith(".json"):
                with open(path, "r", encoding="utf-8") as f: data = json.load(f)
                for item in data:
                    cp = item["cp"] if isinstance(item, dict) else int(item)
                    if cp not in self.favorites: self.favorites.append(cp); added += 1
            else:
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            try: cp = int(line)
                            except: continue
                            if cp not in self.favorites: self.favorites.append(cp); added += 1
            self._save_favorites()
            if self.view_mode == "favorites": self._refresh_current_view()
            messagebox.showinfo(LANG[self.lang]["import_title"], LANG[self.lang]["import_success"].format(added))
        except Exception as e: messagebox.showerror(LANG[self.lang]["import_title"], LANG[self.lang]["import_error"].format(e))

    # Historia i Statystyki logiki
    def _load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try: self.history.append(int(line))
                        except: pass

    def _save_history(self):
        with open(self.history_file, "w", encoding="utf-8") as f:
            for cp in self.history: f.write(f"{cp}\n")

    def _add_to_history(self, cp):
        if cp in self.history: self.history.remove(cp)
        self.history.insert(0, cp)
        del self.history[HISTORY_MAX:]
        self._save_history()
        if self.view_mode == "history": self._refresh_current_view()

    def _clear_history(self):
        self.history = []
        self._save_history()
        if self.view_mode == "history": self._refresh_current_view()

    def _load_frequent(self):
        if os.path.exists(self.frequent_file):
            try:
                with open(self.frequent_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.frequent = {int(k): v for k, v in data.items()}
            except: self.frequent = {}

    def _save_frequent(self):
        try:
            with open(self.frequent_file, "w", encoding="utf-8") as f:
                json.dump({str(k): v for k, v in self.frequent.items()}, f, ensure_ascii=False)
        except: pass

    def _increment_frequent(self, cp):
        self.frequent[cp] = self.frequent.get(cp, 0) + 1
        self._save_frequent()
        if self.view_mode == "frequent": self._refresh_current_view()

    def _clear_frequent(self):
        self.frequent = {}
        self._save_frequent()
        if self.view_mode == "frequent": self._refresh_current_view()

    # Nawigacja i Panele widoku
    def _toggle_favorites_panel(self): self._set_view_mode("category" if self.view_mode == "favorites" else "favorites")
    def _toggle_history_panel(self): self._set_view_mode("category" if self.view_mode == "history" else "history")
    def _toggle_frequent_panel(self): self._set_view_mode("category" if self.view_mode == "frequent" else "frequent")

    def _set_view_mode(self, mode):
        self.view_mode = mode
        c = THEMES[self.theme_name]
        self._refresh_button_theme(self.fav_btn, "favorites")
        self._refresh_button_theme(self.history_btn, "history")
        self._refresh_button_theme(self.freq_btn, "frequent")

        if mode in ("favorites", "history", "frequent"):
            self.cat_combo.config(state="disabled")
            self.global_chk.config(state="disabled")
        else:
            self.cat_combo.config(state="readonly")
            self.global_chk.config(state="normal")
        self._clear_selection()
        self.search_var.set("")

    def _make_menu(self):
        c = THEMES[self.theme_name]
        return tk.Menu(self, tearoff=0, bg=c["panel_bg"], fg=c["text"], activebackground=c["accent_light"], activeforeground=c["text"], bd=0, relief="flat", font=FONT_NORMAL)

    def _show_options_menu(self):
        menu = self._make_menu()
        menu.add_command(label=LANG[self.lang]["export_fav"], command=self._export_favorites)
        menu.add_command(label=LANG[self.lang]["import_fav"], command=self._import_favorites)
        menu.add_separator()
        menu.add_command(label=LANG[self.lang]["clear_history"], command=self._clear_history)
        menu.add_command(label=LANG[self.lang]["clear_frequent"], command=self._clear_frequent)
        menu.post(self.options_btn.winfo_rootx(), self.options_btn.winfo_rooty() + self.options_btn.winfo_height())

    def _show_context_menu(self, event, cp):
        menu = self._make_menu()
        if cp in self.favorites: menu.add_command(label=LANG[self.lang]["remove_from_fav"], command=lambda: self._toggle_favorite(cp))
        else: menu.add_command(label=LANG[self.lang]["add_to_fav"], command=lambda: self._toggle_favorite(cp))
        menu.post(event.x_root, event.y_root)

    def _flash_btn(self, seq=False):
        btn = self.copy_seq_btn if seq else self.copy_btn
        orig = btn.cget("text")
        c = THEMES[self.theme_name]
        orig_bg = c["accent"] if not seq else c["btn_bg"]
        
        btn.config(text=LANG[self.lang]["copied"], bg=c["success_bg"], fg=c["success_text"])
        btn._normal_bg = c["success_bg"]

        def _restore():
            btn.config(text=orig, bg=orig_bg, fg="#ffffff" if not seq else c["text"])
            btn._normal_bg = orig_bg

        self.after(1200, _restore)

    def _show_about(self):
        c = THEMES[self.theme_name]
        about_window = tk.Toplevel(self)
        about_window.title(LANG[self.lang]["about_title"])
        about_window.resizable(False, False)
        about_window.configure(bg=c["panel_bg"])

        w, h = 360, 290
        about_window.geometry(f"{w}x{h}+{int(self.winfo_screenwidth()/2 - w/2)}+{int(self.winfo_screenheight()/2 - h/2)}")
        about_window.transient(self)
        about_window.grab_set()

        tk.Frame(about_window, bg=c["accent"], height=4).pack(fill="x", side="top")
        frame = tk.Frame(about_window, bg=c["panel_bg"], padx=20, pady=18)
        frame.pack(fill="both", expand=True)

        header_frame = tk.Frame(frame, bg=c["panel_bg"])
        header_frame.pack(fill="x", pady=(0, 10))

        try:
            png_path = get_resource_path("tz-png.png")
            if os.path.exists(png_path):
                about_window.icon_photo = tk.PhotoImage(file=png_path).subsample(6, 6)
                tk.Label(header_frame, image=about_window.icon_photo, bg=c["panel_bg"]).pack(side="left", padx=(0, 10))
        except: pass

        nv_frame = tk.Frame(header_frame, bg=c["panel_bg"])
        nv_frame.pack(side="left", fill="x", anchor="w")
        tk.Label(nv_frame, text=LANG[self.lang]["program_name"], font=FONT_TITLE, bg=c["panel_bg"], fg=c["text"], anchor="w").pack(side="left")
        tk.Label(nv_frame, text=APP_VERSION, font=(FONT_FAMILY, 9, "bold"), bg=c["accent_light"], fg=c["accent"], padx=7, pady=1).pack(side="left", padx=(8, 0))

        tk.Label(frame, text=f"{LANG[self.lang]['version']} {APP_VERSION}", font=FONT_SMALL, bg=c["panel_bg"], fg=c["text_muted"], anchor="w").pack(fill="x", pady=(2, 6))
        tk.Label(frame, text=f"{LANG[self.lang]['author']} Sebastian Januchowski", font=FONT_NORMAL, bg=c["panel_bg"], fg=c["text"], anchor="w").pack(fill="x", pady=3)
        
        lbl_mail = tk.Label(frame, text=f"{LANG[self.lang]['mail']} polsoft.its@mail.com", font=FONT_NORMAL, bg=c["panel_bg"], anchor="w", fg=c["accent"], cursor="hand2")
        lbl_mail.pack(fill="x", pady=3)
        lbl_mail.bind("<Button-1>", lambda e: import_webbrowser().open("mailto:polsoft.its@mail.com"))
        
        lbl_git = tk.Label(frame, text=f"{LANG[self.lang]['github']} polsoft.ITS™", font=FONT_NORMAL, bg=c["panel_bg"], anchor="w", fg=c["accent"], cursor="hand2")
        lbl_git.pack(fill="x", pady=3)
        lbl_git.bind("<Button-1>", lambda e: import_webbrowser().open("https://github.com/polsoft-IT"))

        def import_webbrowser():
            import webbrowser; return webbrowser

        ok_btn = tk.Button(frame, text="OK", font=FONT_SMALL, command=about_window.destroy, bg=c["accent"], fg="#ffffff", activebackground=c["accent_hover"], activeforeground="#ffffff", relief="flat", bd=0, padx=18, pady=5, cursor="hand2")
        ok_btn.pack(pady=(16, 4))

if __name__ == "__main__":
    app = TablicaZnakow()
    app.mainloop()