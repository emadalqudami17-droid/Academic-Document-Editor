# -*- coding: utf-8 -*-
# main.py
import os
import json
from datetime import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.metrics import dp


# ============================================================
# BASE DIRECTORY
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ============================================================
# ARABIC FONT
# ============================================================
def _find_font():
    candidates = [
        os.path.join(BASE_DIR, "NotoNaskhArabic-Regular.ttf"),
        "NotoNaskhArabic-Regular.ttf",
        os.path.join(os.getcwd(), "NotoNaskhArabic-Regular.ttf"),
        os.path.join(BASE_DIR, "assets", "fonts", "NotoNaskhArabic-Regular.ttf"),
    ]
    try:
        app = App.get_running_app()
        if app:
            candidates.insert(0, os.path.join(app.directory, "NotoNaskhArabic-Regular.ttf"))
    except Exception:
        pass
    for c in candidates:
        if os.path.exists(c):
            print(f"[FONT] Found: {c}")
            return c
    print(f"[FONT] NOT FOUND")
    return candidates[0]


_FONT_PATH = _find_font()
FONT_ARABIC = "Arabic"

try:
    LabelBase.register(name=FONT_ARABIC, fn_regular=_FONT_PATH)
    FONT_LOADED = True
    print(f"[FONT] Registered OK")
except Exception as e:
    FONT_LOADED = False
    print(f"[FONT] ERROR: {e}")


# ============================================================
# ARABIC RESHAPER
# ============================================================
try:
    import arabic_reshaper
    _RESHAPER_OK = True
    print("[RESHAPER] loaded OK")
except Exception as e:
    _RESHAPER_OK = False
    print(f"[RESHAPER] ERROR: {e}")


def _reverse_arabic(text):
    if not text:
        return text
    lines = text.split("\n")
    result_lines = []
    for line in lines:
        if not line.strip():
            result_lines.append(line)
            continue
        words = line.split(" ")
        words.reverse()
        reversed_words = []
        for word in words:
            if not word:
                reversed_words.append("")
                continue
            first_char = word[0]
            if first_char.isdigit() or first_char in "0123456789+-*/=.,:;()[]":
                reversed_words.append(word)
            else:
                reversed_words.append(word[::-1])
        result_lines.append(" ".join(reversed_words))
    return "\n".join(result_lines)


def ar(text):
    if not text:
        return text
    if _RESHAPER_OK:
        try:
            reshaped = arabic_reshaper.reshape(text)
        except Exception as e:
            reshaped = text
    else:
        reshaped = text
    return _reverse_arabic(reshaped)


# ============================================================
# FONT HELPERS
# ============================================================
def afont():
    return {"font_name": FONT_ARABIC} if FONT_LOADED else {}


def make_label(text="", **kwargs):
    return Label(text=ar(text), **afont(), **kwargs)


def make_button(text="", **kwargs):
    return Button(text=ar(text), **afont(), **kwargs)


# ============================================================
# ARABIC TEXT INPUT
# ============================================================
class ArabicTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.raw_text = ""
        self._processing = False
        self.bind(focus=self._on_focus_change)
        if FONT_LOADED:
            self.font_name = FONT_ARABIC

    def _on_focus_change(self, instance, focused):
        if self._processing:
            return
        if focused:
            self._processing = True
            if self.raw_text:
                self.text = self.raw_text
            self._processing = False
        else:
            self._processing = True
            self.raw_text = self.text
            self.text = ar(self.text)
            self._processing = False

    def get_raw_text(self):
        return self.raw_text if self.raw_text else self.text

    def set_raw_text(self, raw):
        self._processing = True
        self.raw_text = raw or ""
        if raw:
            self.text = ar(raw)
        else:
            self.text = ""
        self._processing = False


def make_input(text="", **kwargs):
    return ArabicTextInput(text=text, **kwargs)


# ============================================================
# CONFIG
# ============================================================
APP_NAME = "محرر أكاديمي"
APP_VERSION = "4.1.0"

