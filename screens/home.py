# screens/home.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp

from utils.constants import (
    APP_VERSION, FONT_ARABIC,
    COLOR_PRIMARY, COLOR_BG, COLOR_TEXT_MUTED,
    MSG_NEW_DOC, MSG_OPEN_DOC, MSG_SETTINGS, MSG_WELCOME,
)


class TopBar(BoxLayout):
    """Header with app name + Arabic subtitle."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = dp(160)
        self.padding = [dp(20), dp(35), dp(20), dp(20)]
        self.spacing = dp(6)

        with self.canvas.before:
            Color(*COLOR_PRIMARY)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)

        title = Label(
            text="Academic Word",
            font_size="32sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(50),
        )

        subtitle = Label(
            text="محرر أكاديمي احترافي",
            font_name=FONT_ARABIC,
            font_size="20sp",
            color=(0.90, 0.93, 0.97, 1),
            size_hint_y=None,
            height=dp(38),
        )

        version = Label(
            text=f"v{APP_VERSION}",
            font_size="13sp",
            color=(0.70, 0.75, 0.82, 1),
            size_hint_y=None,
            height=dp(22),
        )

        self.add_widget(title)
        self.add_widget(subtitle)
        self.add_widget(version)

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size


class MenuButton(Button):
    """Styled menu button with Arabic text."""

    def __init__(self, text="", color=None, callback=None, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.font_name = FONT_ARABIC
        self.font_size = "22sp"
        self.size_hint_y = None
        self.height = dp(70)
        self.background_normal = ""
        self.background_down = ""
        self.background_color = color or (0.20, 0.45, 0.70, 1)
        self.color = (1, 1, 1, 1)

        if callback:
            self.bind(on_release=lambda *_: callback())


class HomeScreen(BoxLayout):
    """Home screen with Arabic interface."""

    def __init__(self, on_new_doc=None, on_open_doc=None,
                 on_settings=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 0
        self.spacing = 0

        with self.canvas.before:
            Color(*COLOR_BG)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)

        self._on_new_doc = on_new_doc
        self._on_open_doc = on_open_doc
        self._on_settings = on_settings

        self.add_widget(TopBar())
        self.add_widget(Widget(size_hint_y=None, height=dp(30)))

        menu = BoxLayout(
            orientation="vertical",
            padding=[dp(24), dp(10), dp(24), dp(10)],
            spacing=dp(18),
        )

        menu.add_widget(MenuButton(
            text=MSG_NEW_DOC,
            color=(0.12, 0.20, 0.35, 1),
            callback=self._handle_new,
        ))

        menu.add_widget(MenuButton(
            text=MSG_OPEN_DOC,
            color=(0.20, 0.40, 0.60, 1),
            callback=self._handle_open,
        ))

        menu.add_widget(MenuButton(
            text=MSG_SETTINGS,
            color=(0.30, 0.50, 0.70, 1),
            callback=self._handle_settings,
        ))

        self.add_widget(menu)
        self.add_widget(Widget())

        footer = Label(
            text=MSG_WELCOME,
            font_name=FONT_ARABIC,
            font_size="15sp",
            color=COLOR_TEXT_MUTED,
            size_hint_y=None,
            height=dp(50),
        )
        self.add_widget(footer)

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def _handle_new(self):
        if self._on_new_doc:
            self._on_new_doc()

    def _handle_open(self):
        if self._on_open_doc:
            self._on_open_doc()

    def _handle_settings(self):
        if self._on_settings:
            self._on_settings()


def register_arabic_font():
    """Register Arabic font with Kivy."""
    from kivy.core.text import LabelBase
    import os
    if os.path.exists(FONT_ARABIC_PATH):
        LabelBase.register(
            name=FONT_ARABIC,
            fn_regular=FONT_ARABIC_PATH,
        )
        return True
    return False
