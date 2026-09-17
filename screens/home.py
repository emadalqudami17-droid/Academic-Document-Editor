# screens/home.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.metrics import dp
from kivy.utils import get_color_from_hex

from utils.constants import (
    APP_NAME, APP_VERSION, MSG_WELCOME,
    COLOR_PRIMARY, COLOR_ACCENT, COLOR_BG,
    COLOR_TEXT, COLOR_TEXT_MUTED,
)


def hex_to_rgba(hex_str, alpha=1):
    """Convert hex color to RGBA tuple."""
    c = get_color_from_hex(hex_str)
    return (c[0], c[1], c[2], alpha)


class TopBar(BoxLayout):
    """Top header bar with app title."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = dp(140)
        self.padding = [dp(20), dp(30), dp(20), dp(20)]
        self.spacing = dp(4)

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
            height=dp(45),
            halign="center",
            valign="middle",
        )
        title.bind(size=title.setter("text_size"))

        subtitle = Label(
            text="محرر أكاديمي احترافي",
            font_size="16sp",
            color=(0.85, 0.88, 0.92, 1),
            size_hint_y=None,
            height=dp(30),
            halign="center",
            valign="middle",
        )
        subtitle.bind(size=subtitle.setter("text_size"))

        version = Label(
            text=f"v{APP_VERSION}",
            font_size="12sp",
            color=(0.70, 0.75, 0.82, 1),
            size_hint_y=None,
            height=dp(20),
            halign="center",
            valign="middle",
        )
        version.bind(size=version.setter("text_size"))

        self.add_widget(title)
        self.add_widget(subtitle)
        self.add_widget(version)

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size


class MenuButton(Button):
    """Custom styled menu button."""

    def __init__(self, text="", icon="", color=None, callback=None, **kwargs):
        super().__init__(**kwargs)
        self.text = f"{icon}  {text}" if icon else text
        self.font_size = "17sp"
        self.bold = True
        self.size_hint_y = None
        self.height = dp(60)
        self.background_normal = ""
        self.background_down = ""
        self.background_color = color or COLOR_ACCENT
        self.color = (1, 1, 1, 1)
        self.markup = False

        if callback:
            self.bind(on_release=lambda *_: callback())


class HomeScreen(BoxLayout):
    """Main home screen."""

    def __init__(self, on_new_doc=None, on_open_doc=None,
                 on_settings=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 0
        self.spacing = 0

        # Background
        with self.canvas.before:
            Color(*COLOR_BG)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)

        # Callbacks
        self._on_new_doc = on_new_doc
        self._on_open_doc = on_open_doc
        self._on_settings = on_settings

        # Top bar
        self.add_widget(TopBar())

        # Spacer
        self.add_widget(Widget(size_hint_y=None, height=dp(20)))

        # Menu container
        menu = BoxLayout(
            orientation="vertical",
            padding=[dp(24), dp(10), dp(24), dp(10)],
            spacing=dp(14),
        )

        menu.add_widget(MenuButton(
            text="مستند جديد",
            icon="[b]+[/b]",
            color=hex_to_rgba("#1e3a5f"),
            callback=self._handle_new,
        ))

        menu.add_widget(MenuButton(
            text="فتح مستند",
            icon="[b]>[/b]",
            color=hex_to_rgba("#2e5a8f"),
            callback=self._handle_open,
        ))

        menu.add_widget(MenuButton(
            text="الإعدادات",
            icon="[b]*[/b]",
            color=hex_to_rgba("#4a6a8f"),
            callback=self._handle_settings,
        ))

        self.add_widget(menu)

        # Bottom spacer
        self.add_widget(Widget())

        # Footer
        footer = Label(
            text=MSG_WELCOME,
            font_size="13sp",
            color=COLOR_TEXT_MUTED,
            size_hint_y=None,
            height=dp(40),
            halign="center",
            valign="middle",
        )
        footer.bind(size=footer.setter("text_size"))
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
