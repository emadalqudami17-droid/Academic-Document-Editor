# screens/home.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp

from utils.constants import (
    APP_VERSION, MSG_TITLE, MSG_SUBTITLE, MSG_NEW_DOC,
    MSG_OPEN_DOC, MSG_SETTINGS, MSG_READY,
    COLOR_PRIMARY, COLOR_SECONDARY, COLOR_TERTIARY,
    COLOR_BG, COLOR_TEXT_LIGHT, COLOR_TEXT_MUTED,
    BUTTON_HEIGHT, SPACING_BUTTON,
)


# =====================================================
# Header
# =====================================================
class Header(BoxLayout):
    """Top header bar."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = dp(160)
        self.padding = [dp(20), dp(35), dp(20), dp(20)]
        self.spacing = dp(6)

        with self.canvas.before:
            Color(*COLOR_PRIMARY)
            self.bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)

        self.add_widget(Label(
            text=MSG_TITLE,
            font_size="32sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(50),
        ))

        self.add_widget(Label(
            text=MSG_SUBTITLE,
            font_size="18sp",
            color=COLOR_TEXT_LIGHT,
            size_hint_y=None,
            height=dp(38),
        ))

        self.add_widget(Label(
            text=f"Version {APP_VERSION}",
            font_size="13sp",
            color=(0.70, 0.75, 0.82, 1),
            size_hint_y=None,
            height=dp(22),
        ))

    def _update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size


# =====================================================
# Menu Button
# =====================================================
class MenuButton(Button):
    """Styled menu button."""

    def __init__(self, text="", color=None, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.font_size = "20sp"
        self.size_hint = (1, None)
        self.height = dp(BUTTON_HEIGHT)
        self.background_normal = ""
        self.background_down = ""
        self.background_color = color or COLOR_SECONDARY
        self.color = (1, 1, 1, 1)


# =====================================================
# Home Screen
# =====================================================
class HomeScreen(Screen):
    """Home screen with menu."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "home"

        # Root layout
        root = BoxLayout(
            orientation="vertical",
            padding=0,
            spacing=0,
        )

        # Background
        with root.canvas.before:
            Color(*COLOR_BG)
            self.bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(
            pos=lambda *_: setattr(self.bg, "pos", root.pos),
            size=lambda *_: setattr(self.bg, "size", root.size),
        )

        # Header
        root.add_widget(Header())
        root.add_widget(Widget(size_hint_y=None, height=dp(30)))

        # Menu with proper padding
        menu = BoxLayout(
            orientation="vertical",
            padding=[dp(24), dp(10), dp(24), dp(10)],
            spacing=dp(SPACING_BUTTON),
            size_hint_y=None,
            height=dp(3 * (BUTTON_HEIGHT + SPACING_BUTTON) + 20),
        )

        btn_new = MenuButton(
            text=MSG_NEW_DOC,
            color=COLOR_PRIMARY,
        )
        btn_new.bind(on_release=self._on_new)

        btn_open = MenuButton(
            text=MSG_OPEN_DOC,
            color=COLOR_SECONDARY,
        )
        btn_open.bind(on_release=self._on_open)

        btn_settings = MenuButton(
            text=MSG_SETTINGS,
            color=COLOR_TERTIARY,
        )
        btn_settings.bind(on_release=self._on_settings)

        menu.add_widget(btn_new)
        menu.add_widget(btn_open)
        menu.add_widget(btn_settings)

        root.add_widget(menu)

        # Filler
        root.add_widget(Widget())

        # Footer
        self.footer = Label(
            text=MSG_READY,
            font_size="14sp",
            color=COLOR_TEXT_MUTED,
            size_hint_y=None,
            height=dp(50),
        )
        root.add_widget(self.footer)

        self.add_widget(root)

    def set_footer(self, text):
        self.footer.text = text

    def _on_new(self, *args):
        print("[HOME] New document tapped")
        self.manager.current = "editor"

    def _on_open(self, *args):
        print("[HOME] Open document tapped")
        self.set_footer("Open document - coming soon")

    def _on_settings(self, *args):
        print("[HOME] Settings tapped")
        self.set_footer("Settings - coming soon")
