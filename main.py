# main.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.metrics import dp


# =====================================================
# Configuration
# =====================================================
APP_NAME = "Academic Word Editor"
APP_VERSION = "1.0.0"

# Colors
COLOR_PRIMARY = (0.12, 0.20, 0.35, 1)
COLOR_SECONDARY = (0.20, 0.40, 0.60, 1)
COLOR_TERTIARY = (0.30, 0.50, 0.70, 1)
COLOR_BG = (0.96, 0.97, 0.98, 1)
COLOR_TEXT = (0.15, 0.15, 0.15, 1)
COLOR_TEXT_LIGHT = (0.85, 0.88, 0.92, 1)
COLOR_TEXT_MUTED = (0.45, 0.50, 0.55, 1)


# =====================================================
# Components
# =====================================================
class Header(BoxLayout):
    """Top header with app title and version."""

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

        title = Label(
            text="Academic Word",
            font_size="32sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(50),
        )

        subtitle = Label(
            text="Academic Document Editor",
            font_size="18sp",
            color=COLOR_TEXT_LIGHT,
            size_hint_y=None,
            height=dp(38),
        )

        version = Label(
            text=f"Version {APP_VERSION}",
            font_size="13sp",
            color=(0.70, 0.75, 0.82, 1),
            size_hint_y=None,
            height=dp(22),
        )

        self.add_widget(title)
        self.add_widget(subtitle)
        self.add_widget(version)

    def _update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size


class MenuButton(Button):
    """Styled menu button."""

    def __init__(self, text="", color=None, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.font_size = "20sp"
        self.size_hint_y = None
        self.height = dp(68)
        self.background_normal = ""
        self.background_down = ""
        self.background_color = color or COLOR_SECONDARY
        self.color = (1, 1, 1, 1)


class Footer(Label):
    """Bottom footer label."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "Ready"
        self.font_size = "14sp"
        self.color = COLOR_TEXT_MUTED
        self.size_hint_y = None
        self.height = dp(50)


# =====================================================
# Main App
# =====================================================
class AcademicWordEditorApp(App):

    def build(self):
        self.title = APP_NAME
        Window.clearcolor = COLOR_BG

        root = BoxLayout(
            orientation="vertical",
            padding=0,
            spacing=0,
        )

        # Header
        root.add_widget(Header())

        # Spacer
        root.add_widget(Widget(size_hint_y=None, height=dp(30)))

        # Menu
        menu = BoxLayout(
            orientation="vertical",
            padding=[dp(24), dp(10), dp(24), dp(10)],
            spacing=dp(16),
        )

        btn_new = MenuButton(
            text="New Document",
            color=COLOR_PRIMARY,
        )
        btn_new.bind(on_release=self.on_new_document)

        btn_open = MenuButton(
            text="Open Document",
            color=COLOR_SECONDARY,
        )
        btn_open.bind(on_release=self.on_open_document)

        btn_settings = MenuButton(
            text="Settings",
            color=COLOR_TERTIARY,
        )
        btn_settings.bind(on_release=self.on_settings)

        menu.add_widget(btn_new)
        menu.add_widget(btn_open)
        menu.add_widget(btn_settings)

        root.add_widget(menu)

        # Filler
        root.add_widget(Widget())

        # Footer
        root.add_widget(Footer(text="Academic Word Editor v1.0.0"))

        return root

    # =====================================================
    # Callbacks
    # =====================================================
    def on_new_document(self, *args):
        print("[ACTION] New document")
        self.set_footer("Creating new document... (coming soon)")

    def on_open_document(self, *args):
        print("[ACTION] Open document")
        self.set_footer("Opening documents... (coming soon)")

    def on_settings(self, *args):
        print("[ACTION] Settings")
        self.set_footer("Settings... (coming soon)")

    def set_footer(self, text):
        """Update footer text."""
        try:
            root = self.root
            if root and len(root.children) > 0:
                footer = root.children[0]
                if isinstance(footer, Footer):
                    footer.text = text
        except Exception as e:
            print(f"[FOOTER] {e}")


if __name__ == "__main__":
    AcademicWordEditorApp().run()
