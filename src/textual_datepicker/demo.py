from textual.app import App, ComposeResult
from textual.widgets import Footer

from textual_datepicker.datepicker import DatePicker


class DatePickerDemo(App):
    CSS = """
    Screen {
        align: center middle;
    }
    """
    BINDINGS = [
        ("ctrl+t", "app.toggle_dark", "Toggle Dark mode"),
    ]

    def compose(self) -> ComposeResult:
        yield DatePicker()
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(DatePicker).focus()


if __name__ == "__main__":
    app = DatePickerDemo()
    app.run()
