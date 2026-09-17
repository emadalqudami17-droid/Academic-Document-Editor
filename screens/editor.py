# screens/editor.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp

from utils.constants import (
    MSG_EDITOR_TITLE, MSG_EDITOR_PLACEHOLDER,
    MSG_SAVE, MSG_BACK, MSG_SAVED,
    COLOR_PRIMARY, COLOR_BG, COLOR_SURFACE,
    COLOR_TEXT, COLOR_TEXT_LIGHT,
)


# =====================================================
# Editor Screen
# =====================================================
class EditorScreen(Screen):
    """Document editor screen."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "editor"

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
        top_bar = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(60),
            padding=[dp(8), 0],
            spacing=dp(8),
        )

        with top_bar.canvas.before:
            Color(*COLOR_PRIMARY)
            self.tb_bg = Rectangle(pos=top_bar.pos, size=top_bar.size)
        top_bar.bind(
            pos=lambda *_: setattr(self.tb_bg, "pos", top_bar.pos),
            size=lambda *_: setattr(self.tb_bg, "size", top_bar.size),
        )

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

        title = Label(
            text=MSG_EDITOR_TITLE,
            font_size="18sp",
            color=(1, 1, 1, 1),
            halign="center",
            valign="middle",
        )
        title.bind(size=title.setter("text_size"))

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

        top_bar.add_widget(btn_back)
        top_bar.add_widget(title)
        top_bar.add_widget(btn_save)

        root.add_widget(top_bar)

        # === Text Editor ===
        editor_container = BoxLayout(
            padding=[dp(12), dp(12)],
        )

        with editor_container.canvas.before:
            Color(*COLOR_SURFACE)
            self.ed_bg = Rectangle(
                pos=editor_container.pos,
                size=editor_container.size,
            )
        editor_container.bind(
            pos=lambda *_: setattr(
                self.ed_bg, "pos", editor_container.pos
            ),
            size=lambda *_: setattr(
                self.ed_bg, "size", editor_container.size
            ),
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

        editor_container.add_widget(self.text_input)
        root.add_widget(editor_container)

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
    # Actions
    # =====================================================
    def _on_back(self, *args):
        print("[EDITOR] Back")
        self.manager.current = "home"

    def _on_save(self, *args):
        print("[EDITOR] Save")
        content = self.text_input.text
        print(f"[EDITOR] Content length: {len(content)}")
        self.footer.text = MSG_SAVED
