#!/usr/bin/env python3
"""Analog clock rendered in the terminal, driven by the system clock.

Run with:  python3 analog_clock.py
Quit with: q or Ctrl-C
"""

import argparse
import curses
import math
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo
from zoneinfo import ZoneInfoNotFoundError

# Terminal character cells are roughly twice as tall as they are wide,
# so vertical distances are scaled down by this factor to keep the
# clock face looking circular instead of egg-shaped.
Y_ASPECT = 0.5

VERSION = "1.3"
DEFAULT_TIMEZONE = "America/New_York"
DEFAULT_REFRESH_RATE = 1.0
MIN_RADIUS = 5


@dataclass(frozen=True)
class ClockConfig:
    timezone: ZoneInfo
    refresh_rate: float
    radius: Optional[int]
    show_seconds: bool
    show_digital: bool
    show_border: bool
    time_format: str


def positive_float(value):
    try:
        parsed = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a number") from exc
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be greater than 0")
    return parsed


def valid_radius(value):
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc

    if parsed < MIN_RADIUS:
        raise argparse.ArgumentTypeError(
            f"must be at least {MIN_RADIUS}"
        )

    return parsed


def valid_timezone(value):
    try:
        return ZoneInfo(value)
    except ZoneInfoNotFoundError as exc:
        raise argparse.ArgumentTypeError(f"unknown timezone: {value}") from exc


def parse_args():
    parser = argparse.ArgumentParser(
        description="Render an analog clock in the terminal."
    )
    parser.add_argument(
        "-z",
        "--timezone",
        type=valid_timezone,
        default=ZoneInfo(DEFAULT_TIMEZONE),
        metavar="IANA_NAME",
        help=f"timezone to display, such as America/Chicago (default: {DEFAULT_TIMEZONE})",
    )
    parser.add_argument(
        "-r",
        "--refresh-rate",
        type=positive_float,
        default=DEFAULT_REFRESH_RATE,
        metavar="SECONDS",
        help=f"seconds between redraws (default: {DEFAULT_REFRESH_RATE:g})",
    )
    parser.add_argument(
        "--radius",
        type=valid_radius,
        metavar="CELLS",
        help=(
            "clock radius in terminal columns "
            f"(minimum: {MIN_RADIUS}; default: fit to terminal)"
        ),
    )
    parser.add_argument(
        "--no-seconds",
        action="store_true",
        help="hide seconds from the analog and digital displays",
    )
    parser.add_argument(
        "--no-digital",
        action="store_true",
        help="hide the digital time readout",
    )
    parser.add_argument(
        "--no-border",
        action="store_true",
        help="hide the terminal border",
    )
    parser.add_argument(
        "--format",
        choices=("12", "24"),
        default="24",
        help="digital clock format (default: 24)",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"Analog Clock {VERSION}",
    )
    args = parser.parse_args()

    return ClockConfig(
        timezone=args.timezone,
        refresh_rate=args.refresh_rate,
        radius=args.radius,
        show_seconds=not args.no_seconds,
        show_digital=not args.no_digital,
        show_border=not args.no_border,
        time_format=args.format,
    )


def polar_to_screen(cy, cx, length, angle_deg):
    """Convert a clock-face angle (0 = 12 o'clock, clockwise) to a
    terminal (row, col) coordinate relative to the given center."""
    rad = math.radians(angle_deg - 90)
    x = math.cos(rad) * length
    y = math.sin(rad) * length
    return cy + int(round(y * Y_ASPECT)), cx + int(round(x))


def safe_addch(win, y, x, ch, attr=0):
    """Draw one character only when the target cell is valid."""
    max_y, max_x = win.getmaxyx()

    if not (0 <= y < max_y and 0 <= x < max_x):
        return

    try:
        win.addch(y, x, ch, attr)
    except curses.error:
        pass


def safe_addstr(win, y, x, text, attr=0):
    """Draw the portion of a string that fits inside the window."""
    max_y, max_x = win.getmaxyx()

    if not (0 <= y < max_y and 0 <= x < max_x):
        return

    visible_text = text[: max_x - x]

    if not visible_text:
        return

    try:
        win.addstr(y, x, visible_text, attr)
    except curses.error:
        pass


def draw_line(win, y0, x0, y1, x1, ch):
    """Bresenham line drawing, clipped to the window bounds."""
    dy = abs(y1 - y0)
    dx = abs(x1 - x0)
    sy = 1 if y0 < y1 else -1
    sx = 1 if x0 < x1 else -1
    err = dx - dy
    y, x = y0, x0
    while True:
        safe_addch(win, y, x, ch)
        if y == y1 and x == x1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy


