# main.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.core.window import Window

from utils.constants import (
    APP_NAME, SCREEN_HOME, COLOR_BG, FONT_ARABIC,
)
from screens.home import HomeScreen, register_arabic_font


class HomeScreenWrapper(Screen):
    """Wraps HomeScreen for ScreenManager compatibility."""

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
            self.app_ref.show_message("قريبًا")

    def _settings(self):
        if self.app_ref:
            self.app_ref.show_message("قريبًا")


class AcademicWordEditorApp(App):
    """Main application."""

    def build(self):
        self.title = APP_NAME
        Window.clearcolor = COLOR_BG

        # Register Arabic font FIRST
        ok = register_arabic_font()
        print(f"[FONT] Arabic font registered: {ok}")

        self.sm = ScreenManager(transition=SlideTransition())
        self.sm.add_widget(HomeScreenWrapper(
            app_ref=self,
            name=SCREEN_HOME,
        ))

        return self.sm

    def go_to_editor(self):
        self.show_message("المحرر - الخطوة القادمة")

    def go_to_home(self):
        self.sm.current = SCREEN_HOME

    def show_message(self, text):
        """Simple toast message."""
        try:
            from kivy.uix.label import Label
            from kivy.clock import Clock
            from kivy.uix.floatlayout import FloatLayout
            from kivy.graphics import Color, RoundedRectangle
            from kivy.metrics import dp

            overlay = FloatLayout()
            lbl = Label(
                text=text,
                font_name=FONT_ARABIC,
                font_size="18sp",
                color=(1, 1, 1, 1),
                size_hint=(None, None),
                size=(dp(280), dp(65)),
                pos_hint={"center_x": 0.5, "center_y": 0.15},
            )
            with lbl.canvas.before:
                Color(0.15, 0.15, 0.15, 0.92)
                RoundedRectangle(
                    pos=lbl.pos, size=lbl.size, radius=[dp(15)]
                )

            Window.add_widget(overlay)
            overlay.add_widget(lbl)

            def remove_overlay(dt):
                try:
                    Window.remove_widget(overlay)
                except Exception:
                    pass

            Clock.schedule_once(remove_overlay, 2.0)
        except Exception as e:
            print(f"[TOAST ERROR] {e}")


if __name__ == "__main__":
    AcademicWordEditorApp().run()
