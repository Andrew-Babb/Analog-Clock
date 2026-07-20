# Analog Clock v1.1

Analog Clock is a terminal-based analog clock rendered with Python's `curses`
module. It draws an analog clock face, hour/minute/second hands, and a digital
time readout.

## Requirements

- Python 3.9 or newer
- A terminal that supports `curses`

The clock uses Python's standard-library `zoneinfo` module for timezone-aware
local time.

## Timezone

Version 1.1 displays time for the `America/New_York` timezone:

```python
TIME_ZONE = ZoneInfo("America/New_York")
```

This lets Python handle daylight saving time and standard time automatically.
To use a different timezone, replace `America/New_York` with another IANA
timezone name, such as `America/Chicago`, `Europe/London`, or `Asia/Tokyo`.

## Run

```bash
python3 analog_clock_v1.1.py
```

## Controls

- Press `q` or `Q` to quit.
- Press `Ctrl-C` to interrupt from the terminal.

## Notes

The clock face accounts for terminal cell proportions by scaling vertical
distances, which helps the clock appear circular in typical terminal fonts.
