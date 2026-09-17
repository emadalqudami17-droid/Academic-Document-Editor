# screens/documents_list.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp

from utils.constants import (
    MSG_DOCUMENTS_TITLE, MSG_NO_DOCUMENTS, MSG_NO_DOCUMENTS_HINT,
    MSG_DELETE, MSG_DELETE_CONFIRM, MSG_CANCEL, MSG_YES,
    COLOR_PRIMARY, COLOR_BG, COLOR_SURFACE,
    COLOR_TEXT, COLOR_TEXT_LIGHT, COLOR_TEXT_MUTED,
    COLOR_DANGER, COLOR_SECONDARY,
)
from document.manager import DocumentManager


# =====================================================
# Document Row
# =====================================================
class DocumentRow(Button):
    """A single document row."""

    def __init__(self, doc_data, on_open=None, on_delete=None, **kwargs):
        super().__init__(**kwargs)
        self.doc_data = doc_data
        self._on_open_cb = on_open
        self._on_delete_cb = on_delete

        self.size_hint_y = None
        self.height = dp(90)
        self.background_normal = ""
        self.background_down = ""
        self.background_color = COLOR_SURFACE

        # Row layout
        row = BoxLayout(
            orientation="horizontal",
            padding=[dp(16), dp(10)],
            spacing=dp(10),
        )

        # Info column (title + date)
        info = BoxLayout(orientation="vertical", spacing=dp(4))

        title = Label(
            text=doc_data.get("title", "Untitled"),
            font_size="17sp",
            bold=True,
            color=COLOR_TEXT,
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=dp(28),
        )
        title.bind(size=title.setter("text_size"))

        subtitle = Label(
            text=self._format_subtitle(doc_data),
            font_size="13sp",
            color=COLOR_TEXT_MUTED,
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=dp(22),
        )
        subtitle.bind(size=subtitle.setter("text_size"))

        info.add_widget(title)
        info.add_widget(subtitle)

        # Delete button (X)
        btn_delete = Button(
            text="X",
            font_size="18sp",
            bold=True,
            size_hint=(None, 1),
            width=dp(50),
            background_normal="",
            background_color=COLOR_DANGER,
            color=(1, 1, 1, 1),
        )
        btn_delete.bind(on_release=self._on_delete_pressed)

        row.add_widget(info)
        row.add_widget(btn_delete)

        self.add_widget(row)

        # Make the row clickable
        self.bind(on_release=self._on_row_pressed)

    def _format_subtitle(self, d):
        updated = d.get("updated", "")
        if updated and "T" in updated:
            date_part = updated.split("T")[0]
            time_part = updated.split("T")[1][:5]
            return f"Updated: {date_part} {time_part}"
        return "No date"

    def _on_row_pressed(self, *args):
        if self._on_open_cb:
            self._on_open_cb(self.doc_data.get("id"))

    def _on_delete_pressed(self, *args):
        if self._on_delete_cb:
            self._on_delete_cb(self.doc_data)