COLOR_PRIMARY = (0.12, 0.20, 0.35, 1)
COLOR_SECONDARY = (0.20, 0.40, 0.60, 1)
COLOR_TERTIARY = (0.30, 0.50, 0.70, 1)
COLOR_BG = (0.96, 0.97, 0.98, 1)
COLOR_SURFACE = (1, 1, 1, 1)
COLOR_TEXT = (0.15, 0.15, 0.15, 1)
COLOR_TEXT_LIGHT = (0.85, 0.88, 0.92, 1)
COLOR_TEXT_MUTED = (0.45, 0.50, 0.55, 1)
COLOR_DANGER = (0.85, 0.25, 0.25, 1)
COLOR_GOLD = (0.85, 0.65, 0.15, 1)
COLOR_TOOLBAR_BG = (0.94, 0.95, 0.96, 1)
COLOR_TOOLBAR_BTN = (0.30, 0.40, 0.50, 1)


# ============================================================
# ARABIC STRINGS
# ============================================================
MSG_APP_NAME = "محرر أكاديمي"
MSG_SUBTITLE = "محرر المستندات الأكاديمية"
MSG_VERSION_LABEL = "الإصدار"
MSG_NEW_DOC = "مستند جديد"
MSG_OPEN_DOC = "فتح مستند"
MSG_SETTINGS = "الإعدادات"
MSG_READY = "جاهز"
MSG_SETTINGS_SOON = "الإعدادات - قريبًا"
MSG_MY_DOCS = "مستنداتي"
MSG_NO_DOCS = "لا توجد مستندات بعد"
MSG_NO_DOCS_HINT = "اضغط مستند جديد لإنشاء أول مستند"
MSG_OPEN_BTN = "فتح"
MSG_DELETE = "حذف"
MSG_CANCEL = "إلغاء"
MSG_CONFIRM = "تأكيد الحذف"
MSG_UNTITLED = "بدون عنوان"
MSG_SAVE = "حفظ"
MSG_SAVE_FAILED = "فشل الحفظ"
MSG_SAVED = "تم حفظ المستند"
MSG_LOADED = "تم التحميل"
MSG_NOT_FOUND = "المستند غير موجود"
MSG_UPDATED = "آخر تحديث"

MSG_TOOL_H1 = "ع1"
MSG_TOOL_H2 = "ع2"
MSG_TOOL_BODY = "نص"
MSG_TOOL_TOC = "جدول محتويات"

MSG_HINT = "اكتب سطرًا، ثم اختر نمطه (ع1، ع2، نص)"
MSG_TOC_TITLE = "جدول المحتويات"
MSG_TOC_EMPTY = "لا توجد عناوين. أضف عناوين أولاً (ع1 أو ع2)"

ELEM_H1 = "h1"
ELEM_H2 = "h2"
ELEM_BODY = "body"
ELEM_TOC = "toc"


# ============================================================
# STORAGE
# ============================================================
STORAGE_DIR = None


def get_storage_dir():
    candidates = []
    try:
        if App.get_running_app():
            base = App.get_running_app().user_data_dir
            candidates.append(os.path.join(base, "documents"))
    except Exception:
        pass
    candidates.append(os.path.join("data", "documents"))
    for path in candidates:
        try:
            os.makedirs(path, exist_ok=True)
            print(f"[STORAGE] Using: {path}")
            return path
        except Exception:
            continue
    return candidates[-1]


def set_storage_dir():
    global STORAGE_DIR
    STORAGE_DIR = get_storage_dir()
    return STORAGE_DIR


