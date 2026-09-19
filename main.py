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
from kivy.resources import resource_find
from kivy.metrics import dp


# =====================================================
# Register Arabic Font
# =====================================================
FONT_ARABIC = "NotoNaskh"
FONT_PATH = "assets/fonts/NotoNaskhArabic-Regular.ttf"
FONT_LOADED = False

try:
    real_path = resource_find(FONT_PATH)
    print(f"[FONT] resource_find: {real_path}")
    if real_path:
        LabelBase.register(name=FONT_ARABIC, fn_regular=real_path)
        FONT_LOADED = True
        print(f"[FONT] Registered OK")
except Exception as e:
    print(f"[FONT] ERROR: {e}")


# =====================================================
# ARABIC RESHAPER (built-in, no external deps)
# =====================================================
# Each Arabic letter has up to 4 forms:
#   isolated, initial, medial, final
# Letters that DO NOT connect to the next letter (right-joining only):
#   ا د ذ ر ز و ؤ إ أ آ ة ى ء
#
# We use the Unicode Arabic Presentation Forms (FB50–FEFF)
# to display shaped letters correctly.

ARABIC_FORMS = {
    # key: (isolated, initial, medial, final)
    '\u0621': ('\uFE80', '\uFE80', '\uFE80', '\uFE80'),  # ء
    '\u0622': ('\uFE81', '\uFE81', '\uFE82', '\uFE82'),  # آ
    '\u0623': ('\uFE83', '\uFE83', '\uFE84', '\uFE84'),  # أ
    '\u0624': ('\uFE85', '\uFE85', '\uFE86', '\uFE86'),  # ؤ
    '\u0625': ('\uFE87', '\uFE87', '\uFE88', '\uFE88'),  # إ
    '\u0626': ('\uFE89', '\uFE8B', '\uFE8C', '\uFE8A'),  # ئ
    '\u0627': ('\uFE8D', '\uFE8D', '\uFE8E', '\uFE8E'),  # ا
    '\u0628': ('\uFE8F', '\uFE91', '\uFE92', '\uFE90'),  # ب
    '\u0629': ('\uFE93', '\uFE93', '\uFE94', '\uFE94'),  # ة
    '\u062A': ('\uFE95', '\uFE97', '\uFE98', '\uFE96'),  # ت
    '\u062B': ('\uFE99', '\uFE9B', '\uFE9C', '\uFE9A'),  # ث
    '\u062C': ('\uFE9D', '\uFE9F', '\uFEA0', '\uFE9E'),  # ج
    '\u062D': ('\uFEA1', '\uFEA3', '\uFEA4', '\uFEA2'),  # ح
    '\u062E': ('\uFEA5', '\uFEA7', '\uFEA8', '\uFEA6'),  # خ
    '\u062F': ('\uFEA9', '\uFEA9', '\uFEAA', '\uFEAA'),  # د
    '\u0630': ('\uFEAB', '\uFEAB', '\uFEAC', '\uFEAC'),  # ذ
    '\u0631': ('\uFEAD', '\uFEAD', '\uFEAE', '\uFEAE'),  # ر
    '\u0632': ('\uFEAF', '\uFEAF', '\uFEB0', '\uFEB0'),  # ز
    '\u0633': ('\uFEB1', '\uFEB3', '\uFEB4', '\uFEB2'),  # س
    '\u0634': ('\uFEB5', '\uFEB7', '\uFEB8', '\uFEB6'),  # ش
    '\u0635': ('\uFEB9', '\uFEBB', '\uFEBC', '\uFEBA'),  # ص
    '\u0636': ('\uFEBD', '\uFEBF', '\uFEC0', '\uFEBE'),  # ض
    '\u0637': ('\uFEC1', '\uFEC3', '\uFEC4', '\uFEC2'),  # ط
    '\u0638': ('\uFEC5', '\uFEC7', '\uFEC8', '\uFEC6'),  # ظ
    '\u0639': ('\uFEC9', '\uFECB', '\uFECC', '\uFECA'),  # ع
    '\u063A': ('\uFECD', '\uFECF', '\uFED0', '\uFECE'),  # غ
    '\u0640': ('\u0640', '\u0640', '\u0640', '\u0640'),  # ـ tatweel
    '\u0641': ('\uFED1', '\uFED3', '\uFED4', '\uFED2'),  # ف
    '\u0642': ('\uFED5', '\uFED7', '\uFED8', '\uFED6'),  # ق
    '\u0643': ('\uFED9', '\uFEDB', '\uFEDC', '\uFEDA'),  # ك
    '\u0644': ('\uFEDD', '\uFEDF', '\uFEE0', '\uFEDE'),  # ل
    '\u0645': ('\uFEE1', '\uFEE3', '\uFEE4', '\uFEE2'),  # م
    '\u0646': ('\uFEE5', '\uFEE7', '\uFEE8', '\uFEE6'),  # ن
    '\u0647': ('\uFEE9', '\uFEEB', '\uFEEC', '\uFEEA'),  # ه
    '\u0648': ('\uFEED', '\uFEED', '\uFEEE', '\uFEEE'),  # و
    '\u0649': ('\uFEEF', '\uFEEF', '\uFEF0', '\uFEF0'),  # ى
    '\u064A': ('\uFEF1', '\uFEF3', '\uFEF4', '\uFEF2'),  # ي
    # Special lam-alef ligatures
    '\u0644\u0622': ('\uFEF5', '\uFEF5', '\uFEF6', '\uFEF6'),  # لا آ
    '\u0644\u0623': ('\uFEF7', '\uFEF7', '\uFEF8', '\uFEF8'),  # لأ
    '\u0644\u0625': ('\uFEF9', '\uFEF9', '\uFEFA', '\uFEFA'),  # لإ
    '\u0644\u0627': ('\uFEFB', '\uFEFB', '\uFEFC', '\uFEFC'),  # لا
}

