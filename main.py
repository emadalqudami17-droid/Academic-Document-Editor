from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window


class AcademicWordEditorApp(App):

    def build(self):
        self.title = "Academic Word Editor"

        Window.clearcolor = (0.96, 0.97, 0.98, 1)

        root = BoxLayout(
            orientation="vertical",
            padding=30,
            spacing=20
        )

        title = Label(
            text="Academic Word Editor",
            font_size="28sp",
            bold=True,
            size_hint_y=None,
            height=60,
            color=(0.12, 0.20, 0.35, 1)
        )

        subtitle = Label(
            text="Professional Academic Document Editor",
            font_size="17sp",
            size_hint_y=None,
            height=50,
            color=(0.25, 0.35, 0.45, 1)
        )

        new_button = Button(
            text="New Document",
            font_size="18sp",
            size_hint_y=None,
            height=55
        )

        open_button = Button(
            text="Open Document",
            font_size="18sp",
            size_hint_y=None,
            height=55
        )

        root.add_widget(title)
        root.add_widget(subtitle)
        root.add_widget(new_button)
        root.add_widget(open_button)

        return root


if __name__ == "__main__":
    AcademicWordEditorApp().run()
