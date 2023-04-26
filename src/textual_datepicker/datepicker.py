import calendar
import datetime

from dateutil.relativedelta import relativedelta
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.coordinate import Coordinate
from textual.widget import Widget
from textual.widgets import Button, DataTable, Input, Label


class DatePicker(Widget, can_focus=True):
    DEFAULT_CSS = """
    DatePicker {
        height: auto;
        width: auto;
        border: round $panel-lighten-2;
    }

    DatePicker:focus {
        border: round $accent;
    }

    DatePicker > .header {
        width: 100%;
        background: $primary;
        color: $text;
    }

    DatePicker #title {
        text-style: bold;
        padding-left: 1;
        padding-bottom: 1;
    }

    DatePicker #subtitle {
        padding-left: 1;
        padding-top: 1;
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

    DatePicker #calendar-days-table {
        height: auto;
        width: auto;
        min-height: 7;
    }

    DatePicker #calendar-days-table .datatable--header {
        background: $surface;
        color: $text-disabled;
    }

    DatePicker #calendar-days-table .datatable--header-cursor {
        background: $surface;
        color: $text-disabled;
    }

    DatePicker #calendar-days-table .datatable--header-hover {
        background: $surface;
        color: $text-disabled;
    }
    """

    def __init__(
        self,
        date: datetime.date = datetime.date.today(),
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.date = date
        self._month_calendar = self._get_month_calendar()

    def compose(self) -> ComposeResult:
        yield Label(self.date.strftime("%Y"), classes="header", id="subtitle")
        yield Label(self.date.strftime("%a, %b %d"), classes="header", id="title")

        with Horizontal(id="date-navigation"):
            yield Button("←", classes="left-arrow-btn", id="prev-month-btn")
            yield Button(self.date.strftime("%B"), id="month", disabled=True)
            yield Button("→", classes="right-arrow-btn", id="next-month-btn")

            yield Button("←", classes="left-arrow-btn", id="prev-year-btn")
            yield Button(self.date.strftime("%Y"), id="year", disabled=True)
            yield Button("→", classes="right-arrow-btn", id="next-year-btn")

        yield DataTable(id="calendar-days-table")

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*list(calendar.day_abbr))
        self._update_calendar_days_table()
        self._set_highlighted_day()

    def update(self, date: datetime.date) -> None:
        old_date = self.date
        self.date = date

        if old_date.year != self.date.year or old_date.month != self.date.month:
            self._month_calendar = self._get_month_calendar()
            self._update_calendar_days_table()
            if old_date.year != self.date.year:
                self.query_one("#subtitle", Label).update(self.date.strftime("%Y"))
                self.query_one("#year", Button).label = self.date.strftime("%Y")
            if old_date.month != self.date.month:
                self.query_one("#month", Button).label = self.date.strftime("%B")

        self.query_one("#title", Label).update(self.date.strftime("%a, %b %d"))
        self._set_highlighted_day()

    def _get_month_calendar(self) -> list[list[int | None]]:
        month_calendar = [
            [day if day != 0 else None for day in week]
            for week in calendar.monthcalendar(self.date.year, self.date.month)
        ]

        return month_calendar

    def _update_calendar_days_table(self) -> None:
        table = self.query_one("#calendar-days-table", DataTable)
        table.clear()
        table.add_rows(self._month_calendar)

    def _set_highlighted_day(self) -> None:
        table = self.query_one("#calendar-days-table", DataTable)
        day = self.date.day
        for row, week in enumerate(self._month_calendar):
            try:
                column = week.index(day)
            except ValueError:
                pass
            else:
                table.cursor_coordinate = Coordinate(row, column)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "prev-month-btn":
            new_date = self.date - relativedelta(months=1)
        elif event.button.id == "next-month-btn":
            new_date = self.date + relativedelta(months=1)
        elif event.button.id == "prev-year-btn":
            new_date = self.date - relativedelta(years=1)
        elif event.button.id == "next-year-btn":
            new_date = self.date + relativedelta(years=1)
        else:
            return

        self.update(new_date)

    def on_data_table_cell_selected(self, event: DataTable.CellSelected) -> None:
        if isinstance(event.value, int):
            new_date = self.date.replace(day=event.value)
            self.update(new_date)


class DateInput(Widget):
    DEFAULT_CSS = """
    DateInput {
        height: auto;
        width: auto;
    }

    DateInput #date-input-container {
        height: auto;
        width: auto;
    }

    DateInput #date-input-field {
        width: 20;
    }

    DateInput #date-input-btn {
        max-width: 5;
    }
    """

    def compose(self) -> ComposeResult:
        with Horizontal(id="date-input-container"):
            yield Input(f"{datetime.date.today()}", id="date-input-field")
            yield Button("\u2637", id="date-input-btn")
