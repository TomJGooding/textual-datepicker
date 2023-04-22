import datetime

from dateutil.relativedelta import relativedelta
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Button, DataTable, Input

MONTH = [
    ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"),
    ("1", "2", "3", "4", "5", "6", "7"),
    ("8", "9", "10", "11", "12", "13", "14"),
    ("15", "16", "17", "18", "19", "20", "21"),
    ("22", "23", "24", "25", "26", "27", "28"),
    ("29", "30", "31", "", "", "", ""),
]


class DatePicker(Widget, can_focus=True):
    DEFAULT_CSS = """
    DatePicker {
        height: auto;
        width: auto;
    }

    DatePicker DataTable {
        height: auto;
        width: auto;
    }

    DatePicker Button {
        min-width: 3;
    }

    DatePicker #date-navigation {
        height: 3;
    }

    DatePicker #month {
        min-width: 14;
    }

    DatePicker .left-arrow-btn {
        margin-left: 1;
    }
    """

    date = reactive(datetime.date(2023, 1, 1))

    def compose(self) -> ComposeResult:
        yield Input(self.date.strftime("%F"))

        with Horizontal(id="date-navigation"):
            yield Button("←", classes="left-arrow-btn", id="prev-month-btn")
            yield Button(self.date.strftime("%B"), id="month", disabled=True)
            yield Button("→", classes="right-arrow-btn", id="next-month-btn")

            yield Button("←", classes="left-arrow-btn", id="prev-year-btn")
            yield Button(self.date.strftime("%Y"), id="year", disabled=True)
            yield Button("→", classes="right-arrow-btn", id="next-year-btn")

        yield DataTable()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*MONTH[0])
        table.add_rows(MONTH[1:])

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "prev-month-btn":
            self.date -= relativedelta(months=1)
        elif event.button.id == "next-month-btn":
            self.date += relativedelta(months=1)
        elif event.button.id == "prev-year-btn":
            self.date -= relativedelta(years=1)
        elif event.button.id == "next-year-btn":
            self.date += relativedelta(years=1)

        self.query_one(Input).value = self.date.strftime("%F")
        self.query_one("#month", Button).label = self.date.strftime("%B")
        self.query_one("#year", Button).label = self.date.strftime("%Y")
