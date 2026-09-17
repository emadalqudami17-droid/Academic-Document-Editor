# screens/editor.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp

from utils.constants import (
    MSG_EDITOR_TITLE, MSG_EDITOR_PLACEHOLDER,
    MSG_SAVE, MSG_SAVED, MSG_SAVE_FAILED, MSG_UNTITLED,
    COLOR_PRIMARY, COLOR_BG, COLOR_SURFACE,
    COLOR_TEXT, COLOR_TEXT_LIGHT,
    COLOR_TOOLBAR_BG, COLOR_TOOLBAR_BTN,
    COLOR_DANGER,
    TOOL_H1, TOOL_H2, TOOL_BODY,
    TOOL_BOLD, TOOL_ITALIC, TOOL_UNDERLINE,
)
from document.manager import DocumentManager


# =====================================================
# Editor Screen
# =====================================================
class EditorScreen(Screen):
    """Editor with save + formatting toolbar."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "editor"

        # Current document state
        self.doc_id = None
        self.doc_created = None

        root = BoxLayout(orientation="vertical", spacing=0)

        # Background
        with root.canvas.before:
            Color(*COLOR_BG)
            self.bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(
            pos=lambda *_: setattr(self.bg, "pos", root.pos),
            size=lambda *_: setattr(self.bg, "size", root.size),
        )

        # === Top Bar ===
        root.add_widget(self._build_top_bar())

        # === Formatting Toolbar ===
        root.add_widget(self._build_formatting_toolbar())

        # === Text Editor ===
        root.add_widget(self._build_editor_area())

        # === Footer ===
        self.footer = Label(
            text="",
            font_size="13sp",
            color=(0.45, 0.50, 0.55, 1),
            size_hint_y=None,
            height=dp(35),
        )
        root.add_widget(self.footer)

        self.add_widget(root)

    # =====================================================
    # Top Bar
    # =====================================================
    def _build_top_bar(self):
        bar = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(60),
            padding=[dp(8), 0],
            spacing=dp(8),
        )

        with bar.canvas.before:
            Color(*COLOR_PRIMARY)
            self.tb_bg = Rectangle(pos=bar.pos, size=bar.size)
        bar.bind(
            pos=lambda *_: setattr(self.tb_bg, "pos", bar.pos),
            size=lambda *_: setattr(self.tb_bg, "size", bar.size),
        )

        # Back button
        btn_back = Button(
            text="<",
            font_size="24sp",
            size_hint=(None, 1),
            width=dp(50),
            background_normal="",
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1),
        )
        btn_back.bind(on_release=self._on_back)

        # Title (editable text input)
        self.title_input = TextInput(
            text=MSG_EDITOR_TITLE,
            hint_text=MSG_EDITOR_TITLE,
            font_size="18sp",
            multiline=False,
            background_color=(0, 0, 0, 0),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1),
            hint_text_color=(0.7, 0.75, 0.82, 1),
            padding_y=[dp(15), 0],
        )

        # Save button
        btn_save = Button(
            text=MSG_SAVE,
            font_size="16sp",
            size_hint=(None, 1),
            width=dp(80),
            background_normal="",
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1),
        )
        btn_save.bind(on_release=self._on_save)

        bar.add_widget(btn_back)
        bar.add_widget(self.title_input)
        bar.add_widget(btn_save)

        return bar

    # =====================================================
    # Formatting Toolbar
    # =====================================================
    def _build_formatting_toolbar(self):
        bar = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(50),
            padding=[dp(6), dp(4)],
            spacing=dp(6),
        )

        with bar.canvas.before:
            Color(*COLOR_TOOLBAR_BG)
            self.ft_bg = Rectangle(pos=bar.pos, size=bar.size)
        bar.bind(
            pos=lambda *_: setattr(self.ft_bg, "pos", bar.pos),
            size=lambda *_: setattr(self.ft_bg, "size", bar.size),
        )

        # Tools
        tools = [
            (TOOL_H1, "h1"),
            (TOOL_H2, "h2"),
            (TOOL_BODY, "body"),
            ("|", None),         # separator
            (TOOL_BOLD, "bold"),
            (TOOL_ITALIC, "italic"),
            (TOOL_UNDERLINE, "underline"),
        ]

        self.tool_buttons = {}

        for label, action in tools:
            if label == "|":
                # Separator
                sep = Label(
                    text=" ",
                    size_hint_x=None,
                    width=dp(8),
                )
                bar.add_widget(sep)
                continue

            btn = Button(
                text=label,
                font_size="14sp",
                bold=(action in ("h1", "h2")),
                size_hint_y=None,
                height=dp(42),
                size_hint_x=None,
                width=dp(50),
                background_normal="",
                background_color=COLOR_TOOLBAR_BTN,
                color=(1, 1, 1, 1),
            )
            btn.bind(on_release=lambda b, a=action: self._on_tool(a))
            self.tool_buttons[action] = btn
            bar.add_widget(btn)

        # Filler
        bar.add_widget(Label())

        return bar

    # =====================================================
    # Editor Area
    # =====================================================
    def _build_editor_area(self):
        container = BoxLayout(padding=[dp(12), dp(12)])

        with container.canvas.before:
            Color(*COLOR_SURFACE)
            self.ed_bg = Rectangle(
                pos=container.pos,
                size=container.size,
            )
        container.bind(
            pos=lambda *_: setattr(self.ed_bg, "pos", container.pos),
            size=lambda *_: setattr(self.ed_bg, "size", container.size),
        )

        self.text_input = TextInput(
            text="",
            hint_text=MSG_EDITOR_PLACEHOLDER,
            font_size="16sp",
            foreground_color=COLOR_TEXT,
            background_color=COLOR_SURFACE,
            cursor_color=COLOR_PRIMARY,
            multiline=True,
        )

        container.add_widget(self.text_input)
        return container

    # =====================================================
    # Public API (called from home)
    # =====================================================
    def new_document(self):
        """Reset for a new document."""
        print("[EDITOR] New document")
        self.doc_id = None
        self.doc_created = None
        self.title_input.text = MSG_EDITOR_TITLE
        self.text_input.text = ""
        self.footer.text = ""

    def open_document(self, doc_id):
        """Load an existing document."""
        print(f"[EDITOR] Open: {doc_id}")
        data = DocumentManager.load(doc_id)
        if not data:
            self.footer.text = "Document not found"
            return

        self.doc_id = data.get("id")
        self.doc_created = data.get("created")
        self.title_input.text = data.get("title", MSG_UNTITLED)
        self.text_input.text = data.get("content", "")
        self.footer.text = f"Loaded: {self.title_input.text}"

    # =====================================================
    # Actions
    # =====================================================
    def _on_back(self, *args):
        print("[EDITOR] Back")
        self.manager.current = "home"

    def _on_save(self, *args):
        print("[EDITOR] Save")
        title = self.title_input.text.strip() or MSG_UNTITLED
        content = self.text_input.text

        saved_id = DocumentManager.save(
            doc_id=self.doc_id,
            title=title,
            content=content,
            created=self.doc_created,
        )

        if saved_id:
            self.doc_id = saved_id
            self.footer.text = MSG_SAVED
            print(f"[EDITOR] Saved as: {saved_id}")
        else:
            self.footer.text = MSG_SAVE_FAILED
            print("[EDITOR] Save failed")

    def _on_tool(self, action):
        """Handle formatting tool click."""
        print(f"[EDITOR] Tool: {action}")

        # Visual feedback: highlight active tool briefly
        for key, btn in self.tool_buttons.items():
            if key == action:
                btn.background_color = COLOR_PRIMARY
            else:
                btn.background_color = COLOR_TOOLBAR_BTN

        # For now, just show action in footer
        # Real formatting will come in a later stage
        if action in ("h1", "h2"):
            self.footer.text = f"Style: {action.upper()}"
        elif action in ("bold", "italic", "underline"):
            self.footer.text = f"Format: {action.title()}"
        elif action == "body":
            self.footer.text = "Style: Body"
        else:
            self.footer.text = f"Action: {action}"