# ============================================================
# DOC MANAGER
# ============================================================
class DocManager:
    @staticmethod
    def path_for(doc_id):
        return os.path.join(STORAGE_DIR, f"{doc_id}.json")

    @staticmethod
    def save(doc_id, title, elements, created=None):
        if not doc_id:
            doc_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs(STORAGE_DIR, exist_ok=True)
        if created is None:
            existing = DocManager.load(doc_id)
            created = existing.get("created") if existing else datetime.now().isoformat()

        elements_data = []
        for el in elements:
            elements_data.append({
                "kind": el.get("kind", ELEM_BODY),
                "text": el.get("text", ""),
            })

        data = {
            "id": doc_id,
            "title": title or MSG_UNTITLED,
            "elements": elements_data,
            "created": created,
            "updated": datetime.now().isoformat(),
        }
        try:
            with open(DocManager.path_for(doc_id), "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"[SAVE] {doc_id} ({len(elements_data)} elements)")
            return doc_id
        except Exception as e:
            print(f"[SAVE ERROR] {e}")
            return None

    @staticmethod
    def load(doc_id):
        if not doc_id:
            return None
        path = DocManager.path_for(doc_id)
        if not os.path.exists(path):
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if "elements" not in data and "content" in data:
                old_content = data.get("content", "")
                elements = []
                if old_content:
                    for line in old_content.split("\n"):
                        elements.append({"kind": ELEM_BODY, "text": line})
                data["elements"] = elements
            return data
        except Exception as e:
            print(f"[LOAD ERROR] {e}")
            return None

    @staticmethod
    def delete(doc_id):
        if not doc_id:
            return False
        path = DocManager.path_for(doc_id)
        try:
            if os.path.exists(path):
                os.remove(path)
                print(f"[DELETE] {doc_id}")
                return True
        except Exception as e:
            print(f"[DELETE ERROR] {e}")
        return False

    @staticmethod
    def list_all():
        docs = []
        if not os.path.isdir(STORAGE_DIR):
            return docs
        try:
            for fname in os.listdir(STORAGE_DIR):
                if not fname.endswith(".json"):
                    continue
                try:
                    with open(os.path.join(STORAGE_DIR, fname), "r", encoding="utf-8") as f:
                        data = json.load(f)
                    docs.append({
                        "id": data.get("id", fname[:-5]),
                        "title": data.get("title", MSG_UNTITLED),
                        "created": data.get("created", ""),
                        "updated": data.get("updated", ""),
                    })
                except Exception as e:
                    print(f"[LIST] skip {fname}: {e}")
        except Exception as e:
            print(f"[LIST ERROR] {e}")
        docs.sort(key=lambda d: d.get("updated", ""), reverse=True)
        return docs


# ============================================================
# HOME SCREEN
# ============================================================
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "home"

        root = BoxLayout(orientation="vertical", spacing=0)
        with root.canvas.before:
            Color(*COLOR_BG)
            self.bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(
            pos=lambda *_: setattr(self.bg, "pos", root.pos),
            size=lambda *_: setattr(self.bg, "size", root.size),
        )

        header = BoxLayout(
            orientation="vertical",
            size_hint_y=None, height=dp(170),
            padding=[dp(20), dp(35), dp(20), dp(20)],
            spacing=dp(6),
        )
        with header.canvas.before:
            Color(*COLOR_PRIMARY)
            self.h_bg = Rectangle(pos=header.pos, size=header.size)
        header.bind(
            pos=lambda *_: setattr(self.h_bg, "pos", header.pos),
            size=lambda *_: setattr(self.h_bg, "size", header.size),
        )
        header.add_widget(make_label(
            text=MSG_APP_NAME, font_size="36sp", bold=True,
            color=(1, 1, 1, 1), size_hint_y=None, height=dp(58),
        ))
        header.add_widget(make_label(
            text=MSG_SUBTITLE, font_size="18sp",
            color=COLOR_TEXT_LIGHT, size_hint_y=None, height=dp(38),
        ))
        header.add_widget(make_label(
            text=f"{MSG_VERSION_LABEL} {APP_VERSION}",
            font_size="13sp", color=(0.70, 0.75, 0.82, 1),
            size_hint_y=None, height=dp(22),
        ))
        root.add_widget(header)
        root.add_widget(Widget(size_hint_y=None, height=dp(30)))

        menu = BoxLayout(
            orientation="vertical",
            padding=[dp(24), dp(10), dp(24), dp(10)],
            spacing=dp(16),
            size_hint_y=None,
            height=dp(3 * (68 + 16) + 20),
        )

        btn_new = make_button(
            text=MSG_NEW_DOC, font_size="22sp",
            size_hint=(1, None), height=dp(68),
            background_normal="", background_color=COLOR_PRIMARY,
            color=(1, 1, 1, 1),
        )
        btn_new.bind(on_release=self._on_new)

        btn_open = make_button(
            text=MSG_OPEN_DOC, font_size="22sp",
            size_hint=(1, None), height=dp(68),
            background_normal="", background_color=COLOR_SECONDARY,
            color=(1, 1, 1, 1),
        )
        btn_open.bind(on_release=self._on_open)

        btn_settings = make_button(
            text=MSG_SETTINGS, font_size="22sp",
            size_hint=(1, None), height=dp(68),
            background_normal="", background_color=COLOR_TERTIARY,
            color=(1, 1, 1, 1),
        )
        btn_settings.bind(on_release=self._on_settings)

        menu.add_widget(btn_new)
        menu.add_widget(btn_open)
        menu.add_widget(btn_settings)
        root.add_widget(menu)
        root.add_widget(Widget())

        self.footer = make_label(
            text=MSG_READY, font_size="15sp",
            color=COLOR_TEXT_MUTED, size_hint_y=None, height=dp(50),
        )
        root.add_widget(self.footer)

        self.add_widget(root)

    def _on_new(self, *args):
        editor = self.manager.get_screen("editor")
        editor.new_document()
        self.manager.current = "editor"

    def _on_open(self, *args):
        docs = self.manager.get_screen("documents")
        docs.refresh()
        self.manager.current = "documents"

    def _on_settings(self, *args):
        self.footer.text = ar(MSG_SETTINGS_SOON)


# ============================================================
# ELEMENT ROW
# ============================================================
class ElementRow(BoxLayout):
    def __init__(self, kind=ELEM_BODY, text="", on_focus=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.kind = kind

        self.badge = Label(
            text="",
            font_size="10sp",
            color=(1, 1, 1, 1),
            size_hint=(None, 1),
            width=dp(38),
            **afont()
        )
        with self.badge.canvas.before:
            self.badge_bg = Color(0.55, 0.60, 0.65, 1)
            self.badge_rect = Rectangle(pos=self.badge.pos, size=self.badge.size)
        self.badge.bind(
            pos=lambda *_: setattr(self.badge_rect, "pos", self.badge.pos),
            size=lambda *_: setattr(self.badge_rect, "size", self.badge.size),
        )

        self.text_input = ArabicTextInput(
            text=text,
            font_size="16sp",
            multiline=True,
            background_color=(1, 1, 1, 1),
            foreground_color=COLOR_TEXT,
            cursor_color=COLOR_PRIMARY,
            size_hint_x=1,
            halign="right",
        )

        try:
            self.text_input.set_raw_text(text)
        except Exception as e:
            print(f"[ROW] set_raw_text error: {e}")
            self.text_input.text = text

        if on_focus:
            self.text_input.bind(focus=on_focus)

        self.add_widget(self.badge)
        self.add_widget(self.text_input)

        # Apply initial style
        self.set_kind(kind)

    def set_kind(self, kind):
        self.kind = kind

        if kind == ELEM_H1:
            self.height = dp(80)
            self.text_input.font_size = "22sp"
        elif kind == ELEM_H2:
            self.height = dp(70)
            self.text_input.font_size = "19sp"
        elif kind == ELEM_TOC:
            self.height = dp(180)
            self.text_input.font_size = "14sp"
        else:
            self.height = dp(70)
            self.text_input.font_size = "16sp"

        self.badge.text = self._badge_text()

        color = self._badge_color()
        try:
            self.badge_bg.rgba = color
        except Exception as e:
            print(f"[ROW] badge color error: {e}")

    def _badge_text(self):
        if self.kind == ELEM_H1:
            return "ع1"
        elif self.kind == ELEM_H2:
            return "ع2"
        elif self.kind == ELEM_TOC:
            return "TOC"
        return "نص"

    def _badge_color(self):
        if self.kind == ELEM_H1:
            return (0.12, 0.20, 0.35, 1)
        elif self.kind == ELEM_H2:
            return (0.20, 0.40, 0.60, 1)
        elif self.kind == ELEM_TOC:
            return (0.85, 0.65, 0.15, 1)
        return (0.55, 0.60, 0.65, 1)

    def get_text(self):
        try:
            return self.text_input.get_raw_text()
        except Exception:
            return self.text_input.text

    def get_kind(self):
        return self.kind


# ============================================================
# EDITOR SCREEN
# ============================================================
class EditorScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "editor"
        self.doc_id = None
        self.doc_created = None
        self.rows = []
        self.last_focused_row = None

        root = BoxLayout(orientation="vertical", spacing=0)
        with root.canvas.before:
            Color(*COLOR_BG)
            self.bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(
            pos=lambda *_: setattr(self.bg, "pos", root.pos),
            size=lambda *_: setattr(self.bg, "size", root.size),
        )

        # --- Top bar ---
        top = BoxLayout(
            orientation="horizontal",
            size_hint_y=None, height=dp(60),
            padding=[dp(8), 0], spacing=dp(8),
        )
        with top.canvas.before:
            Color(*COLOR_PRIMARY)
            self.t_bg = Rectangle(pos=top.pos, size=top.size)
        top.bind(
            pos=lambda *_: setattr(self.t_bg, "pos", top.pos),
            size=lambda *_: setattr(self.t_bg, "size", top.size),
        )

        btn_back = make_button(
            text=">", font_size="24sp",
            size_hint=(None, 1), width=dp(50),
            background_normal="", background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1),
        )
        btn_back.bind(on_release=self._on_back)

        self.title_input = make_input(
            text=MSG_UNTITLED, font_size="18sp", multiline=False,
            background_color=(0, 0, 0, 0),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1),
            halign="right",
        )

        btn_save = make_button(
            text=MSG_SAVE, font_size="16sp",
            size_hint=(None, 1), width=dp(80),
            background_normal="", background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1),
        )
        btn_save.bind(on_release=self._on_save)

        top.add_widget(btn_back)
        top.add_widget(self.title_input)
        top.add_widget(btn_save)
        root.add_widget(top)

        # --- Toolbar ---
        toolbar = BoxLayout(
            orientation="horizontal",
            size_hint_y=None, height=dp(50),
            padding=[dp(4), dp(4)], spacing=dp(4),
        )
        with toolbar.canvas.before:
            Color(*COLOR_TOOLBAR_BG)
            self.tb_bg = Rectangle(pos=toolbar.pos, size=toolbar.size)
        toolbar.bind(
            pos=lambda *_: setattr(self.tb_bg, "pos", toolbar.pos),
            size=lambda *_: setattr(self.tb_bg, "size", toolbar.size),
        )

        btn_h1 = make_button(
            text=MSG_TOOL_H1, font_size="14sp", bold=True,
            size_hint_y=None, height=dp(42),
            size_hint_x=None, width=dp(50),
            background_normal="", background_color=COLOR_TOOLBAR_BTN,
            color=(1, 1, 1, 1),
        )
        btn_h1.bind(on_release=lambda *_: self._apply_style(ELEM_H1))

        btn_h2 = make_button(
            text=MSG_TOOL_H2, font_size="14sp", bold=True,
            size_hint_y=None, height=dp(42),
            size_hint_x=None, width=dp(50),
            background_normal="", background_color=COLOR_TOOLBAR_BTN,
            color=(1, 1, 1, 1),
        )
        btn_h2.bind(on_release=lambda *_: self._apply_style(ELEM_H2))

        btn_body = make_button(
            text=MSG_TOOL_BODY, font_size="14sp",
            size_hint_y=None, height=dp(42),
            size_hint_x=None, width=dp(50),
            background_normal="", background_color=COLOR_TOOLBAR_BTN,
            color=(1, 1, 1, 1),
        )
        btn_body.bind(on_release=lambda *_: self._apply_style(ELEM_BODY))

        sep = Label(size_hint_x=None, width=dp(6))

        btn_toc = make_button(
            text=MSG_TOOL_TOC, font_size="12sp", bold=True,
            size_hint_y=None, height=dp(42),
            size_hint_x=None, width=dp(110),
            background_normal="", background_color=COLOR_GOLD,
            color=(1, 1, 1, 1),
        )
        btn_toc.bind(on_release=lambda *_: self._insert_toc())

        toolbar.add_widget(btn_h1)
        toolbar.add_widget(btn_h2)
        toolbar.add_widget(btn_body)
        toolbar.add_widget(sep)
        toolbar.add_widget(btn_toc)
        toolbar.add_widget(Label())
        root.add_widget(toolbar)

        # --- Hint ---
        hint = make_label(
            text=MSG_HINT,
            font_size="12sp", color=COLOR_TEXT_MUTED,
            halign="center",
            size_hint_y=None, height=dp(28),
        )
        root.add_widget(hint)

        # --- Scrollable editor ---
        self.scroll = ScrollView()
        self.rows_container = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(4),
            padding=[dp(8), dp(8)],
        )
        self.rows_container.bind(
            minimum_height=self.rows_container.setter("height")
        )
        self.scroll.add_widget(self.rows_container)
        root.add_widget(self.scroll)

        # --- Footer ---
        self.footer = make_label(
            text="", font_size="13sp",
            color=COLOR_TEXT_MUTED,
            size_hint_y=None, height=dp(35),
        )
        root.add_widget(self.footer)

        self.add_widget(root)

    # --- Row management ---
    def _add_row(self, kind=ELEM_BODY, text=""):
        row = ElementRow(kind=kind, text=text, on_focus=self._on_row_focus)
        self.rows.append(row)
        self.rows_container.add_widget(row)
        return row

    def _remove_row(self, row):
        if row in self.rows:
            self.rows.remove(row)
            self.rows_container.remove_widget(row)

    def _clear_rows(self):
        self.rows_container.clear_widgets()
        self.rows = []
        self.last_focused_row = None

    def _on_row_focus(self, instance, focused):
        if focused:
            for r in self.rows:
                if r.text_input == instance:
                    self.last_focused_row = r
                    break
            self.footer.text = ar("جاهز للتنسيق")
        else:
            if not self.rows or self.rows[-1].get_text().strip() != "":
                self._add_row(ELEM_BODY, "")

    def _get_active_row(self):
        for r in self.rows:
            if r.text_input.focus:
                return r
        if self.last_focused_row and self.last_focused_row in self.rows:
            return self.last_focused_row
        return None

    # --- Public API ---
    def new_document(self):
        self.doc_id = None
        self.doc_created = None
        self.title_input.set_raw_text(MSG_UNTITLED)
        self._clear_rows()
        self._add_row(ELEM_BODY, "")
        self.footer.text = ""

    def open_document(self, doc_id):
        data = DocManager.load(doc_id)
        if not data:
            self.footer.text = ar(MSG_NOT_FOUND)
            return
        self.doc_id = data.get("id")
        self.doc_created = data.get("created")
        self.title_input.set_raw_text(data.get("title", MSG_UNTITLED))

        self._clear_rows()
        elements = data.get("elements", [])
        if not elements:
            self._add_row(ELEM_BODY, "")
        else:
            for el in elements:
                self._add_row(el.get("kind", ELEM_BODY), el.get("text", ""))
            self._add_row(ELEM_BODY, "")

        self.footer.text = ar(f"{MSG_LOADED}: {data.get('title', '')}")

    # --- Actions ---
    def _on_back(self, *args):
        self.manager.current = "home"

    def _on_save(self, *args):
        title = self.title_input.get_raw_text().strip() or MSG_UNTITLED
        elements = []
        for r in self.rows:
            text = r.get_text()
            if not text.strip() and r is self.rows[-1]:
                continue
            elements.append({"kind": r.get_kind(), "text": text})

        saved_id = DocManager.save(
            doc_id=self.doc_id, title=title,
            elements=elements, created=self.doc_created,
        )
        if saved_id:
            self.doc_id = saved_id
            self.footer.text = ar(MSG_SAVED)
        else:
            self.footer.text = ar(MSG_SAVE_FAILED)

    def _apply_style(self, kind):
        row = self._get_active_row()
        if row is None:
            self.footer.text = ar("اضغط في سطر أولاً ثم اختر النمط")
            return
        try:
            row.set_kind(kind)
            self.footer.text = ar(f"النمط: {self._style_name(kind)}")
        except Exception as e:
            print(f"[APPLY_STYLE] error: {e}")
            self.footer.text = ar(f"خطأ: {e}")

    def _style_name(self, kind):
        if kind == ELEM_H1:
            return "عنوان 1"
        elif kind == ELEM_H2:
            return "عنوان 2"
        return "نص"

    def _insert_toc(self):
        headings = []
        for r in self.rows:
            if r.get_kind() in (ELEM_H1, ELEM_H2):
                text = r.get_text().strip()
                if text:
                    headings.append({"kind": r.get_kind(), "text": text})

        if not headings:
            self.footer.text = ar(MSG_TOC_EMPTY)
            return

        toc_lines = [MSG_TOC_TITLE, "─" * 40]
        for i, h in enumerate(headings, 1):
            if h["kind"] == ELEM_H1:
                toc_lines.append(f"{i}. {h['text']}")
            else:
                toc_lines.append(f"     • {h['text']}")

        toc_text = "\n".join(toc_lines)

        toc_row = None
        for r in self.rows:
            if r.get_kind() == ELEM_TOC:
                toc_row = r
                break

        if toc_row:
            toc_row.text_input.set_raw_text(toc_text)
            self.footer.text = ar("تم تحديث جدول المحتويات")
        else:
            new_row = ElementRow(kind=ELEM_TOC, text=toc_text, on_focus=self._on_row_focus)
            self.rows.insert(0, new_row)

            self.rows_container.clear_widgets()
            for r in self.rows:
                self.rows_container.add_widget(r)

            self.footer.text = ar("تم إدراج جدول المحتويات")


