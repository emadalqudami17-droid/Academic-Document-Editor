# main.py
from kivy.app import App
from kivy.uix.label import Label
from kivy.core.text import LabelBase
from kivy.core.window import Window

# STEP 1: Register font at module level (not inside build)
try:
    LabelBase.register(
        name="NotoNaskh",
        fn_regular="assets/fonts/NotoNaskhArabic-Regular.ttf",
    )
    print("[FONT] Registered OK")
    FONT_OK = True
except Exception as e:
    print(f"[FONT] FAILED: {e}")
    FONT_OK = False

# STEP 2: Import constants
try:
    from utils.constants import FONT_ARABIC, COLOR_BG
    print("[CONSTANTS] Loaded OK")
    CONSTANTS_OK = True
except Exception as e:
    print(f"[CONSTANTS] FAILED: {e}")
    CONSTANTS_OK = False

# STEP 3: Import home screen
try:
    from screens.home import HomeScreen
    print("[HOME] Imported OK")
    HOME_OK = True
except Exception as e:
    print(f"[HOME] FAILED: {e}")
    HOME_OK = False


class DiagnosticApp(App):

    def build(self):
        Window.clearcolor = (1, 1, 1, 1)

        # Show status of each component
        text = f"Font: {FONT_OK}\nConstants: {CONSTANTS_OK}\nHome: {HOME_OK}"

        if not FONT_OK:
            # Fallback: no font
            return Label(
                text=f"ERROR:\n{text}",
                font_size="20sp",
                color=(1, 0, 0, 1),
            )

        # Try Arabic text with registered font
        return Label(
            text=f"مرحبا\n\n{text}",
            font_name="NotoNaskh",
            font_size="24sp",
            color=(0, 0, 0, 1),
        )


if __name__ == "__main__":
    DiagnosticApp().run()