# Letters that connect to the following letter (on their left side)
DUAL_JOINING = set()
for c, forms in ARABIC_FORMS.items():
    # Only single-char keys with 4 distinct forms count as dual-joining
    if len(c) == 1 and len(set(forms)) >= 3:
        DUAL_JOINING.add(c)

# Letters that do NOT connect to the following letter
RIGHT_JOINING = set()
for c, forms in ARABIC_FORMS.items():
    if len(c) == 1 and c not in DUAL_JOINING:
        RIGHT_JOINING.add(c)

# Arabic letter detection range
def is_arabic_letter(ch):
    if not ch:
        return False
    cp = ord(ch)
    return (
        0x0621 <= cp <= 0x064A or   # Arabic letters
        0x0660 <= cp <= 0x0669 or   # Arabic-Indic digits
        0x06F0 <= cp <= 0x06F9      # Extended Arabic-Indic digits
    )


def is_diacritic(ch):
    """Arabic diacritics (tashkeel) - they don't affect joining."""
    if not ch:
        return False
    cp = ord(ch)
    return 0x064B <= cp <= 0x065F or cp == 0x0670 or 0x06D6 <= cp <= 0x06ED


def reshape_arabic(text):
    """Convert Arabic letters to their contextual presentation forms."""
    if not text:
        return text

    result = []
    chars = list(text)
    n = len(chars)

    i = 0
    while i < n:
        ch = chars[i]

        # Check for lam-alef ligature (2-char)
        if i + 1 < n and ch == '\u0644':
            next_ch = chars[i + 1]
            key = ch + next_ch
            if key in ARABIC_FORMS:
                # Determine form based on context before
                prev_real = None
                j = i - 1
                while j >= 0 and is_diacritic(chars[j]):
                    j -= 1
                if j >= 0:
                    prev_real = chars[j]
                prev_connects = prev_real and (prev_real in DUAL_JOINING)

                # Lam-alef ligature: isolated or final
                if prev_connects:
                    result.append(ARABIC_FORMS[key][3])  # final
                else:
                    result.append(ARABIC_FORMS[key][0])  # isolated
                i += 2
                continue

        # Regular letter
        if ch in ARABIC_FORMS and len(ch) == 1:
            # Find previous real (non-diacritic) letter
            prev_real = None
            j = i - 1
            while j >= 0 and is_diacritic(chars[j]):
                j -= 1
            if j >= 0:
                prev_real = chars[j]

            # Find next real letter
            next_real = None
            j = i + 1
            while j < n and is_diacritic(chars[j]):
                j += 1
            if j < n:
                next_real = chars[j]

            # Determine connection
            connects_prev = prev_real and (prev_real in DUAL_JOINING)
            connects_next = next_real and (next_real in ARABIC_FORMS)

            # Can this letter connect to next? Only dual-joining
            can_connect_next = ch in DUAL_JOINING
            will_connect_next = connects_next and can_connect_next

            # Choose the form
            if connects_prev and will_connect_next:
                form = ARABIC_FORMS[ch][2]  # medial
            elif connects_prev:
                form = ARABIC_FORMS[ch][3]  # final
            elif will_connect_next:
                form = ARABIC_FORMS[ch][1]  # initial
            else:
                form = ARABIC_FORMS[ch][0]  # isolated

            result.append(form)
        else:
            result.append(ch)

        i += 1

    return ''.join(result)


