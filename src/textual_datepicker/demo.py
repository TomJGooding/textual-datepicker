from textual.app import App, ComposeResult

from textual_datepicker.datepicker import DatePicker


class DatePickerDemo(App):
    CSS = """
    Screen {
        align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        yield DatePicker()

    def on_mount(self) -> None:
        self.query_one(DatePicker).focus()


if __name__ == "__main__":
    app = DatePickerDemo()
    app.run()
