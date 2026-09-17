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
from kivy.metrics import dp


# =====================================================
# Configuration (inline, no utils.constants dependency)
# =====================================================
APP_NAME = "Academic Word Editor"
APP_VERSION = "1.3.0"

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
# Storage
# =====================================================
def get_storage_dir():
    """Get the best storage directory for documents."""
    candidates = []

    # 1) Kivy user_data_dir (works on Android and desktop)
    try:
        if App.get_running_app():
            base = App.get_running_app().user_data_dir
            candidates.append(os.path.join(base, "documents"))
    except Exception:
        pass

    # 2) Local relative directory (for desktop testing)
    candidates.append(os.path.join("data", "documents"))

    for path in candidates:
        try:
            os.makedirs(path, exist_ok=True)
            print(f"[STORAGE] Using: {path}")
            return path
        except Exception:
            continue

    return candidates[-1]


STORAGE_DIR = None  # will be set in App.build()


def set_storage_dir():
    global STORAGE_DIR
    STORAGE_DIR = get_storage_dir()
    return STORAGE_DIR


# =====================================================
# Document Manager (inline)
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
            "title": title or "Untitled",
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
                        "title": data.get("title", "Untitled"),
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

        # Header
        header = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(160),
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

        header.add_widget(Label(
            text="Academic Word",
            font_size="32sp", bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None, height=dp(50),
        ))
        header.add_widget(Label(
            text="Academic Document Editor",
            font_size="18sp", color=COLOR_TEXT_LIGHT,
            size_hint_y=None, height=dp(38),
        ))
        header.add_widget(Label(
            text=f"Version {APP_VERSION}",
            font_size="13sp", color=(0.70, 0.75, 0.82, 1),
            size_hint_y=None, height=dp(22),
        ))

        root.add_widget(header)
        root.add_widget(Widget(size_hint_y=None, height=dp(30)))

        # Menu
        menu = BoxLayout(
            orientation="vertical",
            padding=[dp(24), dp(10), dp(24), dp(10)],
            spacing=dp(16),
            size_hint_y=None,
            height=dp(3 * (68 + 16) + 20),
        )

        btn_new = Button(
            text="New Document",
            font_size="20sp",
            size_hint=(1, None), height=dp(68),
            background_normal="",
            background_color=COLOR_PRIMARY,
            color=(1, 1, 1, 1),
        )
        btn_new.bind(on_release=self._on_new)

        btn_open = Button(
            text="Open Document",
            font_size="20sp",
            size_hint=(1, None), height=dp(68),
            background_normal="",
            background_color=COLOR_SECONDARY,
            color=(1, 1, 1, 1),
        )
        btn_open.bind(on_release=self._on_open)

        btn_settings = Button(
            text="Settings",
            font_size="20sp",
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

        self.footer = Label(
            text="Ready",
            font_size="14sp", color=COLOR_TEXT_MUTED,
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
        self.footer.text = "Settings - coming soon"


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

        # Top bar
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

        btn_back = Button(
            text="<", font_size="24sp",
            size_hint=(None, 1), width=dp(50),
            background_normal="", background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1),
        )
        btn_back.bind(on_release=self._on_back)

        self.title_input = TextInput(
            text="New Document", hint_text="Title",
            font_size="18sp", multiline=False,
            background_color=(0, 0, 0, 0),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1),
        )

        btn_save = Button(
            text="Save", font_size="16sp",
            size_hint=(None, 1), width=dp(80),
            background_normal="", background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1),
        )
        btn_save.bind(on_release=self._on_save)

        top.add_widget(btn_back)
        top.add_widget(self.title_input)
        top.add_widget(btn_save)
        root.add_widget(top)

        # Toolbar
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
            ("H1", "h1"), ("H2", "h2"), ("Body", "body"),
            ("B", "bold"), ("I", "italic"), ("U", "underline"),
        ]:
            b = Button(
                text=label, font_size="14sp",
                size_hint_y=None, height=dp(42),
                size_hint_x=None, width=dp(50),
                background_normal="",
                background_color=COLOR_TOOLBAR_BTN,
                color=(1, 1, 1, 1),
            )
            b.bind(on_release=lambda btn, a=action: self._on_tool(a))
            toolbar.add_widget(b)
        toolbar.add_widget(Label())
        root.add_widget(toolbar)

        # Text area
        editor_area = BoxLayout(padding=[dp(12), dp(12)])
        with editor_area.canvas.before:
            Color(*COLOR_SURFACE)
            self.ed_bg = Rectangle(pos=editor_area.pos, size=editor_area.size)
        editor_area.bind(
            pos=lambda *_: setattr(self.ed_bg, "pos", editor_area.pos),
            size=lambda *_: setattr(self.ed_bg, "size", editor_area.size),
        )

        self.text_input = TextInput(
            text="", hint_text="Start writing here...",
            font_size="16sp",
            foreground_color=COLOR_TEXT,
            background_color=COLOR_SURFACE,
            cursor_color=COLOR_PRIMARY,
            multiline=True,
        )
        editor_area.add_widget(self.text_input)
        root.add_widget(editor_area)

        # Footer
        self.footer = Label(
            text="", font_size="13sp",
            color=COLOR_TEXT_MUTED,
            size_hint_y=None, height=dp(35),
        )
        root.add_widget(self.footer)

        self.add_widget(root)

    # ---------- API ----------
    def new_document(self):
        self.doc_id = None
        self.doc_created = None
        self.title_input.text = "New Document"
        self.text_input.text = ""
        self.footer.text = ""

    def open_document(self, doc_id):
        data = DocManager.load(doc_id)
        if not data:
            self.footer.text = "Document not found"
            return
        self.doc_id = data.get("id")
        self.doc_created = data.get("created")
        self.title_input.text = data.get("title", "Untitled")
        self.text_input.text = data.get("content", "")
        self.footer.text = f"Loaded: {self.title_input.text}"

    def _on_back(self, *args):
        self.manager.current = "home"

    def _on_save(self, *args):
        title = self.title_input.text.strip() or "Untitled"
        content = self.text_input.text
        saved_id = DocManager.save(
            doc_id=self.doc_id,
            title=title,
            content=content,
            created=self.doc_created,
        )
        if saved_id:
            self.doc_id = saved_id
            self.footer.text = "Document saved"
        else:
            self.footer.text = "Save failed"

    def _on_tool(self, action):
        self.footer.text = f"Action: {action}"


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

        # Top bar
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

        btn_back = Button(
            text="<", font_size="24sp",
            size_hint=(None, 1), width=dp(50),
            background_normal="", background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1),
        )
        btn_back.bind(on_release=lambda *_: self._back())

        top.add_widget(btn_back)
        top.add_widget(Label(
            text="My Documents",
            font_size="18sp", color=(1, 1, 1, 1),
        ))
        top.add_widget(Label(size_hint=(None, 1), width=dp(50)))

        root.add_widget(top)

        # Scrollable list
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

        # Empty state
        self.empty = Label(
            text="No documents yet\n\nTap 'New Document' to create one",
            font_size="16sp",
            color=COLOR_TEXT_MUTED,
            halign="center",
        )
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
            row = self._make_row(doc)
            self.list_layout.add_widget(row)

    def _make_row(self, doc):
        row = BoxLayout(
            orientation="horizontal",
            size_hint_y=None, height=dp(80),
            padding=[dp(12), dp(8)],
            spacing=dp(10),
        )
        with row.canvas.before:
            Color(*COLOR_SURFACE)
            bg = Rectangle(pos=row.pos, size=row.size)
        row.bind(
            pos=lambda *_: setattr(bg, "pos", row.pos),
            size=lambda *_: setattr(bg, "size", row.size),
        )

        info = BoxLayout(orientation="vertical", spacing=dp(4))
        info.add_widget(Label(
            text=doc.get("title", "Untitled"),
            font_size="17sp", bold=True,
            color=COLOR_TEXT, halign="left",
            size_hint_y=None, height=dp(28),
        ))
        updated = doc.get("updated", "")[:16].replace("T", " ")
        info.add_widget(Label(
            text=f"Updated: {updated}",
            font_size="12sp", color=COLOR_TEXT_MUTED,
            halign="left",
            size_hint_y=None, height=dp(22),
        ))

        # Buttons
        btn_open = Button(
            text="Open",
            font_size="14sp",
            size_hint=(None, 1), width=dp(70),
            background_normal="",
            background_color=COLOR_SECONDARY,
            color=(1, 1, 1, 1),
        )
        btn_open.bind(
            on_release=lambda b, did=doc["id"]: self._open(did)
        )

        btn_del = Button(
            text="X",
            font_size="16sp", bold=True,
            size_hint=(None, 1), width=dp(45),
            background_normal="",
            background_color=COLOR_DANGER,
            color=(1, 1, 1, 1),
        )
        btn_del.bind(
            on_release=lambda b, d=doc: self._confirm_delete(d)
        )

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
        content.add_widget(Label(
            text=f"Delete:\n\n{doc.get('title', 'Untitled')}?",
            halign="center",
        ))
        btns = BoxLayout(
            orientation="horizontal", size_hint_y=None,
            height=dp(50), spacing=dp(10),
        )
        btn_no = Button(text="Cancel", background_normal="",
                        background_color=COLOR_SECONDARY)
        btn_yes = Button(text="Delete", background_normal="",
                         background_color=COLOR_DANGER)
        btns.add_widget(btn_no)
        btns.add_widget(btn_yes)
        content.add_widget(btns)

        popup = Popup(
            title="Confirm Delete",
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

        # Set storage dir NOW (after app is running)
        set_storage_dir()
        print(f"[APP] Storage: {STORAGE_DIR}")

        sm = ScreenManager(transition=SlideTransition(duration=0.2))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(EditorScreen(name="editor"))
        sm.add_widget(DocumentsListScreen(name="documents"))
        sm.current = "home"
        return sm


if __name__ == "__main__":
    AcademicWordEditorApp().run()