def draw_face(win, cy, cx, radius):
    for hour in range(12):
        angle = hour * 30
        y, x = polar_to_screen(cy, cx, radius, angle)
        label = "12" if hour == 0 else str(hour)
        ch = "#" if hour % 3 == 0 else "*"

        if hour % 3 == 0:
            ly = y
            lx = x - (len(label) // 2)
            safe_addstr(win, ly, lx, label)
        else:
            safe_addch(win, y, x, ch)

    steps = 120
    for i in range(steps):
        angle = i * (360 / steps)
        y, x = polar_to_screen(cy, cx, radius, angle)
        safe_addch(win, y, x, ".")


def maximum_fitted_radius(
        max_y,
        max_x,
        show_border,
        show_digital,
    ):
        """Return the largest radius that fits inside the current layout."""
        left_edge = 1 if show_border else 0
        right_edge = max_x - 2 if show_border else max_x - 1
        top_edge = 1 if show_border else 0

        if show_digital:
            bottom_edge = max_y - 3
        elif show_border:
            bottom_edge = max_y - 2
        else:
            bottom_edge = max_y - 1

        cy = max_y // 2 - 1
        cx = max_x // 2

        horizontal_space = min(
            cx - left_edge,
            right_edge - cx,
        )
        vertical_space = min(
            cy - top_edge,
            bottom_edge - cy,
        )

        vertical_radius = int(vertical_space / Y_ASPECT)

        return min(horizontal_space, vertical_radius)


def draw_too_small(win):
    """Display a message when the minimum clock cannot fit."""
    max_y, max_x = win.getmaxyx()
    message = "Terminal too small"

    y = max_y // 2
    x = max(0, (max_x - len(message)) // 2)

    safe_addstr(
        win,
        y,
        x,
        message,
        curses.A_BOLD,
    )
    win.refresh()


def digital_time(now, time_format, show_seconds):
    if time_format == "12":
        pattern = "%I:%M:%S %p" if show_seconds else "%I:%M %p"
        return now.strftime(pattern).lstrip("0")

    pattern = "%H:%M:%S" if show_seconds else "%H:%M"
    return now.strftime(pattern)

def render(win, config):
    now = datetime.now(config.timezone)
    hour, minute, second = now.hour % 12, now.minute, now.second

    max_y, max_x = win.getmaxyx()
    cy, cx = max_y // 2 - 1, max_x // 2

    available_radius = maximum_fitted_radius(
        max_y,
        max_x,
        config.show_border,
        config.show_digital,
    )

    win.erase()

    if available_radius < MIN_RADIUS:
        draw_too_small(win)
        return

    if config.radius is None:
        radius = available_radius
    else:
        radius = min(config.radius, available_radius)

    if config.show_border:
        win.border()

    draw_face(win, cy, cx, radius)

    hour_angle = (hour + minute / 60) * 30
    minute_angle = (minute + second / 60) * 6

    hy, hx = polar_to_screen(cy, cx, radius * 0.5, hour_angle)
    my, mx = polar_to_screen(cy, cx, radius * 0.8, minute_angle)

    draw_line(win, cy, cx, my, mx, "|" if abs(mx - cx) < abs(my - cy) else "-")
    draw_line(win, cy, cx, hy, hx, "#")
    if config.show_seconds:
        second_angle = second * 6
        sy, sx = polar_to_screen(cy, cx, radius * 0.9, second_angle)
        draw_line(win, cy, cx, sy, sx, "o")

    safe_addch(win, cy, cx, "+")

    if config.show_digital:
        digital = digital_time(
            now,
            config.time_format,
            config.show_seconds,
        )
        safe_addstr(
            win,
            max_y - 2,
            max(1, cx - len(digital) // 2),
            digital,
            curses.A_BOLD,
        )

    win.refresh()


def main(stdscr, config):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(0)

    while True:
        render(stdscr, config)

        deadline = time.monotonic() + config.refresh_rate
        while time.monotonic() < deadline:
            key = stdscr.getch()
            if key in (ord("q"), ord("Q")):
                return
            if key == curses.KEY_RESIZE:
                break
            remaining = deadline - time.monotonic()
            if remaining > 0:
                time.sleep(min(0.02, remaining))


if __name__ == "__main__":
    curses.wrapper(main, parse_args())
