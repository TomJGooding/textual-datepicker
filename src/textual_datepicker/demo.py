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

    def on_mount(self) -> None:
        self.query_one(DatePicker).styles.visibility = "hidden"

    def on_date_picker_changed(self, event: DatePicker.Changed) -> None:
        self.query_one(DateInput).value = event.value

    def on_date_input_changed(self, event: DateInput.Changed) -> None:
        self.query_one(DatePicker).value = event.value

    def on_button_pressed(self) -> None:
        datepicker = self.query_one(DatePicker)
        datepicker.styles.visibility = "visible"
        datepicker.focus()


if __name__ == "__main__":
    app = DatePickerDemo()
    app.run()
