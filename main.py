# main.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.core.window import Window

from utils.constants import (
    APP_NAME, SCREEN_HOME, SCREEN_EDITOR,
    COLOR_BG,
)
from screens.home import HomeScreen


class HomeScreenWrapper(Screen):
    """Wrapper to make HomeScreen compatible with ScreenManager."""

    def __init__(self, app_ref=None, **kwargs):
        super().__init__(**kwargs)
        self.app_ref = app_ref
        self.add_widget(HomeScreen(
            on_new_doc=self._new_doc,
            on_open_doc=self._open_doc,
            on_settings=self._settings,
        ))

    def _new_doc(self):
        if self.app_ref:
            self.app_ref.go_to_editor()

    def _open_doc(self):
        if self.app_ref:
            self.app_ref.show_message("Open document - coming soon")

    def _settings(self):
        if self.app_ref:
            self.app_ref.show_message("Settings - coming soon")


class AcademicWordEditorApp(App):
    """Main application class."""

    def build(self):
        self.title = APP_NAME
        Window.clearcolor = COLOR_BG

        # Screen manager
        self.sm = ScreenManager(transition=SlideTransition())
        self.sm.add_widget(HomeScreenWrapper(
            app_ref=self,
            name=SCREEN_HOME,
        ))

        return self.sm

    def go_to_editor(self):
        """Navigate to editor screen."""
        self.show_message("Editor screen - next step")

    def go_to_home(self):
        """Navigate to home screen."""
        self.sm.current = SCREEN_HOME

    def show_message(self, text):
        """Display a toast message."""
        try:
            from kivy.uix.label import Label
            from kivy.clock import Clock
            from kivy.uix.floatlayout import FloatLayout
            from kivy.graphics import Color, RoundedRectangle

            overlay = FloatLayout()
            lbl = Label(
                text=text,
                font_size="15sp",
                color=(1, 1, 1, 1),
                size_hint=(None, None),
                size=(300, 60),
                pos_hint={"center_x": 0.5, "center_y": 0.15},
            )
            with lbl.canvas.before:
                Color(0.15, 0.15, 0.15, 0.9)
                RoundedRectangle(
                    pos=lbl.pos, size=lbl.size, radius=[15]
                )
            lbl.bind(
                pos=lambda w, v: setattr(
                    w.canvas.before.children[-1], 'pos', v
                )
            )

            Window.add_widget(overlay)
            overlay.add_widget(lbl)

            def remove_overlay(dt):
                Window.remove_widget(overlay)

            Clock.schedule_once(remove_overlay, 2.0)
        except Exception as e:
            print(f"Toast error: {e}")


if __name__ == "__main__":
    AcademicWordEditorApp().run()
