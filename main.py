# main.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.core.window import Window

from utils.constants import (
    APP_NAME, COLOR_BG,
    SCREEN_HOME, SCREEN_EDITOR, SCREEN_DOCUMENTS,
)
from screens.home import HomeScreen
from screens.editor import EditorScreen
from screens.documents_list import DocumentsListScreen


class AcademicWordEditorApp(App):
    """Main application."""

    def build(self):
        self.title = APP_NAME
        Window.clearcolor = COLOR_BG

        # Screen Manager with slide transition
        sm = ScreenManager(transition=SlideTransition(duration=0.2))

        # Register all screens
        sm.add_widget(HomeScreen(name=SCREEN_HOME))
        sm.add_widget(EditorScreen(name=SCREEN_EDITOR))
        sm.add_widget(DocumentsListScreen(name=SCREEN_DOCUMENTS))

        # Start at home
        sm.current = SCREEN_HOME

        return sm


if __name__ == "__main__":
    AcademicWordEditorApp().run()