def bidi_reorder(text):
    """
    Reverse Arabic segments so they display correctly RTL.
    Keeps Latin words and numbers LTR within Arabic text.
    """
    if not text:
        return text

    # Split into runs of Arabic vs non-Arabic
    runs = []
    current = ""
    current_is_ar = None

    for ch in text:
        # Treat Arabic letters as RTL, everything else as LTR/neutral
        is_ar = is_arabic_letter(ch)
        if current_is_ar is None:
            current_is_ar = is_ar
            current = ch
        elif is_ar == current_is_ar:
            current += ch
        else:
            runs.append((current_is_ar, current))
            current = ch
            current_is_ar = is_ar

    if current:
        runs.append((current_is_ar, current))

    # Reverse the order of runs
    runs.reverse()

    # Within RTL runs, reverse the characters too
    result = []
    for is_ar, segment in runs:
        if is_ar:
            result.append(segment[::-1])
        else:
            result.append(segment)

    return ''.join(result)


def ar(text):
    """Prepare Arabic text for Kivy rendering."""
    if not text:
        return text
    try:
        reshaped = reshape_arabic(text)
        return bidi_reorder(reshaped)
    except Exception as e:
        print(f"[AR] ERROR: {e}")
        return text


# =====================================================
# Font Helpers
# =====================================================
def afont():
    if FONT_LOADED:
        return {"font_name": FONT_ARABIC}
    return {}


def aLabel(text="", **kwargs):
    return Label(text=ar(text), **afont(), **kwargs)


def aButton(text="", **kwargs):
    return Button(text=ar(text), **afont(), **kwargs)


def aTextInput(text="", **kwargs):
    return TextInput(text=text, **afont(), **kwargs)


# =====================================================
# Configuration
# =====================================================
APP_NAME = "محرر أكاديمي"
APP_VERSION = "2.2.0"

COLOR_PRIMARY = (0.12, 0.20, 0.35, 1)
COLOR_SECONDARY = (0.20, 0.40, 0.60, 1)
COLOR_TERTIARY = (0.30, 0.50, 0.70, 1)
COLOR_BG = (0.96, 0.97, 0.98, 1)
COLOR_SURFACE = (1, 1, 1, 1)
COLOR_TEXT = (0.15, 0.15, 0.15, 1)
COLOR_TEXT_LIGHT = (0.85, 0.88, 0.92, 1)
COLOR_TEXT_MUTED = (0.45, 0.50, 0.55, 1)
COLOR_DANGER = (0.85, 0.25, 0.25, 1)
COLOR_TOOLBAR_BG = (0.94, 0.95, 0.96, 1)
COLOR_TOOLBAR_BTN = (0.30, 0.40, 0.50, 1)


