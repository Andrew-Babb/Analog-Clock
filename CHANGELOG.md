# Changelog

## v1.2

- Added command-line argument parsing.
- Added configurable timezone selection with `--timezone` / `-z`.
- Added configurable redraw timing with `--refresh-rate` / `-r`.
- Added optional manual clock sizing with `--radius`.
- Added display toggles for the second hand, digital readout, and border.
- Added 12-hour and 24-hour digital time formats with `--format`.
- Added `--version` output.

## v1.1

- Replaced the fixed UTC offset with Python's `zoneinfo.ZoneInfo`.
- Set the clock timezone to `America/New_York`.
- Removed the manual `timedelta(hours=-4)` adjustment so daylight saving time
  is handled automatically.

## v1.0

- Initial terminal analog clock implementation.
- Added a bordered clock face with hour markers.
- Added hour, minute, and second hands.
- Added a centered digital time readout.
- Added keyboard exit support with `q` and `Q`.
