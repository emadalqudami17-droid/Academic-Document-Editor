# main.py
import sys
import traceback

# Capture any import errors
_error_log = []

def _log(msg):
    _error_log.append(str(msg))
    print(msg)


try:
    from kivy.app import App
    from kivy.uix.screenmanager import ScreenManager, SlideTransition
    from kivy.core.window import Window
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.label import Label
    from kivy.uix.scrollview import ScrollView
    from kivy.graphics import Color, Rectangle
    from kivy.metrics import dp
    _log("Kivy imports OK")
except Exception as e:
    _error_log.append(f"Kivy FAILED: {e}\n{traceback.format_exc()}")


try:
    from utils.constants import (
        APP_NAME, COLOR_BG,
        SCREEN_HOME, SCREEN_EDITOR, SCREEN_DOCUMENTS,
    )
    _log("Constants OK")
except Exception as e:
    _error_log.append(f"Constants FAILED: {e}\n{traceback.format_exc()}")


try:
    from screens.home import HomeScreen
    _log("Home OK")
except Exception as e:
    _error_log.append(f"Home FAILED: {e}\n{traceback.format_exc()}")


try:
    from screens.editor import EditorScreen
    _log("Editor OK")
except Exception as e:
    _error_log.append(f"Editor FAILED: {e}\n{traceback.format_exc()}")


try:
    from screens.documents_list import DocumentsListScreen
    _log("DocumentsList OK")
except Exception as e:
    _error_log.append(f"DocumentsList FAILED: {e}\n{traceback.format_exc()}")


# =====================================================
# Error Screen (shown when something fails)
# =====================================================
class ErrorScreen(BoxLayout):
    """Shows the error log on screen."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = dp(16)
        self.spacing = dp(8)

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(
            pos=lambda *_: setattr(self.bg, "pos", self.pos),
            size=lambda *_: setattr(self.bg, "size", self.size),
        )

        title = Label(
            text="DIAGNOSTIC MODE",
            font_size="20sp",
            bold=True,
            color=(1, 0, 0, 1),
            size_hint_y=None,
            height=dp(40),
        )
        self.add_widget(title)

        scroll = ScrollView()
        content = Label(
            text="\n\n".join(_error_log),
            font_size="11sp",
            color=(0, 0, 0, 1),
            size_hint_y=None,
            halign="left",
            valign="top",
        )
        content.bind(
            width=lambda *_: content.setter("text_size")(content, (content.width, None)),
            texture_size=lambda *_: setattr(content, "height", content.texture_size[1]),
        )
        content.text_size = (500, None)
        scroll.add_widget(content)
        self.add_widget(scroll)


# =====================================================
# App
# =====================================================
class AcademicWordEditorApp(App):

    def build(self):
        self.title = APP_NAME
        Window.clearcolor = COLOR_BG

        # If any import failed, show errors
        if any("FAILED" in line for line in _error_log):
            print(">>> DIAGNOSTIC MODE")
            return ErrorScreen()

        try:
            sm = ScreenManager(transition=SlideTransition(duration=0.2))
            sm.add_widget(HomeScreen(name=SCREEN_HOME))
            sm.add_widget(EditorScreen(name=SCREEN_EDITOR))
            sm.add_widget(DocumentsListScreen(name=SCREEN_DOCUMENTS))
            sm.current = SCREEN_HOME
            return sm
        except Exception as e:
            _error_log.append(f"BUILD FAILED: {e}\n{traceback.format_exc()}")
            return ErrorScreen()


if __name__ == "__main__":
    AcademicWordEditorApp().run()