# =====================================================
# Arabic Strings
# =====================================================
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
MSG_NO_DOCS_HINT = "اضغط \"مستند جديد\" لإنشاء أول مستند"

MSG_OPEN_BTN = "فتح"
MSG_DELETE = "حذف"
MSG_CANCEL = "إلغاء"
MSG_CONFIRM = "تأكيد الحذف"

MSG_UNTITLED = "بدون عنوان"
MSG_PLACEHOLDER = "ابدأ الكتابة هنا..."
MSG_SAVE = "حفظ"
MSG_SAVE_FAILED = "فشل الحفظ"
MSG_SAVED = "تم حفظ المستند"
MSG_LOADED = "تم التحميل"
MSG_NOT_FOUND = "المستند غير موجود"
MSG_UPDATED = "آخر تحديث"

MSG_TOOL_H1 = "ع1"
MSG_TOOL_H2 = "ع2"
MSG_TOOL_BODY = "نص"
MSG_TOOL_BOLD = "B"
MSG_TOOL_ITALIC = "I"
MSG_TOOL_UNDERLINE = "U"


# =====================================================
# Storage
# =====================================================
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


# =====================================================
# DocManager
# =====================================================
class DocManager:

    @staticmethod
    def path_for(doc_id):
        return os.path.join(STORAGE_DIR, f"{doc_id}.json")

    @staticmethod
    def save(doc_id, title, content, created=None):
        if not doc_id:
            doc_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs(STORAGE_DIR, exist_ok=True)

        if created is None:
            existing = DocManager.load(doc_id)
            created = existing.get("created") if existing else datetime.now().isoformat()

        data = {
            "id": doc_id,
            "title": title or MSG_UNTITLED,
            "content": content or "",
            "created": created,
            "updated": datetime.now().isoformat(),
        }
        try:
            with open(DocManager.path_for(doc_id), "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"[SAVE] {doc_id}")
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
                return json.load(f)
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


# =====================================================
# Home Screen
# =====================================================
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

        header.add_widget(aLabel(
            text=MSG_APP_NAME,
            font_size="36sp", bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None, height=dp(58),
        ))
        header.add_widget(aLabel(
            text=MSG_SUBTITLE,
            font_size="18sp", color=COLOR_TEXT_LIGHT,
            size_hint_y=None, height=dp(38),
        ))
        header.add_widget(aLabel(
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

        btn_new = aButton(
            text=MSG_NEW_DOC,
            font_size="22sp",
            size_hint=(1, None), height=dp(68),
            background_normal="",
            background_color=COLOR_PRIMARY,
            color=(1, 1, 1, 1),
        )
        btn_new.bind(on_release=self._on_new)

        btn_open = aButton(
            text=MSG_OPEN_DOC,
            font_size="22sp",
            size_hint=(1, None), height=dp(68),
            background_normal="",
            background_color=COLOR_SECONDARY,
            color=(1, 1, 1, 1),
        )
        btn_open.bind(on_release=self._on_open)

        btn_settings = aButton(
            text=MSG_SETTINGS,
            font_size="22sp",
            size_hint=(1, None), height=dp(68),
            background_normal="",
            background_color=COLOR_TERTIARY,
            color=(1, 1, 1, 1),
        )
        btn_settings.bind(on_release=self._on_settings)

        menu.add_widget(btn_new)
        menu.add_widget(btn_open)
        menu.add_widget(btn_settings)

        root.add_widget(menu)
        root.add_widget(Widget())

        self.footer = aLabel(
            text=MSG_READY,
            font_size="15sp", color=COLOR_TEXT_MUTED,
            size_hint_y=None, height=dp(50),
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


# =====================================================
# Editor Screen
# =====================================================
class EditorScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "editor"
        self.doc_id = None
        self.doc_created = None

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

        btn_back = aButton(
            text=">", font_size="24sp",
            size_hint=(None, 1), width=dp(50),
            background_normal="", background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1),
        )
        btn_back.bind(on_release=self._on_back)

        # Title input - user types raw (no reshaping in TextInput)
        self.title_input = aTextInput(
            text=MSG_UNTITLED,
            font_size="18sp", multiline=False,
            background_color=(0, 0, 0, 0),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1),
            hint_text_color=(0.7, 0.75, 0.82, 1),
            halign="right",
        )

        btn_save = aButton(
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

        toolbar = BoxLayout(
            orientation="horizontal",
            size_hint_y=None, height=dp(50),
            padding=[dp(6), dp(4)], spacing=dp(6),
        )
        with toolbar.canvas.before:
            Color(*COLOR_TOOLBAR_BG)
            self.tb_bg = Rectangle(pos=toolbar.pos, size=toolbar.size)
        toolbar.bind(
            pos=lambda *_: setattr(self.tb_bg, "pos", toolbar.pos),
            size=lambda *_: setattr(self.tb_bg, "size", toolbar.size),
        )

        for label, action in [
            (MSG_TOOL_H1, "h1"), (MSG_TOOL_H2, "h2"), (MSG_TOOL_BODY, "body"),
            (MSG_TOOL_BOLD, "bold"), (MSG_TOOL_ITALIC, "italic"), (MSG_TOOL_UNDERLINE, "underline"),
        ]:
            b = aButton(
                text=label, font_size="14sp", bold=(action in ("h1", "h2")),
                size_hint_y=None, height=dp(42),
                size_hint_x=None, width=dp(55),
                background_normal="",
                background_color=COLOR_TOOLBAR_BTN,
                color=(1, 1, 1, 1),
            )
            b.bind(on_release=lambda btn, a=action: self._on_tool(a))
            toolbar.add_widget(b)
        toolbar.add_widget(Label())
        root.add_widget(toolbar)

        editor_area = BoxLayout(padding=[dp(12), dp(12)])
        with editor_area.canvas.before:
            Color(*COLOR_SURFACE)
            self.ed_bg = Rectangle(pos=editor_area.pos, size=editor_area.size)
        editor_area.bind(
            pos=lambda *_: setattr(self.ed_bg, "pos", editor_area.pos),
            size=lambda *_: setattr(self.ed_bg, "size", editor_area.size),
        )

        self.text_input = aTextInput(
            text="",
            font_size="17sp",
            foreground_color=COLOR_TEXT,
            background_color=COLOR_SURFACE,
            cursor_color=COLOR_PRIMARY,
            hint_text_color=(0.6, 0.65, 0.70, 1),
            multiline=True,
            halign="right",
        )
        editor_area.add_widget(self.text_input)
        root.add_widget(editor_area)

        self.footer = aLabel(
            text="", font_size="13sp",
            color=COLOR_TEXT_MUTED,
            size_hint_y=None, height=dp(35),
        )
        root.add_widget(self.footer)

        self.add_widget(root)

    def new_document(self):
        self.doc_id = None
        self.doc_created = None
        self.title_input.text = MSG_UNTITLED
        self.text_input.text = ""
        self.footer.text = ""

    def open_document(self, doc_id):
        data = DocManager.load(doc_id)
        if not data:
            self.footer.text = ar(MSG_NOT_FOUND)
            return
        self.doc_id = data.get("id")
        self.doc_created = data.get("created")
        self.title_input.text = data.get("title", MSG_UNTITLED)
        self.text_input.text = data.get("content", "")
        self.footer.text = ar(f"{MSG_LOADED}: {self.title_input.text}")

    def _on_back(self, *args):
        self.manager.current = "home"

    def _on_save(self, *args):
        title = self.title_input.text.strip() or MSG_UNTITLED
        content = self.text_input.text
        saved_id = DocManager.save(
            doc_id=self.doc_id,
            title=title,
            content=content,
            created=self.doc_created,
        )
        if saved_id:
            self.doc_id = saved_id
            self.footer.text = ar(MSG_SAVED)
        else:
            self.footer.text = ar(MSG_SAVE_FAILED)

    def _on_tool(self, action):
        self.footer.text = ar(action)


# =====================================================
# Documents List Screen
# =====================================================
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

        btn_back = aButton(
            text=">", font_size="24sp",
            size_hint=(None, 1), width=dp(50),
            background_normal="", background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1),
        )
        btn_back.bind(on_release=lambda *_: self._back())

        top.add_widget(btn_back)
        top.add_widget(aLabel(
            text=MSG_MY_DOCS,
            font_size="20sp", color=(1, 1, 1, 1),
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
        self.empty.add_widget(aLabel(
            text=MSG_NO_DOCS,
            font_size="20sp", bold=True,
            color=COLOR_TEXT_MUTED,
            size_hint_y=None, height=dp(40),
        ))
        self.empty.add_widget(aLabel(
            text=MSG_NO_DOCS_HINT,
            font_size="15sp",
            color=COLOR_TEXT_MUTED,
            size_hint_y=None, height=dp(30),
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
            padding=[dp(12), dp(8)],
            spacing=dp(8),
        )
        with row.canvas.before:
            Color(*COLOR_SURFACE)
            bg = Rectangle(pos=row.pos, size=row.size)
        row.bind(
            pos=lambda *_: setattr(bg, "pos", row.pos),
            size=lambda *_: setattr(bg, "size", row.size),
        )

        info = BoxLayout(orientation="vertical", spacing=dp(4))
        info.add_widget(aLabel(
            text=doc.get("title", MSG_UNTITLED),
            font_size="18sp", bold=True,
            color=COLOR_TEXT, halign="right",
            size_hint_y=None, height=dp(30),
        ))
        updated = doc.get("updated", "")[:16].replace("T", " ")
        info.add_widget(aLabel(
            text=f"{MSG_UPDATED}: {updated}",
            font_size="12sp", color=COLOR_TEXT_MUTED,
            halign="right",
            size_hint_y=None, height=dp(22),
        ))

        btn_open = aButton(
            text=MSG_OPEN_BTN,
            font_size="15sp",
            size_hint=(None, 1), width=dp(80),
            background_normal="",
            background_color=COLOR_SECONDARY,
            color=(1, 1, 1, 1),
        )
        btn_open.bind(on_release=lambda b, did=doc["id"]: self._open(did))

        btn_del = aButton(
            text="X",
            font_size="16sp", bold=True,
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
        content.add_widget(aLabel(
            text=f"{MSG_CONFIRM}: {doc.get('title', MSG_UNTITLED)}",
            halign="center",
        ))
        btns = BoxLayout(
            orientation="horizontal", size_hint_y=None,
            height=dp(50), spacing=dp(10),
        )
        btn_no = aButton(text=MSG_CANCEL, background_normal="",
                         background_color=COLOR_SECONDARY, color=(1, 1, 1, 1))
        btn_yes = aButton(text=MSG_DELETE, background_normal="",
                          background_color=COLOR_DANGER, color=(1, 1, 1, 1))
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


# =====================================================
# App
# =====================================================
class AcademicWordEditorApp(App):

    def build(self):
        self.title = APP_NAME
        Window.clearcolor = COLOR_BG

        set_storage_dir()
        print(f"[APP] Storage: {STORAGE_DIR}")
        print(f"[APP] Font: {FONT_LOADED}")

        sm = ScreenManager(transition=SlideTransition(duration=0.2))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(EditorScreen(name="editor"))
        sm.add_widget(DocumentsListScreen(name="documents"))
        sm.current = "home"
        return sm


if __name__ == "__main__":
    AcademicWordEditorApp().run()
