#!/usr/bin/env python3
"""Analog clock rendered in the terminal, driven by the system clock.

Run with:  python3 analog_clock.py
Quit with: q or Ctrl-C
"""

import curses
import math
import time
from datetime import datetime
from zoneinfo import ZoneInfo

# Terminal character cells are roughly twice as tall as they are wide,
# so vertical distances are scaled down by this factor to keep the
# clock face looking circular instead of egg-shaped.
Y_ASPECT = 0.5

TIME_ZONE = ZoneInfo("America/New_York")


def polar_to_screen(cy, cx, length, angle_deg):
    """Convert a clock-face angle (0 = 12 o'clock, clockwise) to a
    terminal (row, col) coordinate relative to the given center."""
    rad = math.radians(angle_deg - 90)
    x = math.cos(rad) * length
    y = math.sin(rad) * length
    return cy + int(round(y * Y_ASPECT)), cx + int(round(x))


def draw_line(win, y0, x0, y1, x1, ch):
    """Bresenham line drawing, clipped to the window bounds."""
    max_y, max_x = win.getmaxyx()
    dy = abs(y1 - y0)
    dx = abs(x1 - x0)
    sy = 1 if y0 < y1 else -1
    sx = 1 if x0 < x1 else -1
    err = dx - dy
    y, x = y0, x0
    while True:
        if 0 <= y < max_y - 1 and 0 <= x < max_x:
            try:
                win.addch(y, x, ch)
            except curses.error:
                pass
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
            try:
                win.addstr(ly, lx, label)
            except curses.error:
                pass
        else:
            try:
                win.addch(y, x, ch)
            except curses.error:
                pass

    steps = 120
    for i in range(steps):
        angle = i * (360 / steps)
        y, x = polar_to_screen(cy, cx, radius, angle)
        try:
            win.addch(y, x, ".")
        except curses.error:
            pass


def render(win):
    now = datetime.now(TIME_ZONE)
    hour, minute, second = now.hour % 12, now.minute, now.second

    max_y, max_x = win.getmaxyx()
    cy, cx = max_y // 2 - 1, max_x // 2
    radius = max(5, min((max_y - 6) // 2, (max_x - 4) // 2) - 1)

    win.erase()
    win.border()

    draw_face(win, cy, cx, radius)

    hour_angle = (hour + minute / 60) * 30
    minute_angle = (minute + second / 60) * 6
    second_angle = second * 6

    hy, hx = polar_to_screen(cy, cx, radius * 0.5, hour_angle)
    my, mx = polar_to_screen(cy, cx, radius * 0.8, minute_angle)
    sy, sx = polar_to_screen(cy, cx, radius * 0.9, second_angle)

    draw_line(win, cy, cx, my, mx, "|" if abs(mx - cx) < abs(my - cy) else "-")
    draw_line(win, cy, cx, hy, hx, "#")
    draw_line(win, cy, cx, sy, sx, "o")

    try:
        win.addch(cy, cx, "+")
    except curses.error:
        pass

    digital = now.strftime("%H:%M:%S")
    try:
        win.addstr(max_y - 2, max(1, cx - len(digital) // 2), digital, curses.A_BOLD)
    except curses.error:
        pass

    win.refresh()


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(0)

    while True:
        render(stdscr)

        start = time.time()
        while time.time() - start < 1.0:
            key = stdscr.getch()
            if key in (ord("q"), ord("Q")):
                return
            time.sleep(0.02)


if __name__ == "__main__":
    curses.wrapper(main)