# ============================================================
# DOCUMENTS LIST SCREEN
# ============================================================
class DocumentsListScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "documents"

        root = BoxLayout(orientation="vertical", spacing=0)
        with root.canvas.before:
            Color(*COLOR_BG)
            self.bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(
            pos=lambda *_: setattr(self.bg, "pos", root.pos),
            size=lambda *_: setattr(self.bg, "size", root.size),
        )

        top = BoxLayout(
            orientation="horizontal",
            size_hint_y=None, height=dp(60),
            padding=[dp(8), 0], spacing=dp(8),
        )
        with top.canvas.before:
            Color(*COLOR_PRIMARY)
            self.t_bg = Rectangle(pos=top.pos, size=top.size)
        top.bind(
            pos=lambda *_: setattr(self.t_bg, "pos", top.pos),
            size=lambda *_: setattr(self.t_bg, "size", top.size),
        )

        btn_back = make_button(
            text=">", font_size="24sp",
            size_hint=(None, 1), width=dp(50),
            background_normal="", background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1),
        )
        btn_back.bind(on_release=lambda *_: self._back())

        top.add_widget(btn_back)
        top.add_widget(make_label(
            text=MSG_MY_DOCS, font_size="20sp", color=(1, 1, 1, 1),
        ))
        top.add_widget(Label(size_hint=(None, 1), width=dp(50)))
        root.add_widget(top)

        self.scroll = ScrollView()
        self.list_layout = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(6),
            padding=[dp(10), dp(10)],
        )
        self.list_layout.bind(
            minimum_height=self.list_layout.setter("height")
        )
        self.scroll.add_widget(self.list_layout)
        root.add_widget(self.scroll)

        self.empty = BoxLayout(orientation="vertical", padding=dp(30))
        self.empty.add_widget(Widget())
        self.empty.add_widget(make_label(
            text=MSG_NO_DOCS, font_size="20sp", bold=True,
            color=COLOR_TEXT_MUTED, size_hint_y=None, height=dp(40),
        ))
        self.empty.add_widget(make_label(
            text=MSG_NO_DOCS_HINT, font_size="15sp",
            color=COLOR_TEXT_MUTED, size_hint_y=None, height=dp(30),
        ))
        self.empty.add_widget(Widget())
        root.add_widget(self.empty)

        self.add_widget(root)

    def refresh(self):
        self.list_layout.clear_widgets()
        docs = DocManager.list_all()
        print(f"[DOCS] {len(docs)} document(s)")

        if not docs:
            self.scroll.opacity = 0
            self.empty.opacity = 1
            return

        self.scroll.opacity = 1
        self.empty.opacity = 0

        for doc in docs:
            self.list_layout.add_widget(self._make_row(doc))

    def _make_row(self, doc):
        row = BoxLayout(
            orientation="horizontal",
            size_hint_y=None, height=dp(90),
            padding=[dp(12), dp(8)], spacing=dp(8),
        )
        with row.canvas.before:
            Color(*COLOR_SURFACE)
            bg = Rectangle(pos=row.pos, size=row.size)
        row.bind(
            pos=lambda *_: setattr(bg, "pos", row.pos),
            size=lambda *_: setattr(bg, "size", row.size),
        )

        info = BoxLayout(orientation="vertical", spacing=dp(4))
        info.add_widget(make_label(
            text=doc.get("title", MSG_UNTITLED),
            font_size="18sp", bold=True,
            color=COLOR_TEXT, halign="right",
            size_hint_y=None, height=dp(30),
        ))
        updated = doc.get("updated", "")[:16].replace("T", " ")
        info.add_widget(make_label(
            text=f"{MSG_UPDATED}: {updated}",
            font_size="12sp", color=COLOR_TEXT_MUTED,
            halign="right", size_hint_y=None, height=dp(22),
        ))

        btn_open = make_button(
            text=MSG_OPEN_BTN, font_size="15sp",
            size_hint=(None, 1), width=dp(80),
            background_normal="",
            background_color=COLOR_SECONDARY,
            color=(1, 1, 1, 1),
        )
        btn_open.bind(on_release=lambda b, did=doc["id"]: self._open(did))

        btn_del = make_button(
            text="X", font_size="16sp", bold=True,
            size_hint=(None, 1), width=dp(45),
            background_normal="",
            background_color=COLOR_DANGER,
            color=(1, 1, 1, 1),
        )
        btn_del.bind(on_release=lambda b, d=doc: self._confirm_delete(d))

        row.add_widget(info)
        row.add_widget(btn_open)
        row.add_widget(btn_del)
        return row

    def _open(self, doc_id):
        editor = self.manager.get_screen("editor")
        editor.open_document(doc_id)
        self.manager.current = "editor"

    def _confirm_delete(self, doc):
        content = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(12))
        content.add_widget(make_label(
            text=f"{MSG_CONFIRM}: {doc.get('title', MSG_UNTITLED)}",
            halign="center",
        ))
        btns = BoxLayout(
            orientation="horizontal", size_hint_y=None,
            height=dp(50), spacing=dp(10),
        )
        btn_no = make_button(
            text=MSG_CANCEL, background_normal="",
            background_color=COLOR_SECONDARY, color=(1, 1, 1, 1),
        )
        btn_yes = make_button(
            text=MSG_DELETE, background_normal="",
            background_color=COLOR_DANGER, color=(1, 1, 1, 1),
        )
        btns.add_widget(btn_no)
        btns.add_widget(btn_yes)
        content.add_widget(btns)

        popup = Popup(
            title=ar(MSG_CONFIRM),
            content=content,
            size_hint=(0.85, 0.4),
            auto_dismiss=False,
        )
        btn_no.bind(on_release=popup.dismiss)
        btn_yes.bind(on_release=lambda *_: self._do_delete(doc["id"], popup))
        popup.open()

    def _do_delete(self, doc_id, popup):
        popup.dismiss()
        DocManager.delete(doc_id)
        self.refresh()

    def _back(self):
        self.manager.current = "home"


# ============================================================
# APP
# ============================================================
class AcademicWordEditorApp(App):
    def build(self):
        self.title = APP_NAME
        Window.clearcolor = COLOR_BG

        set_storage_dir()
        print(f"[APP] Storage: {STORAGE_DIR}")
        print(f"[APP] Font: {FONT_LOADED}")
        print(f"[APP] Reshaper: {_RESHAPER_OK}")

        sm = ScreenManager(transition=SlideTransition(duration=0.2))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(EditorScreen(name="editor"))
        sm.add_widget(DocumentsListScreen(name="documents"))
        sm.current = "home"
        return sm


if __name__ == "__main__":
    AcademicWordEditorApp().run()
