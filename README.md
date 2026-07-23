# Analog Clock v1.3

Analog Clock is a terminal-based analog clock rendered with Python's `curses`
module.  It draws an analog clock face, hour, minute, and optional second hands,
along with an optional digital time readout.

Version 1.3 improves terminal resilience and responsiveness.  The clock now
automatically fits the available terminal space, safely limits oversized manual
radius requests, displays a clear message when the terminal is too small, and
redraws immediately when the terminal is resized.  The `--no-seconds` option now
removes seconds from both the analog and digital displays.

## Requirements

- Python 3.9 or newer
- A terminal that supports `curses`

The clock uses Python's standard-library `zoneinfo` module for timezone-aware
local time.

On Windows, two additional packages are required (Linux/macOS already provide
these via the OS):

```bash
pip install windows-curses tzdata
```

## Timezone

By default, the clock displays time for the `America/New_York` timezone. Use
`--timezone` or `-z` with any valid IANA timezone name to display a different
timezone:

```bash
python3 analog_clock.py --timezone America/Chicago
```

This lets Python handle daylight saving time and standard time automatically.

## Run

```bash
python3 analog_clock.py
```

## Options

```text
-z, --timezone IANA_NAME   Timezone to display (default: America/New_York)
-r, --refresh-rate SECONDS Seconds between redraws (default: 1)
--radius CELLS             Clock radius in terminal columns
                           (minimum: 5; default: fit to terminal)
--no-seconds               Hide seconds from the analog and digital displays
--no-digital               Hide the digital time readout
--no-border                Hide the terminal border
--format {12,24}           Digital clock format (default: 24)
--version                  Show the program version
```

Examples:

```bash
python3 analog_clock.py --timezone Europe/London --format 12
python3 analog_clock.py --refresh-rate 0.25 --radius 18 --no-border
python3 analog_clock.py --format 12 --no-seconds
python3 analog_clock.py --no-border --no-digital
```

## Responsive sizing

By default, the clock uses the largest radius that safely fits inside the current terminal window.

A radius supplied with `--radius` is treated as the preferred size.  If the requested radius is larger than the available terminal space, the clock reduces it to the largest size that fits.

The minimum supported radius is 5.  If the terminal cannot fit a clock at that size, the program displays `Terminal too small`.  Enlarging the terminal causes the clock to return automatically.

## Controls

- Press `q` or `Q` to quit.
- Press `Ctrl-C` to interrupt from the terminal.
- Resize the terminal to recalculate and redraw the clock layout.

## Notes

The clock face accounts for terminal cell proportions by scaling vertical
distances, which helps the clock appear circular in typical terminal fonts.

Terminal drawing operations are clipped to the available windows bounds to
prevent ordinary edge and resize conditions from crashing the display.

The refresh interval is measured with Python's monotonic clock so elapsed-time
measurement is not affected by changes to the system wall clock.
