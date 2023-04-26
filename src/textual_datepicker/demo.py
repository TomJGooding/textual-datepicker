from textual.app import App, ComposeResult
from textual.widgets import Footer

from textual_datepicker.datepicker import DateInput, DatePicker


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
        yield DateInput()
        yield DatePicker()
        yield Footer()


if __name__ == "__main__":
    app = DatePickerDemo()
    app.run()
