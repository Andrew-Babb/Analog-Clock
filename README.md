# Terminal Analog Clock

A Python terminal analog clock rendered with `curses`. The clock draws a live analog face, hour/minute/second hands, and a digital time display at the bottom of the terminal.

## Requirements

- Python 3
- A terminal that supports `curses`

No third-party Python packages are required.

## Run

From this project directory:

```bash
python3 analog_clock.py
```

## Controls

- `q` or `Q`: quit the clock
- `Ctrl-C`: force quit from the terminal

## Timezone

The program currently applies a fixed East Coast USA offset:

```python
TZ_OFFSET = timedelta(hours=-4)
```

This means the displayed time is calculated from the system clock plus a `-4` hour offset. To use your local system time directly, change that line in `analog_clock.py` to:

```python
TZ_OFFSET = timedelta(hours=0)
```

## How It Works

- `curses` manages the full-screen terminal display.
- `polar_to_screen()` converts clock angles into terminal row/column positions.
- `draw_face()` renders the hour markers and circular face.
- `draw_line()` draws the clock hands using Bresenham line drawing.
- `render()` refreshes the clock once per second using the current time.

## Notes

The clock scales to the current terminal size. If the display looks cramped, enlarge the terminal window and run the program again.