# =====================================================
# Documents List Screen
# =====================================================
class DocumentsListScreen(Screen):
    """Shows saved documents."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "documents"

        root = BoxLayout(orientation="vertical", spacing=0)

        # Background
        with root.canvas.before:
            Color(*COLOR_BG)
            self.bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(
            pos=lambda *_: setattr(self.bg, "pos", root.pos),
            size=lambda *_: setattr(self.bg, "size", root.size),
        )

        # === Top Bar ===
        top_bar = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(60),
            padding=[dp(8), 0],
            spacing=dp(8),
        )

        with top_bar.canvas.before:
            Color(*COLOR_PRIMARY)
            self.tb_bg = Rectangle(pos=top_bar.pos, size=top_bar.size)
        top_bar.bind(
            pos=lambda *_: setattr(self.tb_bg, "pos", top_bar.pos),
            size=lambda *_: setattr(self.tb_bg, "size", top_bar.size),
        )

        btn_back = Button(
            text="<",
            font_size="24sp",
            size_hint=(None, 1),
            width=dp(50),
            background_normal="",
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1),
        )
        btn_back.bind(on_release=self._on_back)

        title = Label(
            text=MSG_DOCUMENTS_TITLE,
            font_size="18sp",
            color=(1, 1, 1, 1),
            halign="center",
            valign="middle",
        )
        title.bind(size=title.setter("text_size"))

        # Spacer (same size as back button) for balance
        spacer = Label(size_hint=(None, 1), width=dp(50))

        top_bar.add_widget(btn_back)
        top_bar.add_widget(title)
        top_bar.add_widget(spacer)

        root.add_widget(top_bar)

        # === Scrollable list ===
        self.scroll = ScrollView()
        self.list_layout = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(6),
            padding=[dp(10), dp(10)],
        )
        self.list_layout.bind(
            minimum_height=self.list_layout.setter("height")
        )
        self.scroll.add_widget(self.list_layout)
        root.add_widget(self.scroll)

        # === Empty state ===
        self.empty_state = BoxLayout(
            orientation="vertical",
            padding=[dp(30), dp(50)],
            spacing=dp(10),
        )

        empty_title = Label(
            text=MSG_NO_DOCUMENTS,
            font_size="20sp",
            bold=True,
            color=COLOR_TEXT_MUTED,
            size_hint_y=None,
            height=dp(40),
        )

        empty_hint = Label(
            text=MSG_NO_DOCUMENTS_HINT,
            font_size="14sp",
            color=COLOR_TEXT_MUTED,
            size_hint_y=None,
            height=dp(30),
        )

        self.empty_state.add_widget(Label())  # filler
        self.empty_state.add_widget(empty_title)
        self.empty_state.add_widget(empty_hint)
        self.empty_state.add_widget(Label())  # filler

        root.add_widget(self.empty_state)

        self.add_widget(root)

    # =====================================================
    # Refresh
    # =====================================================
    def on_enter(self, *args):
        """Called when screen becomes visible."""
        self.refresh()

    def on_pre_enter(self, *args):
        """Called before screen becomes visible."""
        self.refresh()

    def refresh(self):
        """Reload the documents list."""
        print("[DOCS] Refreshing list")

        # Clear
        self.list_layout.clear_widgets()

        # Get documents
        docs = DocumentManager.list_all()
        print(f"[DOCS] Found {len(docs)} document(s)")

        if not docs:
            # Show empty state
            self.scroll.opacity = 0
            self.scroll.disabled = True
            self.empty_state.opacity = 1
            self.empty_state.disabled = False
            return

        # Show list
        self.scroll.opacity = 1
        self.scroll.disabled = False
        self.empty_state.opacity = 0
        self.empty_state.disabled = True

        for doc in docs:
            row = DocumentRow(
                doc_data=doc,
                on_open=self._open_doc,
                on_delete=self._confirm_delete,
            )
            self.list_layout.add_widget(row)

    # =====================================================
    # Actions
    # =====================================================
    def _on_back(self, *args):
        print("[DOCS] Back")
        self.manager.current = "home"

    def _open_doc(self, doc_id):
        print(f"[DOCS] Open: {doc_id}")
        editor = self.manager.get_screen("editor")
        editor.open_document(doc_id)
        self.manager.current = "editor"

    def _confirm_delete(self, doc_data):
        """Show confirmation popup before delete."""
        doc_id = doc_data.get("id")
        title = doc_data.get("title", "Untitled")

        content = BoxLayout(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(16),
        )

        content.add_widget(Label(
            text=f"{MSG_DELETE_CONFIRM}\n\n[{title}]",
            halign="center",
        ))

        buttons = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(50),
            spacing=dp(10),
        )

        btn_no = Button(
            text=MSG_CANCEL,
            background_color=COLOR_SECONDARY,
            background_normal="",
        )

        btn_yes = Button(
            text=MSG_YES,
            background_color=COLOR_DANGER,
            background_normal="",
        )

        buttons.add_widget(btn_no)
        buttons.add_widget(btn_yes)
        content.add_widget(buttons)

        popup = Popup(
            title=MSG_DELETE,
            content=content,
            size_hint=(0.85, 0.4),
            auto_dismiss=False,
        )

        btn_no.bind(on_release=popup.dismiss)
        btn_yes.bind(
            on_release=lambda *_: self._delete_doc(doc_id, popup)
        )

        popup.open()

    def _delete_doc(self, doc_id, popup):
        """Actually delete the document."""
        popup.dismiss()
        ok = DocumentManager.delete(doc_id)
        if ok:
            print(f"[DOCS] Deleted: {doc_id}")
            self.refresh()
        else:
            print(f"[DOCS] Delete failed: {doc_id}")
