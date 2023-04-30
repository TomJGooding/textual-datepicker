from __future__ import annotations

import calendar
import datetime
from typing import Optional

from dateutil.relativedelta import relativedelta
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.coordinate import Coordinate
from textual.message import Message
from textual.reactive import reactive
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

    value = reactive(datetime.date.today(), init=False)

    class Changed(Message, bubble=True):
        def __init__(self, datepicker: DatePicker, value: datetime.date) -> None:
            super().__init__()
            self.value: datetime.date = value
            self.datepicker: DatePicker = datepicker

        @property
        def control(self) -> DatePicker:
            return self.datepicker

    def __init__(
        self,
        value: datetime.date = datetime.date.today(),
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.value = value
        self._month_calendar = self._get_month_calendar()

    def compose(self) -> ComposeResult:
        yield Label(self.value.strftime("%Y"), classes="header", id="subtitle")
        yield Label(self.value.strftime("%a, %b %d"), classes="header", id="title")

        with Horizontal(id="date-navigation"):
            yield Button("←", classes="left-arrow-btn", id="prev-month-btn")
            yield Button(self.value.strftime("%B"), id="month", disabled=True)
            yield Button("→", classes="right-arrow-btn", id="next-month-btn")

            yield Button("←", classes="left-arrow-btn", id="prev-year-btn")
            yield Button(self.value.strftime("%Y"), id="year", disabled=True)
            yield Button("→", classes="right-arrow-btn", id="next-year-btn")

        yield DataTable(id="calendar-days-table")

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*list(calendar.day_abbr))
        self._update_calendar_days_table()
        self._set_highlighted_day()

    def watch_value(
        self,
        old_value: datetime.date,
        new_value: datetime.date,
    ) -> None:
        if old_value.year != new_value.year or old_value.month != new_value.month:
            self._month_calendar = self._get_month_calendar()
            self._update_calendar_days_table()
            if old_value.year != new_value.year:
                self.query_one("#subtitle", Label).update(self.value.strftime("%Y"))
                self.query_one("#year", Button).label = self.value.strftime("%Y")
            if old_value.month != new_value.month:
                self.query_one("#month", Button).label = self.value.strftime("%B")

        self.value = new_value
        self.query_one("#title", Label).update(self.value.strftime("%a, %b %d"))
        self._set_highlighted_day()
        self.post_message(self.Changed(self, self.value))

    def _get_month_calendar(self) -> list[list[int | None]]:
        month_calendar = [
            [day if day != 0 else None for day in week]
            for week in calendar.monthcalendar(self.value.year, self.value.month)
        ]

        return month_calendar

    def _update_calendar_days_table(self) -> None:
        table = self.query_one("#calendar-days-table", DataTable)
        table.clear()
        table.add_rows(self._month_calendar)

    def _set_highlighted_day(self) -> None:
        table = self.query_one("#calendar-days-table", DataTable)
        day = self.value.day
        for row, week in enumerate(self._month_calendar):
            try:
                column = week.index(day)
            except ValueError:
                pass
            else:
                table.cursor_coordinate = Coordinate(row, column)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "prev-month-btn":
            new_date = self.value - relativedelta(months=1)
        elif event.button.id == "next-month-btn":
            new_date = self.value + relativedelta(months=1)
        elif event.button.id == "prev-year-btn":
            new_date = self.value - relativedelta(years=1)
        elif event.button.id == "next-year-btn":
            new_date = self.value + relativedelta(years=1)
        else:
            return

        self.value = new_date

    def on_data_table_cell_selected(self, event: DataTable.CellSelected) -> None:
        if isinstance(event.value, int):
            old_value = self.value
            self.value = old_value.replace(day=event.value)


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

    value = reactive[Optional[datetime.date]](None, init=False)

    class Changed(Message, bubble=True):
        def __init__(
            self, dateinput: DateInput, value: Optional[datetime.date]
        ) -> None:
            super().__init__()
            self.value: Optional[datetime.date] = value
            self.dateinput: DateInput = dateinput

        @property
        def control(self) -> DateInput:
            return self.dateinput

    def __init__(
        self,
        value: datetime.date | None = None,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.value = value

    def compose(self) -> ComposeResult:
        with Horizontal(id="date-input-container"):
            input_value = "" if not self.value else self.value
            yield Input(f"{input_value}", placeholder="Date", id="date-input-field")
            yield Button("\u2637", id="date-input-btn")

    def watch_value(self) -> None:
        self.query_one(Input).value = f"{self.value}"
        self.post_message(self.Changed(self, self.value))

    def on_input_submitted(self, event: Input.Submitted) -> None:
        try:
            new_value = datetime.datetime.strptime(event.value, "%Y-%m-%d").date()
        except ValueError:
            self.app.bell()
        else:
            self.value = new_value
