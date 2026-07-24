# Changelog

## Unreleased

## v1.3.1 - 2026-07-23

### Added

- Created a `requirements.txt` file to declare the Windows-specific dependencies.

## Changed

- Cleaned up CHANGELOG formatting.

### Fixed

- Fixed clock face markers being overwritten by the dot ring.
- Made `-z/--timezone` error messages consistent for malformed input.
- Suppressed traceback on Ctrl-C exit.
- Synced render loop to wall-clock second boundaries.
- Simplified key-polling loop using blocking getch timeout.
- Skipped redundant redraws when seconds are hidden.
- Clock face now skips redundant redraws when seconds are hidden.

## v1.3

### Added

- Centralized character and string rendering through safe drawing helpers.
- Added boundary checking and text clipping for terminal drawing operations.
- Added a minimum supported clock radius of 5.
- Added responsive radius calculation based on the available terminal layout.
- Added automatic clamping when a manually requested radius is too large.
- Added a `Terminal too small` display when the minimum clock cannot fit.
- Added immediate layout recalculation when the terminal is resized.
- Replaced wall-clock interval measurement with `time.monotonic()`.

### Fixed

- Updated `--no-seconds` to hide seconds from both the analog and digital
  displays.

## v1.2

### Added

- Added command-line argument parsing.
- Added configurable timezone selection with `--timezone` / `-z`.
- Added configurable redraw timing with `--refresh-rate` / `-r`.
- Added optional manual clock sizing with `--radius`.
- Added display toggles for the second hand, digital readout, and border.
- Added 12-hour and 24-hour digital time formats with `--format`.
- Added `--version` output.

## v1.1

### Fixed

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
