# Analog Clock v1.2

Analog Clock is a terminal-based analog clock rendered with Python's `curses`
module. It draws an analog clock face, hour/minute/second hands, and a digital
time readout. Version 1.2 adds command-line options for timezone, refresh rate,
clock size, display toggles, and digital time format.

## Requirements

- Python 3.9 or newer
- A terminal that supports `curses`

The clock uses Python's standard-library `zoneinfo` module for timezone-aware
local time.

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
--radius CELLS             Clock radius in terminal columns (default: fit to terminal)
--no-seconds               Hide the second hand
--no-digital               Hide the digital time readout
--no-border                Hide the terminal border
--format {12,24}           Digital clock format (default: 24)
--version                  Show the program version
```

Examples:

```bash
python3 analog_clock.py --timezone Europe/London --format 12
python3 analog_clock.py --refresh-rate 0.25 --radius 18 --no-border
```

## Controls

- Press `q` or `Q` to quit.
- Press `Ctrl-C` to interrupt from the terminal.

## Notes

The clock face accounts for terminal cell proportions by scaling vertical
distances, which helps the clock appear circular in typical terminal fonts.
