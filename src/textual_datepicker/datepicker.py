import calendar
import datetime

from dateutil.relativedelta import relativedelta
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Button, DataTable, Input


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
        table.add_columns(*list(calendar.day_abbr))
        self._update_month_table()

    def _update_month_table(self) -> None:
        table = self.query_one(DataTable)
        table.clear()
        month_calendar = [
            [day if day != 0 else None for day in week]
            for week in calendar.monthcalendar(self.date.year, self.date.month)
        ]

        table.add_rows(month_calendar)

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
        self._update_month_table()

    def on_data_table_cell_selected(self, event: DataTable.CellSelected) -> None:
        if isinstance(event.value, int):
            self.date = self.date.replace(day=event.value)
            self.query_one(Input).value = self.date.strftime("%F")
