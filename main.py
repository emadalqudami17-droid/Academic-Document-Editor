# main.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.core.window import Window

from utils.constants import (
    APP_NAME, COLOR_BG, SCREEN_HOME, SCREEN_EDITOR,
)
from screens.home import HomeScreen
from screens.editor import EditorScreen


class AcademicWordEditorApp(App):
    """Main application."""

    def build(self):
        self.title = APP_NAME
        Window.clearcolor = COLOR_BG

        # Screen Manager
        sm = ScreenManager(transition=SlideTransition(duration=0.2))

        sm.add_widget(HomeScreen(name=SCREEN_HOME))
        sm.add_widget(EditorScreen(name=SCREEN_EDITOR))

        sm.current = SCREEN_HOME

        return sm


if __name__ == "__main__":
    AcademicWordEditorApp().run()
